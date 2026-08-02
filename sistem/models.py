from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User

class Cihaz(models.Model):
    seri_no = models.CharField(max_length=100, unique=True)
    model = models.CharField(max_length=100)
    tur = models.CharField(max_length=100)
    kurulum_tarihi = models.DateField()
    bakım_aralığı_gun = models.IntegerField(default=90)

    def sonraki_bakim_tarihi(self):
        son_bakim = self.bakimlar.order_by('-tarih').first()
        if son_bakim:
            return son_bakim.tarih + timedelta(days=self.bakım_aralığı_gun)
        return self.kurulum_tarihi + timedelta(days=self.bakım_aralığı_gun)

    def __str__(self):
        return f"{self.model} ({self.seri_no})"

class Bakim(models.Model):
    cihaz = models.ForeignKey(Cihaz, on_delete=models.CASCADE, related_name='bakimlar')
    tarih = models.DateField(default=timezone.now)
    aciklama = models.TextField(blank=True)

    def __str__(self):
        return f"{self.cihaz.seri_no} - {self.tarih.strftime('%d.%m.%Y')}"

class Profile(models.Model):
    ROLE_CHOICES = (
        ('muhendis', 'Mühendis'),
        ('tekniker', 'Tekniker'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Gorev(models.Model):
    STATUS_CHOICES = (
        ('bekliyor', 'Bekliyor'),
        ('tamamlandi', 'Tamamlandı'),
        ('iptal', 'İptal'),
    
    )

    bakim = models.ForeignKey(Bakim, on_delete=models.CASCADE, related_name='gorevler')  # Cihaz yerine Bakim
    muhendis = models.ForeignKey(User, on_delete=models.CASCADE, related_name='atanan_gorevler')
    tekniker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='yapilan_gorevler')
    aciklama = models.TextField()
    atama_tarihi = models.DateTimeField(default=timezone.now)
    tamamlanma_tarihi = models.DateTimeField(null=True, blank=True)
    geri_bildirim = models.TextField(blank=True)
    durum = models.CharField(max_length=20, choices=STATUS_CHOICES, default='bekliyor')

    def __str__(self):
        return f"{self.bakim.cihaz.seri_no} - {self.bakim.tarih} için görev"