from django.urls import path

from e_commerce.api.api_views import *

# Importamos las API_VIEWS:
from e_commerce.api.marvel_view import *

urlpatterns = [
    # User APIs:
    path('user/login/', LoginUserAPIView.as_view()),

    # APIs de Marvel
    path('get_comics/',get_comics),
    path('purchased_item/',purchased_item),
    
    # Comic API View:
    path('comics/get', GetComicAPIView.as_view()),
    path('comics/<comic_id>/get', GetOneComicAPIView.as_view()),
    path('comics/post', PostComicAPIView.as_view()),
    path('comics/get-post', ListCreateComicAPIView.as_view()),
    path('comics/<pk>/update', RetrieveUpdateComicAPIView.as_view()),
    path('comics/<pk>/delete', DestroyComicAPIView.as_view()),

    # TODO: Wish-list API View
    path('get-wishlist', GetWishListAPIVew.as_view()),
    path('post-wishlist', PostWishListAPIView.as_view()),
    path('post-get-wishlist', ListCreateWishListAPIView.as_view()),
    path('wishupdate/<pk>', RetrieveUpdateWishListAPIView.as_view()),
    path('wishdelete/<pk>', DestroyWishListAPIView.as_view()),
    path('user-comic-list/<username>', GetUserWishListAPIView.as_view()),

]

