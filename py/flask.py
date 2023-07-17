from flask import Flask, jsonify, request
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/productdb'
mongo = PyMongo(app)


@app.route('/products', methods=['GET'])
def get_products():
    products = mongo.db.products.find()
    return jsonify([{
        'id': product['id'],
        'name': product['name'],
        'image': product['image']
    } for product in products])


@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = mongo.db.products.find_one({'id': product_id})
    if product:
        return jsonify({
            'id': product['id'],
            'name': product['name'],
            'image': product['image']
        })
    return jsonify({'error': 'Product not found'})


@app.route('/products', methods=['POST'])
def create_product():
    new_product = {
        'id': request.json['id'],
        'name': request.json['name'],
        'image': request.json['image']
    }
    result = mongo.db.products.insert_one(new_product)
    new_product['_id'] = str(result.inserted_id)
    return jsonify(new_product), 201


@app.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    updated_product = mongo.db.products.find_one_and_update(
        {'id': product_id},
        {'$set': {'name': request.json['name'], 'image': request.json['image']}},
        return_document=True
    )
    if updated_product:
        return jsonify({
            'id': updated_product['id'],
            'name': updated_product['name'],
            'image': updated_product['image']
        })
    return jsonify({'error': 'Product not found'})


@app.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = mongo.db.products.delete_one({'id': product_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Product deleted'})
    return jsonify({'error': 'Product not found'})


if __name__ == '__main__':
    app.run(debug=True)
