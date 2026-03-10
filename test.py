import os
os.environ["GROQ_API_KEY"] = "fake_key_for_testing"

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert b"Cold Mail Generator" in response.content

def test_generate_email_invalid_method():
    # GET method on POST route should return 405 Method Not Allowed
    response = client.get("/generate_email")
    assert response.status_code == 405

def test_generate_email_missing_body():
    # Missing parameters should return 422 Unprocessable Entity
    response = client.post("/generate_email", json={})
    assert response.status_code == 422

def test_send_email_invalid_method():
    # GET method on POST route should return 405 Method Not Allowed
    response = client.get("/send_email")
    assert response.status_code == 405

def test_send_email_missing_body():
    # Missing parameters should return 422 Unprocessable Entity
    response = client.post("/send_email", json={})
    assert response.status_code == 422

def test_send_email_mocked(monkeypatch):
    class MockEmailSender:
        def send_email(self, recipient_email, subject, body):
            return True
            
    monkeypatch.setattr("app.main.email_sender", MockEmailSender())
    
    payload = {
        "recipient_email": "test@example.com",
        "subject": "Test Subject",
        "body": "Test Body"
    }
    
    response = client.post("/send_email", json=payload)
    assert response.status_code == 200
    assert response.json() == {"status": "success", "message": "Email sent successfully."}
