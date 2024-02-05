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
- [Design Patterns](#design-patterns)
- [Application Logic](#application-logic)
- [Testing](#testing-and-coverage)

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
#### Interact with ChatBot
- To wake up the chatbot/to create a new session
```bash
curl -X POST http://localhost:8000/chat/ -H "Authorization: Bearer your_token_here" -d "text=hello"
```
- Ask questions
```bash
curl -X POST http://localhost:8000/chat/ -H "Authorization: Bearer your_token_here" -d "text=who created you?"
```
```bash
curl -X POST http://localhost:8000/chat/ -H "Authorization: Bearer your_token_here" -d "text=tell me a joke"
```
- Close session
```bash
curl -X POST http://localhost:8000/chat/ -H "Authorization: Bearer your_token_here" -d "text=bye"
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
 
For detailed information about each endpoint, refer to http://localhost:8000/redoc/.

## Authentication
The API uses Token-based authentication. Include the token in the Authorization header of your requests:
```bash
Authorization: Bearer your_token_here
```

## Design Patterns
### Abstract Factory Pattern
The Abstract Factory Pattern is employed to enhance scalability, maintainability, and adaptability of the codebase. Key aspects of its implementation include:

- **Abstraction of Classes:** Abstract classes are created and implemented to ensure that classes depend on interfaces rather than concrete classes, minimizing coupling. This adheres to the Dependency Inversion Principle.

- **Separate Interfaces:** Distinct interfaces are designed for various classes to prevent the implementation of methods that a class does not utilize.

### Adapter Pattern
The Adapter Pattern is utilized to enhance flexibility in the codebase. Noteworthy aspects of its implementation include:

- **Dependency on Interfaces:** The service class is designed to depend on interfaces rather than concrete classes, facilitating ease in changing the repository to a NoSQL database or switching the chatbot from NLTK to Chat-GPT.

## Application Logic
The application logic follows a structured process to ensure seamless interaction with the chatbot:

- **Session Retrieval:** The system retrieves the latest session by filtering with the created time using the user object.

- **New Session Creation:** If the session does not exist or has ended, a new session is created.

- **Greeting Response:** If the session is new or the text is a greeting, a welcoming response is generated for the user.

- **Goodbye Handling:** If the user's input signals a goodbye, an appropriate farewell is provided.

- **Question Response:** If the session state is 'question', a response is generated from the nltk chatbot and sent to the user.

## Testing and Coverage
- To run tests and assess coverage, execute the following command:
```bash
coverage run manage.py test
```
- To generate a coverage report, use the following command:
```bash
coverage report
```
Note: The application currently achieves an impressive 87% test coverage.
