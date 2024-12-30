from feudle_app import create_app
import sys
from flask_cors import CORS

sys.path.append('../')
sys.path.append('./')
sys.path.append('./feudle_app/')

app = create_app()
CORS(app)  # Enable CORS for all routes

if __name__ == '__main__':
    app.run(debug=True, port=5001)
