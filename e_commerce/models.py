from django.db import models
from django.contrib.auth.models import User




class Comic(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    marvel_id = models.PositiveIntegerField(verbose_name='marvel ids', default=1, unique=True)
    title = models.CharField(verbose_name='titles', max_length=120, default='')
    description = models.TextField(verbose_name='descriptions', default='')
    price = models.FloatField(verbose_name='prices', max_length=5, default=0.00)
    stock_qty = models.PositiveIntegerField(verbose_name='stock qty', default=0)
    picture = models.URLField(verbose_name='pictures', default='')

    class Meta:
        
        verbose_name = 'Comic'
        verbose_name_plural = 'Comics'
    

    def __str__(self):
        return f'{self.id}'


class WishList(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    user_id = models.ForeignKey(User, verbose_name='User', on_delete=models.DO_NOTHING, default=1, blank=True)
    comic_id = models.ForeignKey(Comic, verbose_name='Comic', on_delete=models.DO_NOTHING, default=1, blank=True)
    favorite = models.BooleanField(verbose_name='Favorite', default=False)
    cart = models.BooleanField(verbose_name='carts', default=False)
    wished_qty = models.PositiveIntegerField(verbose_name='wished qty', default=0)
    buied_qty = models.PositiveIntegerField(verbose_name='buied qty', default=0)

    class Meta:
        
        verbose_name = 'Wishlist'
        verbose_name_plural = 'Wishlists'


    def __str__(self):
        return f'{self.id}'


class Profile(models.Model):
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.DO_NOTHING, default=1, blank=True)
    country = models.CharField(verbose_name='Pais', max_length=100)
    state = models.CharField(verbose_name='Provincia/Estado', max_length=100)
    city = models.CharField(verbose_name='Ciudad', max_length=100, default='')
    postal_code = models.CharField(verbose_name='Codigo Postal', max_length=15)
    cell_phone_number = models.CharField(verbose_name='Numero de Tel', max_length=20)
    avatar = models.ImageField(verbose_name='imagen', default='', blank=True, null=True)
    
  

    class Meta:
        verbose_name = 'profile'

    def __str__(self):
        return f'{self.id}'
