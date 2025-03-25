# FastAPI Authentication System

A secure and scalable authentication system built with FastAPI, featuring role-based access control (RBAC), JWT authentication, and comprehensive security measures.

## Features

- 🔐 JWT-based authentication with access and refresh tokens
- 👥 Role-based access control (RBAC)
- 🔒 Password hashing with bcrypt
- 🛡️ Rate limiting for login and registration
- 💾 Caching system for improved performance
- 📝 Comprehensive logging
- 🔍 Input sanitization and validation
- 🚀 Async/await support for better performance

## Tech Stack

- FastAPI
- SQLAlchemy
- Pydantic
- JWT (JSON Web Tokens)
- PostgreSQL
- Python 3.8+

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database
- Virtual environment (recommended)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi_author
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Initialize the database:
```bash
python app/init_db.py
```

## Configuration

The application can be configured through environment variables in the `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
  ```json
  {
    "username": "string",
    "email": "string",
    "password": "string",
    "role": "string"
  }
  ```

- `POST /auth/login` - Login user
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```

- `GET /auth/me` - Get current user information

### Security Features

- Rate limiting on login and registration endpoints
- Password strength validation
- Input sanitization
- JWT token-based authentication
- Role-based access control

## Project Structure

```
fastapi_author/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routes.py
│   ├── security.py
│   ├── cache.py
│   ├── utils.py
│   └── rbac/
│       ├── __init__.py
│       └── dependencies.py
├── tests/
├── .env
├── .env.example
├── requirements.txt
└── README.md
```

## Running the Application

1. Start the server:
```bash
uvicorn app.main:app --reload
```

2. Access the API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run tests using pytest:
```bash
pytest
```

## Security Considerations

- Passwords are hashed using bcrypt
- JWT tokens are used for authentication
- Rate limiting prevents brute force attacks
- Input sanitization prevents injection attacks
- Role-based access control ensures proper authorization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
