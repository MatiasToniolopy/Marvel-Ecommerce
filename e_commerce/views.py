from datetime import datetime
from tkinter import E
from marvel_api import settings
from django.core.mail import send_mail

from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render, reverse
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views.generic import (FormView, ListView, RedirectView, TemplateView, View)
from validate_email import validate_email

from .forms import ProfileUpdateForm, UserForm, UserUpdateForm
from .models import Comic, Profile, WishList

'''Todo es parcial'''
#Registro de usuario
def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registro correcto!')
            return redirect('/e-commerce/login')
    else:
        form = UserForm()
    return render(request, 'e-commerce/register.html', {'form': form})

#Edicion de perfil de usuario utilizando dos form en una sola vista
def profile(request):
    Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Edicion completa!')
            return redirect('user-data')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        return render(request, 'e-commerce/userupdate.html', {'u_form': u_form, 'p_form': p_form})

#Edicion de password de usuario     
def passupdate(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Password actualizado!')
            return redirect('login')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'e-commerce/userchangepass.html', {'form': form})  

class LoginFormView(LoginView):
    template_name = 'e-commerce/login.html'
    
    def get_success_url(self):
        return redirect('login')
    


class LogoutView(RedirectView):
    pattern_name = 'login'
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'Sesion cerrada con exito!')
        logout(request)
        return super().dispatch(request, *args, **kwargs)


class PurchaseView(ListView):
    template_name = 'e-commerce/purchased.html'
    queryset = Comic.objects.all().order_by('-id')
    paginate_by = 2
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comic'] = Comic.objects.all()
        
        return context
    
    
class TableView(TemplateView):
    template_name = 'e-commerce/tabla.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comic'] = Comic.objects.all()
        return context
    
    
class FavoriteView(TemplateView):
    template_name = 'e-commerce/favorites.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        username = self.request.user
        user_obj = User.objects.get(username=username)
        context['fav'] = wish_obj = WishList.objects.filter(user_id=user_obj, favorite=True).count()
        wish_obj = WishList.objects.filter(user_id=user_obj, favorite=True)
        cart_items = [obj.comic_id for obj in wish_obj]
        context['fav_items'] = cart_items
        return context


class UserDataView(TemplateView):
    template_name = 'e-commerce/user.html' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            id_user = self.request.user.pk 
            queryset = User.objects.filter(id=id_user)
            user_data = queryset.values().first()
            context['user_data'] = user_data
            query = Profile.objects.filter(id=id_user)
            extradata = query.values().first()
            context['extradata'] = extradata
        
        return context    
    
class SaludoView(TemplateView):
    template_name = 'e-commerce/saludo.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        user = User.objects.get(username=self.request.user)
        data = WishList.objects.filter(user_id=user, cart=True, wished_qty__gt=0)
        comics = [obj.comic_id for obj in data]
        context['comics'] = comics
        
        if data:
            time = datetime.now()
            context['date'] = time.strftime('%Y-%m-%d')
            
        for (comic, wish_obj) in zip(comics, data):
            comic.stock_qty = comic.stock_qty - wish_obj.wished_qty
            comic.save()
            wish_obj.buied_qty += wish_obj.wished_qty
            wish_obj.wished_qty = 0
            wish_obj.cart = False
            wish_obj.save()
        messages.success(self.request, 'Tu compra se realizó con exito!')   
        return context
    
class ContacView(TemplateView):
    template_name = 'e-commerce/contacto.html'
    
class RecivedView(TemplateView):
    template_name = 'e-commerce/mail.html'
    
class GaleriaView(TemplateView):
    template_name = 'e-commerce/galeria.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comic'] = Comic.objects.all()
        return context


class DetailsView(TemplateView):
    template_name = 'e-commerce/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            comic_obj = Comic.objects.get(
                marvel_id=self.request.GET.get('marvel_id'))
            context["comic"] = comic_obj
            context['comic_picture_full'] = str(
                comic_obj.picture).replace('/standard_xlarge', '')
            context['comic_desc'] = str(
                comic_obj.description).replace('<br>', '\n')
            username = self.request.user
            if username != None:
                user_obj = User.objects.filter(username=username)
                if user_obj.first() != None:
                    wish_obj = WishList.objects.filter(
                        user_id=user_obj[0].id, comic_id=comic_obj)
                    if wish_obj.first() != None:
                        context["favorite"] = wish_obj.first().favorite
                        context["cart"] = wish_obj.first().cart
                        context["wished_qty"] = wish_obj.first().wished_qty
                    else:
                        context["favorite"] = False
                        context["cart"] = False
                        context["wished_qty"] = 0
        except:
            return context
        return context


