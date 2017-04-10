from django.db import models
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class Receipt(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, unique=True)
    user = models.ForeignKey(User, default=4, related_name="ownership")

    name = models.CharField(max_length=254, blank=False)

    store_name = models.CharField(max_length=255, blank=False)

    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False)

    file = models.FileField(
        upload_to='uploads/%Y/%m/%d',
        max_length=510,
        blank=False)

    comment = models.CharField(max_length=254, blank=True)

    creation_DT = models.DateTimeField(null=False, blank=False)
    modification_DT = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return 'Receipt: [' + self.name + '] ' + \
               '[' + 'at store ' + self.store_name + ']' + \
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
