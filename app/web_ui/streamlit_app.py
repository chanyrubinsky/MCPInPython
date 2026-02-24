import asyncio
try:
    import streamlit as st
except Exception:
    # lightweight stub so static analysis / tests can import this module without Streamlit installed
    class _STStub:
        def set_page_config(self, *a, **k):
            pass
        def title(self, *a, **k):
            pass
        def sidebar(self):
            return self
        def form(self, *a, **k):
            class _DummyCtx:
                def __enter__(self):
                    return self
                def __exit__(self, exc_type, exc, tb):
                    return False
            return _DummyCtx()
        def text_area(self, *a, **k):
            return ""
        def selectbox(self, *a, **k):
            return ""
        def checkbox(self, *a, **k):
            return False
        def form_submit_button(self, *a, **k):
            return False
        def error(self, *a, **k):
            pass
        def spinner(self, *a, **k):
            class _DummySpinner:
                def __enter__(self):
                    return self
                def __exit__(self, exc_type, exc, tb):
                    return False
            return _DummySpinner()
        def subheader(self, *a, **k):
            pass
        def write(self, *a, **k):
            pass
        def download_button(self, *a, **k):
            pass
        def info(self, *a, **k):
            pass
        def success(self, *a, **k):
            pass
    st = _STStub()

import os
import sys
import socket
from importlib import import_module
from importlib import util as importutil
from dotenv import load_dotenv
import streamlit as st  # prefer real import here for enhanced features

# Ensure the project root (pythonProject) is on sys.path so `app` can be imported when running with streamlit
here = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(here, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Load .env from project root so GEMINI_API_KEY or GOOGLE_API_KEY are available
load_dotenv(os.path.join(project_root, '.env'))

# small helper functions
def sdk_installed() -> bool:
    # check if google.generativeai (or google.genai) is importable
    try:
        return importutil.find_spec('google.generativeai') is not None or importutil.find_spec('google.genai') is not None
    except Exception:
        return False

def api_key_present() -> bool:
    return bool(os.getenv('GEMINI_API_KEY') or os.getenv('GOOGLE_API_KEY'))

def can_reach_google(host: str = 'ai.google.com', port: int = 443, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except Exception:
        return False

# Lazy import LetterStyle at runtime to avoid static-analysis import errors
try:
    LetterStyle = import_module('app.models.LetterStyle').LetterStyle
    style_options = [s.value for s in LetterStyle]
except Exception:
    # fallback default options (in Hebrew, matching LetterStyle values)
    style_options = ["רשמי", "מחורז", "תכני", "חברי"]

# עיצוב כללי
st.set_page_config(page_title="MCP - מחולל מכתבים", layout="centered")

# סגנון CSS עדין
st.markdown(
    "<style>\n"
    "body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial; }\n"
    ".card {background: #ffffff; border-radius: 10px; padding: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.06);}\n"
    ".muted {color:#6b7280;}\n"
    "</style>",
    unsafe_allow_html=True,
)

# צדבר עם סטטוס
sidebar = st.sidebar
sidebar.title("הגדרות")
sidebar.markdown("---")
api_key = sidebar.text_input("מפתח API ל‑Gemini (אופציונלי)", type="password")
use_remote = sidebar.checkbox("להשתמש בשירות חיצוני (אם זמין)", value=False)
sidebar.markdown("---")
# סטטוס חבילות / רשת
sdk_ok = sdk_installed()
key_ok = api_key_present() or bool(api_key)
net_ok = can_reach_google()
sidebar.markdown("**סטטוס שירות**")
sidebar.write(f"SDK מותקן: {'✅' if sdk_ok else '❌'}")
sidebar.write(f"מפתח API מוגדר: {'✅' if key_ok else '❌'}")
sidebar.write(f"חיבור ל‑Google: {'✅' if net_ok else '❌'}")
sidebar.info("אם אחד מהפריטים ❌ — הממשק ישתמש בגנרטור מקומי בעברית (ולא יקיים קריאות חיצוניות)")

# כותרת ראשית
st.markdown('<div class="card"><h1 style="margin:0;">MCP — מעצב מכתבים</h1><p class="muted">הכנס/י טקסט בעברית, בחרי סגנון וקבלי נוסח משופר ומעוצב.</p></div>', unsafe_allow_html=True)
st.write("")

with st.form(key="letter_form"):
    st.subheader("הזן טקסט")
    text = st.text_area("הזן את הטקסט שברצונך לשכתב", height=220, placeholder="כתוב כאן את תוכן המכתב...")
    col1, col2 = st.columns([3,1])
    with col1:
        style = st.selectbox("בחר סגנון", style_options)
    with col2:
        add_emojis = st.checkbox("הכנס אימוג'ים", value=False)
        submitted = st.form_submit_button("צור מכתב")

    # דוגמאות מהירות
    st.markdown("**תבניות דוגמה:**")
    c1, c2, c3 = st.columns(3)
    if c1.button("טקסט רשמי לדוגמה"):
        text = "תודה על פנייתכם. מבקשים עדכון על סטטוס הפרויקט עד יום חמישי."
    if c2.button("טקסט חברי לדוגמה"):
        text = "היי, ממש לפי התכנון — נתראה מחר! תודה רבה :)"
    if c3.button("טקסט תכני לדוגמה"):
        text = "מבקשים לספק את הנתונים הבאים: מזהה, תאריך, סכום." 

if submitted:
    if not text.strip():
        st.error("נא להזין טקסט לפני יצירה.")
    else:
        # אם הוזן מפתח API בסיידבר — נעדכן את משתנת הסביבה כך שה‑gemini_service יוכל להשתמש בו
        if api_key and isinstance(api_key, str) and api_key.strip():
            os.environ['GEMINI_API_KEY'] = api_key.strip()
            st.info("מפתח API הוגדר לשימוש בשירות Gemini.")

        # import the UI wrapper lazily to avoid static-analysis issues
        mcp_api = import_module('app.web_ui.mcp_api')
        with st.spinner("מייצר את המכתב... אנא המתן"):
            # run the async function in the event loop
            try:
                # respect sidebar choice to use remote
                if use_remote:
                    os.environ['MCP_USE_REMOTE'] = '1'
                result = asyncio.get_event_loop().run_until_complete(mcp_api.generate_letter(text, style, add_emojis))
            except RuntimeError:
                # If no running event loop (some Streamlit setups), create a new one
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(mcp_api.generate_letter(text, style, add_emojis))

        st.subheader("התוצאה")
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.code(result)
        st.markdown('</div>', unsafe_allow_html=True)
        cold1, cold2 = st.columns([1,1])
        with cold1:
            st.download_button("הורד כמסמך .txt", result, file_name="letter.txt")
        with cold2:
            st.button("העתק לתזכיר") and st.write("המלל הועתק ללוח (דמה)")
        st.success("המכתב נוצר בהצלחה")

# הערות שימוש והוראות מהירות
st.markdown("---")
st.markdown("**טיפים:** אם נטפרי/חומת אש חוסמת את החיבור ל‑Google, סמןו \"להשתמש בשירות חיצוני\" בסיידבר רק אם את בטוחה שיש חיבור רשת. אחרת הממשק יציג תוצאות מקומיות בעברית שנראות טוב לפרזנטציה/בדיקה.")
