# # python
# from app.models.LetterStyle import LetterStyle
#
# from app.service.gemini_service import GeminiService
#
# # נסיון לייבא את ה-mcp האמיתי; אם אינו קיים — הגדרת stub דקורטור כך שהמודול ייטען ו-linter/tests יעברו.
# try:
#     import mcp
# except Exception:
#     class _MCPStub:
#         def tool(self):
#             def decorator(func):
#                 return func
#             return decorator
#     mcp = _MCPStub()
#
# gemini_service = GeminiService()
# MAX_CHARACTER_LIMIT = 1500
#
# @mcp.tool()
# async def draft_letter(text: str, style: str, add_emojis: bool) -> str:
#     # בדיקת אורך - כאן ב\-Tools!
#     if len(text) > MAX_CHARACTER_LIMIT:
#         return f"ארוך מדי! מקסימום {MAX_CHARACTER_LIMIT} תווים."
#
#     # בדיקת סגנון - גם כאן ב\-Tools!
#     if style not in [s.value for s in LetterStyle]:
#         return "סגנון לא תקין."
#
#     # רק אם הכל תקין, עוברים ל\-Service
#     return await gemini_service.generate_letter(text, style, add_emojis)

import os
import google.generativeai as genai

async def draft_letter(text: str, style: str, add_emojis: bool) -> str:
    """
    מבצע את הפנייה האמיתית ל-Gemini
    """
    print(f"DEBUG: Starting draft_letter with style {style}")
    # שליפת המפתח (וודאי שהוא מוגדר ב-.env או כאן ישירות לבדיקה)
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "שגיאה: מפתח API לא נמצא."

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # בניית הפרומפט
    emoji_instruction = "עם אימוג'ים" if add_emojis else "ללא אימוג'ים"
    prompt = f"כתוב מכתב בסגנון {style} על בסיס הטקסט הבא: {text}. {emoji_instruction}. ענה רק עם טקסט המכתב."

    try:
        # כאן חשוב להשתמש בשיטה שמתאימה לקריאה אסינכרונית אם רוצים,
        # אבל לבינתיים נשתמש בקריאה הרגילה:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"שגיאה בפנייה ל-Gemini: {str(e)}"