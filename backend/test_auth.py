#!/usr/bin/env python
"""
Simple test to check the auth functionality
"""

from src.database.database import get_session, init_db
from src.services.auth import AuthService
from src.models.user import UserCreate
from sqlmodel import Session

def test_auth():
    print("Testing auth functionality...")

    # Initialize DB
    init_db()
    print("Database initialized")

    # Get a session
    session_gen = get_session()
    session = next(session_gen)

    try:
        # Try to create a user
        user_create = UserCreate(email="test@example.com", name="Test User", password="password123")
        print("Creating user...")
        user = AuthService.register_user(session, user_create)
        print(f"User created successfully: {user.email}")

        # Try to authenticate
        authenticated_user = AuthService.authenticate_user(session, "test@example.com", "password123")
        if authenticated_user:
            print("Authentication successful")
        else:
            print("Authentication failed")

    except Exception as e:
        print(f"Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

    # Close session
    session.close()

if __name__ == "__main__":
    test_auth()