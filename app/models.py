from datetime import datetime
from app import db, login_manager, bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    profile_image = db.Column(db.String(200), default='default.jpg')
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Preferences
    language = db.Column(db.String(10), default='en')
    notifications_enabled = db.Column(db.Boolean, default=True)
    
    # Relationships
    entries = db.relationship('DiaryEntry', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class DiaryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(20))  # happy, sad, neutral, excited, angry
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    images = db.relationship('EntryImage', backref='entry', lazy=True, cascade='all, delete-orphan')
    tags = db.relationship('Tag', secondary='entry_tags', backref=db.backref('entries', lazy=True))
    
    def __repr__(self):
        return f'<DiaryEntry {self.title}>'

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    def __repr__(self):
        return f'<Tag {self.name}>'

# Association Table
entry_tags = db.Table('entry_tags',
    db.Column('entry_id', db.Integer, db.ForeignKey('diary_entry.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class EntryImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    entry_id = db.Column(db.Integer, db.ForeignKey('diary_entry.id'), nullable=False)
    
    def __repr__(self):
        return f'<EntryImage {self.filename}>'
