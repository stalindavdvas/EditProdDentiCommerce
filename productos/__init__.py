# productos/__init__.py
from flask import Blueprint

# Create blueprint to routes
productos_bp = Blueprint('productos', __name__)

# import routes for products
from . import routes