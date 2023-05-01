from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from store.models import Product, Review
from django.contrib.auth.decorators import login_required
from store.forms.review_form import ReviewForm
from django.core.cache import cache


class ProductView(View):
    @staticmethod
    def get(request, product_id):
        key = f'product_{product_id}'
        product = cache.get(key)
        if not product:
            all_products = cache.get('all_products') or Product.objects.all()
            product = get_object_or_404(all_products, pk=product_id)
            cache.set(key, product)

        context = {'product': product}
        return render(request, 'store/product.html', context)


@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid() and request.POST.get('rating'):
            review = Review(
                comment=form.cleaned_data['comment'],
                product=product,
                user=request.user.customer,
                rating=request.POST.get('rating')
            )
            review.save()
            return redirect('store:product', product_id=product_id)
    else:
        form = ReviewForm()
    return render(request, 'store/add_review.html', {'product': product, 'form': form})
