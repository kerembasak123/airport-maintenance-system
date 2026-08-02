from django.shortcuts import render, redirect, get_object_or_404
from .models import Cihaz, Bakim, Gorev
from .forms import CihazForm, BakimForm, LoginForm, SignupForm, GorevForm, GorevGeriBildirimForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date
from django.contrib import messages
from sistem.tasks import send_gorev_notification
import logging
from django.db.models import Count
from datetime import timedelta

logger = logging.getLogger(__name__)

# Cihazlar
@login_required
def cihaz_listesi(request):
    profile = request.user.profile
    if profile.role not in ['muhendis', 'tekniker']:
        return HttpResponseForbidden("Yetkiniz yok")
    
    cihazlar = Cihaz.objects.all()
    form = CihazForm(request.POST or None)
    
    if profile.role == 'muhendis':
        if form.is_valid():
            form.save()
            return redirect('cihaz_listesi')
    else:
        form = None  # tekniker form göremez
    
    return render(request, 'cihazlar.html', {'cihazlar': cihazlar, 'form': form})

@login_required
def cihaz_duzenle(request, pk):
    cihaz = get_object_or_404(Cihaz, pk=pk)
    if request.user.profile.role != 'muhendis':
        return HttpResponseForbidden("Yetkiniz yok")
    form = CihazForm(request.POST or None, instance=cihaz)
    if form.is_valid():
        form.save()
        return redirect('cihaz_listesi')
    return render(request, 'cihaz_form.html', {'form': form})

@login_required
def cihaz_sil(request, pk):
    cihaz = get_object_or_404(Cihaz, pk=pk)
    if request.user.profile.role != 'muhendis':
        return HttpResponseForbidden("Yetkiniz yok")
    cihaz.delete()
    return redirect('cihaz_listesi')

# Bakımlar
@login_required
def bakim_listesi(request):
    if request.user.profile.role not in ['muhendis', 'tekniker']:
        return HttpResponseForbidden("Yetkiniz yok")
    bakimlar = Bakim.objects.all()
    form = BakimForm(request.POST or None)
    if request.user.profile.role == 'muhendis' and form.is_valid():
        form.save()
        return redirect('bakim_listesi')
    if request.user.profile.role != 'muhendis':
        form = None
    return render(request, 'bakimlar.html', {'bakimlar': bakimlar, 'form': form})

@login_required
def bakim_duzenle(request, pk):
    bakim = get_object_or_404(Bakim, pk=pk)
    if request.user.profile.role != 'muhendis':
        return HttpResponseForbidden("Yetkiniz yok")
    form = BakimForm(request.POST or None, instance=bakim)
    if form.is_valid():
        form.save()
        return redirect('bakim_listesi')
    return render(request, 'bakim_form.html', {'form': form})

@login_required
def bakim_sil(request, pk):
    bakim = get_object_or_404(Bakim, pk=pk)
    if request.user.profile.role != 'muhendis':
        return HttpResponseForbidden("Yetkiniz yok")
    bakim.delete()
    return redirect('bakim_listesi')

@login_required
def cihaz_bakim_gecmisi(request, pk):
    cihaz = get_object_or_404(Cihaz, pk=pk)
    bakimlar = cihaz.bakimlar.all()
    return render(request, 'cihaz_bakim_gecmisi.html', {'cihaz': cihaz, 'bakimlar': bakimlar})

# Görevler
@login_required
def gorev_listesi(request):
    if request.user.profile.role == 'muhendis':
        gorevler = Gorev.objects.filter(muhendis=request.user)
    else:
        gorevler = Gorev.objects.filter(tekniker=request.user)
    return render(request, 'gorevler.html', {'gorevler': gorevler})

@login_required
def gorev_ata(request):
    if request.user.profile.role != 'muhendis':
        return HttpResponseForbidden("Yetkiniz yok")
    
    if request.method == 'POST':
        form = GorevForm(request.POST)
        if form.is_valid():
            gorev = form.save(commit=False)
            gorev.muhendis = request.user  # Mühendis bilgisi atanıyor
            gorev.save()
            
            try:
                send_gorev_notification.delay(gorev.id)
                messages.success(request, "Görev başarıyla atandı ve bildirim gönderildi.")
            except Exception as e:
                messages.error(request, f"Bildirim gönderilemedi: {str(e)}")
            
            return redirect('gorev_listesi')  # ✅ Form başarılıysa yönlendir
        
        else:
            messages.error(request, "Form verileri geçersiz. Lütfen kontrol edin.")
    
    else:
        form = GorevForm()
    
    return render(request, 'gorev_form.html', {'form': form})

@login_required
def gorev_geri_bildirim(request, pk):
    gorev = get_object_or_404(Gorev, pk=pk)
    if request.user.profile.role != 'tekniker' or gorev.tekniker != request.user:
        return HttpResponseForbidden("Yetkiniz yok")
    form = GorevGeriBildirimForm(request.POST or None, instance=gorev)
    if form.is_valid():
        gorev = form.save(commit=False)
        if gorev.durum == 'tamamlandi':
            gorev.tamamlanma_tarihi = timezone.now()
        gorev.save()
        return redirect('gorev_listesi')
    return render(request, 'gorev_geri_bildirimi.html', {'form': form, 'gorev': gorev})

