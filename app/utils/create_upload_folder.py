'''
creates the upload folder if it doesn't exist
'''
import os

def create_upload_folder(app):
    '''
    checks it the uploads folder is available
    if not it is created
    if it exists nothing happens
    '''
    upload_path = os.path.join(app.root_path, 'static', 'uploads')
    if not os.path.exists(upload_path):
        os.makedirs(upload_path)
