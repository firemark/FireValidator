import doctest
import firevalidator.validator


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(firevalidator.validator))
    return tests