from django.test.runner import DiscoverRunner
from django.db import connections, DEFAULT_DB_ALIAS

# see https://www.caktusgroup.com/blog/2010/09/24/simplifying-the-testing-of-unmanaged-database-models-in-django/
class UnManagedModelTestRunner(DiscoverRunner):
    """
    Test runner that automatically makes all unmanaged models managed for the
     duration of the test run.  Also causes SQL to be printed.
    """
    def setup_test_environment(self, *args, **kwargs):
        print("\nsetup_test_environment\n")
        from django.db.models.loading import get_models
        super(UnManagedModelTestRunner, self).setup_test_environment(*args,
                                                                   **kwargs)

        # flip all models to managed=True
        self.unmanaged_models = [m for m in get_models()
                                 if not m._meta.managed]
        for m in self.unmanaged_models:
            m._meta.managed = True

        # show SQL
        connections[DEFAULT_DB_ALIAS].use_debug_cursor = True


    def teardown_test_environment(self, *args, **kwargs):
        print("\nteardown_test_environment\n")
        super(UnManagedModelTestRunner, self).teardown_test_environment(*args,
                                                                      **kwargs)
        # reset unmanaged models
        for m in self.unmanaged_models:
            m._meta.managed = False