import uuid
from django.db import models
from admintion.models import BaseModel, BaseModelID
from ckeditor.fields import RichTextField
from users.models import CustomUser
from django.utils.text import slugify
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from hitcount.settings import MODEL_HITCOUNT
from hitcount.utils import get_hitcount_model
from hitcount.models import HitCountMixin


class Category(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)
    image = models.ImageField(upload_to='images/category/')

    def __str__(self):
        return self.name


class Tag(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True)

    def __str__(self):
        return self.name


class Blog(BaseModelID, HitCountMixin):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Kategoriya")
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    sub_title = models.CharField(max_length=250, null=True, blank=True, verbose_name="Qisqach mazmuni")
    image = models.ImageField(upload_to='images/category/', verbose_name="Maqola uchun rasm")
    content = RichTextField(verbose_name="Maqola matni")
    slug = models.SlugField(max_length=250, unique=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    top = models.BooleanField(default=False)
    is_remove = models.BooleanField(default=False)
    active = models.BooleanField(default=False)
    is_main = models.BooleanField(default=False)
    hash_tags = models.TextField(null=True, help_text="(Vergul orqali ajratib yozish kerak)",
                                 verbose_name="Hesh teglar")

    hitcounts = GenericRelation(
        MODEL_HITCOUNT,
        content_type_field='content_type',
        object_id_field='object_pk',
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_identifier = self.id
            self.slug = f"{base_slug}-{unique_identifier}"

        super().save(*args, **kwargs)

    def hashtags(self):
        if self.hash_tags:
            return list(self.hash_tags.split(','))

    def __str__(self):
        return self.title

    def views_count(self):
        c = get_hitcount_model().objects.get_for_object(self).hits
        return c

    def comments(self):
        return Comments.objects.filter(blog=self).all()


class Comments(BaseModel):
    comment = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class SavedBlog(BaseModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)