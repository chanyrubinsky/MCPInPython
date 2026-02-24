def test_import_streamlit_app():
    import importlib
    mod = importlib.import_module('app.web_ui.streamlit_app')
    assert mod is not None
