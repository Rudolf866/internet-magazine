"""
Definition of urls for firstDjangosite.
"""

from app.views import my_order
from app.views import account_view
from django.views.generic import TemplateView
from app.views import make_order_view
from app.views import order_create_view
from app.views import checkout_view
from app.views import change_item_qty
from app.views import remove_from_cart_view
from app.views import add_to_cart_view
from app import views
from app.views import cart_view
from app.views import category_view,product_view




from django.conf import settings#это объект.Файл настроек Django содержит полную конфигурацию установленного проект
from django.conf.urls.static import static#Работа со статическими файлами (CSS, изображения)
from django.contrib.staticfiles.urls import staticfiles_urlpatterns#собирает статические файлы со всех ваших приложений


from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views

# Uncomment the next lines to enable the admin:
from django.conf.urls import include
from django.contrib import admin
admin.autodiscover() # инициализирует административный раздел

urlpatterns = [
    # Examples:
    url(r'^$', app.views.home, name='home'),
    url(r'^contact$', app.views.contact, name='contact'),
    url(r'^about$', app.views.about, name='about'),
    url(r'^base_view$', app.views.base_view, name='base_view'),
    url(r'^gallery$', app.views.gallery, name='gallery'),
    url(r'^blog$', app.views.blog, name='blog'),
    url(r'^(?P<parametr>\d+)/$', app.views.blogpost, name='blogpost'),
    url(r'^newpost$', app.views.newpost, name='newpost'),
    url(r'^login/$',
        django.contrib.auth.views.login,
        {
            'template_name': 'app/login.html',
            'authentication_form': app.forms.BootstrapAuthenticationForm,
            'extra_context':
            {
                'title': 'Авторизоваться',
                'year': datetime.now().year,
            }
        },
        name='login'),
    url(r'^logout$',
        django.contrib.auth.views.logout,
        {
            'next_page': '/',
        },
        name='logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
     url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
     url(r'^registration$', app.views.registration, name='registration'),
     url(r'^category/(?P<category_slug>[-\w]+)/$',category_view, name='category_detail'),
     url(r'^product/(?P<product_slug>[-\w]+)/$', product_view, name='product_detail'),
     url(r'^add_to_cart/$', add_to_cart_view, name='add_to_cart'),
     url(r'^remove_from_cart/$', remove_from_cart_view, name='remove_from_cart'),
     url(r'^change_item_qty/$', change_item_qty, name='change_item_qty'),
     url(r'^cart/$',cart_view,name='cart'),
     url(r'^checkout/$',checkout_view,name='checkout'),
     url(r'^order/$',order_create_view,name='order_create'),
     url(r'^make_order/$',make_order_view,name='make_order'),
     url(r'^thank_you/$',TemplateView.as_view(template_name='app/thank_you.html'),name='thank_you'),
     url(r'^account/$',account_view,name='account'),
     url(r'^my_order/$',my_order,name='my_order'),

]

if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   urlpatterns += staticfiles_urlpatterns() 
