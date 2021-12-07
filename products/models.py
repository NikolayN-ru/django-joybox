from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.urls import reverse

User = get_user_model()


def get_product_url(obj, viewname):
    ct_model = obj.__class__._meta.model_name
    return reverse(viewname, kwargs={'ct_model': ct_model, 'slug': obj.slug})


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        abstract = True

    brand = models.ForeignKey('Brand', verbose_name='бренд', on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, verbose_name='категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='изображение')
    description = models.TextField(verbose_name='описание', null=True)
    price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='цена')

    def __str__(self):
        return self.title


# промежуточный продукт относящийся только к корзине
class CartProduct(models.Model):
    user = models.ForeignKey(
        'Customer', verbose_name='покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey(
        'Cart', verbose_name='корзина', on_delete=models.CASCADE, related_name='related_products')
    # product = models.ForeignKey(
    #     'Product', verbose_name='товар', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='Общая_цена')

    def __str__(self):
        return 'продукт: {} (для корзины)'.format(self.content_object.title)


class Cart(models.Model):
    owner = models.ForeignKey(
        'Customer', verbose_name='владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(
        CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(
        max_digits=9, decimal_places=2, verbose_name='общая_цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return self.pk


class Customer(models.Model):
    user = models.ForeignKey(
        User, verbose_name='пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='номер телефона')
    address = models.CharField(max_length=225, verbose_name='адрес')

    def __str__(self):
        return 'покупатель: {} {}'.format(self.user.first_name, self.user.last_name)


class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name='имя бренда')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Notebook(Product):
    diagonal = models.CharField(max_length=255, verbose_name='диагональ')
    display_type = models.CharField(max_length=255, verbose_name='тип дисплея')
    processor = models.CharField(max_length=255, verbose_name='частота процессора')
    ram = models.CharField(max_length=255, verbose_name='оперативная память')
    video = models.CharField(max_length=255, verbose_name='видеокарта')
    time_without_charge = models.CharField(max_length=255, verbose_name='время работы аккумулятора')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Smartphone(Product):
    diagonal = models.CharField(max_length=255, verbose_name='диагональ')
    display_type = models.CharField(max_length=255, verbose_name='тип дисплея')
    resolution = models.CharField(max_length=255, verbose_name='Объем батареи')
    accum_volume = models.CharField(max_length=255, verbose_name='Объем батареи')
    rem = models.CharField(max_length=255, verbose_name='Оперативная память')
    sd = models.BooleanField(default=True)
    sd_volume_max = models.CharField(max_length=255, verbose_name='Максимальный объем встраиваемой памяти')
    main_cam_mp = models.CharField(max_length=255, verbose_name='Главная камера')
    frontal_cam_mp = models.CharField(max_length=255, verbose_name='Фронтальная камера')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')
