from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.db import connection
from .models import TargetSite

@receiver(pre_save, sender=TargetSite)
def pre_save_targetsite(sender, instance, **kwargs):
    if (instance.active):
        TargetSite.objects.all().update(active=False)