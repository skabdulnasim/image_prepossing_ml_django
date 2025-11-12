Run migrations:

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver


Now the backend endpoints are:

POST /api/upload/ — form-data image → returns {id, url}

POST /api/save_crop/ — JSON payload with original_id, selection (bbox or polygon), label, gender, age → returns saved crop record

GET /api/originals/ and GET /api/crops/ for listing