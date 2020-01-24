"""
Definition of forms.
"""
from .models import Blog
from.models import Comment
from django.contrib.auth.models import User
from django.utils import timezone



from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))



class OrderForm(forms.Form):
    name=forms.CharField()
    last_name=forms.CharField(required=False)
    phone=forms.CharField()
    buying_type=forms.ChoiceField(widget=forms.Select(), 
    choices=([("self","Самовывоз"),("delivery","Доставка")]))
    date=forms.DateField(widget=forms.SelectDateWidget(),initial=timezone.now())
    address=forms.CharField(required=False)
    comments=forms.CharField(widget=forms.Textarea,required=False)

   
    def __init__(self,*args,**kwargs):
        super(OrderForm,self).__init__(*args,**kwargs)
        self.fields['name'].label='Имя'
        self.fields['last_name'].label='Фамилия'
        self.fields['phone'].label='Контактный телефон'
        self.fields['phone'].help_text='Пожалуйста, указывайте реальный номер телефона, по которому с Вами можно связаться' 
        self.fields['buying_type'].label='Способ получения'
        self.fields['address'].label='Адрес доставки'
        self.fields['address'].help_text='*Обязательно указывайте город!'
        self.fields['comments'].label='Комментарий к заказу'
        self.fields['date'].label='Дата доставки'
        self.fields['date'].help_text='Доставка производится на следующий день после оформления заказа. Менеджер с Вами предварительно свяжется.'



class CommentForm (forms.ModelForm):
   class Meta:
     model = Comment # используемая модель
     fields = ('text',) # требуется заполнить только поле text
     labels = {'text': "Комментарий"} # метка к полю формы text


class BlogForm (forms.ModelForm):
   class Meta:
     model = Blog # используемая модель
     fields = ('image','title','description','content','posted',) # требуется заполнить только поле text
