pip install -r requirements.txt

pyton manange.py makemigrations --noinput
pytho manage.py migrate --noinput

python manage.py collectstatic --noinput