import sys
import json
import asyncio

# This runner is executed in a separate process to safely import and call
# app.service.gemini_service without risking blocking the main UI process.
# Usage: python remote_runner.py '{"text":"...","style":"...","add_emojis":false}'

async def call_service(payload):
    # Import here to avoid doing it at module import time in the parent.
    try:
        from app.service import gemini_service
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"import_error: {e}"}, ensure_ascii=False))
        return

    text = payload.get('text')
    style = payload.get('style')
    add_emojis = payload.get('add_emojis', False)

    try:
        # gemini_service.draft_letter is async in this project
        res = await gemini_service.draft_letter(text, style, add_emojis)
        print(json.dumps({"ok": True, "result": res}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"service_error: {e}"}, ensure_ascii=False))


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"ok": False, "error": "no_input"}, ensure_ascii=False))
        return
    try:
        payload = json.loads(sys.argv[1])
    except Exception as e:
        print(json.dumps({"ok": False, "error": f"bad_input: {e}"}, ensure_ascii=False))
        return

    asyncio.run(call_service(payload))

if __name__ == '__main__':
    main()
