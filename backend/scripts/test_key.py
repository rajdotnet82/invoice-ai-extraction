import os
import sys
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENAI_API_KEY")
if not key:
    print("❌ ERROR: OPENAI_API_KEY not found.")
    print("Create a file named .env in this folder and add:")
    print("OPENAI_API_KEY=your_key_here")
    sys.exit(1)

try:
    from openai import OpenAI
except ImportError:
    print("❌ ERROR: openai package not installed.")
    print("Run: python -m pip install openai python-dotenv")
    sys.exit(1)

client = OpenAI(api_key=key)

def main():
    try:
        # Simple, low-cost test call
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are concise."},
                {"role": "user", "content": "Say 'API key works' in 3 words."}
            ],
            temperature=0
        )

        text = resp.choices[0].message.content
        print("✅ Success! Your API key works.")
        print("Model response:", text)

    except Exception as e:
        print("❌ API call failed.")
        print("Error:", str(e))
        sys.exit(2)

if __name__ == "__main__":
    main()
