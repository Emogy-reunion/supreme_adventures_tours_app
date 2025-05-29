from Flask import Blueprint
from app.utils.role import role_required
from flask_jwt_extended import jwt_required
from app.models import Users, Tours, TourImages
from sqlalchemy.orm import selectinload

admin_posts_bp = Blueprint('admin_posts_bp', __name__)


@admin_posts_bp.routes('/admin_tour', methods=['GET'])
@jwt_required()
@role_required('admin')
def admin_tours():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    try:
        paginated_results = Tours.query.options(selectinload(Tours.images)).paginate(page=page, per_page=per_page, error_out=True)

        if not paginated_results.items:
            return jsonify({'error': 'No upcoming tours available at the moment. Please check again later!'}), 404

        tours = [{
            'name': tour.name,
            'destination': tour.location,
            'start_date': tour.start_date,
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

