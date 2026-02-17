#!/usr/bin/env python3
"""
Test script to verify JWT token creation and validation
"""

import sys
sys.path.append(".")

from src.utils.jwt_utils import create_access_token, verify_token
from src.config.settings import settings

print(f"Using JWT Secret Key: {settings.JWT_SECRET_KEY[:20]}...")
print(f"Using JWT Algorithm: {settings.JWT_ALGORITHM}")
print(f"Access Token Expiry: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} minutes")

# Create a test token
test_data = {"sub": "test-user-id", "email": "test@example.com"}
token = create_access_token(test_data)
print(f"\nCreated token: {token[:50]}...")

# Verify the token
decoded = verify_token(token)
print(f"\nDecoded token: {decoded}")

if decoded:
    print("\nSUCCESS: Token verification SUCCESSFUL!")
    print(f"Subject: {decoded.get('sub')}")
    print(f"Email: {decoded.get('email')}")
    print(f"Expiration: {decoded.get('exp')}")
else:
    print("\nFAILED: Token verification FAILED!")

# Also test with the actual user data format
user_data = {"sub": "2d5c314d-b3c4-4c86-ab4a-9b1360ca3fcf", "email": "mmuzammilmeo456@gmail.com"}
user_token = create_access_token(user_data)
print(f"\nUser token created: {user_token[:50]}...")

user_decoded = verify_token(user_token)
print(f"\nUser token decoded: {user_decoded}")

if user_decoded:
    print("\nSUCCESS: User token verification SUCCESSFUL!")
else:
    print("\nFAILED: User token verification FAILED!")