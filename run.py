import sys, os
# Fuerza a Python a incluir la carpeta raíz del proyecto en el sys.path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
