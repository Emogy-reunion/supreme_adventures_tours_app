from flask import Blueprint, request, jsonify
from app.models import Products, ProductImages
from sqlalchemy.orm import selectinload

merch_bp = Blueprint('merch_bp', __name__)

@merch_bp.route('/merchandise', methods=['GET'])
def merchandise():
    '''
    retrieves merchandise from the database
    '''
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)

    try:
        paginated_results = Products.query.options(selectinload(Products.images)).paginate(page=page, per_page=per_page)

        if not paginated_results.items:
            return jsonify({'error': 'No available merchandise. Please check again later!'}), 404

        products = [{
            'product_id': item.id,
            'name': item.name.title(),
            'original_price': item.original_price,
            'discount_rate': item.discount_rate,
            'final_price': item.final_price,
            'status': item.status.capitalize(),
            'size': item.size,
            'status': item.status,
            'image': item.images[0].filename if item.images else None
            } for item in paginated_results.items]
        response = {
                'products': products,
                'pagination': {
                    'page': paginated_results.page,
                    'per_page': paginated_results.per_page,
                    'pages': paginated_results.pages,
                    'next': paginated_results.next_num if paginated_results.has_next else None,
                    'previous': paginated_results.prev_num if paginated_results.has_prev else None
                    }
                }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500

@merch_bp.route('/merchandise_details/<int:product_id>', methods=['GET'])
def merchandise_details(product_id):
    try:
        product = Products.query.options(selectinload(Products.images)).filter_by(id=product_id).first()

        if not product:
            return jsonify({'error': 'Product not found'}), 404

        product_details = {
                'product_id': product.id,
                'name': product.name.title(),
                'product_type': product.product_type,
                'original_price': product.original_price,
                'discount_rate': product.discount_rate,
                'final_price': product.final_price,
                'status': product.status,
                'size': product.size,
                'images': [image.filename for image in product.images] if product.images else []
                }
        return jsonify({'product_details': product_details}), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred. Please try again!'}), 500
