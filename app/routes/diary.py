from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import DiaryEntry, EntryImage, Tag
from datetime import datetime
import os
from werkzeug.utils import secure_filename

bp = Blueprint('diary', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
UPLOAD_FOLDER = 'app/static/uploads/entries'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_or_create_tags(tag_string):
    """Parse comma-separated tags and create/get Tag objects"""
    if not tag_string:
        return []
    
    tag_names = [t.strip().lower() for t in tag_string.split(',') if t.strip()]
    tags = []
    
    for name in tag_names:
        # Remove # if present
        name = name.lstrip('#')
        if not name:
            continue
            
        tag = Tag.query.filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name)
            db.session.add(tag)
        tags.append(tag)
    
    return tags

@bp.route('/entry/new', methods=['GET', 'POST'])
@login_required
def new_entry():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        mood = request.form.get('mood')
        date_str = request.form.get('date')
        tags_str = request.form.get('tags', '')
        
        # Parse date
        if date_str:
            entry_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            entry_date = datetime.utcnow().date()
        
        # Create entry
        entry = DiaryEntry(
            title=title,
            content=content,
            mood=mood,
            date=entry_date,
            author=current_user
        )
        
        # Add tags
        entry.tags = get_or_create_tags(tags_str)
        
        db.session.add(entry)
        db.session.commit()
        
        # Handle image uploads
        if 'images' in request.files:
            files = request.files.getlist('images')
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(f"{entry.id}_{datetime.utcnow().timestamp()}_{file.filename}")
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(filepath)
                    
                    image = EntryImage(filename=filename, entry=entry)
                    db.session.add(image)
            
            db.session.commit()
        
        flash('Diary entry created successfully!', 'success')
        return redirect(url_for('main.home'))
    
    today = datetime.utcnow().strftime('%Y-%m-%d')
    return render_template('diary/new_entry.html', today=today)

@bp.route('/entry/<int:id>')
@login_required
def entry_detail(id):
    entry = DiaryEntry.query.get_or_404(id)
    
    # Ensure user can only view their own entries
    if entry.user_id != current_user.id:
        flash('You do not have permission to view this entry.', 'danger')
        return redirect(url_for('main.home'))
    
    return render_template('diary/entry_detail.html', entry=entry)

@bp.route('/entry/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_entry(id):
    entry = DiaryEntry.query.get_or_404(id)
    
    if entry.user_id != current_user.id:
        flash('You do not have permission to edit this entry.', 'danger')
        return redirect(url_for('main.home'))
    
    if request.method == 'POST':
        entry.title = request.form.get('title')
        entry.content = request.form.get('content')
        entry.mood = request.form.get('mood')
        
        date_str = request.form.get('date')
        if date_str:
            entry.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Update tags
        tags_str = request.form.get('tags', '')
        entry.tags = get_or_create_tags(tags_str)
        
        # Handle new image uploads
        if 'images' in request.files:
            files = request.files.getlist('images')
            for file in files:
                if file and file.filename and allowed_file(file.filename):
                    filename = secure_filename(f"{entry.id}_{datetime.utcnow().timestamp()}_{file.filename}")
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    
                    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                    file.save(filepath)
                    
                    image = EntryImage(filename=filename, entry=entry)
                    db.session.add(image)
        
        entry.updated_at = datetime.utcnow()
        db.session.commit()
        
        flash('Entry updated successfully!', 'success')
        return redirect(url_for('diary.entry_detail', id=entry.id))
    
    # Convert tags to comma-separated string for the form
    tags = ', '.join([tag.name for tag in entry.tags])
    return render_template('diary/edit_entry.html', entry=entry, tags=tags, title='Edit Entry')

@bp.route('/entry/<int:id>/delete', methods=['POST'])
@login_required
def delete_entry(id):
    entry = DiaryEntry.query.get_or_404(id)
    
    if entry.user_id != current_user.id:
        flash('You do not have permission to delete this entry.', 'danger')
        return redirect(url_for('main.home'))
    
    # Delete associated images
    for image in entry.images:
        filepath = os.path.join(UPLOAD_FOLDER, image.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
    
    db.session.delete(entry)
    db.session.commit()
    
    flash('Entry deleted successfully!', 'success')
    return redirect(url_for('main.home'))

@bp.route('/entry/<int:entry_id>/image/<int:image_id>/delete', methods=['POST'])
@login_required
def delete_image(entry_id, image_id):
    entry = DiaryEntry.query.get_or_404(entry_id)
    
    if entry.user_id != current_user.id:
        flash('You do not have permission to delete this image.', 'danger')
        return redirect(url_for('main.home'))
    
    image = EntryImage.query.get_or_404(image_id)
    if image.entry_id != entry_id:
        flash('Image not found.', 'danger')
        return redirect(url_for('diary.edit_entry', id=entry_id))
    
    # Delete file
    filepath = os.path.join(UPLOAD_FOLDER, image.filename)
    if os.path.exists(filepath):
        os.remove(filepath)
    
    db.session.delete(image)
    db.session.commit()
    
    flash('Image deleted successfully!', 'success')
    return redirect(url_for('diary.edit_entry', id=entry_id))
