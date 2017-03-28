from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class AccessPoint(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=255, blank=False)
    purpose = models.CharField(max_length=255, blank=True)
    creationDT = models.DateTimeField(null=True, blank=True)
    modificationDT = models.DateTimeField(null=True, blank=True)

    def num_of_pwds(self):
        return PasswordAccessPoint.objects.filter(
            access_point_id=self.id).count()

    def __str__(self):
        return 'accesspoint: [' + self.name + ']'

    def get_absolute_url(self):
        return reverse('access_point_detail', kwargs={'pk': self.pk})


class Password(models.Model):
    # id = models.BigIntegerField(primary_key=True, auto_created=True, unique=True)
    user = models.ForeignKey(User, default=4, related_name="ownership")
    website = models.CharField(max_length=255, blank=True)
    username = models.CharField(max_length=255, blank=True)
    password = models.CharField(max_length=255, blank=True)
    comment = models.CharField(max_length=255, null=True, blank=True)
    email = models.CharField(max_length=255, null=True, blank=True)
    security_questions = models.CharField(
        max_length=256, null=True, blank=True)
    creationDT = models.DateTimeField(null=True, blank=True)
    modificationDT = models.DateTimeField(null=True, blank=True)

    access_points = models.ManyToManyField(
        AccessPoint, through='PasswordAccessPoint')

    def __str__(self):
        return 'password entry: [' + self.website + '] ' + \
               '[' + self.username + ']' + ' [' + self.password + ']'

    def is_private(self):
        if PasswordAccessPoint.objects.filter(
                password_id=self.id).count():
            return "No"
        elif PasswordTrustedPartner.objects.filter(
                password_id=self.id).count():
            return "Partially"
        else:
            return "Yes"

    def get_absolute_url(self):
        # return reverse('password', kwargs={'pk': self.pk})
        return reverse('password_detail', kwargs={'pk': self.pk})


class PasswordAccessPoint (models.Model):
    password = models.ForeignKey(Password, on_delete=models.CASCADE)
    access_point = models.ForeignKey(AccessPoint, on_delete=models.CASCADE)
    DT_established = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'PasswordAccessPoint: password_id: [' + \
               str(self.password_id) + ']' + \
               'access_point_id: [' + \
               str(self.access_point_id) + ']'


class MaxNumPassword(models.Model):
    max_num_pwd = models.IntegerField(null=True, blank=True)
    gen_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'MaxNumPassword: max_num_pwd: [' + \
               str(self.max_num_pwd) + ']' + \
               'gen_date_time: [' + \
               str(self.gen_date_time) + ']'


class MaxNumAccessPoint(models.Model):
    max_num_ap = models.IntegerField(null=True, blank=True)
    gen_date_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'MaxNumAccessPoint: max_num_ap: [' + \
               str(self.max_num_ap) + ']' + \
               'gen_date_time: [' + \
               str(self.gen_date_time) + ']'


class PasswordTrustedPartner(models.Model):
    password = models.ForeignKey(Password, on_delete=models.CASCADE)
    trusted_partner = models.ForeignKey(User, on_delete=models.CASCADE)
    DT_established = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return 'PasswordTrustedParter: password_id: [' + \
               str(self.password_id) + ']' + \
               'trusted_partner_id: [' + \
               str(self.trusted_partner_id) + ']'