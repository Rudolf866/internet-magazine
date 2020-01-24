"""
Definition of models.
"""

from datetime import datetimefrom django.contrib.auth.models import User #для импорта автора комментариев


from django.core.urlresolvers import reverse
import site
from decimal import Decimal
from transliterate import translit # переводит кириллицу
from django.utils.text import slugify #превращает поле в тип slug
from django.db.models.signals import pre_save



from django.db import models #В этом модуле объявлен базовый класс модели Model и классы полей, предназначенных для хранения данных различных типов.
from django.contrib import admin #добавили использование административного модуля
from django.conf import settings #это объект.Файл настроек Django содержит полную конфигурацию установленного проект
# Create your models here.




class Category(models.Model):
    name=models.CharField(max_length=120)
    slug=models.SlugField(blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse ('category_detail',kwargs={'category_slug':self.slug})

def pre_save_category_slug(sender,instance,*args,**kwargs):
    if not instance.slug:
        slug=slugify(translit(instance.name,reversed=True))# заполняет латиницей slug
        instance.slug=slug

pre_save.connect(pre_save_category_slug,sender=Category)



admin.site.register(Category)

class Brand(models.Model):
    name=models.CharField(max_length=120)
   

    def __str__(self):
        return self.name


admin.site.register(Brand)

#Чтобы корректно сохранять изображения
def image_folder(instance,filename):
    filename=instance.slug + '.'+ filename.split('.')[1]
    return "{0}/{1}".format(instance.slug,filename)


#Чтобы при снятие галочки в admin ->available изчезал продукт с каталога
class ProductManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(ProductManager,self).get_queryset().filter(available=True)



class Product(models.Model):
    category=models.ForeignKey(Category)
    brand=models.ForeignKey(Brand)
    title=models.CharField(max_length=120)
    slug=models.SlugField()
    description=models.TextField()
    image=models.ImageField(upload_to=image_folder)
    price=models.DecimalField(max_digits=9,decimal_places=2)
    available=models.BooleanField(default=True)
    objects=ProductManager()

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse ('product_detail',kwargs={'product_slug':self.slug})



admin.site.register(Product)

                          # Создаем корзину
#модель продукта
class CartItem(models.Model):
    product=models.ForeignKey(Product)#продукт
    qty=models.PositiveIntegerField(default=1)#кол-во yне может быть отрицательным поэтому PositiveIntegerField
    item_total=models.DecimalField(max_digits=9, decimal_places=2, default=0.0)#для изменения в корзине кол-во

    def __str__(self):
        return "Cart item for product {0}". format(self.product.title)
    
admin.site.register(CartItem)

#модель корзины

class Cart(models.Model):
    items=models.ManyToManyField(CartItem,blank=True)#Мы можем добавить много в корзину CartItem
    cart_total=models.DecimalField(max_digits=9, decimal_places=2, default=0.0)

    def __str__(self):
        return str(self.id)# возращает id корзины

    def add_to_cart(self,product_slug):
     cart=self
     product=Product.objects.get(slug=product_slug)
     new_item, _=CartItem.objects.get_or_create(product=product,item_total=product.price)
     if new_item not in cart.items.all():
      cart.items.add(new_item)
      cart.save()
   

    def remove_from_cart(self,product_slug):
          cart=self
          product=Product.objects.get(slug=product_slug)
          for cart_item in cart.items.all():
           if cart_item.product == product:
             cart.items.remove(cart_item)
             cart.save()


    def change_qty(self,qty,item_id):
        cart=self
        cart_item=CartItem.objects.get(id=int(item_id))
        cart_item.qty=int(qty)
        cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
        cart_item.save()
        new_cart_total=0.00
        for item in cart.items.all():
         new_cart_total+=float(item.item_total)
        cart.cart_total=new_cart_total
        cart.save()

ORDER_STATUS_CHOICES=(('Принят в обработку','Принят в обработку'),
                      ('Выполняется','Выполняется'),
                      ('Оплачен','Оплачен')
                      )
admin.site.register(Cart)

class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL)
    items=models.ManyToManyField(Cart)
    total=models.DecimalField(max_digits=9, decimal_places=2,default=0.00)
    first_name=models.CharField(max_length=200)
    last_name=models.CharField(max_length=200)
    phone=models.CharField(max_length=20)
    address=models.CharField(max_length=255)
    buying_type=models.CharField(max_length=40, choices=(('Самовывоз','Самовывоз'),('Доставка','Доставка')),default='Самовывоз')
    date=models.DateTimeField(auto_now_add=True)
    comments=models.TextField()
    status=models.CharField(max_length=100,choices=ORDER_STATUS_CHOICES,
                            default=ORDER_STATUS_CHOICES[0][0])

    def __str__(self):
        return "Заказ №{0}".format(str(self.id))

admin.site.register(Order)




class CaruselInfo(models.Model):
    title=models.CharField(max_length=255)
    content = models.TextField()
    image=models.ImageField(upload_to=image_folder)
    slug=models.SlugField()#Slug – газетный термин. “Slug” – это короткое название-метка, которое содержит только буквы, числа, подчеркивание или дефис. В основном используются в URL.
    available=models.BooleanField(default=True)
    objects=ProductManager()

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse ('caruselInfo_detail',kwargs={'caruselInfo_slug':self.slug})

admin.site.register(CaruselInfo)


# Модель данных Блога
class Blog(models.Model):
 title = models.CharField(max_length = 100, unique_for_date = "posted", verbose_name = "Заголовок")
 description = models.TextField (verbose_name = "Краткое содержание")
 content = models.TextField (verbose_name = "Полное содержание")
 posted = models.DateTimeField (default = datetime.now(), db_index = True,verbose_name = "Опубликована")
 image = models.FileField(default = '112.jpg', verbose_name = "Путь к картинке")
 def get_absolute_url(self): # метод возвращает строку с уникальным интернет-адресом записи (для просмотра записи на сайте)
  return reverse("blogpost", args=[str(self.id)])

 def __str__(self): # метод возвращает название, используемое для представления отдельных записей в административном разделе
  return self.title
class Meta: # метаданные — вложенный класс, который задает дополнительные параметры модели:
 db_table = "Posts" # имя таблицы для модели
 ordering = ["-posted"] # порядок сортировки данных в модели ("–"означает по убыванию)
 verbose_name = "статья блога" # имя, под которым модель будет отображаться в административном разделе (для одной статьи блога)
 verbose_name_plural = "статьи блога" # тоже для всех статей блога

admin.site.register(Blog)

# Модель комментариев
class Comment(models.Model):
 text = models.TextField(verbose_name = "Комментарий")
 date = models.DateTimeField(default = datetime.now(), db_index = True, verbose_name = "Дата")
 author = models.ForeignKey(User, on_delete = models.CASCADE, verbose_name = "Автор") # из модели User (вторичный ключ), каскадноеудаление записей в обоих таблицах
 post = models.ForeignKey(Blog, on_delete = models.CASCADE, verbose_name = "Статья") # из модели Blog (вторичный ключ), каскадное удаление записей в обоих таблицах

 def __str__(self):
  return 'Комментарий %s к %s' % (self.author, self.post)

 class Meta: # метаданные — вложенный класс, который задает дополнительные параметры модели:
  db_table = "Comments" # имя таблицы для модели
 verbose_name = "Комментарий"
 verbose_name_plural = "Комментарии к статьям блога"
 ordering = ["-date"]

admin.site.register(Comment)
