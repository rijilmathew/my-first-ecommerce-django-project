from admins.models import ProductCategory

def categories(request):
    categories = ProductCategory.objects.all()
    return {'categories': categories}
