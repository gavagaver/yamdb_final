from django.urls import include, path
from rest_framework import routers

from . import views
from .views import get_token, register

app_name = 'api_v1'

router_v1 = routers.DefaultRouter()

router_v1.register('users', views.UserViewSet, basename='users')
router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register(
    r'titles\/(?P<title_id>\d+)\/reviews',
    views.ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles\/(?P<title_id>\d+)\/reviews\/(?P<review_id>\d+)\/comments',
    views.CommentViewSet, basename='comments'
)

auth_patterns = [
    path('signup/', register, name='register'),
    path('token/', get_token, name='get_token'),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router_v1.urls))
]
