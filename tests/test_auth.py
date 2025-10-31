import pytest
from src.controllers.authorization import AuthCtrl
from src.classes.user import User

@pytest.fixture
def auth_system():
    return AuthCtrl.create()

@pytest.fixture
def user():
    return User(
        name="Test User",
        email="test@example.com",
        pw="password123"
    )

def test_register_user_success(auth_system, user):
    result = auth_system.register_user(user)
    assert result == "Registration successful"
    assert user.email in auth_system.registered_users

def test_register_user_already_exists(auth_system, user):
    auth_system.register_user(user)
    result = auth_system.register_user(user)
    assert result == "User already exists"

def test_login_success(auth_system, user):
    auth_system.register_user(user)
    result = auth_system.login(user.email, user.pw)
    assert result == "Login successful"
    assert user.email in auth_system.logged_in_users

def test_login_user_not_found(auth_system):
    result = auth_system.login("nonexistent@example.com", "password")
    assert result == "User not found"

def test_login_incorrect_password(auth_system, user):
    auth_system.register_user(user)
    result = auth_system.login(user.email, "wrongpassword")
    assert result == "Incorrect password"
    assert user.email not in auth_system.logged_in_users

def test_logout_success(auth_system, user):
    auth_system.register_user(user)
    auth_system.login(user.email, user.pw)
    result = auth_system.logout(user.email)
    assert result == "Logout successful"
    assert user.email not in auth_system.logged_in_users

def test_logout_user_not_logged_in(auth_system, user):
    auth_system.register_user(user)
    result = auth_system.logout(user.email)
    assert result == "User not logged in"