@login_required
def ana_sayfa(request):
    cihazlar = Cihaz.objects.all()
    bugun = date.today()
    yaklasan = []
    geciken = []
    
    for cihaz in cihazlar:
        sonraki = cihaz.sonraki_bakim_tarihi()
        if sonraki:
            fark = (sonraki - bugun).days
            if 0 <= fark <= 7:
                yaklasan.append(cihaz)
            elif fark < 0:
                geciken.append(cihaz)
    
    return render(request, 'ana_sayfa.html', {
        'yaklasan': yaklasan,
        'geciken': geciken
    })

def giris(request):
    logger.debug(f"Kullanıcı durumu: is_authenticated={request.user.is_authenticated}, user={request.user}")
    if request.user.is_authenticated:
        logout(request)
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('ana_sayfa')
            else:
                form.add_error(None, "Kullanıcı adı veya şifre yanlış.")
    else:
        form = LoginForm()
    return render(request, 'giris.html', {'form': form})

def kayit(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            role = form.cleaned_data['role']
            
            if User.objects.filter(username=username).exists():
                return render(request, "kayit.html", {"form": form, "error": "Bu kullanıcı adı zaten var."})
            
            user = User.objects.create_user(username=username, email=email, password=password)
            user.profile.role = role
            user.profile.save()
            return redirect('giris')
        else:
            return render(request, "kayit.html", {"form": form, "error": "Lütfen formu doğru doldurun."})
    else:
        form = SignupForm()
    return render(request, "kayit.html", {"form": form})

def cikis(request):
    logout(request)
    return redirect('giris')

@login_required
def gorev_duzenle(request, pk):
    if request.user.profile.role != 'muhendis':
        return HttpResponseForbidden("Yetkiniz yok")
    
    gorev = get_object_or_404(Gorev, pk=pk, muhendis=request.user)
    
    if gorev.durum == 'tamamlandi':
        messages.error(request, "Tamamlanmış görevler düzenlenemez.")
        return redirect('gorev_listesi')
    
    if request.method == 'POST':
        form = GorevForm(request.POST, instance=gorev)
        if form.is_valid():
            gorev = form.save(commit=False)
            if gorev.durum == 'iptal':
                gorev.durum = 'bekliyor'  # Yeniden aktif hale getiriliyor
            gorev.muhendis = request.user  # 👈 güvenlik açısından mühendis atanmasını yinele
            gorev.save()
            logger.info(f"Görev düzenlendi: {gorev.id}, kullanıcı: {request.user.username}")
            messages.success(request, "Görev başarıyla düzenlendi.")
            return redirect('gorev_listesi')
        else:
            messages.error(request, "Lütfen formu doğru doldurun.")
    else:
        form = GorevForm(instance=gorev)
    
    return render(request, 'gorev_duzenle.html', {'form': form, 'gorev': gorev})

@login_required
def gorev_sil(request, pk):
    if request.user.profile.role != 'muhendis':
        return HttpResponseForbidden("Yetkiniz yok")
    gorev = get_object_or_404(Gorev, pk=pk, muhendis=request.user)
    if gorev.durum == 'tamamlandi':
        messages.error(request, "Tamamlanmış görevler düzenlenemez.")
        return redirect('gorev_listesi')
    
    if request.method == 'POST':
        gorev_id = gorev.id
        gorev.delete()
        logger.info(f"Görev silindi: {gorev_id}, kullanıcı: {request.user.username}")
        messages.success(request, "Görev başarıyla silindi.")
        return redirect('gorev_listesi')
    return redirect('gorev_listesi')

@login_required
def raporlar(request):
    if request.user.profile.role not in ['muhendis', 'tekniker']:
        return HttpResponseForbidden("Yetkiniz yok")
    
    bugun = date.today()
    yaklasan = []
    geciken = []
    cihazlar = Cihaz.objects.all()
    
    # Yaklaşan ve geciken bakımlar
    for cihaz in cihazlar:
        sonraki = cihaz.sonraki_bakim_tarihi()
        if sonraki:
            fark = (sonraki - bugun).days
            if 0 <= fark <= 7:
                yaklasan.append(cihaz)
            elif fark < 0:
                geciken.append(cihaz)
    
    # Görev istatistikleri
    if request.user.profile.role == 'muhendis':
        gorev_ozeti = Gorev.objects.filter(muhendis=request.user).values('tekniker__username', 'durum').annotate(sayi=Count('id')).order_by('tekniker__username')
        tum_gorevler = Gorev.objects.filter(muhendis=request.user)
    else:
        gorev_ozeti = Gorev.objects.filter(tekniker=request.user).values('durum').annotate(sayi=Count('id'))
        tum_gorevler = Gorev.objects.filter(tekniker=request.user)
    
    # Cihaz bazında bakım geçmişi
    cihaz_bakim_ozeti = []
    for cihaz in cihazlar:
        bakim_sayisi = cihaz.bakimlar.count()
        son_bakim = cihaz.bakimlar.order_by('-tarih').first()
        cihaz_bakim_ozeti.append({
            'cihaz': cihaz,
            'bakim_sayisi': bakim_sayisi,
            'son_bakim': son_bakim.tarih if son_bakim else None,
        })
    
    context = {
        'yaklasan': yaklasan,
        'geciken': geciken,
        'gorev_ozeti': gorev_ozeti,
        'tum_gorevler': tum_gorevler,
        'cihaz_bakim_ozeti': cihaz_bakim_ozeti,
        'role': request.user.profile.role,
    }
    return render(request, 'raporlar.html', context)