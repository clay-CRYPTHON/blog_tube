from django.db import models
import uuid
from users.models import CustomUser
from simple_history.models import HistoricalRecords


class BaseModel(models.Model):
    uuid = models.UUIDField(unique=True,editable=False,primary_key = True, default = uuid.uuid4)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(inherit=True)
    is_remove = models.BooleanField(default=False,editable=False)

    class Meta:
        abstract = True


class BaseModelID(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    history = HistoricalRecords(inherit=True)
    is_remove = models.BooleanField(default=False,editable=False)

    class Meta:
        abstract = True


class AllIPs(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    ip = models.CharField(max_length=200)
    ip_type = models.CharField(max_length=100)
    path = models.CharField(max_length=500,null=True,blank=True)
    sec_ch_ua = models.CharField(max_length=500,null=True,blank=True)
    platform = models.CharField(max_length=500,null=True,blank=True)
    user_agent = models.CharField(max_length=500,null=True,blank=True)
    lang = models.CharField(max_length=500,null=True,blank=True)
    comp_name = models.CharField(max_length=500,null=True,blank=True)
    cpu_architecture = models.CharField(max_length=500,null=True,blank=True)
    cpu_identifier = models.CharField(max_length=500,null=True,blank=True)
    cpu_level = models.CharField(max_length=500,null=True,blank=True)
    method = models.CharField(max_length=500,null=True,blank=True)
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self) -> str:
        return self.ip + " " +self.ip_type