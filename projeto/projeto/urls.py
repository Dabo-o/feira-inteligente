from django.contrib import admin
from django.urls import path, include
from app.urls import router
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

urlpatterns = [
    path('api/', include(router.urls)),  # Sem v1 e v2, direto 'api/'
    path('admin/', admin.site.urls),
    path('auth/', include('rest_framework.urls')),
    path("api-token-auth/", obtain_auth_token)
]