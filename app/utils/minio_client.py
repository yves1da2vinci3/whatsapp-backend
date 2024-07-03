from minio import Minio # type: ignore

minio_client = Minio(
    "minio:9000",
    access_key="your_access_key",
    secret_key="your_secret_key",
    secure=False
)
