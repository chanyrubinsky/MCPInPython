import sys
import os
import asyncio
from dotenv import load_dotenv

# Ensure project root is importable
here = os.path.abspath(os.path.dirname(__file__))
if here not in sys.path:
    sys.path.insert(0, here)

# Load .env from project folder
load_dotenv(os.path.join(here, '.env'))

print('Running smoke tests...')
print('GEMINI_API_KEY present in env:', bool(os.getenv('GEMINI_API_KEY')))

# 1) Import the Streamlit app module (import only, do not run server)
try:
    import importlib
    mod = importlib.import_module('app.web_ui.streamlit_app')
    print('Imported streamlit_app OK')
except Exception as e:
    print('Failed to import streamlit_app:', repr(e))

# 2) Call generate_letter from the mcp_api wrapper
try:
    mcp_api = importlib.import_module('app.web_ui.mcp_api')
    async def run_test():
        res = await mcp_api.generate_letter('שלום, זה מבחן קצר', 'רשמי', False)
        print('generate_letter result:\n', res)
    asyncio.run(run_test())
except Exception as e:
    print('Failed to run generate_letter:', repr(e))

print('Smoke tests finished')
