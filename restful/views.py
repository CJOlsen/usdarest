from restful.models import FoodGroup, FoodDesc, Weight, NutrientDef
from restful.serializers import FoodGroupSerializer, FoodDescBasicSerializer, \
    FoodDetailSerializer, FoodSeqListSerializer, FoodSeqSerializer, \
    NutrientBasicSerializer, NutrientDetailSerializer, FoodSeqNutrientObj
from restful.mixins import MultipleFieldLookupMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics


# these views comprise a read-only REST api of the foods, nutrients and food
# groups of the USDA Food Database
#
#
# generics.ListAPIView
#   read-only
#   serializer_class: data handler defined in serializers.py
#   queryset: queryset to be returned
#   lookup_field: used to filter the queryset
# generics.RetrieveAPIView
#   read-only
#   serializer_class: data handler defined in serializers.py
#   queryset: queryset that defines the possible objects to be returned
#   lookup_field: used to select an object from the queryset


# /foods
class FoodList(generics.ListAPIView):
    """
    A paginated list of all foods in the database, basic information only.
    """
    serializer_class = FoodDescBasicSerializer
    queryset = FoodDesc.objects.all()
    paginate_by = 30


# /foods/<food_id>
class FoodDetail(generics.RetrieveAPIView):
    """
    Details of a single food object.
    """
    serializer_class = FoodDetailSerializer
    lookup_field = 'food_id'
    queryset = FoodDesc.objects.all()


# /foods/<food_id>/seqs
class FoodSeqList(generics.ListAPIView):
    """
    A list of available food measures, by sequence number.
    """
    serializer_class = FoodSeqListSerializer
    lookup_field = 'food_id'
    def get_queryset(self):
        queryset = Weight.objects.all().filter(food=self.kwargs.get('food_id'))
        return queryset


# /foods/<food_id>/seqs/<seq_id>
class FoodSeqDetail(generics.RetrieveAPIView, MultipleFieldLookupMixin):
    """
    Detail information of a specific measure of a food.
    """
    # see mixins.py for details on multiple lookup fields
    serializer_class = FoodSeqSerializer
    lookup_fields = ('food_id', 'seq_id')

    def get_object(self):
        queryset = Weight.objects.all().filter(food=self.kwargs.get('food_id')).filter(seq=self.kwargs.get('seq_id'))
        # food and seq are "together_unique" in the database so this queryset
        # will have at most one member.  If this could be an objects.get() call
        # it would avoid any errors resulting from calling an index on an empty
        # queryset.
        try:
            obj = queryset[0]
        except IndexError:
            return
        return obj


# /foods/<food_id>/seqs/<seq_id>/nutrients/<nutr_id>
class FoodSeqNutrientView(APIView):
    """
    Nutrient value for a given food, and seq_id (measurement)
    """
    def get(self, request, *args, **kwargs):
        food = kwargs.get('food_id')
        seq = kwargs.get('seq_id')
        nutrient = kwargs.get('nutr_id')

        # see serializers.py for definition of FoodSeqNutrientObj
        obj = FoodSeqNutrientObj(food, seq, nutrient)
        result = obj.calculate()
        response = Response(result, status=status.HTTP_200_OK)
        return response


# /foods/<food_id>/seqs/<seq_id>/nutrients
# /nutrients
class NutrientList(generics.ListAPIView):
    """
    List of all nutrients.
    """
    serializer_class = NutrientBasicSerializer
    queryset = NutrientDef.objects.all()
    paginate_by = 30


# /nutrients/<nutr_id>
class NutrientDetail(generics.RetrieveAPIView):
    """
    Details of a specific nutrient.
    """
    serializer_class = NutrientDetailSerializer
    lookup_field = 'nutr_id'
    queryset = NutrientDef.objects.all()


# /foodgroups
class FoodGroupList(generics.ListAPIView):
    """
    List of available food groups.
    """
    model = FoodGroup
    serializer_class = FoodGroupSerializer
    queryset = FoodGroup.objects.all()


# /foodgroups/<foodgroup_id>
class FoodGroupDetail(generics.RetrieveAPIView):
    """
    Details of a specific food group.
    """
    model = FoodDesc
    serializer_class = FoodGroupSerializer
    lookup_field = 'food_group_id'
    queryset = FoodGroup.objects.all()
    def get_queryset(self):
        queryset = super(FoodGroupDetail, self).get_queryset()
        return queryset.filter(food_group=self.kwargs.get('food_group_id'))

