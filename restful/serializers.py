from django.forms import widgets
from rest_framework import serializers, status
from rest_framework.response import Response
from restful.models import FoodGroup, FoodDesc, Weight, NutrientDef, NutrientData


# /foods
class FoodDescBasicSerializer(serializers.Serializer):
    """
    Basic information for individual foods.
    """
    food_id = serializers.CharField(max_length=5, read_only=True)
    long_desc = serializers.CharField(max_length=200, read_only=True)
    short_desc = serializers.CharField(max_length=200, read_only=True)


# /foods/<food_id>
class FoodDetailSerializer(serializers.ModelSerializer):
    """
    Detailed information for individual foods.
    """
    class Meta:
        model = FoodDesc
        fields = ('food_id', 'food_group_id', 'long_desc', 'short_desc',
                  'common_name', 'manufacture_name', 'survey', 'refuse_desc',
                  'refuse', 'scientific_name', 'n_factor', 'pro_factor',
                  'fat_factor', 'cho_factor')


# /foods/<food_id>/seqs
class FoodSeqListSerializer(serializers.ModelSerializer):
    """
    List the available seq numbers (measures) for the Weights table.
    """
    class Meta:
        model = Weight
        fields = ('food', 'seq')


# /foods/<food_id>/seqs/<seq_id>
class FoodSeqSerializer(serializers.ModelSerializer):
    """
    Detail information on a food measure.  (Food and seq are a compound
    primary key)
    """
    class Meta:
        model = Weight
        fields = ('food', 'seq', 'amount', 'measure_desc', 'grams',
                  'num_data_pts', 'std_dev')


# /foods/<food_id>/seqs/<seq_id>/nutrients/<nutr_id>
class FoodSeqNutrientObj(object):
    """
    Custom object instead of a serializer to calculate data from multiple
    sources.
    """
    def __init__(self, food, seq, nutrient):
        self.food = food
        self.seq = seq
        self.nutrient = nutrient

    def calculate(self):
        """
        Calculate the nutrient value per seq (measure) of a food.
        """
        # N = (V*W)/100
        # where:
        # N = nutrient value per household measure,
        # V = nutrient value per 100 g (Nutr_Val in the Nutrient Data file)
        # W = g weight of portion (Gm_Wgt in the Weight file). *(Gm_Wgt -> grams)
        V = NutrientData.objects.all().filter(food_id=self.food).filter(nutr_id=self.nutrient)[0].nutr_value
        W = Weight.objects.all().filter(food=self.food).filter(seq=self.seq)[0].grams
        N = (V*W)/100
        result = {"food_id": self.food,
                  "seq_id": self.seq,
                  "nutr_id": self.nutrient,
                  "value": N}
        return result


# /nutrients
# /foods/<food_id>/seqs/<seq_id>/nutrients  ## TODO: filter on food_id
class NutrientBasicSerializer(serializers.ModelSerializer):
    """
    Detail Nutrient Definition information.
    """
    class Meta:
        model = NutrientDef
        fields = ('nutr_id', 'nutr_desc')


# /nutrients/<nutr_id>
class NutrientDetailSerializer(serializers.ModelSerializer):
    """
    Detail Nutrient Definition information.
    """
    class Meta:
        model = NutrientDef
        fields = ('nutr_id', 'units', 'tagname', 'nutr_desc',
                  'decimal_places', 'sr_order')


# /foodgroups
# /foodgroups/<foodgroup_id>
class FoodGroupSerializer(serializers.ModelSerializer):
    """
    List of foodgroups and their primary keys.
    """
    class Meta:
        model = FoodGroup
        fields = ('food_group_id', 'food_group_desc')

