web: gunicorn social_media_Project.wsgi --log-file -
#or works good with external database
web: python manage.py migrate && gunicorn social_media_Project.wsgi