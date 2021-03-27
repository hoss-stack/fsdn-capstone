. setup.sh
export ENV='test'
dropdb casting_agency_test
createdb casting_agency_test
python manager.py db upgrade
python manager.py seed
python test_app.py
export ENV='development'