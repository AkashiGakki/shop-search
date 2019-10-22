from rest_framework import serializers

from apps.shop.models import Shop, Tmall, You, Jd


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = "__all__"


class TmallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tmall
        fields = '__all__'


class YouSerializer(serializers.ModelSerializer):
    class Meta:
        model = You
        fields = '__all__'


class VipSerializer(serializers.ModelSerializer):
    class Meta:
        model = You
        fields = '__all__'


class JdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jd
        fields = '__all__'
