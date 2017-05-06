from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    street = models.CharField(
        max_length=255, null=True, blank=True)
    city = models.CharField(
        max_length=255, null=True, blank=True)
    state = models.CharField(
        max_length=255, null=True, blank=True)
    zip = models.CharField(
        max_length=255, null=True, blank=True)
    country = models.CharField(
        max_length=255, null=True, blank=True,
        default="USA")

    cell_phone = models.CharField(
        max_length=100, null=True, blank=True)
    home_phone = models.CharField(
        max_length=100, null=True, blank=True)
    work_phone = models.CharField(
        max_length=100, null=True, blank=True)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Receipt(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, unique=True)
    user = models.ForeignKey(User)

    name = models.CharField(max_length=254, blank=False)

    store_name = models.CharField(max_length=255, blank=False)

    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=False)

    filename = models.CharField(max_length=999, blank=True)

    file_url = models.CharField(max_length=999, blank=True)

    comment = models.CharField(max_length=254, blank=True)

    creation_DT = models.DateTimeField(null=False, blank=False)
    modification_DT = models.DateTimeField(null=False, blank=False)

    def __str__(self):
        return 'Receipt: [receipt_name:' + self.name + '] ' + \
               '[bought at store: ' + self.store_name + '] ' + \
               '[created on: ' + str(self.creation_DT) + ']'

    def get_absolute_url(self):
        # return reverse('password', kwargs={'pk': self.pk})
        return reverse('receipt_detail', kwargs={'pk': self.pk})


class Prescription(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, unique=True)
    user = models.ForeignKey(User)

    name = models.CharField(max_length=254, null=False, blank=False)
    doctor_name = models.CharField(max_length=999, null=True, blank=True)
    expiration_date = models.DateField(null=True, blank=True)

    left_eye_sphere = \
        models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)
    left_eye_cylinder = \
        models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)
    left_eye_axis = \
        models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)
    left_eye_prism = \
        models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)
    left_eye_base = \
        models.CharField(
            max_length=255, null=True, blank=True)
    left_eye_added_power = \
        models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)

    right_eye_sphere = \
        models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)
    right_eye_cylinder = \
        models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)
    right_eye_axis = \
        models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)
    right_eye_prism = \
        models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=False)
    right_eye_base = \
        models.CharField(
            max_length=255, null=True, blank=True)
    right_eye_added_power = \
        models.DecimalField(
            max_digits=10, decimal_places=2, null=True, blank=True)

    filename = models.CharField(
        max_length=999, null=True, blank=True)

    file_url = models.CharField(
        max_length=999, null=True, blank=True)

    comment = models.CharField(
        max_length=254, null=True, blank=True)

    creation_DT = models.DateTimeField(null=True, blank=False)
    modification_DT = models.DateTimeField(null=True, blank=False)

    def __str__(self):
        return 'Prescription: [name:' + self.name + '] ' + \
               '[prescribed by: ' + self.doctor_name + '] ' + \
               '[created on: ' + str(self.creation_DT) + ']'

    def get_absolute_url(self):
        # return reverse('password', kwargs={'pk': self.pk})
        return reverse('prescription_detail', kwargs={'pk': self.pk})


class MaxNumReceipt(models.Model):
    max_num_receipt = models.IntegerField(null=True, blank=True)
    gen_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'MaxNumReceipt: max_num_receipt [' + \
               str(self.max_num_receipt) + ']' + \
               'gen_date_time: [' + \
               str(self.gen_date_time) + ']'
