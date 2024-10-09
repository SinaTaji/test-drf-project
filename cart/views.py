from rest_framework import status, views
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .Cart import Cart
from product.models import Product


class AddToCartAPIView(views.APIView):
    """
    کاربر محصول را انتخاب میکند و باید تعداد را ارسال کنه اگر سبد خرید داشت به تعداد محصول اضافه میشه اگر نداشت سبد جدید ساخته میشه
    """

    def post(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        quantity = request.data.get('quantity')

        cart.add(product, quantity)
        return Response({'message': 'محصول با موفقیت به سبد خرید شما اضافه شد'}, status=status.HTTP_200_OK)


class RemoveFromCartAPIView(views.APIView):
    """
    کاربر میتونه محصولی که نیاز نداره از سبد خرید حذف کنه ما آی دی محصول را نیاز داریم
    """

    def delete(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)

        cart.remove(product)
        return Response({'message': 'محصول با موفقیت از سبد خرید شما حذف شد'}, status=status.HTTP_200_OK)


class CartDetailAPIView(views.APIView):
    """
    کاربر میتونه جزئیات سبد خرید خودشو مشاهده کنه
    """

    def get(self, request):
        cart = Cart(request)
        cart_items = list(cart)
        total_price = cart.get_total_price()

        return Response({'cart': cart_items, 'total_price': total_price}, status=status.HTTP_200_OK)
