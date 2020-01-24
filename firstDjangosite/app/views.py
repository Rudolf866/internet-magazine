"""
Definition of views.
"""

from.forms import BlogForm
from.models import Comment # использование модели комментариев
from.forms import CommentForm # использование формы ввода комментария
from .models import Blog
from app.models import CaruselInfo
#from django.urls import reverse
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from app.models import Category,Product,CartItem
from app.models import Cart
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from decimal import Decimal
from app.forms import OrderForm
from app.models import Order



from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime

def home(request):
    """Главная страница."""
    assert isinstance(request, HttpRequest)
    carusels=CaruselInfo.objects.all()
    return render(
        request,
        'app/index.html',
        {
            'carusels':carusels,
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Контакты."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Контакты  интернет магазина «CONNECT electronics».',
            'Developer':'Контакты разработчика сайта',
            'year':datetime.now().year,
        }
    )

def about(request):
    """О компании"""
    assert isinstance(request, HttpRequest)
    categories=Category.objects.all()
    products=Product.objects.all()
    return render(
        request,
        'app/about.html',
        {
            
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )


def gallery(request):
    """Главная страница."""
    assert isinstance(request, HttpRequest) 
    return render(
        request,
        'app/gallery.html',
        {
           'title':'gallery',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )



def registration(request):
 """Регистрация."""
 regform = UserCreationForm (request.POST)
 if request.method == "POST": # после отправки формы
     regform = UserCreationForm (request.POST)
 if regform.is_valid(): #валидация полей формы
     reg_f = regform.save(commit=False) # не сохраняем данные формы
     reg_f.is_staff = False # запрещен вход в административный раздел
     reg_f.is_active = True # активный пользователь
     reg_f.is_superuser = False # не является суперпользователем
     reg_f.date_joined = datetime.now() # дата регистрации
     reg_f.last_login = datetime.now() # дата последней авторизации

     reg_f.save() # сохраняем изменения после добавления данных (добавление пользователя в БД пользователей)

     return redirect('home')      # переадресация на главную страницу после регистрации
 else:
     regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
 assert isinstance(request, HttpRequest) 
 return render(request,'app/registration.html',{
'regform': regform, # передача формы в шаблон веб-страницы
 'year':datetime.now().year,
 }
 )


def base_view(request):
      try:
        cart_id=request.session['cart_id']# Получение значения сессии при помощи ключа(то есть, 'cart_id'). 
        cart=Cart.objects.get(id=cart_id)
        request.session['total']=cart.items.count()
      except:
        cart=Cart()
        cart.save()
        cart_id=cart.id
        request.session['cart_id']=cart_id# Передача значения в сессию
        cart=Cart.objects.get(id=cart_id)

      categories=Category.objects.all()
      products=Product.objects.all()
      context={
        'categories':categories,
        'products':products,
        
        }
      return render(request,'app/base.html',context)



def product_view(request,product_slug):
    try:
     cart_id=request.session['cart_id']
     cart=Cart.objects.get(id=cart_id)
     request.session['total']=cart.items.count()
    except:
     cart=Cart()
     cart.save()
     cart_id=cart.id
     request.session['cart_id']=cart_id
     cart=Cart.objects.get(id=cart_id)

    product=Product.objects.get(slug=product_slug)
    categories=Category.objects.all()
    context={
        'product':product,
        'categories':categories,
        'cart':cart,
        }
    return render(request,'app/product.html',context)

def category_view(request,category_slug):
    category=Category.objects.get(slug=category_slug)
    products_of_category=Product.objects.filter(category=category)
    context={
        'category':category,
        'products_of_category': products_of_category
        }
    return render(request,'app/category.html',context)


def cart_view(request):
      try:
          cart_id=request.session['cart_id']# Получение значения сессии при помощи ключа(то есть, 'cart_id'). 
          cart=Cart.objects.get(id=cart_id)
          request.session['total']=cart.items.count()
      except:
          cart=Cart()
          cart.save()
          cart_id=cart.id
          request.session['cart_id']=cart_id# Передача значения в сессию
          cart=Cart.objects.get(id=cart_id)
      context={
          'cart':cart   
        }
      return render(request,'app/cart.html',context)


def add_to_cart_view(request):
     try:
        cart_id=request.session['cart_id']# Получение значения сессии при помощи ключа(то есть, 'cart_id'). 
        cart=Cart.objects.get(id=cart_id)
        request.session['total']=cart.items.count()
     except:
       cart=Cart()
       cart.save()
       cart_id=cart.id
       request.session['cart_id']=cart_id# Передача значения в сессию
       cart=Cart.objects.get(id=cart_id)
     product_slug=request.GET.get('product_slug')
     product=Product.objects.get(slug=product_slug)
     cart.add_to_cart(product.slug)
     new_cart_total=0.00
     for item in cart.items.all():
         new_cart_total+=float(item.item_total)
         cart.cart_total=new_cart_total
         cart.save()
     return JsonResponse({'cart_total':cart.items.count(),'cart_total_price':cart.cart_total})
    

def remove_from_cart_view(request):
     try:
        cart_id=request.session['cart_id']# Получение значения сессии при помощи ключа(то есть, 'cart_id'). 
        cart=Cart.objects.get(id=cart_id)
        request.session['total']=cart.items.count()
     except:
       cart=Cart()
       cart.save()
       cart_id=cart.id
       request.session['cart_id']=cart_id# Передача значения в сессию
       cart=Cart.objects.get(id=cart_id)
     product_slug=request.GET.get('product_slug')
     product=Product.objects.get(slug=product_slug)
     cart.remove_from_cart(product.slug)
     new_cart_total=0.00
     for item in cart.items.all():
         new_cart_total+=float(item.item_total)
         cart.cart_total=new_cart_total
         cart.save()
     return JsonResponse({'cart_total':cart.items.count(),'cart_total_price':cart.cart_total})



def change_item_qty(request):
     try:
        cart_id=request.session['cart_id']# Получение значения сессии при помощи ключа(то есть, 'cart_id'). 
        cart=Cart.objects.get(id=cart_id)
        request.session['total']=cart.items.count()
     except:
       cart=Cart()
       cart.save()
       cart_id=cart.id
       request.session['cart_id']=cart_id# Передача значения в сессию
       cart=Cart.objects.get(id=cart_id)

     qty=request.GET.get('qty')
     item_id=request.GET.get('item_id')
     cart.change_qty(qty, item_id)
     cart_item=CartItem.objects.get(id=int(item_id))
     cart_item.qty=int(qty)
     cart_item.item_total = int(qty) * Decimal(cart_item.product.price)
     cart_item.save()
     return JsonResponse({'cart_total':cart.items.count(),
                          'item_total':cart_item.item_total,
                          'cart_total_price':cart.cart_total})





def checkout_view(request):
     try:
        cart_id=request.session['cart_id']# Получение значения сессии при помощи ключа(то есть, 'cart_id'). 
        cart=Cart.objects.get(id=cart_id)
        request.session['total']=cart.items.count()
     except:
       cart=Cart()
       cart.save()
       cart_id=cart.id
       request.session['cart_id']=cart_id# Передача значения в сессию
       cart=Cart.objects.get(id=cart_id)
     context={
             'cart':cart  
           }
     return render(request,'app/checkout.html',context)


def order_create_view(request):
     try:
        cart_id=request.session['cart_id']# Получение значения сессии при помощи ключа(то есть, 'cart_id'). 
        cart=Cart.objects.get(id=cart_id)
        request.session['total']=cart.items.count()
     except:
       cart=Cart()
       cart.save()
       cart_id=cart.id
       request.session['cart_id']=cart_id# Передача значения в сессию
       cart=Cart.objects.get(id=cart_id)
     form=OrderForm(request.POST or None)
     context={
         'form':form,
         'cart':cart
          }
     return render(request,'app/order.html',context)


def make_order_view(request):
     try:
        cart_id=request.session['cart_id']# Получение значения сессии при помощи ключа(то есть, 'cart_id'). 
        cart=Cart.objects.get(id=cart_id)
        request.session['total']=cart.items.count()
     except:
       cart=Cart()
       cart.save()
       cart_id=cart.id
       request.session['cart_id']=cart_id# Передача значения в сессию
       cart=Cart.objects.get(id=cart_id)
     form=OrderForm(request.POST or None)
     
     if form.is_valid():
         name=form.cleaned_data['name']
         last_name=form.cleaned_data['last_name']
         phone=form.cleaned_data['phone']
         buying_type=form.cleaned_data['buying_type']
         address=form.cleaned_data['address']
         comments=form.cleaned_data['comments']
         new_order=Order()
         new_order.user=request.user
         new_order.save()
         new_order.items.add(cart)
         new_order.first_name=name
         new_order.last_name=last_name
         new_order.phone=phone
         new_order.address=address
         new_order.buying_type=buying_type
         new_order.comments=comments
         new_order.total=cart.cart_total
         new_order.save()
         del request.session['cart_id']
         del request.session['total']
         return HttpResponseRedirect(reverse('thank_you'))
    


def account_view(request):

    order=Order.objects.filter(user=request.user).order_by('-id')#.order_by('-id') более новый заказ на верхних строчках
    
    context={
        'order':order,
  
        }
    return render(request,'app/account.html',context)

def blog(request):
 """Renders the blog page."""
 posts = Blog.objects.order_by('-posted') # запрос на выбор всех статей из модели, отсортированных по убыванию даты опубликования
 assert isinstance(request, HttpRequest)
 return render(
 request,
 'app/blog.html',
 { # параметр в {} — данные для использования в шаблоне.
 'title':'Блог',
 'posts': posts, # передача списка статей в шаблон веб-страницы
 'year':datetime.now().year
 }
 )


def blogpost(request, parametr):
 """Renders the blogpost page."""

 post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
 comments=Comment.objects.filter(post=parametr)
   
 if request.method=="POST":# после отправки данных формы на сервер методом POST
    form=CommentForm(request.POST)
    if form.is_valid():
        comment_f=form.save(commit=False)
        comment_f.author=request.user# добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
        comment_f.date=datetime.now() # добавляем в модель Комментария (Comment) текущую дату
        comment_f.post=Blog.objects.get(id=parametr)# добавляем в модель Комментария (Comment) статью, для которой данный комментарий
        comment_f.save()# сохраняем изменения после добавления полей
  
        return redirect('blogpost', parametr=post_1.id)# переадресация на ту же страницу статьи после отправки комментария
 else:
  form = CommentForm() # создание формы для ввода комментария
   

 assert isinstance(request, HttpRequest)
   
 return render(
 request,
 'app/blogpost.html',
 {
 'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
 'form': form, # передача формы в шаблон веб-страницы 
 'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
 'year':datetime.now().year,
 }
 
 )

def newpost(request):
    if request.method=="POST"and request.FILES:
     form = BlogForm(request.POST, request.FILES)
    
     if form.is_valid():
         
           cd = form.cleaned_data
           file = cd['image']
           title = cd['title']
           description = cd['description']
           content = cd['content']
           form.save()
     return redirect('blog')
    else:

        form = BlogForm()


    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/newpost.html',
        {
            'form': form
        }
    )


def my_order(request):
     order=Order.objects.all().order_by('-id')#.order_by('-id') более новый заказ на верхних строчках
     context={

        'order':order,        
        }
     return render(request,'app/my_order.html',context)
