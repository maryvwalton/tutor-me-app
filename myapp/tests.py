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

        with self.assertRaises(ValueError):
            sis_api.check_if_year_valid("a string")

        with self.assertRaises(ValueError):
            sis_api.check_if_year_valid("123")

    def test_check_if_year_valid_VALID(self):
        self.assertEqual(None, sis_api.check_if_year_valid(23))

    def test_check_if_semester_valid_INVALID(self):
        with self.assertRaises(ValueError):
            sis_api.check_if_semester_valid("something else")

    def test_check_if_semester_valid_VALID(self):
        with self.assertRaises(ValueError):
            sis_api.check_if_semester_valid("fAll")

    def test_return_get_semester_to_URL_number_VALID(self):
        self.assertEqual("8", sis_api.get_semester_to_URL_number("fall"), "Testing whether entering fall yields 8")
        self.assertEqual("2", sis_api.get_semester_to_URL_number("spring"), "Testing whether entering spring yields 2")
