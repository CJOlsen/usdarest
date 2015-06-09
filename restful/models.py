from django.db import models
from django.contrib.auth.models import User
from django.db import connection
from collections import OrderedDict


class FoodGroup(models.Model):
    """ Food group model class, corresponds to the USDA's FD_GROUP table.

    25 records from the USDA FD_GROUP table.
    """
    food_group_id = models.CharField(primary_key=True, max_length=4)
    food_group_desc = models.CharField(max_length=60)

    def __str__(self):
        return self.food_group_desc.strip()  # are the names all 60 chars long in the db?

    class Meta:
        managed = False
        db_table = 'usda_food_group'


class FoodDesc(models.Model):
    """ Food description, includes name(s), whether food was in FNDDS survey,
    and protein/fat/carbohydrate calorie calculation factors.

    8,618 records from the USDA's FOOD_DES table.
    See sr27_doc.pdf page 29 for details.

    common_name: i.e. "soda" or "pop" for "carbonated beverage"
    survey: used in the USDA Food and Nutrient Database for Dietary Studies
            (FNDDS)?  If so it has a complete nutrient profile for the 65 FNDDS
            nutrients.  (Should be boolean?  Contains "Y" for true.)
    refuse_desc: i.e. seeds or bone
    refuse: percent of food that is refuse
    scientific_name: "Scientific name of the food item. Given for the least
                      processed form of the food (usually raw), if applicable."
    n_factor: Factor for converting nitrogen to protein.
    pro_factor: Factor for calculating calories from protein.
    fat_factor: Factor for calculating calories from fat.
    cho_factor: Factor for calculating calories from carbohydrate.
    """

    food_id = models.CharField(primary_key=True, max_length=5, db_column='food_id')
    #  food_group_id = models.CharField(max_length=4)
    food_group_id = models.ForeignKey(FoodGroup, db_column='food_group_id',
                                      related_name='food_desc')
    long_desc = models.CharField(max_length=200)
    short_desc = models.CharField(max_length=200)
    common_name = models.CharField(max_length=100, blank=True)
    manufacture_name = models.CharField(max_length=65, blank=True)
    survey = models.CharField(max_length=1, blank=True)
    refuse_desc = models.CharField(max_length=135, blank=True)
    refuse = models.DecimalField(max_digits=2, decimal_places=0,
                                 blank=True, null=True)
    scientific_name = models.CharField(max_length=65, blank=True)
    n_factor = models.DecimalField(max_digits=4, decimal_places=2,
                                   blank=True, null=True)
    pro_factor = models.DecimalField(max_digits=4, decimal_places=2,
                                     blank=True, null=True)
    fat_factor = models.DecimalField(max_digits=4, decimal_places=2,
                                     blank=True, null=True)
    cho_factor = models.DecimalField(max_digits=4, decimal_places=2,
                                     blank=True, null=True)

    def __str__(self):
        return self.short_desc

    class Meta:
        managed = False
        db_table = 'usda_food_desc'
        verbose_name = 'Food description'




class Weight(models.Model):
    """ Weight in grams of common measures for each food item.

    15,228 records from the USDA WEIGHT table.

    No new data.  Corresponds to the USDA's FD_GROUP table.
    See sr27_doc page 36 for more info.
    food: food_id from FoodDesc
    seq: Labels multiple measures for each food.
    amount: 1 as in "1 cup"
    measure_desc: cup as in "1 cup"
    grams: Number of grams per amount of measure.
    num_data_points: number of data points
    std_dev: standard deviation
    """

    food = models.ForeignKey(FoodDesc, related_name='weight')
    seq = models.CharField(max_length=2)
    amount = models.DecimalField(max_digits=5, decimal_places=3)
    measure_desc = models.CharField(max_length=84)
    grams = models.DecimalField(max_digits=7, decimal_places=1)
    num_data_pts = models.DecimalField(max_digits=4, decimal_places=0,
                                       blank=True, null=True)
    std_dev = models.DecimalField(max_digits=7, decimal_places=3,
                                  blank=True, null=True)

    def __str__(self):
        return str(float(self.amount)) + " " + str(self.measure_desc)

    class Meta:
        managed = False
        db_table = 'usda_weight'
        unique_together = ('food', 'seq')


