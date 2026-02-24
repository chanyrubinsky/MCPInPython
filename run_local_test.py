"""
Local test runner that avoids Streamlit and remote gRPC calls.
It forces local mock usage (MCP_USE_REMOTE=0) and prints the generated Hebrew text.
"""
import os
import sys
import asyncio
import traceback
from dotenv import load_dotenv

# ensure project root on path
here = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(here, '.'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# load .env (if exists) from project root
load_dotenv(os.path.join(project_root, '.env'))

# Force local mock (do not attempt remote calls)
os.environ['MCP_USE_REMOTE'] = '0'

def safe_print(*a, **k):
    print(*a, **k)
    try:
        sys.stdout.flush()
    except Exception:
        pass

safe_print('Local test runner')
safe_print('MCP_USE_REMOTE=', os.environ.get('MCP_USE_REMOTE'))
safe_print('GEMINI_API_KEY present:', bool(os.getenv('GEMINI_API_KEY')))

async def main():
    try:
        # Import late, after we've set MCP_USE_REMOTE
        from app.web_ui import mcp_api
    except Exception as e:
        safe_print('Failed to import mcp_api:')
        traceback.print_exc()
        return

    try:
        res = await mcp_api.generate_letter('שלום, זה מבחן מקומי ללא רשת', 'רשמי', True)
        safe_print('\n--- GENERATED TEXT ---\n')
        safe_print(res)
        safe_print('\n--- END ---')
    except Exception as e:
        safe_print('Error while generating letter:')
        traceback.print_exc()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception:
        safe_print('Unhandled exception:')
        traceback.print_exc()
