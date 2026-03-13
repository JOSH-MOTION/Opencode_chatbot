import os
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")


def call_gemini(prompt, model="gemini-2.0-flash"):
    """Call Gemini API with a prompt."""
    if not GEMINI_API_KEY:
        return "Error: GEMINI_API_KEY not set"

    genai.configure(api_key=GEMINI_API_KEY)

    model_instance = genai.GenerativeModel(model)
    response = model_instance.generate_content(prompt)

    return response.text


if __name__ == "__main__":
    import os

    os.environ["GEMINI_API_KEY"] = "AIzaSyCXGjT4-iv60NytECOK7CtUdY3MOD76vfA"
    print(call_gemini("Hello, how are you?"))
