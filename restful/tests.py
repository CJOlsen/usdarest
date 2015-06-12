from django.core.urlresolvers import reverse
from rest_framework.test import APITestCase, APIRequestFactory
from decimal import Decimal


class AssertStatusCodesMixin(object):
    """ Mixin to streamline checking status codes. """
    def assert_statuses(self, url, status_dict):
        """
        Runs 7 status code checks corresponding to the supplied dictionary.

        url: String, i.e. "/foods/01001"
        status_dict: a dictionary with 'get', 'post', 'put', 'patch', 'delete',
                     'head', and 'options' keys corresponding to their desired
                     status codes.
        """
        self.assertEqual(self.client.get(url).status_code, status_dict['get'])
        self.assertEqual(self.client.post(url).status_code, status_dict['post'])
        self.assertEqual(self.client.put(url).status_code, status_dict['put'])
        self.assertEqual(self.client.patch(url).status_code, status_dict['patch'])
        self.assertEqual(self.client.delete(url).status_code, status_dict['delete'])
        self.assertEqual(self.client.options(url).status_code, status_dict['options'])
        self.assertEqual(self.client.head(url).status_code, status_dict['head'])

    def assert_readonly_endpoint(self, url):
        """ Run asserts to ensure endpoint is read-only. """
        self.assert_statuses(url, {'get': 200, 'post': 405, 'put': 405,
                                   'patch': 405, 'delete': 405,
                                   'options': 200, 'head': 200})


class FoodTest(APITestCase, AssertStatusCodesMixin):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_food_list(self):
        url = reverse("food:food-list", kwargs={})

        # test response status codes
        self.assert_readonly_endpoint(url)

        # test response data
        response = self.client.get(url)
        # only looking at the keys
        # {}.keys() grabs the dict_keys type with the desired keys
        _keys = {"food_id": 0, "long_desc": 0, "short_desc": 0}.keys()
        self.assertEqual(response.data["results"][0].keys(), _keys)

    def test_food_detail(self):
        url = reverse("food:food-detail", kwargs={'food_id': '01001'})

        # test response status codes
        self.assert_readonly_endpoint(url)

        # test response data
        response = self.client.get(url)
        data = {"food_id": "01001",
                "food_group": "0100",
                "long_desc": "Butter, salted",
                "short_desc": "BUTTER,WITH SALT",
                "common_name": "",
                "manufacture_name": "",
                "survey": "Y",
                "refuse_desc": "",
                "refuse": "0",
                "scientific_name": "",
                "n_factor": "6.38",
                "pro_factor": "4.27",
                "fat_factor": "8.79",
                "cho_factor": "3.87"}
        self.assertEqual(response.data, data)


class WeightTest(APITestCase, AssertStatusCodesMixin):
    def test_weight_list(self):
        url = reverse("food:weight-list", kwargs={'food_id': '01001'})

        # test response status codes
        self.assert_readonly_endpoint(url)

        # test response data
        response = self.client.get(url)
        self.assertEqual(response.data[0]["food"], "01001")
        # TODO: more data tests here

    def test_weight_detail(self):
        url = reverse("food:weight-detail", kwargs={'food_id': '01001',
                                                    'seq_id': '1'})

        # test response status codes
        self.assert_readonly_endpoint(url)

        # test response data
        data = {"food": "01001",
                "seq": "1",
                "amount": "1.000",
                "measure_desc": "pat (1\" sq, 1/3\" high)",
                "grams": "5.0",
                "num_data_pts": None,
                "std_dev": None}
        response = self.client.get(url)
        self.assertEqual(response.data, data)


class NutrientTest(APITestCase, AssertStatusCodesMixin):
    # **in the food url namespace
    def test_food_nutrient_list(self):
        url = reverse("food:nutrient-list", kwargs={'food_id': '01001', 'seq_id': '01'})

        # test response status codes
        self.assert_readonly_endpoint(url)

        # test response data
        response = self.client.get(url)
        # grab the dict_keys type with the desired keys
        _keys = {"nutr_id": 0, "nutr_desc": 0}.keys()
        self.assertEqual(response.data["results"][0].keys(), _keys)

    def test_food_nutrient_detail(self):
        url = reverse("food:nutrient-detail", kwargs={'food_id': '01001',
                                                      'seq_id': '1',
                                                      'nutr_id': '203'})

        # test response status codes
        self.assert_readonly_endpoint(url)

        # test response data
        response = self.client.get(url)
        data = {"value": Decimal('0.0425'),
                "food_id": "01001",
                "nutr_id": "203",
                "seq_id": "1"}
        self.assertEqual(response.data, data)

    # **in the nutrient url namespace
    def test_nutrient_list(self):
        url = reverse("nutrient:nutrient-list", kwargs={})

        # test response status codes
        self.assert_readonly_endpoint(url)

        # test response data
        response = self.client.get(url)
        # grab the dict_keys type with the desired keys
        _keys = {"nutr_id": 0, "nutr_desc": 0}.keys()
        self.assertEqual(response.data["results"][0].keys(), _keys)

    def test_nutrient_detail(self):
        url = reverse("nutrient:nutrient-detail", kwargs={'nutr_id': '203'})

        # test response status codes
        self.assert_readonly_endpoint(url)

        # test response data
        response = self.client.get(url)
        data = {"nutr_id": "203",
                "units": "g",
                "tagname": "PROCNT",
                "nutr_desc": "Protein",
                "decimal_places": "2",
                "sr_order": "600"}
        self.assertEqual(response.data, data)
