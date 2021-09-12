import uuid
import os
import io
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.core.files.storage import default_storage as storage
from django.conf import settings
from PIL import Image



def scramble_uploaded_filename(instance, filename):
    extension = filename.split(".")[-1]
    return "media/profile/{}.{}".format(uuid.uuid4(), extension)

# creates a thumbnail of an existing image
def create_thumbnail(input_image, thumbnail_size=(256, 256)):
    
    if not input_image or input_image == "":
        return
    img_read = storage.open(input_image.name, 'rb')
    img = Image.open(img_read)

    # use PILs thumbnail method; use anti aliasing to make the scaled picture look good
    img.thumbnail(thumbnail_size, Image.ANTIALIAS)
    in_mem_file = io.BytesIO()
    print(storage.open(input_image.name))
    new_filename = "thumb_"+str(storage.open(input_image.name))
    # save the image in MEDIA_ROOT and return the filename
    img.save(in_mem_file, format='PNG')
    img_write = storage.open(new_filename, 'w+')
    img_write.write(in_mem_file.getvalue())
    img_write.close()
    img_read.close()

    return new_filename

class CustomUser(AbstractUser):
    # add additional fields in here
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_choices = (
        ('Client', 'Client'),
        ('Dealer', 'Dealer'),
    )
    user_type = models.CharField(
        max_length=20, choices=type_choices, default='Client')
    number=models.CharField(max_length=12,default=None,null=True)
    fcm_token = models.CharField(max_length=400,default=None,null=True)

    def __str__(self):
        return self.username


class ClientDetail(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    extra_info = models.CharField(max_length=200)
    image = models.ImageField("media",upload_to=scramble_uploaded_filename,default='def.jpg')
    thumbnail = models.ImageField("Thumbnail of uploaded image", blank=True,default='defthumb.jpg')
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # generate and set thumbnail or none
        self.thumbnail = create_thumbnail(self.image)

        # Check if a pk has been set, meaning that we are not creating a new image, but updateing an existing one
        

        # force update as we just changed something
        #save(update_fields=['field_a', 'field_b'])
        super(ClientDetail, self).save(update_fields=['thumbnail'])
    

    def __str__(self):
        return self.type.username

    def client_name(self):
        return self.type.username


class DealerDetail(models.Model):
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    extra_info = models.CharField(max_length=200)
    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)
    image = models.ImageField("media",upload_to=scramble_uploaded_filename,default='def.jpg')
    thumbnail = models.ImageField("Thumbnail of uploaded image", blank=True,default='defthumb.jpg')
    on_hour=models.DateTimeField(null=True,default=None)
    off_hour=models.DateTimeField(null=True,default=None)
    has_bike = models.BooleanField(default=True)
    add_1=models.CharField(max_length=200,null=True,default=None)
    add_2=models.CharField(max_length=200,null=True,default=None)
    area=models.CharField(max_length=200,null=True,default=None)
    city=models.CharField(max_length=200,null=True,default=None)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # generate and set thumbnail or none
        self.thumbnail = create_thumbnail(self.image)

        # Check if a pk has been set, meaning that we are not creating a new image, but updateing an existing one
        if self.pk:
           force_update = True

        # force update as we just changed something
        super(DealerDetail, self).save(update_fields=['thumbnail'])

    def __str__(self):
        return self.type.username
    def dealer_name(self):
        return self.type.username
    
   
