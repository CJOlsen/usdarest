from django.conf.urls import include, url
from restful import views

# urls separated into namespaces and aggregated in urlpatterns below.

food_urls = [
    # foods/
    url(r'^$', views.FoodList.as_view(), name='food-list'),
    url(r'^/(?P<food_id>\d+)$', views.FoodDetail.as_view(),
        name='food-detail'),
    url(r'^/(?P<food_id>\d+)/seqs$', views.FoodSeqList.as_view(),
        name='weight-list'),
    url(r'^/(?P<food_id>\d+)/seqs/(?P<seq_id>\d+)$',
        views.FoodSeqDetail.as_view(), name='weight-detail'),
    url(r'^/(?P<food_id>\d+)/seqs/(?P<seq_id>\d+)/nutrients$',
        views.NutrientList.as_view(), name='nutrient-list'),
    url(r'^/(?P<food_id>\d+)/seqs/(?P<seq_id>\d+)/nutrients/(?P<nutr_id>\d+)$',
        views.FoodSeqNutrientView.as_view(), name='nutrient-detail'),
]

nutrients_urls = [
    # nutrients/
    url(r'^$', views.NutrientList.as_view(), name='nutrient-list'),
    url(r'^/(?P<nutr_id>\d+)$', views.NutrientDetail.as_view(),
        name='nutrient-detail')
]

food_group_urls = [
    # foodgroups/
    url(r'^$', views.FoodGroupList.as_view(), name='foodgroup-list'),
    url(r'^/(?P<food_group_id>\d+)$', views.FoodGroupDetail.as_view(),
        name='foodgroup-detail'),
]

urlpatterns = [
    url(r'^foods', include(food_urls, namespace='food')),
    url(r'^nutrients', include(nutrients_urls, namespace='nutrient')),
    url(r'^foodgroups', include(food_group_urls, namespace='foodgroup')),
]
