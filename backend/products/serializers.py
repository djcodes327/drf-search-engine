from rest_framework import serializers
from rest_framework.reverse import reverse
from . import validators
from api.serializers import UserPublicSerializer
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    owner = UserPublicSerializer(source='user', read_only=True)
    title = serializers.CharField(validators=[validators.unique_product_title,
                                              validators.unique_product_title])
    body = serializers.CharField(source='content')

    class Meta:
        model = Product
        fields = [
            'id',
            'owner',
            'title',
            'body',
            'price',
            'public',
            'path',
            'endpoint'
        ]

    def get_update_url(self, obj):
        # Check if it has request in it or not.
        request = self.context.get('request')
        if not request:
            return None
        return reverse("product-update", kwargs={"pk": obj.pk}, request=request)
