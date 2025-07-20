# Chat Application

A real-time chat application built with FastAPI, featuring JWT authentication, role-based access control (RBAC), and WebSocket communication.

## Features

- **JWT Authentication**: Secure user authentication with JWT tokens
- **Role-Based Access Control**: Admin and user roles with different permissions
- **Real-time Chat**: WebSocket-based real-time messaging
- **Room-based Chat**: Join different chat rooms
- **Message Persistence**: Messages stored in PostgreSQL database
- **Cursor-based Pagination**: Efficient message loading
- **Admin Panel**: User management and message moderation
- **Modern UI**: Clean and responsive web interface

## Technology Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Authentication**: JWT with python-jose, bcrypt for password hashing
- **Real-time**: WebSocket with FastAPI
- **Database**: PostgreSQL with psycopg2
- **Frontend**: HTML, CSS, JavaScript (vanilla)

## Project Structure

```
Chat-Application/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── crud.py              # Database operations
│   ├── websocket_manager.py # WebSocket connection management
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # Authentication routes
│       ├── chat.py          # Chat and WebSocket routes
│       └── admin.py         # Admin routes
├── static/
│   └── index.html           # Frontend interface
├── alembic/                 # Database migrations
├── requirements.txt         # Python dependencies
├── env.example              # Environment variables template
└── README.md
```

## Setup Instructions

### 1. Environment Setup

Create a virtual environment:
```bash
python3 -m venv venv
```

Activate the virtual environment:
- **Windows**: `venv\Scripts\activate`
- **macOS/Linux**: `source venv/bin/activate`

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Database Setup

1. Install PostgreSQL and create a database:
```sql
CREATE DATABASE chat_app;
```

2. Create a `.env` file from the template:
```bash
cp env.example .env
```

3. Update the `.env` file with your database credentials:
```env
DATABASE_URL=postgresql://postgres:umesh@@@1234567@localhost:5432/chat_app
SECRET_KEY=your-secret-key-here-make-it-long-and-secure
```

### 4. Database Migrations

Initialize Alembic (if not already done):
```bash
alembic init alembic
```

Run migrations:
```bash
alembic upgrade head
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **API**: http://localhost:8000
- **Frontend**: http://localhost:8000/static/index.html
- **API Documentation**: http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /auth/signup` - Create a new user account
- `POST /auth/login` - Authenticate and get JWT token
- `GET /auth/me` - Get current user information

### Chat
- `GET /chat/messages/{room_id}` - Get messages for a room
- `DELETE /chat/messages/{message_id}` - Delete a message
- `WebSocket /chat/ws/{room_id}` - Real-time chat connection

### Admin (Admin role required)
- `GET /admin/users` - Get all users
- `GET /admin/users/{user_id}` - Get specific user
- `DELETE /admin/messages/{message_id}` - Delete any message

## Usage

### 1. Create an Account
- Visit http://localhost:8000/static/index.html
- Click "Sign Up" and create an account
- By default, users are assigned the "user" role

### 2. Login and Chat
- Login with your credentials
- Enter a room ID (e.g., "general")
- Start chatting in real-time!

### 3. Admin Features
To access admin features, you need to manually update a user's role in the database:
```sql
UPDATE users SET role = 'admin' WHERE username = 'your_username';
```

## Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **JWT Tokens**: Secure authentication with role information
- **Role-Based Access**: Different permissions for admin and user roles
- **Input Validation**: Pydantic schemas for data validation
- **CORS Protection**: Configurable CORS settings

## Development

### Running Tests
```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

