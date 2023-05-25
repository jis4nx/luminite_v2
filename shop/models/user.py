from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver


class Address(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    flat_no = models.CharField(max_length=255)
    street_no = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=30)

    def __str__(self):
        return " ".join((self.flat_no, self.street_no, self.address_line1))

    class Meta:
        verbose_name_plural = "Addresses"


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

    address = models.ForeignKey(Address, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(default="../static/images/default.jpg")

    def __str__(self):
        return self.user.email


# POST SAVE UserProfile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
