from django.contrib import admin
from .models import CustomUser
from django.utils.html import mark_safe


@admin.register(CustomUser)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'username', 'first_name', 'last_name', 'about')

    def image_tag(self, obj):
        return mark_safe('<img src="%s" width="100px" height="100px" />' % obj.image.url)

    image_tag.short_description = 'Image'

    def get_exclude(self, request, obj=None):
        # Foydalanuvchi superuser bo'lsa, barcha maydonlar ko'rsatiladi
        if request.user.is_superuser:
            return ()
        # Foydalanuvchi o'zining yozgan bloglarini boshqaradi
        return (
        'is_staff', 'is_superuser', 'is_active', 'last_seen', 'groups', 'password', 'user_permissions', 'last_seen')

    def get_queryset(self, request):
        # Foydalanuvchi faqat o'zi yozgan bloglarni chiqaradi
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            self.exclude = ()
            return qs
        else:
            self.exclude = (
            'is_staff', 'is_superuser', 'is_active', 'last_seen', 'groups', 'password', 'user_permissions', 'last_seen')
            return qs.filter(uuid=request.user.uuid)
