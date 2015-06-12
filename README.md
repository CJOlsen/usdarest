# usdarest

A RESTful API for the USDA Food and Nutrition Database built using Django's Django REST Framework.

The data is owned by the USDA and available in several formats here: http://www.ars.usda.gov/Services/docs.htm?docid=24912

Currently includes a subset of the entire USDA dataset.  Provides endpoints for foods, nutrients and food groups.  After more thorough testing and finalization of project architecture the remaining data and endpoints will be included.

The API should be hosted and public shortly.


## Requirements

* a Unix type system, tested on Debian 8
* Django 1.8
* Python 3.4
* Django REST framework v3.1.3
* PostgreSQL
* virtualenv and pip are recommended

## Usage

Unit tests can be run from the command line using the command:

    python manage.py test --settings=restful.test.test_settings -v 2

For a full working local copy:

* install and configure PostgreSQL (http://www.postgresql.org/docs/9.0/static/tutorial.html)
* install virtualenv (https://virtualenv.pypa.io/en/latest/)
* enter virtual environment configured to run Python 3.4
* install Django 1.8 (https://www.djangoproject.com/download/)
* install Django REST framework (http://www.django-rest-framework.org/tutorial/quickstart/)
* update and rename usdarest/usdarest/local_settings_template.py
* run init_db.sh from (and in) project's root directory
* run tests: python manage.py test --settings=restful.test.test_settings -v 2
* run server: python manage.py runserver


## About

This project is a migration in progress from Django/jQuery to Django REST Framework.

Current URL patterns:

 * foods/\<food id\>/seqs/\<seq id\>/nutrients/\<nutrient id\>  (seq id's correspond to measures)
 * nutrients/\<nutrient id\>

## Copyright

2015 Christopher Olsen.



## License

Please check back later.
