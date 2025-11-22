from flask import Blueprint, jsonify
from app.models import Destinations, DestinationImages
from sqlalchemy.orm import selectinload
from sqlalchemy import desc


dest_bp = Blueprint('dest_bp', __name__)

@dest_bp.route('/destinations', methods=['GET'])
def destinations():
    '''
    fetches the destinations from the table 
    returns an object containing destination details
    '''
    try:
        destination_records = Destinations.query.options(selectinload(Destinations.images)).order_by(desc(Destinations.created_at)).all()

        if not destination_records:
            return jsonify({"error": 'No destinations available at the moment. Please check again later'}), 404

        destinations = [{
            'destination_id': destination.id,
            'name': destination.name,
            'country': destination.country,
            'destination_type': destination.destination_type,
            'short_description': destination.short_description,
            'slug': destination.slug,
            'image': destination.images[0].filename if destination.images else None
            } for destination in destination_records]

        return jsonify(destinations), 200
    except Exception as e:
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
