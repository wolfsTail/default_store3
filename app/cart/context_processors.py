from .cart import Cart


def cart(request):
    """
    Returns a new Cart object created using the request.
    """
    return {'cart': Cart(request)}