def check_button(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        marvel_id = request.POST.get('marvel_id')
        user_authenticated = request.POST.get('user_authenticated')
        type_button = request.POST.get('type_button')
        actual_value = request.POST.get('actual_value')
        path = request.POST.get('path')
        username = username if username != '' else None
        marvel_id = marvel_id if marvel_id != '' else None
        user_authenticated = True if user_authenticated == 'True' else False
        type_button = type_button if type_button != '' else None
        actual_value = True if actual_value == 'True' else False
        path = path if path != None else 'index'

        if user_authenticated and username != None:
            
            user_obj = User.objects.get(username=username)
            comic_obj = Comic.objects.get(marvel_id=marvel_id)
            wish_obj = WishList.objects.filter(
                user_id=user_obj, comic_id=comic_obj).first()
            if not wish_obj:
                wish_obj = WishList.objects.create(
                    user_id=user_obj, comic_id=comic_obj)
            if type_button == "cart":
                wish_obj.cart = not actual_value
                messages.success(request, 'El comic se agregó a tu carrito!')
                if wish_obj.cart is False:
                    wish_obj.wished_qty = 0
                    messages.success(request, 'Se eliminó el comic de tu carrito!')
                
                wish_obj.save()
            elif type_button == "favorite":
                messages.success(request, 'El comic se agregó a tus favoritos!')
                wish_obj.favorite = not actual_value
                if wish_obj.favorite is False:
                    wish_obj.favorite = 0
                    messages.success(request, 'Se eliminó el comic de tus favoritos!')
                wish_obj.save()
                
                
            else:
                pass
            if 'detail' in path:
                path += f'?marvel_id={marvel_id}'
    
            return redirect(path)
        else:
            return redirect('login')
    else:
        return redirect('purchased')


class CartView(TemplateView):
     
    template_name = 'e-commerce/cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.user
        user_obj = User.objects.get(username=username)
        wish_obj = WishList.objects.filter(user_id=user_obj, cart=True)

        ids = [id[0] for id in wish_obj.values_list('comic_id')]
        
        d_comics = Comic.objects.filter(id__in=ids).order_by('id').values()

        list_wished_qty = [qty[0] for qty in wish_obj.order_by('comic_id').values_list('wished_qty')]

        context['total_price'] = 0.00

        for (d, qty) in zip(d_comics, list_wished_qty):
            d['wished_qty_act'] = qty
            d['wished_qty_restant'] = d['stock_qty'] - qty

            if qty != 0:
                context['total_price']+= float(d['price']) * qty              

        context['total_price'] = round(context['total_price'], 2)
        context['cart_items'] = d_comics
        return context


def update_wish (request):
    if request.method == 'POST':
        comic_id = request.POST.get('comic_id')
        qty = int(request.POST.get('quantity'))
        
        comic_obj = Comic.objects.get(id=comic_id)
        stock_act = comic_obj.stock_qty

        if qty > stock_act:
            qty = 0
            
        wish_obj = WishList.objects.filter(comic_id=comic_id)
        wished_act = wish_obj.first().wished_qty
        aux = wished_act + qty
        if aux <= stock_act:
            wished_act = aux

        wish_obj.update(wished_qty=wished_act)

    return redirect('cart')

class PassView(View):
    
    def get(self, request):
        return render(request, 'e-commerce/resetpassword.html')
    
    def post(self, request):
        email = request.POST['email']
        context = {'values': request.POST}
        data = User.objects.filter(email=email)
        if not data.exists():
            messages.error(request, 'Email invalido')
            return render(request, 'e-commerce/resetpassword.html', context)
        
        current_site = get_current_site(request)
        user = User.objects.filter(email=email)
        if user.exists():
            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            } 
            link = reverse('change_password', kwargs = {
                'uidb64': email_contents['uid'], 'token': email_contents['token']
            })
            email_subject = 'Reset Password'
            reset_url = 'http://'+current_site.domain+link
            email = EmailMessage(
                email_subject,
                'Hola solicitaste restablecer tu contraseña, da click en el enlace y sigue los pasos \n'+reset_url,
                'noreply@marvel.com',
                [email],
            )
            email.send(fail_silently=False)
            messages.success(request, 'Te enviamos un mail, revisa tu casilla de correo')
        return render(request, 'e-commerce/resetpassword.html')
   

class ChangePasswordView(FormView):
    
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        return render(request, 'e-commerce/changepwd.html', context)
    
    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password != password2:
            return render(request, 'e-commerce/changepwd.html', context)
        if len(password) < 6:
            return render(request, 'e-commerce/changepwd.html', context)
        
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)
        user.set_password(password)
        user.save()
        
        messages.success(request, 'Se restableció  tu contraseña!')
        
        return redirect('login')
        
   
def contact(request):
    if request.method == 'POST':
        subject = request.POST['asunto']
        message = request.POST['mensaje'] + " " + request.POST['email']
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['taekwondotae9@gmail.com']
        send_mail(subject, message, email_from, recipient_list)
        messages.success(request, 'Tu mensaje ha sido enviado!')
        return render(request, 'e-commerce/mail.html')
    
    return render(request, 'e-commerce/contacto.html')