from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Configuración de la conexión a PostgreSQL
def get_db_connection():
    return psycopg2.connect(
        host="host.docker.internal",  # host
        database="items",             # database name
        user="postgres",              # User PostgreSQL
        password="stalin"             # password de PostgreSQL
    )

@app.route('/productos/<int:product_id>', methods=['PUT'])
def actualizar_producto(product_id):
    """Actualizar un producto existente por ID"""
    data = request.get_json()
    nombre = data.get('name')
    descripcion = data.get('description')
    precio = data.get('price')
    stock = data.get('stock')
    categoria_id = data.get('category_id')
    imagen_url = data.get('image_url')

    if not (nombre and precio and categoria_id):
        return jsonify({'error': 'Nombre, precio y categoría son obligatorios'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
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
            return jsonify({'error': 'Producto no encontrado'}), 404

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
        cursor.close()
        conn.close()

# Bloque __main__ to execute el microservicio in port 5003
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
