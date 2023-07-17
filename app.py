from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# MongoDB configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/productsdb1'
mongo = PyMongo(app)


@app.route('/products1', methods=['GET'])
def get_products1():
    products1 = mongo.db.products1.find()
    return jsonify([{
        'id': product['id'],
        'name': product['name'],
        'phone': product['phone'],
        # 'phone': product['phone']
    } for product in products1])


@app.route('/products1/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = mongo.db.products1.find_one({'id': product_id})
    if product:
        return jsonify({
            'id': product['id'],
            'name': product['name'],
            'phone': product['phone'],
            # 'phone': product['phone']
        })
    return jsonify({'error': 'Product not found'})


@app.route('/products1', methods=['POST'])
def create_product():
    new_product = {
        'id': request.json['id'],
        'name': request.json['name'],
        'phone': request.json['phone'],
        # 'phone': request.json['phone']
    }
    result = mongo.db.products1.insert_one(new_product)
    new_product['_id'] = str(result.inserted_id)
    return jsonify(new_product), 201


@app.route('/products1/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    updated_product = mongo.db.products1.find_one_and_update(
        {'id': product_id},
        {'$set': {'name': request.json['name']}},
        return_document=True
    )
    if updated_product:
        return jsonify({
            'id': updated_product['id'],
            'name': updated_product['name'],
            'phone': updated_product['phone']
        })
    return jsonify({'error': 'Product not found'})


@app.route('/products1/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    result = mongo.db.products1.delete_one({'id': product_id})
    if result.deleted_count > 0:
        return jsonify({'message': 'Product deleted'})
    return jsonify({'error': 'Product not found'})


if __name__ == '__main__':
    app.run(debug=True)
