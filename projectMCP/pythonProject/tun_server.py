import os
import sys
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# 1. טעינת סביבה ועדכון נתיבים
load_dotenv()
current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# ייבוא השירות של ג'ימיני שכתבת
from app.service import gemini_service as gs

app = Flask(__name__)
# הגדרת CORS חיונית כדי ש-Gmail יאפשר לתוסף לדבר עם הלוקלהוסט
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/compose", methods=["POST"])
async def compose():
    try:
        data = request.get_json(silent=True) or {}
        text = data.get("text", "")
        style = data.get("style", "Formal")

        if not text:
            return jsonify({"error": "Text is required"}), 400

        # קריאה לפונקציה האמיתית שלך שמדברת עם Gemini
        # שימי לב: הפונקציה שלך היא async ולכן נשתמש ב-await
        result = await gs.draft_letter(text, style, True)

        return jsonify({"result": result})
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal Server Error"}), 500


if __name__ == "__main__":
    # הרצה על פורט 5678 כפי שמוגדר בתוסף שלך
    app.run(host="127.0.0.1", port=5678, debug=True)