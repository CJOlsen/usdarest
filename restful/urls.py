from django.conf.urls import include, url
from restful import views


food_urls = [
    # foods/
    url(r'^$', views.FoodList.as_view()),
    url(r'^/(?P<food_id>\d+)/$', views.FoodDetail.as_view()),
    url(r'^/(?P<food_id>\d+)/seqs$', views.FoodSeqList.as_view()),
    url(r'^/(?P<food_id>\d+)/seqs/(?P<seq_id>\d+)$',
        views.FoodSeqDetail.as_view()),
    url(r'^/(?P<food_id>\d+)/seqs/(?P<seq_id>\d+)/nutrients$',
        views.NutrientList.as_view()),
    url(r'^/(?P<food_id>\d+)/seqs/(?P<seq_id>\d+)/nutrients/(?P<nutr_id>\d+)$',
        views.FoodSeqNutrientView.as_view()),
]

nutrients_urls = [
    # nutrients/
    url(r'^$', views.NutrientList.as_view()),
    url(r'^/(?P<nutr_id>\d+)/$', views.NutrientDetail.as_view())
]

food_group_urls = [
    # foodgroups/
    url(r'^$', views.FoodGroupList.as_view()),
    url(r'^/(?P<food_group_id>\d+)/$', views.FoodGroupDetail.as_view()),
]

urlpatterns = [
    url(r'^foods', include(food_urls)),
    url(r'^nutrients', include(nutrients_urls)),
    url(r'^foodgroups', include(food_group_urls)),
]


