. setup.sh
export ENV='test'
dropdb casting_agency_test
createdb casting_agency_test
python manage.py db upgrade
python manage.py seed
python test_app.py
export ENV='development'