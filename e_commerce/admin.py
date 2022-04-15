from django.contrib import admin

from e_commerce.models import Comic, WishList, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'country', 'state', 'city', 'postal_code')

@admin.register(Comic)
class ComicAdmin(admin.ModelAdmin):
    list_display = ('marvel_id', 'title', 'stock_qty', 'price')
    list_filter= ('marvel_id','title')
    search_fields = ['title']
    
    fieldsets = (
        (None, {
            'fields': ('marvel_id', 'title', 'stock_qty')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('description','price', 'picture'),
        }),
    )


@admin.register(WishList)
class wish_listAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'comic_id', 'favorite', 'cart')
    list_display_links = ('user_id', 'comic_id')
    list_filter= ('favorite','cart')