class NutrientData(models.Model):
    """
    Nutritional information for a food, per 100 grams.

    654,572 records from the USDA NUT_DATA table.
    See sr27_doc page 31 for more info.

    (names have been slightly modified)
    food_id (NDB_No): 5-digit Nutrient Databank number.
    nutr_id (Nutr_No): Unique 3-digit identifier code for a nutrient.
    Nutr_Val: Amount in 100 grams, edible portion †.
    Num_Data_Pts: Number of data points (previously called Sample_Ct)
                  is the number of analyses used to calculate the
                  nutrient value. If the number of data points is 0, the
                  value was calculated or imputed.
    Std_Error: Standard error of the mean. Null if cannot be
               calculated. The standard error is also not given if the
               number of data points is less than three.
    Src_Cd: Code indicating type of data.
    Deriv_Cd: Data Derivation Code giving specific information on
              how the value is determined. This field is populated
              only for items added or updated starting with SR14.
    Ref_NDB_No: NDB number of the item used to calculate a missing
                value. Populated only for items added or updated
                starting with SR14.
    Add_Nutr_Mark: Indicates a vitamin or mineral added for fortification
                   or enrichment. This field is populated for ready-to-
                   eat breakfast cereals and many brand-name hot
                   cereals in food group 8.
    Num_Studies: Number of studies.
    Min: Minimum value.
    Max: Maximum value.
    DF: Degrees of freedom.
    Low_EB: Lower 95% error bound.
    Up_EB: Upper 95% error bound.
    Stat_cmt: Statistical comments. See definitions below.
    AddMod_Date: Indicates when a value was either added to the
                 database or last modified.
    CC: Confidence Code indicating data quality, based on
        evaluation of sample plan, sample handling,
        analytical method, analytical quality control, and
        number of samples analyzed. Not included in this
        release, but is planned for future releases.
    """

    food_id = models.ForeignKey('FoodDesc', db_column='food_id',
                                related_name='nutrient_data',
                                verbose_name='Food Name')
    nutr_id = models.ForeignKey('NutrientDef', db_column='nutr_id',
                                verbose_name='nutrient_data')
    nutr_value = models.DecimalField(max_digits=10, decimal_places=3,
                                     verbose_name='Value')
    num_data_pts = models.DecimalField(max_digits=5, decimal_places=0)
    std_error = models.DecimalField(max_digits=8, decimal_places=3,
                                    blank=True, null=True)
    source_code = models.CharField(max_length=2)
    derivation_code = models.CharField(max_length=4, blank=True)
    ref_food_id = models.CharField(max_length=5, blank=True)
    fortified = models.CharField(max_length=1, blank=True)
    number_studies = models.DecimalField(max_digits=2, decimal_places=0,
                                         blank=True, null=True)
    min_value = models.DecimalField(max_digits=10, decimal_places=3,
                                    blank=True, null=True)
    max_value = models.DecimalField(max_digits=10, decimal_places=3,
                                    blank=True, null=True)
    degrees_freedom = models.DecimalField(max_digits=4, decimal_places=0,
                                          blank=True, null=True)
    low_error_bound = models.DecimalField(max_digits=10, decimal_places=3,
                                          blank=True, null=True)
    upper_error_bound = models.DecimalField(max_digits=10, decimal_places=3,
                                            blank=True, null=True)
    statistical_cmt = models.CharField(max_length=10, blank=True)
    addmod_date = models.CharField(max_length=10, blank=True)
    confidence_code = models.CharField(max_length=1, blank=True)

    class Meta:
        managed = False
        db_table = 'usda_nutrient_data'


class NutrientDef(models.Model):
    """
    Definitions of nutrients used in the database.

    150 records from the USDA NUTR_DEF table.
    See sr27doc page 34 for more info.

    Nutr_No: Unique 3-digit identifier code for a nutrient.
    Units: Units of measure (mg, g, μg, and so on).
    Tagname: International Network of Food Data Systems
             (INFOODS) Tagnames.† A unique abbreviation for a
             nutrient/food component developed by INFOODS to
             aid in the interchange of data.
    NutrDesc: Name of nutrient/food component.
    Num_Dec: Number of decimal places to which a nutrient value is
             rounded.
    SR_Order: Used to sort nutrient records in the same order as
              various reports produced from SR
    """
    nutr_id = models.CharField(primary_key=True, max_length=3, db_column='nutr_id')
    units = models.CharField(max_length=7)
    tagname = models.CharField(max_length=20, blank=True)
    nutr_desc = models.CharField(max_length=60)
    decimal_places = models.CharField(max_length=1)
    sr_order = models.DecimalField(max_digits=6, decimal_places=0)

    def __str__(self):
        return self.nutr_desc

    class Meta:
        managed = False
        db_table = 'usda_nutrient_def'
        verbose_name = 'Nutrient definition'
