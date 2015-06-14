from django.test import TestCase
from restful.serializers import FoodSeqNutrientObj
from decimal import Decimal

class CalculateNutrientValueTestCase(TestCase):
    """
    This tests the serializer that calculates nutrient values.
    """
    def test_serializer_nutrient_value(self):
        obj = FoodSeqNutrientObj(food_id='01001', seq_id='1', nutr_id='203')
        result = obj.calculate()
        self.assertEqual(result, {'nutr_id': '203',
                                  'value': Decimal('0.0425'),
                                  'food_id': '01001',
                                  'seq_id': '1'})
