# from django.test import TestCase
# from django.core.urlresolvers import reverse
# from restful.views import FoodList, FoodDetail
# from rest_framework.test import APIRequestFactory
#
#
# class FoodTest(TestCase):
#     def setUp(self):
#         self.factory = APIRequestFactory()
#
#     def test_view_food_list(self):
#         url = reverse("food:food-list", kwargs={})
#         request = self.factory.get(url)
#         view = FoodList.as_view()
#         response = view(request)
#         response.render();
#         print("\n", response.content)
#         self.assertEqual(response.content, None)
#
#     def test_view_food_detail(self):
#         url = reverse("food:food-detail", kwargs={'food_id': '01001'})
#         print("url: ", url)
#         request = self.factory.get(url)
#         view = FoodDetail.as_view()
#         response = view(request, food_id='01001')
#         response.render()
#         print("\n", response.content)
#         self.assertEqual(response.content, None)