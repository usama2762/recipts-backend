from django.urls import include, path
from rest_framework.routers import DefaultRouter

from API import views

router = DefaultRouter()
router.register(r'images', views.ImageView, basename='Image'),
router.register(r'mall', views.MallView, basename='Mall'),
router.register(r'user', views.UserView, basename='MyUsers'),


urlpatterns = [
    path('', include(router.urls)),
    path('api/login', views.LoginView.as_view({'get': 'post'})),
]
