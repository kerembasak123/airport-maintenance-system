from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone
from datetime import date, timedelta
from .models import Cihaz, Gorev
from django.contrib.auth.models import User
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_bakim_notifications():
    logger.info("Bakım bildirimleri başlatıldı")
    today = date.today()
    cihazlar = Cihaz.objects.all()
    for cihaz in cihazlar:
        sonraki_bakim = cihaz.sonraki_bakim_tarihi()
        fark = (sonraki_bakim - today).days
        if 0 <= fark <= 7 or fark < 0:
            muhendisler = User.objects.filter(profile__role__in=['muhendis', 'tekniker'], email__isnull=False)
            alici_listesi = [user.email for user in muhendisler if user.email]
            if alici_listesi:
                subject = f"{cihaz.seri_no} için Bakım Uyarısı"
                message = (
                    f"Merhaba,\n\n"
                    f"Cihaz: {cihaz.model} ({cihaz.seri_no})\n"
                    f"Tür: {cihaz.tur}\n"
                    f"Sonraki Bakım Tarihi: {sonraki_bakim.strftime('%d.%m.%Y')}\n"
                    f"Durum: {'Yaklaşan' if fark >= 0 else 'Geciken'} ({fark} gün)\n"
                    f"Lütfen gerekli işlemleri yapınız.\n\n"
                    f"Terminal Elektronik Sistemleri"
                )
                try:
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        alici_listesi,
                        fail_silently=False,
                    )
                    logger.info(f"Bakım bildirimi gönderildi: {cihaz.seri_no}, alıcılar: {alici_listesi}")
                except Exception as e:
                    logger.error(f"Bakım bildirimi gönderilemedi: {str(e)}")

@shared_task
def send_gorev_notification(gorev_id):
    logger.info(f"Görev bildirimi başlatıldı: Görev ID {gorev_id}")
    try:
        gorev = Gorev.objects.get(id=gorev_id)
        bakim = gorev.bakim
        cihaz = bakim.cihaz
        tekniker = gorev.tekniker
        muhendis = gorev.muhendis

        alici_listesi = []
        if tekniker.email:
            alici_listesi.append(tekniker.email)
        else:
            logger.warning(f"Tekniker e-posta adresi eksik: {tekniker.username}")
        if muhendis.email and muhendis.email != tekniker.email:
            alici_listesi.append(muhendis.email)
        else:
            logger.warning(f"Mühendis e-posta adresi eksik veya teknikerle aynı: {muhendis.username}")

        logger.info(f"Alıcı listesi: {alici_listesi}")
        if alici_listesi:
            subject = f"{cihaz.seri_no} için Yeni Görev Ataması"
            message = (
                f"Merhaba,\n\n"
                f"Yeni bir görev ataması yapılmıştır:\n"
                f"Bakım: {bakim.cihaz.seri_no} - {bakim.tarih.strftime('%d.%m.%Y')}\n"
                f"Cihaz: {cihaz.model} ({cihaz.seri_no})\n"
                f"Tür: {cihaz.tur}\n"
                f"Tekniker: {tekniker.username}\n"
                f"Mühendis: {muhendis.username}\n"
                f"Açıklama: {gorev.aciklama}\n"
                f"Atama Tarihi: {gorev.atama_tarihi.strftime('%d.%m.%Y %H:%M')}\n"
                f"Durum: {gorev.get_durum_display()}\n\n"
                f"Lütfen gerekli işlemleri yapınız.\n"
                f"Terminal Elektronik Sistemleri"
            )
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                alici_listesi,
                fail_silently=False,
            )
            logger.info(f"Görev bildirimi gönderildi: Görev ID {gorev_id}, alıcılar: {alici_listesi}")
        else:
            logger.warning(f"Görev bildirimi gönderilemedi: Alıcı listesi boş, Görev ID {gorev_id}")
    except Gorev.DoesNotExist:
        logger.error(f"Görev bulunamadı: Görev ID {gorev_id}")
    except Exception as e:
        logger.error(f"Görev bildirimi gönderilemedi: {str(e)}")