# Piyu Flask Diary Web Application

A beautiful and functional web-based diary application built with Flask.

## Features

- 📝 Create, edit, and delete diary entries
- 📅 Calendar view to browse entries by date
- 🖼️ Add multiple photos to your entries
- 😊 Track your mood with each entry
- 👤 User authentication and profile management
- 🎨 Beautiful, responsive UI
- 🔒 Secure and private

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. **Install dependencies:**

```powershell
pip install -r requirements.txt
```

2. **Set up environment variables:**

Edit the `.env` file and update the `SECRET_KEY`:

```
SECRET_KEY=your-very-secret-key-here
```

3. **Initialize the database:**

```powershell
python run.py
```

The application will automatically create the database on first run.

## Running the Application

Start the Flask development server:

```powershell
python run.py
```

The application will be available at: `http://localhost:5000`

## Project Structure

```
DIARY/
├── app/
│   ├── __init__.py          # Flask app initialization
│   ├── models.py            # Database models
│   ├── routes/              # Route blueprints
│   │   ├── auth.py          # Authentication routes
│   │   ├── main.py          # Main app routes
│   │   ├── diary.py         # Diary entry routes
│   │   └── profile.py       # User profile routes
│   ├── templates/           # HTML templates
│   │   ├── base.html
│   │   ├── auth/            # Auth pages
│   │   ├── main/            # Main pages
│   │   ├── diary/           # Diary pages
│   │   └── profile/         # Profile pages
│   └── static/              # Static files
│       ├── css/
│       ├── js/
│       ├── images/
│       └── uploads/         # User uploads
├── config.py                # Configuration
├── run.py                   # Application entry point
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables
```

## Usage

### Creating an Account

1. Navigate to `http://localhost:5000`
2. Click "Get Started" or "Sign Up"
3. Fill in your details and create an account

### Writing Diary Entries

1. Log in to your account
2. Click "New Entry" in the navigation
3. Add a title, select your mood, write your thoughts
4. Optionally add photos
5. Click "Save Entry"

### Viewing Entries

- **Home**: See all your entries in a card layout
- **Calendar**: Browse entries by date
- **Gallery**: View all photos from your entries

## Database

The application uses SQLite by default. The database file (`diary.db`) will be created in the root directory.

### Database Models

- **User**: User accounts with authentication
- **DiaryEntry**: Diary entries with title, content, mood, and date
- **EntryImage**: Photos attached to diary entries

## Security Features

- Password hashing with bcrypt
- Session-based authentication with Flask-Login
- CSRF protection
- Secure file uploads with validation

## Customization

### Changing Colors

Edit `app/static/css/style.css` and modify the CSS variables:

```css
:root {
    --brown: #8B4513;
    --beige: #F5F5DC;
}
```

### Adding Languages

Update the language options in `app/templates/profile/language.html`

## Production Deployment

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Use a strong `SECRET_KEY`
3. Use PostgreSQL or MySQL instead of SQLite
4. Enable HTTPS and set `SESSION_COOKIE_SECURE=True`
5. Use a production WSGI server like Gunicorn

## License

This project is open source and available for personal use.

## Support

For issues or questions, please open an issue on the project repository.
