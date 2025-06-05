import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")

def get_gemini_llm():
    return ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)
