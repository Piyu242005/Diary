from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from werkzeug.utils import secure_filename
import os

bp = Blueprint('profile', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'app/static/uploads/profiles'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile/profile.html')

@bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        
        # Check if username is taken by another user
        if username != current_user.username:
            existing_user = db.session.query(db.exists().where(
                (User.username == username) & (User.id != current_user.id)
            )).scalar()
            if existing_user:
                flash('Username already taken.', 'danger')
                return render_template('profile/account.html')
        
        # Check if email is taken by another user
        if email != current_user.email:
            from app.models import User
            existing_user = db.session.query(db.exists().where(
                (User.email == email) & (User.id != current_user.id)
            )).scalar()
            if existing_user:
                flash('Email already registered.', 'danger')
                return render_template('profile/account.html')
        
        current_user.username = username
        current_user.email = email
        
        # Handle profile image
        if 'profile_image' in request.files:
            file = request.files['profile_image']
            if file and allowed_file(file.filename):
                filename = secure_filename(f"{current_user.id}_{file.filename}")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(filepath)
                
                current_user.profile_image = filename
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('profile.profile'))
    
    return render_template('profile/account.html')

@bp.route('/language', methods=['GET', 'POST'])
@login_required
def language():
    if request.method == 'POST':
        lang = request.form.get('language')
        current_user.language = lang
        db.session.commit()
        flash('Language preference updated!', 'success')
        return redirect(url_for('profile.profile'))
    
    return render_template('profile/language.html')
