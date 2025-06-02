from flask import Blueprint, jsonify, request
from app.models import Tours, TourImages, Products, ProductImages
from app.forms import TourSearchForm, MerchandiseSearchForm
from sqlalchemy.orm import selectinload


filter = Blueprint('filter', __name__)


@filter.route('/search_tours', methods=['GET'])
def search_tours():
    '''
    allows users to filter tours based on a certain criteria
    '''
    form = TourSearchForm(request.args)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)

    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    name = form.name.data.lower()
    destination = form.destination.data.lower()
    start_date = form.start_date.data
    end_date = form.end_date.data
    days = form.days.data
    nights = form.nights.data
    maximum_price = form.maximum_price.data
    minimum_price = form.minimum_price.data
    status = form.status.data.lower()

    try:
        tours = Tours.query.options(selectinload(Tours.images))

        if name:
            tours = tours.filter(Tours.name.ilike(f"%{name}%"))

        if destination:
            tours = tours.filter(Tours.destination.ilike(f"%{destination}%"))

        if start_date:
            tours = tours.filter(Tours.start_date == start_date)

        if end_date:
            tours = tours.filter(Tours.end_date == end_date)

        if days:
            tours = tours.filter(Tours.days == days)

        if nights:
            tours = tours.filter(Tours.nights == nights)

        if maximum_price:
            tours = tours.filter(Tours.final_price <= maximum_price)

        if minimum_price:
            tours = tours.filter(Tours.final_price >= minimum_price)

        if status:
            tours = tours.filter(Tours.status.ilike(f"%{status}%"))

        paginated_results = tours.paginate(page=page, per_page=per_page)

        if not paginated_results.items:
            return jsonify({'error': 'No tours match your selected criteria'}), 404

        results = [{
            'tour_id': tour.id,
            'name': tour.name,
            'destination': tour.destination,
            'start_date': tour.start_date.isoformat(),
            'days': tour.days,
            'nights': tour.nights,
            'price': tour.final_price,
            'discount': tour.discount_percent,
            'status': tour.status,
            'image': tour.images[0].filename if tour.images else None
            } for tour in paginated_results.items]

        response = {
                'tours': results,
                'pagination': {
                    'total': paginated_results.total,
                    'page': paginated_results.page,
                    'per_page': paginated_results.per_page,
                    'pages': paginated_results.pages,
                    'next': paginated_results.next_num if paginated_results.has_next else None,
                    'previous': paginated_results.prev_num if paginated_results.has_prev else None
                    }
                }
        return jsonify(response), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500


@filter.route('/search_merchandise', methods=['GET'])
def search_merchandise():
    '''
    allows users to filter merchandises
    '''
    form = MerchandiseSearchForm(request.args)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)

    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    name = form.name.data
    product_type = form.product_type.data
    size = form.data.size
    maximum_price = form.maximum_price.data
    minimum_price = form.minimum_price.data

    try:
        products = Products.query.options(selectinload(Products.images))

        if name:
            products = products.filter(Products.name.ilike(f"%{name}%"))

        if product_type:
            products = products.filter(Products.product_type.ilike(f"%{product_type}%"))

        if size:
            products = products.filter(Products.size.ilike(f"%{size}%"))

        if maximum_price:
            products = products.filter(Products.final_price <= maximum_price)

        if minimum_price:
            products = products.filter(Prodcts.final_price >= minimum_price)

        paginated_results = products.paginate(page=page, per_page=per_page)

        if not paginated_results.items:
            return jsonify({'error': 'No merchandise match your selected criteria'}), 404

        results = [{
            'product_id': item.id,
            'name': item.name,
            'original_price': item.original_price,
            'discount_rate': item.discount_rate,
            'final_price': item.final_price,
            'status': item.status,
            'size': item.size,
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



