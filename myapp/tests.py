from django.test import TestCase
import myapp.query_SIS_API as sis_api
from django.contrib.auth.models import User


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


#
# class ViewsTester(TestCase):
#
#     # from: https://stackoverflow.com/questions/57425954/usage-of-self-client-get-vs-self-browser-get
#     def test_home_page_uses_correct_template(self):
#         response = self.client.get('/')
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, "myapp/index.html")
#
#     def test_profile_uses_correct_template(self):
#         response = self.client.get('/profile/')
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, "myapp/profile.html")
#
#     def test_submit_listing_uses_correct_template(self):
#         response = self.client.get('/submit_listing/')
#         self.assertEquals(response.status_code, 200)
#         self.assertTemplateUsed(response, "myapp/submit_listing.html")
#
# class UserAuthenticationTestCase(TestCase):
#     def setUp(self):
#         # Create a test user
#         self.user = User.objects.create_user(
#             username='testuser',
#             email='testuser@example.com',
#             password='testpassword'
#         )
#
#     def test_user_can_register(self):
#         # Send a POST request to the registration page with valid data
#         response = self.client.post('/accounts/signup/', {
#             'username': 'newuser',
#             'email': 'newuser@example.com',
#             'password1': 'newpassword1111',
#             'password2': 'newpassword1111',
#         })
#         # Verify that the user is redirected to the home page after successful registration
#         self.assertRedirects(response, '/')
#
#     # def test_user_can_log_in(self):
#     #     # Send a POST request to the login page with valid credentials
#     #     response = self.client.post('/accounts/login/', {
#     #         'username': 'newuser',
#     #         'password': 'newpassword1111',
#     #     })
#     #     # Verify that the user is logged in and redirected to the home page
#     #     self.assertRedirects(response, '/')
#     #     # Verify that the user is now authenticated
#     #     # self.assertTrue(response.wsgi_request.user.is_authenticated)
#
#     # def test_user_can_log_out(self):
#     #     # Log in the test user first
#     #     self.client.login(username='testuser', password='testpassword')
#     #     # Send a POST request to the logout page
#     #     response = self.client.post('/logout/')
#     #     # Verify that the user is logged out and redirected to the login page
#     #     self.assertRedirects(response, '/login/')
#     #     # Verify that the user is now not authenticated
#     #     self.assertFalse(response.wsgi_request.user.is_authenticated)
