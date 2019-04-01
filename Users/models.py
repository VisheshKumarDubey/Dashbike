from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
import uuid
import os
from django.conf import settings
from PIL import Image



def scramble_uploaded_filename(instance, filename):
    """
    Scramble / uglify the filename of the uploaded file, but keep the files extension (e.g., .jpg or .png)
    :param instance:
    :param filename:
    :return:
    """
    extension = filename.split(".")[-1]
    return "{}.{}".format(uuid.uuid4(), extension)

# creates a thumbnail of an existing image
def create_thumbnail(input_image, thumbnail_size=(256, 256)):
    """
    Create a thumbnail of an existing image
    :param input_image:
    :param thumbnail_size:
    :return:
    """
    # make sure an image has been set
    if not input_image or input_image == "":
        return

    # open image
    image = Image.open(input_image)

    # use PILs thumbnail method; use anti aliasing to make the scaled picture look good
    image.thumbnail(thumbnail_size, Image.ANTIALIAS)

    # parse the filename and scramble it
    filename = scramble_uploaded_filename(None, os.path.basename(input_image.name))
    arrdata = filename.split(".")
    # extension is in the last element, pop it
    extension = arrdata.pop()
    basename = "".join(arrdata)
    # add _thumb to the filename
    new_filename = basename + "_thumb." + extension

    # save the image in MEDIA_ROOT and return the filename
    image.save(os.path.join(settings.MEDIA_ROOT, new_filename))

    return new_filename

class CustomUser(AbstractUser):
    # add additional fields in here
    type_choices = (
        ('Client', 'Client'),
        ('Dealer', 'Dealer'),
    )
    user_type = models.CharField(
        max_length=20, choices=type_choices, default='Client')
    number=models.CharField(max_length=12,default='0000000000')

    def __str__(self):
        return self.username


class ClientDetail(models.Model):
    type = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    extra_info = models.CharField(max_length=200)
    image = models.ImageField("media",upload_to=scramble_uploaded_filename,default='def.jpeg')
    thumbnail = models.ImageField("Thumbnail of uploaded image", blank=True,default='defthumb.jpeg')
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        On save, generate a new thumbnail
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        # generate and set thumbnail or none
        self.thumbnail = create_thumbnail(self.image)

        # Check if a pk has been set, meaning that we are not creating a new image, but updateing an existing one
        if self.pk:
           force_update = True

        # force update as we just changed something
        super(ClientDetail, self).save(force_update=force_update)

    def __str__(self):
        return self.type.username


class DealerDetail(models.Model):
    type = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    extra_info = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)
   # distance= models.FloatField(null=True, blank=True, default=None)
    image = models.ImageField("media",upload_to=scramble_uploaded_filename,default='def.jpeg')
    thumbnail = models.ImageField("Thumbnail of uploaded image", blank=True,default='defthumb.jpeg')
    has_bike = models.BooleanField(default=True)


    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        On save, generate a new thumbnail
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        # generate and set thumbnail or none
        self.thumbnail = create_thumbnail(self.image)

        # Check if a pk has been set, meaning that we are not creating a new image, but updateing an existing one
        if self.pk:
          force_update = True


        # force update as we just changed something
        super(DealerDetail, self).save(force_update=force_update)

    def __str__(self):
        return self.type.username
