from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include(('users.urls', 'users'), namespace='users')),
    path('api/', include(('lms.urls', 'lms'), namespace='lms')),
]