pip install -r requirements.txt

python3.9 manange.py makemigrations --noinput
python3.9 manage.py migrate --noinput

python3.9 manage.py collectstatic --noinput