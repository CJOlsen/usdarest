from usdarest.settings import *

# to use this file: python manage.py test --settings=restful.test.test_settings -v 2

TEST_RUNNER = 'restful.test.runner.UnManagedModelTestRunner'

FIXTURE_DIRS = ('restful/test_fixtures',)

MIGRATION_MODULES = {'restful': 'migrations_not_used_in_tests'}
