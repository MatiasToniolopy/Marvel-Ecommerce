from django.urls import path
from django.conf.urls.static import static
from . views import *
from django.contrib.auth.decorators import login_required


urlpatterns = [
    path('register', register, name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('purchased', PurchaseView.as_view(), name='purchased'),
    path('table', login_required(TableView.as_view()), name='table'),
    path('cart', login_required(CartView.as_view()), name='cart'),
    path('favorites', login_required(FavoriteView.as_view()), name='favorites'),
    path('user-data', login_required(UserDataView.as_view()), name='user-data'),
    path('saludo', SaludoView.as_view(), name='saludo'),
    path('contacto', ContacView.as_view(), name='contacto'),
    path('mail', RecivedView.as_view(), name='mail'),
    path('user-update', profile, name='user-update'),
    path('pass-update', passupdate, name='pass-update'),
    path('galeria', GaleriaView.as_view(), name='galeria'), 
    path('detail', DetailsView.as_view(), name='detail'),
    path('checkbutton', check_button, name='checkbutton'),
    path('update-qty', update_wish, name='updateqty'),
    path('reset-passw', PassView.as_view(), name='reset-passw'),
    path('change-password/<uidb64>/<token>', ChangePasswordView.as_view(), name='change_password'),
    path('contact-mail', contact, name='contact'),
    
    
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)