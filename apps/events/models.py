from django.db import models
from ..account.models import User
from datetime import timedelta

class Tag(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nombre')
    frequency = models.IntegerField(blank=True, null=True, verbose_name='Frecuencia')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Ponent(models.Model):
    full_name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nombre')
    image = models.ImageField(upload_to='events/ponents', blank=True, null=True, verbose_name='Imagen')
    description = models.CharField(max_length=200, blank=True, null=True, verbose_name='Descripción')
    twitter = models.URLField(blank=True, null=True, verbose_name='Twitter')
    facebook = models.URLField(blank=True, null=True, verbose_name='Facebook')
    google = models.URLField(blank=True, null=True, verbose_name='Google')
    linkdn = models.URLField(blank=True, null=True, verbose_name='Linkdn')

    class Meta:
        ordering = ('full_name',)
        verbose_name = 'Ponente'
        verbose_name_plural = 'Ponentes'

    def __str__(self):
        return self.full_name


class Place(models.Model):
    latitude = models.FloatField(blank=True, null=True, verbose_name='Latitud')
    longitude = models.FloatField(blank=True, null=True, verbose_name='Longitud')
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nombre')
    image = models.ImageField(upload_to='events/places', blank=True, null=True, verbose_name='Imagen')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Lugar'
        verbose_name_plural = 'Lugares'

    def __str__(self):
        return self.name


class Tematic(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True, verbose_name='Nombre')
    description = models.TextField(blank=True, null=True, verbose_name='Tematicas')
    image = models.ImageField(upload_to='events/tematics', blank=True, null=True, verbose_name='Imagen')

    class Meta:
        ordering = ('name',)
        verbose_name = 'Tematica'
        verbose_name_plural = 'Tematicas'

    def __str__(self):
       return self.name


class Event(models.Model):
    title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Titulo')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Fecha')
    content = models.TextField(verbose_name='Descripcion', blank=True, null=True)
    type = models.CharField(max_length=200, verbose_name='Tipo', blank=True, null=True)
    image = models.ImageField(upload_to='events/event',blank=True,null=True,verbose_name='imagen')
    places = models.ManyToManyField(Place, related_name='events',blank=True, verbose_name='Lugares del evento')
    ponents = models.ManyToManyField(Ponent, related_name='events', blank=True,verbose_name='Ponentes')
    tags = models.ManyToManyField(Tag, related_name='events',blank=True, verbose_name='Tags')
    tematics = models.ManyToManyField(Tematic, related_name='events',blank=True, verbose_name='Tematicas')

    class Meta:
        ordering = ('date',)
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'

    @property
    def not_server_hour(self):
        return self.date-timedelta(hours=5)

    def __str__(self):
        return self.title


class Calendar(models.Model):
    user = models.ForeignKey(User, related_name='calendars', verbose_name='Usuario')
    event = models.ForeignKey(Event, related_name='calendars', verbose_name='Evento')

    class Meta:
        verbose_name_plural = "Calendars"
        verbose_name = "Calendar"

    def __str__(self):
        return u'{}{} - {}'.format(self.user.first_name, self.user.last_name, self.event.title)
