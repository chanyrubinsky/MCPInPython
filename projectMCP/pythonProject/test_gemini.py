import asyncio
from app.service.gemini_service import draft_letter
from dotenv import load_dotenv

load_dotenv()

async def test():
    print("Testing Gemini connection...")
    result = await draft_letter("בדיקה", "רשמי", False)
    print(f"Result: {result}")

asyncio.run(test())