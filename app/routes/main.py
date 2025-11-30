from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required, current_user
from app.models import DiaryEntry, Tag
from app import db
from sqlalchemy import func
from datetime import datetime
import calendar

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('auth/onboarding.html')

@bp.route('/home')
@login_required
def home():
    # Search and Filter
    query = request.args.get('q')
    mood_filter = request.args.get('mood')
    tag_filter = request.args.get('tag')
    
    entries_query = DiaryEntry.query.filter_by(user_id=current_user.id)
    
    if query:
        entries_query = entries_query.filter(
            (DiaryEntry.title.ilike(f'%{query}%')) | 
            (DiaryEntry.content.ilike(f'%{query}%'))
        )
    
    if mood_filter:
        entries_query = entries_query.filter_by(mood=mood_filter)
    
    if tag_filter:
        entries_query = entries_query.join(DiaryEntry.tags).filter(Tag.name == tag_filter)
        
    entries = entries_query.order_by(DiaryEntry.date.desc()).all()
    
    # Dashboard Stats
    total_entries = len(current_user.entries)
    
    current_month = datetime.now().month
    current_year = datetime.now().year
    entries_this_month = DiaryEntry.query.filter_by(user_id=current_user.id).filter(
        func.extract('month', DiaryEntry.date) == current_month,
        func.extract('year', DiaryEntry.date) == current_year
    ).count()
    
    # Most common mood
    most_common_mood = db.session.query(DiaryEntry.mood, func.count(DiaryEntry.mood))\
        .filter_by(user_id=current_user.id)\
        .filter(DiaryEntry.mood.isnot(None))\
        .group_by(DiaryEntry.mood)\
        .order_by(func.count(DiaryEntry.mood).desc())\
        .first()
    
    stats = {
        'total_entries': total_entries,
        'entries_this_month': entries_this_month,
        'most_common_mood': most_common_mood[0] if most_common_mood else None
    }
    
    return render_template('main/home.html', entries=entries, stats=stats)

@bp.route('/calendar')
@login_required
def calendar_view():
    return render_template('main/calendar.html')

@bp.route('/api/calendar-entries')
@login_required
def calendar_entries():
    """API endpoint to get entries for calendar view"""
    year = request.args.get('year', datetime.now().year, type=int)
    month = request.args.get('month', datetime.now().month, type=int)
    
    entries = DiaryEntry.query.filter_by(user_id=current_user.id).filter(
        func.extract('year', DiaryEntry.date) == year,
        func.extract('month', DiaryEntry.date) == month
    ).all()
    
    entries_data = []
    for entry in entries:
        entries_data.append({
            'id': entry.id,
            'title': entry.title,
            'date': entry.date.strftime('%Y-%m-%d'),
            'day': entry.date.day,
            'mood': entry.mood,
            'preview': entry.content[:50] + '...' if len(entry.content) > 50 else entry.content
        })
    
    return jsonify(entries_data)

@bp.route('/gallery')
@login_required
def gallery():
    return render_template('main/gallery.html')

@bp.route('/faq')
@login_required
def faq():
    return render_template('main/faq.html')

@bp.route('/rate-us')
@login_required
def rate_us():
    return render_template('main/rate_us.html')

@bp.route('/privacy-policy')
def privacy_policy():
    return render_template('main/privacy_policy.html')

@bp.route('/notifications')
@login_required
def notifications():
    return render_template('main/notifications.html')
