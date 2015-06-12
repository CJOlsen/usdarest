from rest_framework import serializers, status
from restful.models import FoodGroup, FoodDesc, Weight, NutrientDef, NutrientData

# serializers.  Organized by url tree location.

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
        fields = ('food_id', 'food_group', 'long_desc', 'short_desc',
                  'common_name', 'manufacture_name', 'survey', 'refuse_desc',
                  'refuse', 'scientific_name', 'n_factor', 'pro_factor',
                  'fat_factor', 'cho_factor')


# /foods/<food_id>/seqs
class FoodSeqListSerializer(serializers.ModelSerializer):
    """
    List the available seq numbers (measures) from the Weights table.
    """
    class Meta:
        model = Weight
        fields = ('food', 'seq')


# /foods/<food_id>/seqs/<seq_id>
class FoodSeqSerializer(serializers.ModelSerializer):
    """
    Detail information on a food measure.  (food_id and seq_id form a compound
    primary key on the Weights table, implemented as unique_only)
    """
    class Meta:
        model = Weight
        fields = ('food', 'seq', 'amount', 'measure_desc', 'grams',
                  'num_data_pts', 'std_dev')


# /foods/<food_id>/seqs/<seq_id>/nutrients/<nutr_id>
class FoodSeqNutrientObj(object):
    """
    Custom object instead of a serializer to calculate data from multiple
    sources.  This does not correspond to a single model or database table.
    """
    def __init__(self, food_id, seq_id, nutr_id):
        self.food_id = food_id
        self.seq_id = seq_id
        self.nutr_id = nutr_id

    def calculate(self):
        """
        Calculate the nutrient value per seq (measure) of a food.
        """
        # N = (V*W)/100
        # where:
        # N = nutrient value per household measure,
        # V = nutrient value per 100 g (Nutr_Val in the Nutrient Data file)
        # W = g weight of portion (Gm_Wgt in the Weight file). *(Gm_Wgt -> grams)
        V = NutrientData.objects.all().filter(food_id=self.food_id).filter(nutrient=self.nutr_id)[0].nutr_value
        W = Weight.objects.all().filter(food=self.food_id).filter(seq=self.seq_id)[0].grams
        N = (V*W)/100
        result = {"food_id": self.food_id,
                  "seq_id": self.seq_id,
                  "nutr_id": self.nutr_id,
                  "value": N}
        return result


# /nutrients
# /foods/<food_id>/seqs/<seq_id>/nutrients  ## TODO: filter on food_id
class NutrientBasicSerializer(serializers.ModelSerializer):
    """
    List of Nutrient Definitions.
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

