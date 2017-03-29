from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


fs = FileSystemStorage(location='/media/photos')


class Receipt(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, unique=True)
    user = models.ForeignKey(User, default=4, related_name="ownership")

    name = models.CharField(max_length=255, blank=True)

    store_name = models.CharField(max_length=255, blank=True)

    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    photo = models.ImageField(storage=fs)

    creation_DT = models.DateTimeField(null=True, blank=True)
    modification_DT = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'Receipt: [' + self.name + '] ' + \
               '[' + self.store_name + ']' + \
               '[' + 'Created on ' + str(self.creation_DT) + ']'


    def get_absolute_url(self):
        # return reverse('password', kwargs={'pk': self.pk})
        return reverse('receipt_detail', kwargs={'pk': self.pk})


class MaxNumReceipt(models.Model):
    max_num_receipt = models.IntegerField(null=True, blank=True)
    gen_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'MaxNumReceipt: max_num_receipt [' + \
               str(self.max_num_receipt) + ']' + \
               'gen_date_time: [' + \
               str(self.gen_date_time) + ']'
