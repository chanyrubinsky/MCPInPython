import google.generativeai as genai
import os
import importlib

# Minimal dynamic import for LetterStyle to avoid IDE/static-analysis unresolved reference warnings
try:
    LetterStyle = importlib.import_module('app.models.LetterStyle').LetterStyle
except Exception:
    try:
        LetterStyle = importlib.import_module('.models.LetterStyle', package=__package__ or 'app').LetterStyle
    except Exception:
        class LetterStyle:
            pass

from limits import parse
from limits.strategies import MovingWindowRateLimiter
from limits.storage import MemoryStorage

# הגדרת אחסון להגבלות (בזיכרון המערכת)
storage = MemoryStorage()
limiter = MovingWindowRateLimiter(storage)

# הגדרה: 5 בקשות לדקה לכל "משתמש"
limit = parse("5 per minute")


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")

        if not api_key:
            # אם הוא לא מוצא, נדפיס שגיאה ברורה לטרמינל
            print("ERROR: API Key not found in environment variables!")
            return

        # כאן אנחנו מגדירים את המפתח בצורה מפורשת עבור הספרייה
        genai.configure(api_key=api_key.strip())
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    async def draft_letter(self, text: str, style: LetterStyle, add_emojis: bool) -> str:
        """
        Rewrites a letter based on provided content and style.
        Styles available: Formal (רשמי), Rhymed (מחורז), Technical (תכני), Friendly (חברי).
        """
        if not limiter.hit(limit, "user_identifier"):
            return "שגיאה: הגעת למכסת הבקשות המותרת. נסה שוב בעוד דקה."

        # Converting boolean to a clear instruction for the prompt
        emoji_status = "Yes" if add_emojis else "No"

        # The Prompt: Defined in English for high-quality instruction following
        prompt = f"""
            You are an expert professional letter writer.
            Your goal is to rewrite the user's text based on the following constraints:
    
            ### INPUT TEXT:
            "{text}"
    
            ### CONSTRAINTS:
            - Target Style: {style}
            - Include Emojis: {emoji_status}
    
            ### STYLE DEFINITIONS:
            - Formal (רשמי): Professional, high-level vocabulary, respectful, and slightly distant.
            - Rhymed (מחורז): Creative poem-like writing with clear rhymes.
            - Technical (תכני): Direct, factual, no emotional fillers or extra connecting words.
            - Friendly (חברי): Heartfelt, warm, showing closeness and kindness.
    
            ### INSTRUCTIONS:
            - If 'Include Emojis' is Yes, integrate them naturally. If No, do not use any.
            - Respond ONLY with the drafted letter text.
            """

        # בדיקה שהמודל אכן נוצר ב-init
        if not self.model:
            return "שגיאה: מודל ה-AI לא אותחל (בדוק API Key)"

        # שימוש במודל הקיים
        response = self.model.generate_content(prompt)
        return response.text
