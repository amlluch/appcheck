from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import URLValidator
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class TargetSite(models.Model):

    url = models.URLField(_('url'), max_length = 255, validators=[URLValidator], blank = False, null = False)
    port = models.IntegerField(_('port'), validators=[MaxValueValidator(65535), MinValueValidator(1)], default = 80, blank=False, null=False )
    timeout = models.IntegerField(_('timeout'), default = 10, blank=True, null=True)
    active = models.BooleanField(_('active'), blank=False, null=False)

    class Meta:
        verbose_name = u'Target sites list'

    def __str__(self):
        return self.url + ':' + str(self.port) + '/'

    @property
    def uri(self):
        return ''.join([self.url,':',str(self.port),'/'])

class LinkedSite(models.Model):

    linkname = models.name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = u'Link names to control injection'

    def __str__(self):
        return self.linkname