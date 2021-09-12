import io
from django.core.files.storage import default_storage as storage


def save(self, *args, **kwargs):
    super().save(*args, **kwargs)

    img_read = storage.open(self.image.name, 'rb')
    img = Image.open(img_read)

    if img.height > 300 or img.width > 300:
        output_size = (300, 300)
        img.thumbnail(output_size)
        in_mem_file = io.BytesIO()
        img.save(in_mem_file, format='JPEG')
        img_write = storage.open(self.image.name, 'w+')
        img_write.write(in_mem_file.getvalue())
        img_write.close()

img_read.close()