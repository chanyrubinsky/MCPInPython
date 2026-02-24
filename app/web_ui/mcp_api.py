import os
import asyncio
import random
import json
import subprocess
from ..models.LetterStyle import LetterStyle

# Allow overriding to use remote Gemini: set MCP_USE_REMOTE=1 in the environment.
USE_REMOTE = str(os.getenv('MCP_USE_REMOTE', '0')).lower() in ('1', 'true', 'yes')
REMOTE_TIMEOUT_SEC = 6


async def _local_mock_generate(text: str, style: LetterStyle, add_emojis: bool) -> str:
    """Generate a friendly Hebrew letter locally (no external API).
    This is a simple, deterministic generator for dev/demo purposes.
    """
    # Determine style value (handle enum or string)
    s = None
    try:
        if hasattr(style, 'value'):
            s = style.value
        else:
            s = str(style)
    except Exception:
        s = str(style)

    t = text.strip()
    if not t:
        return ""

    # Compose different styles
    if s in ("רשמי", "FORMAL", "Formal"):
        body = f"לכבוד הנידון/ת,\n\n{t}\n\nבברכה,\nצוות MCP"
    elif s in ("מחורז", "RHYMED", "Rhymed"):
        # very simple rhymed-like output (for demo only)
        words = t.split()
        last = words[-1] if words else ''
        rhyme = last + ("ה" if last and not last.endswith("ה") else "")
        body = f"{t}\n\n{rhyme} — שורה שמנגנת ומתחרזת קצת.\nבברכה,\nMCP"
    elif s in ("תכני", "TECHNICAL", "Technical"):
        body = f"תקציר תכליתי:\n{t}\n\nנקודות מפתח:\n- קצר ותמציתי\n- מנוסח מקצועי\n"
    else:
        # friendly/default
        body = f"היי,\n{t}\nשמחנו לקרוא!\nבאהבה,\nMCP"

    if add_emojis:
        emojis = ["🙂", "✨", "👍", "💡", "📩", "🎉"]
        body = body + "\n\n" + ' '.join(random.sample(emojis, k=2))

    # simulate slight delay
    await asyncio.sleep(0.1)
    return body


async def _call_remote_subprocess(text: str, style, add_emojis: bool) -> (bool, str):
    """Call the remote_runner.py in a subprocess with timeout and return (ok, result_or_error)."""
    payload = {"text": text, "style": style, "add_emojis": add_emojis}
    cmd = ["python", os.path.join(os.path.dirname(__file__), "remote_runner.py"), json.dumps(payload, ensure_ascii=False)]

    try:
        # Use asyncio subprocess for non-blocking, but keep simple with run and timeout
        proc = await asyncio.create_subprocess_exec(*cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        try:
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=REMOTE_TIMEOUT_SEC)
        except asyncio.TimeoutError:
            proc.kill()
            return False, "timeout"
        if stderr:
            return False, stderr.decode('utf-8', errors='ignore')
        out = stdout.decode('utf-8', errors='ignore').strip()
        try:
            data = json.loads(out)
            return data.get('ok', False), data.get('result') or data.get('error')
        except Exception:
            return False, out
    except Exception as e:
        return False, str(e)


async def generate_letter(text: str, style: str, add_emojis: bool) -> str:
    """Generate a letter: prefer remote if USE_REMOTE, else local mock. Returns Hebrew string."""
    # basic validation
    if not isinstance(text, str) or not text.strip():
        return "נא להזין טקסט תקף לכתיבה."

    # map style string/name/value to LetterStyle enum if possible
    style_enum = None
    try:
        # If caller passed the enum already
        if isinstance(style, LetterStyle):
            style_enum = style
        else:
            # Try to match by value or name
            for s in LetterStyle:
                if style == s.value or style.upper() == s.name or style == s.name:
                    style_enum = s
                    break
    except Exception:
        # If LetterStyle isn't importable as enum, keep style as string
        style_enum = style

    if style_enum is None:
        style_enum = getattr(LetterStyle, 'FRIENDLY', None) or style

    if USE_REMOTE:
        ok, res = await _call_remote_subprocess(text, style_enum, add_emojis)
        if ok and isinstance(res, str) and res.strip():
            return res
        # else fall through to local mock

    try:
        return await _local_mock_generate(text, style_enum, add_emojis)
    except Exception as e:
        return f"שגיאה פנימית בייצור הטקסט: {e}"
