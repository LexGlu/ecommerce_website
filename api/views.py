from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from store.models import Product, Review
from api.serializers import ProductSerializer, ReviewSerializer
from rest_framework.serializers import ValidationError


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        return Product.objects.filter(pk=self.kwargs['pk'])


class ReviewCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer = self.request.user.customer
        product_id = self.kwargs['product_id']
        return Review.objects.filter(user=customer, product_id=product_id)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already reviewed this product.')

        serializer.save(user=self.request.user.customer, product_id=self.kwargs['product_id'])

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You have not reviewed this product yet.')
