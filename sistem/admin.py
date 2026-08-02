from django.contrib import admin
from .models import Cihaz, Bakim, Profile, Gorev

@admin.register(Cihaz)
class CihazAdmin(admin.ModelAdmin):
    list_display = ("seri_no", "model", "tur", "kurulum_tarihi", "bakım_aralığı_gun")

@admin.register(Bakim)
class BakimAdmin(admin.ModelAdmin):
    list_display = ("cihaz", "tarih", "aciklama")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role")

@admin.register(Gorev)
class GorevAdmin(admin.ModelAdmin):
    list_display = ("get_bakim_bilgisi", "muhendis", "tekniker", "durum", "atama_tarihi")

    def get_bakim_bilgisi(self, obj):
        return f"{obj.bakim.cihaz.seri_no} - {obj.bakim.tarih.strftime('%d.%m.%Y')}"
    get_bakim_bilgisi.short_description = "Bakım"