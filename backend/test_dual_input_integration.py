import sys
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_pasted_math():
    print("Testing Pasted Math...")
    res = client.post("/smart-verify", json={
        "question": "What is 15 * 12?",
        "response": "15 * 12 is 180. The final answer is 180."
    })
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "MATH"
    assert data["is_user_response"] is True
    assert data["verification"]["verified"] is True
    assert data["verification"]["calculated"] == 180
    print("  ✓ Pasted math verified successfully!")

def test_auto_math():
    print("Testing Math Question Alone (Auto-generate)...")
    res = client.post("/smart-verify", json={
        "question": "What is 144 / 12?"
    })
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "MATH"
    assert data["is_user_response"] is False
    assert data["verification"]["verified"] is True
    assert data["verification"]["calculated"] == 12
    print("  ✓ Auto math verified successfully!")

def test_pasted_code():
    print("Testing Pasted Code...")
    code_snippet = """```python
def multiply(a, b):
    return a * b

print(multiply(7, 8))
```"""
    res = client.post("/smart-verify", json={
        "question": "Write Python code to multiply two numbers",
        "response": code_snippet
    })
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "CODE"
    assert data["is_user_response"] is True
    assert data["execution"]["success"] is True
    assert "56" in data["execution"]["output"]
    print("  ✓ Pasted code executed and verified successfully! Output: " + data["execution"]["output"].strip())

def test_pasted_code_failing():
    print("Testing Pasted Invalid Code...")
    bad_code = "print(1 / 0)"
    res = client.post("/smart-verify", json={
        "question": "Write Python code that divides 1 by 0",
        "response": bad_code
    })
    assert res.status_code == 200
    data = res.json()
    assert data["type"] == "CODE"
    assert data["is_user_response"] is True
    assert data["execution"]["success"] is False
    assert "ZeroDivisionError" in data["execution"]["error"]
    print("  ✓ Pasted faulty code caught in sandbox!")

if __name__ == "__main__":
    test_pasted_math()
    test_auto_math()
    test_pasted_code()
    test_pasted_code_failing()
    print("\nALL INTEGRATION TESTS PASSED PERFECTLY!")
