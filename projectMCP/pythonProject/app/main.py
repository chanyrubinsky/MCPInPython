# # import os
# # import google.generativeai as genai
# # from mcp.server.fastmcp import FastMCP
# #
# # app = FastAPI()
# # genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# #
# #
# # @app.post("/chat")
# # async def chat_endpint(request: Request):
# #     data = await request.json()
# #     provider = data.get("provider")  #####gemini
# #     prompt = data.get("prompt")
# #     if provider == 'genimi':
# #         model = genai.GenerativeModele('gemini-pro')
# #         response = model.generate - content(promt)
# #         return {'response': response.text}
# #     else:
# #         raise HTTPException(status_code=400, detail="Unknown provider")
# import asyncio
# import os
# from mcp.server.fastmcp import FastMCP
# from app.tools.letter_tools import draft_letter
#
# mcp = FastMCP("LetterWriter")
#
# # רישום הפונקציה ככלי של MCP
# @mcp.tool()
# async def draft_letter(text: str, style: str, add_emojis: bool) -> str:
#     # קריאה ללוגיקה שכתבנו בתיקיית tools
#     return await draft_letter(text, style, add_emojis)
# if __name__ == "__main__":
#     mcp.run()
#
#
#  mcp.run()

import os
import sys
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# 1. טעינת המפתח מקובץ ה-.env שיצרת בתיקייה הראשית
load_dotenv()

# 2. תיקון נתיבים כדי שהשרת יכיר את תיקיית app
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path)
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# 3. יצירת שרת ה-MCP
mcp = FastMCP("Letter Designer")

# 4. ייבוא הלוגיקה מהשירות (Gemini)
from app.service.gemini_service import draft_letter
from app.models.LetterStyle import LetterStyle

# 5. הגדרת הכלי (Tool) שיופיע ב-Inspector
@mcp.tool()
async def rewrite_letter(text: str, style: LetterStyle, add_emojis: bool) -> str:
    """
    Rewrites a letter based on provided content and style.
    :param text: The content of the letter.
    :param style: Style to use (Formal, Rhymed, Technical, Friendly).
    :param add_emojis: Whether to include emojis in the result.
    """
    # קריאה לפונקציה ב-gemini_service
    return await draft_letter(text, style, add_emojis)

if __name__ == "__main__":
    mcp.run()