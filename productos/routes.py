# productos/routes.py
from . import productos_bp  # Importar el Blueprint desde el módulo productos
from flask import request, jsonify
from database import get_db_connection  # Importar la conexión a la base de datos

# Registrar la ruta PUT /productos/<int:product_id> en el Blueprint
@productos_bp.route('/<int:product_id>', methods=['PUT'])
def actualizar_producto(product_id):
    """Actualizar un producto por ID"""
    data = request.get_json()
    nombre = data.get('name')
    descripcion = data.get('description')
    precio = data.get('price')
    stock = data.get('stock')
    categoria_id = data.get('category_id')
    imagen_url = data.get('image_url')

    # Validar campos obligatorios
    if not (nombre and precio and categoria_id):
        return jsonify({'error': 'Nombre, precio y categoría son obligatorios'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Actualizar el producto en la base de datos
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
            'price': str(producto[3]),  # Convertir a string para evitar problemas con JSON
            'stock': producto[4],
            'category_id': producto[5],
            'image_url': producto[6]
        }), 200
    except Exception as e:
        # En caso de error, hacer rollback y devolver el mensaje de error
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        # Cerrar la conexión a la base de datos
        cursor.close()
        conn.close()