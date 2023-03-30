from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path('logout', views.logout_page, name='logout'),

    path('Reservations', views.reservations_pages, name='Reservations'),
    path('reservation/<str:school_name>', views.courses_list, name='courses_list'),
    path('create_course/', views.create_course, name='create_course'),
    path('login_register/', views.login_register_page, name='login_register'),
    path('', views.index, name='index'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)