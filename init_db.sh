#!/bin/bash

# This file wipes out the current database and migrations (if any) and starts
# from scratch.
#
# The current user must have privileges to create and drop PostgreSQL databases
# from the command line.  This requires superuser or CREATEDB privileges.
# see: http://www.postgresql.org/docs/9.1/static/sql-createdatabase.html
# see: http://www.postgresql.org/docs/9.1/static/sql-createuser.html
#
# File paths are relative to the current working directory.
# Only run from the root folder (usdarest) of the usdarest project.
#
# Current user must also be in a properly configured environment which
# includes an installation of Django REST Framework or the migration will
# fail.  In practice this should be a virtualenv.

echo "Drop database"
dropdb usdafood
echo "Clear old migrations"
mv './restful/migrations/'* ./restful/oldmigrations
echo "Create new database 'usdafood'"
createdb usdafood
echo "Load schema and data"
psql -d usdafood -f ./database/initial_build.sql
echo "Make migrations"
python manage.py makemigrations usdarest
echo "Apply migrations"
python manage.py migrate
echo "All done.  Exit."
exit 1
