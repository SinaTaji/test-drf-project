from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.AddToCartAPIView.as_view(), name='add-to-cart'),
    path('remove/<int:product_id>/', views.RemoveFromCartAPIView.as_view(), name='remove-from-cart'),
    path('detail/', views.CartDetailAPIView.as_view(), name='cart-detail'),
]
