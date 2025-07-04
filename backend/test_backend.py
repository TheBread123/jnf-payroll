#!/usr/bin/env python3
"""
Simple test script to verify the backend works correctly
"""

import requests
import json
import sys

# Configuration
BASE_URL = "http://localhost:5000"
ADMIN_CREDENTIALS = {"username": "admin", "password": "password123"}
DEMO_CREDENTIALS = {"username": "demo", "password": "demo123"}


def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            print("✓ Health check endpoint working")
            return True
        else:
            print(f"✗ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health check error: {e}")
        return False


def test_login_endpoint():
    """Test the login endpoint"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/login",
            json=ADMIN_CREDENTIALS,
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("success") and data.get("token"):
                print("✓ Login endpoint working")
                return data["token"]
            else:
                print("✗ Login response missing required fields")
                return None
        else:
            print(f"✗ Login failed with status {response.status_code}")
            return None
    except Exception as e:
        print(f"✗ Login error: {e}")
        return None


def test_protected_endpoint(token):
    """Test the protected endpoint"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/protected", headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code == 200:
            data = response.json()
            if data.get("user") and data.get("backend_status"):
                print("✓ Protected endpoint working")
                return True
            else:
                print("✗ Protected response missing required fields")
                return False
        else:
            print(f"✗ Protected endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Protected endpoint error: {e}")
        return False


def test_invalid_login():
    """Test login with invalid credentials"""
    try:
        response = requests.post(
            f"{BASE_URL}/api/login",
            json={"username": "invalid", "password": "invalid"},
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == 401:
            print("✓ Invalid login properly rejected")
            return True
        else:
            print(f"✗ Invalid login should return 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Invalid login test error: {e}")
        return False


def main():
    """Run all tests"""
    print("Testing JNF Payroll Backend")
    print("=" * 50)

    tests_passed = 0
    total_tests = 4

    # Test health endpoint
    if test_health_endpoint():
        tests_passed += 1

    # Test login endpoint
    token = test_login_endpoint()
    if token:
        tests_passed += 1

        # Test protected endpoint
        if test_protected_endpoint(token):
            tests_passed += 1

    # Test invalid login
    if test_invalid_login():
        tests_passed += 1

    print("\n" + "=" * 50)
    print(f"Tests passed: {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("🎉 All tests passed!")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Check the backend server.")
        sys.exit(1)


if __name__ == "__main__":
    main()
