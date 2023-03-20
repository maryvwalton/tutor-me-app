from django.test import TestCase
import myapp.query_SIS_API as sis_api


# Create your tests here.

# SHERRIFF: Dummy test added.
class DummyTestCase(TestCase):
    def setUp(self):
        x = 1
        y = 2

    def test_dummy_test_case(self):
        self.assertEqual(2, 2)


class Query_SIS_API_Tests(TestCase):
    # def setUp(self):

    def test_check_if_year_valid_INVALID(self):
        with self.assertRaises(ValueError):
            sis_api.check_if_year_valid(4932882)

    def test_check_if_year_valid_VALID(self):
        self.assertEqual(None, sis_api.check_if_year_valid(23))

    def test_check_if_semester_valid_INVALID(self):
        with self.assertRaises(ValueError):
            sis_api.check_if_semester_valid("something else")

    def test_check_if_semester_valid_VALID(self):
        with self.assertRaises(ValueError):
            sis_api.check_if_semester_valid("fAll")
