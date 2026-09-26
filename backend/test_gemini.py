import os
import httpx
import dotenv

dotenv.load_dotenv(r'c:\Users\reddy\Desktop\AI-MULTIAGENT\backend\.env')
key = os.getenv('GEMINI_API_KEY')
print("Testing with key:", key[:10] if key else "None")

test_models = ['gemini-3.8-flash', 'gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-3-flash-preview', 'gemini-2.5-pro']
for m in test_models:
    for ver in ['v1', 'v1beta']:
        url = f'https://generativelanguage.googleapis.com/{ver}/models/{m}:generateContent?key={key}'
        payload = {
            'contents': [{'parts': [{'text': 'Return valid JSON object: {"verdict": "VERIFIED", "confidence": 0.99, "explanation": "OK"}'}]}],
            'generationConfig': {'responseMimeType': 'application/json'}
        }
        try:
            r = httpx.post(url, json=payload, timeout=10)
            print(f'{ver}/{m} -> {r.status_code}')
            if r.status_code == 200:
                print('SUCCESS! Model works perfectly:', r.json()['candidates'][0]['content']['parts'][0]['text'])
                exit(0)
            else:
                err = r.json().get('error', {}).get('message', r.text[:100])
                print('Error:', err[:150])
        except Exception as e:
            print('Ex:', e)