# forms.py
from django import forms
from .models import Cihaz, Bakim, Gorev
from django.contrib.auth.models import User
from datetime import date, timedelta

class CihazForm(forms.ModelForm):
    class Meta:
        model = Cihaz
        fields = ['seri_no', 'model', 'tur', 'kurulum_tarihi', 'bakım_aralığı_gun']
        widgets = {
            'kurulum_tarihi': forms.DateInput(attrs={'type': 'date'}),
        }

class BakimForm(forms.ModelForm):
    class Meta:
        model = Bakim
        fields = ['cihaz', 'tarih', 'aciklama']
        widgets = {
            'tarih': forms.DateInput(attrs={'type': 'date'}),
        }

class SignupForm(forms.Form):
    username = forms.CharField(label='Kullanıcı Adı')
    email = forms.EmailField(label='E-posta', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Şifre')
    role = forms.ChoiceField(choices=[('muhendis', 'Mühendis'), ('tekniker', 'Tekniker')], label='Rol')

class LoginForm(forms.Form):
    username = forms.CharField(label='Kullanıcı Adı')
    password = forms.CharField(widget=forms.PasswordInput, label='Şifre')

class GorevForm(forms.ModelForm):
    tekniker = forms.ModelChoiceField(queryset=User.objects.filter(profile__role='tekniker'), label='Atanacak Tekniker')
    bakim = forms.ModelChoiceField(
        queryset=Bakim.objects.all(),
        label='Bakım',
        to_field_name='id',
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    # 👇 Ek alan: mühendis formda görünmesin ama ihtiyaç varsa programatik olarak atanabilir.
    # Gösterim istenirse form alanı aktif edilir
    muhendis = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role='muhendis'),
        required=False,
        widget=forms.HiddenInput()  # İsteğe göre TextInput da olabilir
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bakım filtrelemesi - son 7 gün ve sonrası
        self.fields['bakim'].queryset = Bakim.objects.filter(
            tarih__gte=date.today() - timedelta(days=7)
        ).select_related('cihaz')
        # Etiketleri özelleştir (bakım açıklamasında cihaz seri no ve tarih)
        self.fields['bakim'].label_from_instance = lambda obj: f"{obj.cihaz.seri_no} - {obj.tarih.strftime('%d.%m.%Y')}"

    class Meta:
        model = Gorev
        fields = ['bakim', 'tekniker', 'aciklama']
        widgets = {
            'aciklama': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

class GorevGeriBildirimForm(forms.ModelForm):
    class Meta:
        model = Gorev
        fields = ['geri_bildirim', 'durum']
        widgets = {
            'geri_bildirim': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'durum': forms.Select(attrs={'class': 'form-control'}),
        }
