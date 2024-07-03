---

# WhatsApp Flow Backend

This project implements the backend of a WhatsApp-like application using FastAPI, MongoDB, Redis, MinIO, and Socket.io. It supports user authentication, chat functionalities, stories, and audio/video calls.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [ERD Diagram](#erd-diagram)
- [Contributing](#contributing)
- [License](#license)

## Features

- **User Authentication**
  - Enter phone number
  - Send OTP code
  - Register name and user image
  - Modify user information

- **Chats**
  - Get all user chats
  - Get chat details
  - Send and receive messages (text, image, audio, video, file)
  - Delete messages
  - See sent media

- **Stories**
  - Create stories (image, video, text)
  - View stories

- **Calls**
  - Make audio/video calls
  - Receive audio/video calls
  - View call history

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yves1da2vinci3/whatsapp-backend.git
    cd whatsapp-backend
    ```

2. Create a `.env` file with the following content:

    ```env
    MINIO_ACCESS_KEY=your_access_key
    MINIO_SECRET_KEY=your_secret_key
    ```

3. Build and start the Docker containers:

    ```sh
    docker-compose up --build
    ```

4. The FastAPI application will be available at `http://localhost:8000`.

## Usage

- To interact with the API, use a tool like [Postman](https://www.postman.com/) or [curl](https://curl.se/).
- Access the FastAPI interactive documentation at `http://localhost:8000/docs`.

## Project Structure

```plaintext
project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── schemas.py
│   ├── chats/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── schemas.py
│   ├── stories/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── schemas.py
│   ├── calls/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── schemas.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── minio_client.py
│   │   ├── redis_client.py
│   │   ├── socket.py
│   │   ├── otp.py
└── docker-compose.yml
└── requirements.txt
```

## API Endpoints

### Auth

- **POST** `/auth/enter_number` - Enter phone number
- **POST** `/auth/register_user` - Register name and user image
- **PUT** `/auth/modify_user` - Modify user information

### Chats

- **GET** `/chats` - Get all user chats
- **GET** `/chats/{chat_id}` - Get chat details
- **POST** `/chats/{chat_id}/send_message` - Send a message
- **DELETE** `/chats/{chat_id}/delete_message` - Delete a message
- **GET** `/chats/{chat_id}/media` - See sent media

### Stories

- **POST** `/stories` - Create a story
- **GET** `/stories` - View stories

### Calls

- **POST** `/calls/make_call` - Make a call
- **GET** `/calls/history` - View call history
- **GET** `/calls/history/{call_id}` - View a specific call's history

## ERD Diagram

```plaintext
+-----------+         +-----------+         +-----------+         +-----------+
|   User    |         |   Chat    |         |  Message  |         |  Story    |
+-----------+         +-----------+         +-----------+         +-----------+
| user_id   |1------< | chat_id   |1------< | message_id|         | story_id  |
| phone     |         | participants >------| sender    |         | user_id   |
| name      |         +-----------+         | content   |         | content   |
| image     |                              | type      |         | type      |
+-----------+                              | timestamp |         | timestamp |
                                           | read      |         +-----------+
                                           +-----------+

+-----------+ 
|   Call    |
+-----------+
| call_id   |
| caller >--|1
| receiver >--|
| type      |
| timestamp |
| duration  |
| participants >------|
+-----------+
```

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss what you would like to change.

## License

This project is licensed under the MIT License.
