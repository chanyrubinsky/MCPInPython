# from flask import Flask, request, jsonify
# from flask_cors import CORS
# from app.service.gemini_service import draft_letter
# from app.models.LetterStyle import LetterStyle
# import asyncio
#
# app = Flask(__name__)
# CORS(app, origins=["https://mail.google.com", "chrome-extension://*"])
#
# style_map = {
#     "מקצועי": LetterStyle.FORMAL,
#     "חברותי": LetterStyle.FRIENDLY,
#     "תמציתי": LetterStyle.TECHNICAL,
#     "פורמלי": LetterStyle.FORMAL,
#     "שכנועי": LetterStyle.FRIENDLY,
# }
#
# @app.route("/health", methods=["GET"])
# def health():
#     return jsonify({"status": "ok"})
#
# @app.route("/compose", methods=["POST"])
# def compose():
#     data = request.get_json(silent=True) or {}
#     text  = data.get("text", "")
#     style = data.get("style", "מקצועי")
#     tone  = float(data.get("tone", 0.5))
#
#     if not text:
#         return jsonify({"error": "text is required"}), 400
#
#     letter_style = style_map.get(style, LetterStyle.FORMAL)
#     add_emojis = tone > 0.5
#
#     result = asyncio.run(draft_letter(text, letter_style, add_emojis))
#     return jsonify({"result": result, "style": style})
#
# if __name__ == "__main__":
#     app.run(port=5678, debug=False)


from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://mail.google.com", "chrome-extension://*"])

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

@app.route("/compose", methods=["POST"])
def compose():
    data = request.get_json(silent=True) or {}
    text  = data.get("text", "")
    style = data.get("style", "מקצועי")
    tone  = float(data.get("tone", 0.5))

    if not text:
        return jsonify({"error": "text is required"}), 400

    # תשובה מדומה — זמני עד שנפתח את Gemini
    result = f"תשובה לבדיקה! סגנון: {style}, טקסט: {text}"
    return jsonify({"result": result, "style": style})

if __name__ == "__main__":
    app.run(port=5678, debug=False)