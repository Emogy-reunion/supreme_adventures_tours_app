from flask import Blueprint, request, jsonify, current_app
from app.forms import ToursUploadForm, ProductsUploadForm
from app.utils.discount import calculate_final_price
from app.utils.check_file_extension import check_file_extension
from app.models import Tours, TourImages, db, Products, ProductImages
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.role import role_required
from werkzeug.utils import secure_filename



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
        return jsonify({'error': 'No images selected. Select three or more images and try again!'}), 400

    form = TourUploadForm(request.form)

    if not form.validate():
        return jsonify({'errors': form.errors}), 400

    name = form.name.data.lower()
    start_location = form.start_location.data.lower()
    destination = form.destination.data.lower()
    description = form.description.data
    start_date = form.start_date.data
    end_date = form.end_date.data
    days = form.days.data
    nights = form.nights.data
    original_price = form.original_price.data
    discount_percent = form.discount_percent.data
    final_price = original_price
    included = form.included.data
    excluded = form.excluded.data
    status = form.status.data
    files = request.files.getlist('files')

    if discount_percent > 0:
        final_price = calculate_final_price(discount_percent=discount_percent, original_price=original_price)

    if not files or len(files) < 3:
        return jsonify({'error': 'You must upload at least three images.'}), 400

    if len(files) > 7:
        return jsonify({'error': 'You can upload a maximum of 7 images only.'}), 400
     
     try:
         user_id = int(get_jwt_identity())

         tour = Tours(name=name, user_id=user_id, start_location=start_location, destination=destination, description=description, start_date=start_date,
                      end_date=end_date, days=days, nights=nights, original_price=original_price, discount_percent=discount_percent, status=status,
                      final_price=final_price, included=included, excluded=excluded)
         db.session.add(tour)
         db.session.flush()

         for file in files:
             if file and check_file_extension(file.filename):
                 filename = secure_filename(file.filename)
                 file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                 tour_image = TourImages(tour_id=tour.id, filename=filename)
                 db.session.add(tour_image)
            else:
                return jsonify({'error': 'Invalid image file extension or file missing. Please try again!'}), 400
        db.session.commit()
        return jsonify({'success': 'Tour uploaded successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500

@post.route('/upload_product', methods=['POST'])
@jwt_required()
@role_required('admin')
def upload_product():
    '''
    allows admins to upload tours
    it validates the input
    saves the files in a folder
    saves the filenames in a database
    '''
    if not request.files:
        return jsonify({'error': 'No images selected. Select three or more images and try again!'}), 400

    form = ProductsUploadForm(request.form)

    if not form.validate():
        return jsonify({"errors": form.errors}), 400

    name = form.name.data
    original_price = form.original_price.data
    discount_percent = form.discount_rate.data
    product_type = form.product_type.data
    final_price = original_price
    description = form.description.data
    status = form.status.data
    size = form.size.data
    files = request.files.getlist('images')

    if discount_percent > 0:
        final_price = calculate_final_price(discount_percent=discount_percent, original_price=original_price)

    if not files or len(files) < 3:
        return jsonify({'error': 'You must upload at least three images.'}), 400

    if len(files) > 7:
        return jsonify({'error': 'You can upload a maximum of 7 images only.'}), 400

    try:
        user_id = int(get_jwt_identity())
        product = Products(name=name, user_id=user_id, product_type=product_type, original_price=original_price,
                           discount_rate=discount_percent, final_price=final_price, description=description,
                           status=status, size=size)
        db.session.add(product)
        db.session.flush()

        for file in files:
            if file and check_file_extension(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                
                product_image = ProductImages(product_id=product.id, filename=filename)
                db.session.add(product_image)
            else:
                return jsonify({'error': 'Invalid image file extension or file missing. Please try again!'}), 400
        db.session.commit()
        return jsonify({'success': 'Tour uploaded successfully!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'An unexpected error occured. Please try again!'}), 500
