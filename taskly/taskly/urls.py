
from django.contrib import admin
from django.urls import path , include
# from todo import views
# from user import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('task/', include('todo.urls')),
    path('auth/', include('user.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]


