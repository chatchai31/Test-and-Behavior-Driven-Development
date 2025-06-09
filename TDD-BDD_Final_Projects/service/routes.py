from flask import Flask, request, jsonify, abort
from service.common import status
from service import app
from service.models import Product, Category



def check_content_type(media_type):
    if request.content_type != media_type:
        abort(415, f"Content-Type must be {media_type}")

# Read a Product
@app.route("/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND)
    return jsonify(product.serialize()), status.HTTP_200_OK

# Update a Product
@app.route("/products/<int:product_id>", methods=["PUT"])
def update_products(product_id):
    """
    Update a Product
    This endpoint will update a Product based the body that is posted
    """
    app.logger.info("Request to Update a product with id [%s]", product_id)
    check_content_type("application/json")
    product = Product.find(product_id)
    if not product:
        abort(status.HTTP_404_NOT_FOUND, f"Product with id '{product_id}' was not found.")
    product.deserialize(request.get_json())
    product.id = product_id
    product.update()
    return product.serialize(), status.HTTP_200_OK

# Delete a Product
@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_products(product_id):
    """
    Delete a Product
    This endpoint will delete a Product based the id specified in the path
    """
    app.logger.info("Request to Delete a product with id [%s]", product_id)
    product = Product.find(product_id)
    if product:
        product.delete()
    return "", status.HTTP_204_NO_CONTENT

# List Products with optional filters
@app.route("/products", methods=["GET"])
def list_products():
    name = request.args.get("name")
    category = request.args.get("category")
    available = request.args.get("available")

    if name:
        products = Product.find_by_name(name)
    elif category:
        try:
            category_enum = getattr(Category, category.upper())
            products = Product.find_by_category(category_enum)
        except AttributeError:
            return jsonify({"error": f"Invalid category: {category}"}), status.HTTP_400_BAD_REQUEST
    elif available:
        available_value = available.lower() in ["true", "yes", "1"]
        products = Product.find_by_availability(available_value)
    else:
        products = Product.all()

    results = [product.serialize() for product in products]
    return jsonify(results), status.HTTP_200_OK

# Create Product (if needed)
@app.route("/products", methods=["POST"])
def create_product():
    check_content_type("application/json")
    product = Product()
    product.deserialize(request.get_json())
    product.create()
    return jsonify(product.serialize()), status.HTTP_201_CREATED