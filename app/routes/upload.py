from flask import Blueprint, request, jsonify
from app.forms import TourUploadForm



post = Blueprint('post', __name__)

@post.route('/upload_tour', methods=['POST'])
@jwt_required()
@role_required('admin')
def upload_tour():
    '''
    allows admins to upload tours
    it validates the input
    saves the files in a folder
    saves the filenames in a database
    '''
    if not request.files:
        return jsonify({'error': 'No images selected. Select one or more images and try again!'}), 400

    form = TourUploadForm(request.form)

    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    name = form.name.data.lower()
    start_location = form.start_location.data.lower()
    location = form.location.data.lower()
    description = form.description.data
    start_date = form.start_data.data
    end_date = form.end_date.data
    days = form.days.data
    nights = form.nights.data
    original_price = form.original_price.data
    discount_percent = form.discount_percent.data
    final_price = original_price
    included = form.included.data
    excluded = form.excluded.data
    file = request.files.getlist('files')
