from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='product')

urlpatterns = [
    path("products/categories/", views.CategoryListView.as_view(), name="category_list"),
]+ router.urls
