python -m pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
python manage.py makemigrations  --noinput
python manage.py migrate  --noinput