from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import ClientDetail, CustomUser, DealerDetail


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'Client':
            ClientDetail.objects.create(type=instance, extra_info="wola")

        if instance.user_type == 'Dealer':
            DealerDetail.objects.create(type=instance, extra_info="wola")


# @receiver(post_save, sender=CustomUser)
# def save_profile(sender, instance, **kwargs):
#    print('123456789098765432'+'  '+instance)
 #   if instance.user_type == 'Client':
  #      ClientDetail.objects.save()
   # if instance.user_type == 'Dealer':
    #    instance.profile.save()
