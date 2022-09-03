from django.db import models


class Organization(models.Model):
    name = models.CharField('Имя', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'


class Client(models.Model):
    name = models.CharField('Имя', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


class Service(models.Model):
    name = models.CharField('название', max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сервис'
        verbose_name_plural = 'Сервисы'


class Bill(models.Model):
    client = models.ForeignKey(Client, models.CASCADE, related_name='bills', verbose_name='клиенты')
    organization = models.ForeignKey(Organization, models.CASCADE, related_name='bills', verbose_name='организация')
    num = models.PositiveIntegerField('номер')
    sum = models.FloatField('сумма')
    date = models.DateField('дата')
    service = models.ForeignKey(Service, models.CASCADE, related_name='bills', verbose_name='сервисы')

    def __str__(self):
        return ' '.join(filter(None, [
            str(self.id),
            self.client.name,
            str(self.num),
            self.organization.name,
            self.service.name
        ]))

    class Meta:
        verbose_name = 'Счёт'
        verbose_name_plural = 'Счета'
        unique_together = ('client', 'organization', 'num')
        ordering = ('client', 'num',)
