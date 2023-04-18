from rest_framework import generics, permissions, mixins, status
from rest_framework.response import Response
from store.models import Product, Review, Customer
from api.serializers import ProductSerializer, ReviewSerializer
from rest_framework.serializers import ValidationError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token


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


@csrf_exempt
def sign_up(request):
    if request.method == 'POST':
        try:
            data = JSONParser().parse(request)
            user = User.objects.create_user(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password'],
            )
            user.save()
            customer = Customer.objects.create(user=user)
            customer.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'That username has already been taken'}, status=400)


@csrf_exempt
def log_in(request):
    if request.method == 'POST':
            data = JSONParser().parse(request)
            user = authenticate(request, username=data['username'], password=data['password'])
            if not user:
                return JsonResponse({'error': 'Invalid username or password'}, status=400)
            else:
                try:
                    token = Token.objects.get(user=user)
                except Token.DoesNotExist:
                    token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=200)
