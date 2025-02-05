# app.py
from flask import Flask
from flask_cors import CORS
from productos import productos_bp

app = Flask(__name__)
CORS(app)

# register blue print routes
app.register_blueprint(productos_bp, url_prefix='/productos')

# block main in port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)