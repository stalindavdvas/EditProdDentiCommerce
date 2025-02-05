# productos/routes.py
from . import productos_bp
from flask import request, jsonify
from database import get_db_connection

@productos_bp.route('/<int:product_id>', methods=['PUT'])
def actualizar_producto(product_id):
    """Update by ID"""
    data = request.get_json()
    nombre = data.get('name')
    descripcion = data.get('description')
    precio = data.get('price')
    stock = data.get('stock')
    categoria_id = data.get('category_id')
    imagen_url = data.get('image_url')

    # Validar campos obligatorios
    if not (nombre and precio and categoria_id):
        return jsonify({'error': 'name, price and category are required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update database
        query = """
            UPDATE products
            SET name = %s, description = %s, price = %s, stock = %s, 
                category_id = %s, image_url = %s, updated_at = NOW()
            WHERE id = %s
            RETURNING id, name, description, price, stock, category_id, image_url;
        """
        cursor.execute(query, (nombre, descripcion, precio, stock, categoria_id, imagen_url, product_id))
        producto = cursor.fetchone()

        if not producto:
            return jsonify({'error': 'Product not found'}), 404

        conn.commit()
        return jsonify({
            'id': producto[0],
            'name': producto[1],
            'description': producto[2],
            'price': str(producto[3]),
            'stock': producto[4],
            'category_id': producto[5],
            'image_url': producto[6]
        }), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        # Close database connection
        cursor.close()
        conn.close()