import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.views.generic.base import View
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import viewsets, mixins, filters
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination

from apps.shop.models import Shop, Tmall
from apps.shop.serializer import ShopSerializer, TmallSerializer


class ShopPagination(PageNumberPagination):
    page_size = 10
    page_size_query_description = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class TmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_description = 'page_size'
    page_query_param = 'p'
    max_page_size = 100


class ShopViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    pagination_class = ShopPagination


class TmallViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Tmall.objects.all()
    serializer_class = TmallSerializer
    pagination_class = TmallPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['keyword', 'describe', 'shop']
    ordering_fields = ['goods_price']


class ShopListView(View):
    def get(self, request):
        queryset = Shop.objects.all()
        data = serializers.serialize('json', queryset)
        return JsonResponse(json.loads(data), safe=False)


def index(request):
    return HttpResponse('Hello, akashi!')
