from django.db import models

from admintion.models import BaseModel

# Create your models here.
class Social(BaseModel):
    name = models.CharField(max_length=200)
    icon = models.CharField(max_length=200)
    url = models.TextField()

    def __str__(self) -> str:
        return self.name
    

class AboutSection(BaseModel):
    min_content = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200)
    content = models.TextField()
    btn_name = models.CharField(max_length=200,default="Ba'tafsil")
    btn_url = models.CharField(max_length=200,default="/")
    img1 = models.ImageField(upload_to='images/about/')
    img2 = models.ImageField(upload_to='images/about/')
    img3 = models.ImageField(upload_to='images/about/')
    def __str__(self) -> str:
        return self.title
    
class AboutTeam(BaseModel):
    min_content = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    content = models.TextField()
    def __str__(self) -> str:
        return self.title
    

class ContactSection(BaseModel):
    title1 = models.CharField(max_length=200)
    title1_name = models.CharField(max_length=200)
    title2 = models.CharField(max_length=200)
    title2_name = models.CharField(max_length=200)
    title3 = models.CharField(max_length=200)
    title3_name = models.CharField(max_length=200)
    google_map = models.TextField()
    form_title = models.CharField(max_length=200)
    form_content = models.CharField(max_length=200)
    form_btn_name = models.CharField(max_length=200,default="Yuborish")
    img1 = models.ImageField(upload_to='images/contact/',null=True)
    img2 = models.ImageField(upload_to='images/contact/',null=True)
    img3 = models.ImageField(upload_to='images/contact/',null=True)
    image = models.ImageField(upload_to='images/contact/',null=True)
    def __str__(self) -> str:
        return self.title1
    

class ContactForm(BaseModel):
    full_name = models.CharField(max_length=200)
    email_or_phone = models.CharField(max_length=200)
    message = models.TextField()
    
    def __str__(self) -> str:
        return self.full_name
    
class DayImages(BaseModel):
    name = models.CharField(max_length=200)
    img1 = models.ImageField(upload_to='images/days/')
    img2 = models.ImageField(upload_to='images/days/')
    img3 = models.ImageField(upload_to='images/days/')
    img4 = models.ImageField(upload_to='images/days/')
    img5 = models.ImageField(upload_to='images/days/')
    img6 = models.ImageField(upload_to='images/days/')
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name