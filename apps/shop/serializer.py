from rest_framework import serializers

from apps.shop.models import Shop, Tmall


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class TmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tmall
        fields = '__all__'
