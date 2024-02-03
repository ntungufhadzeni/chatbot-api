# ChatBot API

The ChatBot API is a Django REST Framework-based backend for a simple chatbot application. It allows users to interact with the chatbot, and perform user authentication.

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)

## Features

- User registration and authentication.
- Chatbot interaction with basic conversation logic.

## Getting Started

### Prerequisites

- Python (>=3.8)
- Django (>=5.0.1)
- Django REST Framework (>=3.14)
- nltk (>=3.8.1)

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ntungufhadzeni/chatbot-api.git
   cd chatbot-api/backend
   ```
2. **Create a virtual environment:**
    - **Windows:**
    ```bash
    python -m venv .venv
   ```
   
    - **Unix/Linux:**
   ```bash
   python3 -m venv .venv
    ```
3. **Activate the virtual environment:**
    - **Windows:**
    ```bash
   .venv\Scripts\activate
    ```
    - **Unix/Linux:**
    ```bash
   source .venv/bin/activate
   ```
4. **Install dependencies:**
    ```bash
   pip install -r requirements.txt
    ```
5. **Apply database migrations:**
    ```bash
   python manage.py migrate
    ```
   
## Usage

1. **Run the development server:**
    ```bash
   python manage.py runserver
    ```
2. Access the API at http://localhost:8000/ and Swagger documentation at http://localhost:8000/swagger/

### Example Usage with curl
#### Register a New User
```bash
curl -X POST http://localhost:8000/register/ -d "username=newuser&email=newuser@example.com&password=password&password2=password"
```
#### Login to get Authentication Token
```bash
curl -X POST http://localhost:8000/token/ -d "username=newuser&password=password"
```
#### Access ChatBot
```bash
curl -X POST http://localhost:8000/chat/ -H "Authorization: Bearer your_token_here" -d "text=who created you?"
```
#### Refresh Token
```bash
curl -X POST http://localhost:8000/token/refresh/ -H "Authorization: Bearer your_token_here" -d "refresh=your_refresh_token_here"
```
#### Logout
```bash
curl -X POST http://localhost:8000/logout/ -H "Authorization: Bearer your_token_here" -d "refresh_token=your_refresh_token_here"
```

## API Endpoints

- Register User: /register/ (POST)
- Login: /token/ (POST)
- Refresh Token: /token/refresh/
- Logout: /logout/ (POST)
- Chat: /chat/ (POST)
- Home: / (GET)
 
For detailed information about each endpoint, refer to the [API Documentation](#).

## Authentication
The API uses Token-based authentication. Include the token in the Authorization header of your requests:
```bash
Authorization: Bearer your_token_here
```

   