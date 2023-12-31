from .models import Category


def categories(request):
    """
    Get a list of all categories.
    """
    context = {'categories': Category.objects.filter(parent=None)}
    return context