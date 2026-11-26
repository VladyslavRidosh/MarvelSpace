
# MarvelSpace 🦸

A social network for Marvel fans, inspired by Instagram.

Users can explore the Marvel universe, publish posts, share stories, follow other users and interact with the community.

## Technologies

- Python
- Django 6.1.3
- SQLite
- HTML
- CSS
- JavaScript
- Pillow

## Features

- User registration and authentication
- User profiles and avatars
- Posts with images and videos
- Likes and following
- Stories with 24-hour expiration
- Search for users
- Explore page
- Responsive interface

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/VladyslavRidosh/MarvelSpace.git
cd MarvelSpace
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure local settings

Copy:

`config/local_settings.example.py`

to:

`config/local_settings.py`

Generate your own Django secret key:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Put the generated key into `config/local_settings.py`.

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Run the development server

```bash
python manage.py runserver
```

Open:

http://127.0.0.1:8000/

## Project Structure

```text
MarvelSpace/
├── accounts/
├── config/
├── core/
├── posts/
├── static/
├── templates/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

## Development

This project is currently under development.

## License

For educational and development purposes.
