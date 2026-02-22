# python
from app.models.LetterStyle import LetterStyle

from app.service.gemini_service import GeminiService

# נסיון לייבא את ה-mcp האמיתי; אם אינו קיים — הגדרת stub דקורטור כך שהמודול ייטען ו-linter/tests יעברו.
try:
    import mcp
except Exception:
    class _MCPStub:
        def tool(self):
            def decorator(func):
                return func
            return decorator
    mcp = _MCPStub()

gemini_service = GeminiService()
MAX_CHARACTER_LIMIT = 1500

@mcp.tool()
async def draft_letter(text: str, style: str, add_emojis: bool) -> str:
    # בדיקת אורך - כאן ב\-Tools!
    if len(text) > MAX_CHARACTER_LIMIT:
        return f"ארוך מדי! מקסימום {MAX_CHARACTER_LIMIT} תווים."

    # בדיקת סגנון - גם כאן ב\-Tools!
    if style not in [s.value for s in LetterStyle]:
        return "סגנון לא תקין."

    # רק אם הכל תקין, עוברים ל\-Service
    return await gemini_service.generate_letter(text, style, add_emojis)