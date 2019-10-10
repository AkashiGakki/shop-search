from django.urls import path, include
from rest_framework import routers

from apps.shop import views
from apps.shop.views import ShopListView, TmallViewSet
from apps.shop.views import ShopViewSet


app_name = 'shop'

router = routers.DefaultRouter()
router.register('view', ShopViewSet)
router.register('tmall', TmallViewSet)

urlpatterns = [
    path('', views.index, name='index'),
    path('list', ShopListView.as_view(), name='list'),
    # path('view', ShopViewSet.as_view(), name='view'),
    path('', include(router.urls)),
]
