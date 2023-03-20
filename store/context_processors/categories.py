from store.models.category import Category


def categories(request):
    return {'categories': Category.objects.all()}
