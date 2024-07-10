from minio import Minio  # type: ignore
from dotenv import load_dotenv
import os
import json
from typing import List, Generator

load_dotenv()

minio_client = Minio(
    "localhost:9000",
    access_key=os.getenv("MINIO_ACCESS_KEY"),
    secret_key=os.getenv("MINIO_SECRET_KEY"),
    secure=False,
)


def upload_to_minio(file_path: str, bucket_name: str, object_name: str) -> str:
    # Check if bucket exists and create it if it doesn't
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)
        print(f"Created bucket {bucket_name}")
    else:
        print(f"Bucket {bucket_name} already exists")

    # Define the policy
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": "*"},
                "Action": ["s3:GetObject", "s3:ListBucket"],
                "Resource": [
                    f"arn:aws:s3:::{bucket_name}",
                    f"arn:aws:s3:::{bucket_name}/*",
                ],
            },
            {
                "Effect": "Deny",
                "Principal": {"AWS": "*"},
                "Action": ["s3:PutObject", "s3:DeleteObject"],
                "Resource": [f"arn:aws:s3:::{bucket_name}/*"],
            },
        ],
    }

    # Set the policy
    minio_client.set_bucket_policy(bucket_name, json.dumps(policy))
    print(f"Policy set for bucket {bucket_name}")

    # Upload the file
    minio_client.fput_object(bucket_name, object_name, file_path)
    print(f"File uploaded: {object_name}")

    # Construct and return the object path
    object_path = f"{bucket_name}/{object_name}"
    return object_path


def get_bucket_objects(
    bucket_name: str, prefix: str = "", page_size: int = 1000
) -> Generator[List[str], None, None]:
    objects = minio_client.list_objects(bucket_name, prefix=prefix, recursive=True)

    page = []
    for obj in objects:
        object_path = f"{bucket_name}/{obj.object_name}"
        page.append(object_path)

        if len(page) == page_size:
            yield page
            page = []

    if page:
        yield page
