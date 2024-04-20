import debug_toolbar
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = 'Console santé admin'
admin.site.index_title = 'Administration'
admin.site.site_title = 'Console Santé'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('soins/', include('unité_de_soins.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
