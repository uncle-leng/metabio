from django import forms
from django.db import models
from metabio import settings

class UploadFile(models.Model):
    upload_file = models.FileField(upload_to=settings.MEDIA_URL + '/uploadfile')

class DownloadFile(models.Model):
    download_file = models.FileField(upload_to=settings.MEDIA_URL + '/downloadfile')
    upload_file = models.ForeignKey('UploadFile', on_delete=models.CASCADE)

class OutputJSON(models.Model):
    JSON_file = models.FileField(upload_to=settings.MEDIA_URL + '/outputjson')
    download_file = models.ForeignKey('DownloadFile', on_delete=models.CASCADE)

class InputJSON(models.Model):
    input_json = models.FileField(upload_to=settings.MEDIA_URL + '/inputjson')
    upload_file = models.ForeignKey('UploadFile', on_delete=models.CASCADE)

class UploadFileForm(forms.Form):
    upload_form = forms.FileField(required=False)

