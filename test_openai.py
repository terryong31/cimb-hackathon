from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

endpoint = os.getenv('AZURE_OPENAI_ENDPOINT')
key = os.getenv('AZURE_OPENAI_KEY')
deployment = os.getenv('AZURE_OPENAI_DEPLOYMENT', 'gpt-4')

print(f"Endpoint: {endpoint}")
print(f"Key: {key[:20]}..." if key else "Key: None")
print(f"Deployment: {deployment}")
print("\nTesting Azure OpenAI connection...")

try:
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=key,
        api_version="2024-08-01-preview"
    )
    
    response = client.chat.completions.create(
        model=deployment,
        messages=[
            {"role": "user", "content": "Say 'Hello, testing Azure OpenAI!' if you can read this."}
        ],
        max_tokens=2000  # Increased for reasoning models
    )
    
    result = response.choices[0].message.content
    print(f"\n✅ SUCCESS!")
    print(f"Response object: {response}")
    print(f"Content: '{result}'")
    print(f"Content length: {len(result) if result else 0}")
    print(f"Content is None: {result is None}")
    print(f"Content is empty string: {result == ''}")
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
