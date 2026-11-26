@echo off

cd /d "C:\Users\Admin\Desktop\MarvelSpace"

call ".venv\Scripts\activate.bat"

python manage.py cleanup_stories

deactivate