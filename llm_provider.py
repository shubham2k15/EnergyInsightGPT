import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def get_llm():
    if os.getenv("GROQ_API_KEY"):
        return ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.3
        )

    elif os.getenv("GOOGLE_API_KEY"):
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.3
        )

    else:
        raise ValueError("❌ Add GROQ_API_KEY or GOOGLE_API_KEY in .env")