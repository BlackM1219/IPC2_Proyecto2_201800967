import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'example_inputs')
ALLOWED_EXTENSIONS = {'xml'}