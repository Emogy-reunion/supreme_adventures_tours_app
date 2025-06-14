from flask import Blueprint, jsonify, request
from app.models import Users, Tours, TourImages
from sqlalchemy.orm import selectinload

tours_bp = Blueprint('tours_bp', __name__)


@tours_bp.route('/tours', methods=['GET'])
def tours():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    try:
        paginated_results = Tours.query.options(selectinload(Tours.images)).paginate(page=page, per_page=per_page, error_out=True)

        if not paginated_results.items:
            return jsonify({'error': 'No upcoming tours available at the moment. Please check again later!'}), 404

        tours = [{
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
                'tours': tours,
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


@tours_bp.route('/tour_details/<int:tour_id>', methods=['GET'])
def tour_details(tour_id):
    '''
    retrieves all information about a tour from the database
    '''

    try:
        tour = Tours.query.options(selectinload(Tours.images)).filter_by(id=tour_id).first()

        if not tour:
            return jsonify({'error': 'Tour not found!'}), 404

        tour_details = {
                'tour_id': tour.id,
                'name': tour.name,
                'start_location': tour.start_location,
                'destination': tour.destination,
                'description': tour.description,
                'start_date': tour.start_date.isoformat(),
                'end_date': tour.end_date.isoformat(),
                'days': tour.days,
                'nights': tour.nights,
                'original_price': tour.original_price,
                'final_price': tour.final_price,
                'discount': tour.discount_percent,
                'status': tour.status,
                'included': tour.included,
                'excluded': tour.excluded,
                'images': [image.filename for image in tour.images] if tour.images else None
                }
        return jsonify({'tour_details': tour_details}), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
