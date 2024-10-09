from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from .models import Product, ProductCategory
from .serializers import ProductCategorySerializer, ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend


class ProductPagination(PageNumberPagination):
    page_size = 20


class ProductViewSet(viewsets.ModelViewSet):
    """
    در این اند پوینت کاربران میتوانند لیست محصولات را ببینند و
     انواع فیلتر ها در دسترس است و اگر آی دی محصول به یو آر ال اضافه شود به جزئیات اون محصول میره
    """
    permission_classes = [AllowAny]
    http_method_names = ['get']
    pagination_class = ProductPagination
    queryset = Product.objects.prefetch_related('product_per_category').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product_per_category']
    search_fields = ['title']
    ordering_fields = ['price', 'id']


class CategoryListView(ListAPIView):
    """
      دسترسی به تمام دسته بندی های والد و فرزند
    """
    permission_classes = [AllowAny]
    queryset = ProductCategory.objects.prefetch_related('sub_categories').all()
    serializer_class = ProductCategorySerializer
    pagination_class = None
