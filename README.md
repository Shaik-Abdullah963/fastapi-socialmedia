# fastapi-socialmedia

This is a simple **Social Media Application** built with **FastAPI** where users can create posts and like other users' posts. The application aims to provide a basic social media platform where users can interact by posting content and showing appreciation by liking posts.

## Features

- **User Authentication**: Users can create an account, log in, and manage their sessions.
- **Create Posts**: Users can create new posts and share them with others.
- **Like Posts**: Users can like posts created by others, allowing for engagement.
- **Post Feed**: Users can view a feed of all posts created by other users.

## Requirements

Before running the application, ensure you have the following installed:

- Python 3.8 or higher
- [Optional] Conda or Virtual Environment for managing dependencies

### Dependencies

You can install the required dependencies using `pip` or `conda`:

#### Using Conda:
```bash
conda env create -f environment.yaml
conda activate venv
```

## Setting Up the .env File

The `.env` file is used to store sensitive data such as API keys, database credentials, and other environment-specific configurations. Before running the application, you need to create a `.env` file in the root directory of the project.

### Steps to Create a `.env` File:

1. **Create a `.env` file** in the root directory of your project. You can create this file manually or by copying from the template.

2. **Copy the contents of the example `.env` file** into your newly created `.env` file. Below is an example of the variables that should be set:

```env
# .env Example for Local Development

DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_PASSWORD="Your Password"
DATABASE_USERNAME=postgres
DATABASE_NAME=fastapi
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

```

## Running the application Locally
```bash
cd app
fastapi dev main.py
```

## Accessing the API Documentation
FastAPI automatically generates interactive API documentation using Swagger UI and ReDoc.

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc