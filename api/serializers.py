from rest_framework import serializers
from store.models import Product, Review


class ProductSerializer(serializers.ModelSerializer):
    average_rating_ro = serializers.ReadOnlyField(source='average_rating')
    total_reviews_ro = serializers.ReadOnlyField(source='total_reviews')
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'price', 'image', 'digital', 'stock', 'average_rating_ro',
                  'total_reviews_ro']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
