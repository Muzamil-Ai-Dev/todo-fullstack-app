#!/usr/bin/env python3
"""
Test script to verify JWTBearer middleware implementation
"""

import sys
import os
sys.path.append(".")

# Add the backend directory to the path
backend_path = os.path.join(os.getcwd(), "backend")
sys.path.append(backend_path)

from fastapi import Request
from starlette.datastructures import Headers
from src.middleware.auth_middleware import JWTBearer

# Create a JWTBearer instance
jwt_bearer = JWTBearer()

# Create a mock request with a valid token
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyZDVjMzE0ZC1iM2M0LTRjODYtYWI0YS05YjEzNjBjYTNmY2YiLCJlbWFpbCI6Im1tdXphbW1pbG1lbzQ1NkBnbWFpbC5jb20iLCJleHAiOiAxNzY4MDYzMDQxfQ.hmvVGzrTrpTD_kr8g8s-V3BgqfeipCb-EyEEV_mt4l0"

# Create a mock request
class MockRequest:
    def __init__(self, headers):
        self.headers = Headers(headers)
        self.state = type('State', (), {})()  # Create an empty state object

mock_request = MockRequest({"authorization": f"Bearer {token}"})

print("Testing JWTBearer middleware...")
try:
    # This should validate the token and set user info in request.state
    result = jwt_bearer.__call__(mock_request)
    print("SUCCESS: JWTBearer validation worked!")
    print(f"User ID in request.state: {getattr(mock_request.state, 'user_id', 'NOT SET')}")
    print(f"User email in request.state: {getattr(mock_request.state, 'user_email', 'NOT SET')}")
except Exception as e:
    print(f"ERROR: JWTBearer validation failed: {e}")
    import traceback
    traceback.print_exc()