from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.giris, name='giris'),
    path('anasayfa/', views.ana_sayfa, name='ana_sayfa'),
    path('giris/', views.giris, name='giris'),
    path('kayit/', views.kayit, name='kayit'),
    path('cikis/', views.cikis, name='cikis'),
    # Cihaz sayfaları
    path('cihazlar/', views.cihaz_listesi, name='cihaz_listesi'),
    path('cihazlar/duzenle/<int:pk>/', views.cihaz_duzenle, name='cihaz_duzenle'),
    path('cihazlar/sil/<int:pk>/', views.cihaz_sil, name='cihaz_sil'),
    path('cihazlar/<int:pk>/gecmis/', views.cihaz_bakim_gecmisi, name='cihaz_bakim_gecmisi'),
    # Bakım sayfaları
    path('bakimlar/', views.bakim_listesi, name='bakim_listesi'),
    path('bakimlar/duzenle/<int:pk>/', views.bakim_duzenle, name='bakim_duzenle'),
    path('bakimlar/sil/<int:pk>/', views.bakim_sil, name='bakim_sil'),
    # Görev sayfaları
    path('gorevler/', views.gorev_listesi, name='gorev_listesi'),
    path('gorevler/ata/', views.gorev_ata, name='gorev_ata'),
    path('gorevler/geri-bildirim/<int:pk>/', views.gorev_geri_bildirim, name='gorev_geri_bildirim'),
    path('gorevler/duzenle/<int:pk>/', views.gorev_duzenle, name='gorev_duzenle'),
    path('gorevler/sil/<int:pk>/', views.gorev_sil, name='gorev_sil'),
    path('raporlar/', views.raporlar, name='raporlar'),
   
]