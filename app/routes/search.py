from flask import Blueprint, jsonify, request
from app.models import Tours, TourImages, Products, ProductImages
from app.forms import TourSearchForm, MerchandiseSearchForm


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
