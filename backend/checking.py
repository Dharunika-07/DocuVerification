import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

try:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Hello")
    print("MODEL WORKS")
    print(response.text)
except Exception as e:
    print("MODEL FAILED")
    print(e)
