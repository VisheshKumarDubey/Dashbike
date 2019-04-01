from django.db import models
from Users.models import CustomUser, ClientDetail, DealerDetail
from django.contrib.auth import get_user_model
from django.utils import timezone


# Create your models here.

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
    filename = scramble_uploaded_filename(
        None, os.path.basename(input_image.name))
    arrdata = filename.split(".")
    # extension is in the last element, pop it
    extension = arrdata.pop()
    basename = "".join(arrdata)
    # add _thumb to the filename
    new_filename = basename + "_thumb." + extension

    # save the image in MEDIA_ROOT and return the filename
    image.save(os.path.join(settings.MEDIA_ROOT, new_filename))

    return new_filename


class Bike(models.Model):
    bike_name = models.CharField(max_length=500, default='type..')
    image = models.ImageField(
        "media", upload_to=scramble_uploaded_filename, default='def.jpg')
    thumbnail = models.ImageField(
        "Thumbnail of uploaded image", blank=True, default='defthumb.jpg')

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
        super(Bike, self).save(force_update=force_update)

    def __str__(self):
        return self.bike_name


class Booking(models.Model):
    bike_model = models.ForeignKey(
        'BikeModel', on_delete=models.CASCADE, default=None)
    bike_from = models.DateTimeField(default=None)
    dob = models.DateTimeField(default=None)
    duration = models.CharField(max_length=500, default=0.0)
    client = models.ForeignKey(
        ClientDetail, on_delete=models.CASCADE, default=None)
    dealer = models.ForeignKey(
        DealerDetail, on_delete=models.CASCADE, default=None)
    transaction_amt = models.CharField(
        max_length=500, default=0.0)  # change name
    ord_id = models.CharField(max_length=500, default=0.0)
    transaction_id = models.CharField(max_length=500, default=0.0)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return str(self.bike_model.dealer)



class BikeModel(models.Model):
    bike_model = models.ForeignKey(
        'Bike', on_delete=models.PROTECT, default=None)
    dealer = models.ForeignKey(
        DealerDetail, on_delete=models.CASCADE, default=None)
    description = models.CharField(max_length=500, default='type..')
    count = models.IntegerField(default=0)
    bike_rate_hr = models.CharField(max_length=500, null=True, blank=True)
    bike_rate_h = models.CharField(max_length=500, null=True, blank=True)
    bike_rate_f = models.CharField(max_length=500, null=True, blank=True)
    bike_isAvailable = models.BooleanField(default=True)
    isActive = models.BooleanField(default=True)

    def bike_img(self):
        return self.bike_model.image

    def thumbnail(self):
        return self.bike_model.thumbnail

    def __str__(self):

        return str(self.bike_model)
