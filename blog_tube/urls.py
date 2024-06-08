from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import re_path as url
from django.views.static import serve

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('logout/', auth_views.LogoutView.as_view(), name='log_out'),
                  path('social-auth/', include('social_django.urls'), name='social'),
                  path('hitcount/', include(('hitcount.urls', 'hitcount'),
                                            namespace='hitcount')),
                  # path('', include('home.urls')),
                  # path('blogs/', include('blogs.urls')),
                  path('user/', include('users.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    urlpatterns += url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),

# handler404 = 'home.views.handler404'