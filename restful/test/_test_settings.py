from usdarest.settings import *

# to use this file:
#   python manage.py test restful/test --settings=restful.test._test_settings -v 2

TEST_RUNNER = 'restful.test.runner.UnManagedModelTestRunner'

FIXTURE_DIRS = ('restful/test/fixtures',)

MIGRATION_MODULES = {'restful': 'migrations_not_used_in_tests'}
