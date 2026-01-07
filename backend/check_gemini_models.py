import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

print("Modelos Gemini Disponiveis:\n")

for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"OK {model.name}")
        print(f"   Display: {model.display_name}")
        print(f"   Input: {model.input_token_limit}")
        print(f"   Output: {model.output_token_limit}")
        print()
