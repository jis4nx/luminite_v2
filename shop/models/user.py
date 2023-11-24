from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from LuminiteV2.settings import BASE_DIR


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=11)

    image = models.ImageField(upload_to="profile_pic", default="/static/profile.png")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.user.email


class Address(models.Model):
    flat_no = models.CharField(max_length=255)
    street_no = models.CharField(max_length=255)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=30)
    default = models.BooleanField(default=False)
    user_profile = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name="addresses"
    )

    def save(self, *args, **kwargs):
        user_addresses = self.user_profile.addresses.count()
        if user_addresses > 5:
            raise ValidationError("Maximum address limit reached for this user.")
        super().save(*args, **kwargs)

    def __str__(self):
        return " ".join((self.flat_no, self.street_no, self.address_line1))

    class Meta:
        verbose_name_plural = "Addresses"


# POST SAVE UserProfile


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
