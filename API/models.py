from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to='API/static', blank=True, null=True)

    class Meta:
        ordering = ('image',)

    def __str__(self):
        return self.image


class Mall(models.Model):
    id = models.AutoField(primary_key=True)
    gender = models.CharField(max_length=200, blank=True, null=True)
    dateofBirth = models.DateField(null=True)
    mallName = models.CharField(max_length=200, blank=True, null=True)
    mallId = models.CharField(max_length=200, blank=True, null=True)
    imageType = models.CharField(max_length=200, blank=True, null=True)
    userId = models.CharField(max_length=200, blank=True, null=True)
    mallGroupId = models.CharField(max_length=200, blank=True, null=True)
    attachedImages = models.ManyToManyField('API.Image', related_name='Images', blank=True)

    class Meta:
        ordering = ('mallName',)

    def __str__(self):
        return self.mallName
