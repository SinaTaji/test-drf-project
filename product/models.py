from django.db import models


class ProductCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='عنوان در Url', allow_unicode=True)
    is_sub = models.BooleanField(default=False, verbose_name='آیا یک زیر دسته است ؟')
    sub_categories = models.ForeignKey('self', verbose_name='دسته بندی والد', related_name='sub_category',
                                       on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='medias/products/categories', verbose_name='تصویر دسته بندی',
                              blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['title']
        db_table = 'product_category'


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='عنوان در Url', allow_unicode=True)
    price = models.IntegerField(verbose_name='قیمت محصول')
    is_active = models.BooleanField(default=True, verbose_name='آیا موجود است ؟')
    product_per_category = models.ManyToManyField(ProductCategory, verbose_name='دسته بندی های محصول',
                                                  related_name='c_products')
    description = models.TextField('توضیحات محصول')
    image = models.ImageField(upload_to='medias/products', verbose_name='تصویر محصول',
                              blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['title']
        db_table = 'products'
