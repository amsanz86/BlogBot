import http.server
import socketserver
import os
import webbrowser

PORT = 8000
DIRECTORY = "web"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

def serve():
    if not os.path.exists(DIRECTORY):
        print(f"Error: La carpeta '{DIRECTORY}' no existe.")
        return

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"=== VISTA PREVIA DEL BLOG ACTIVADA ===")
        print(f"Abriendo: http://localhost:{PORT}")
        print("Presiona Ctrl+C para detener el servidor.")
        
        # Intentar abrir el navegador automáticamente
        webbrowser.open(f"http://localhost:{PORT}")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor detenido.")

if __name__ == "__main__":
    serve()
