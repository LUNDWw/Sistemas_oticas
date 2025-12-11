import sys
import threading
import webbrowser
from app import create_app
from app.config import DEBUG_MODE, HOST, PORT


def start_flask(open_browser=True):
    app = create_app()
    
    if getattr(sys, 'frozen', False):
        debug_mode = False
        
        try:
            import pyi_splash
            if pyi_splash.is_alive():
                pyi_splash.update_text('Iniciando sistema...')
                pyi_splash.close()
        except Exception:
            pass

        threading.Timer(1.5, lambda: webbrowser.open(f"http://{HOST}:{PORT}")).start()
    else:
        debug_mode = DEBUG_MODE
        if open_browser:
            threading.Timer(1.0, lambda: webbrowser.open(f"http://{HOST}:{PORT}")).start()

    app.run(debug=debug_mode, host=HOST, port=PORT)


if __name__ == '__main__':
    start_flask()
