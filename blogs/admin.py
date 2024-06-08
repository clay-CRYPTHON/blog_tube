from django.contrib import admin
from .models import *
from django.utils.html import mark_safe

admin.site.register(Tag)
admin.site.register(Comments)
admin.site.register(SavedBlog)


@admin.register(Category)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

    def image_tag(self, obj):
        return mark_safe('<img src="%s" width="100px" height="100px" />' % obj.image.url)

    image_tag.short_description = 'Image'


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('image_tag', 'title', 'category', 'user', 'create_date')
    search_fields = ('title', 'user__username')
    prepopulated_fields = {'slug': ('category', 'title',)}
    date_hierarchy = 'create_date'

    def image_tag(self, obj):
        return mark_safe('<img src="%s" width="100px" height="100px" />' % obj.image.url)

    image_tag.short_description = 'Image'

    def get_exclude(self, request, obj=None):
        # Foydalanuvchi superuser bo'lsa, barcha maydonlar ko'rsatiladi
        if request.user.is_superuser:
            return ()
        # Foydalanuvchi o'zining yozgan bloglarini boshqaradi
        return ('top', 'active', 'user', 'is_main', 'is_remove')

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        # Foydalanuvchi faqat o'zi yozgan bloglarni chiqaradi
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            self.exclude = ()
            return qs
        else:
            self.exclude = ('top', 'active', 'user', 'is_main', 'is_remove')
            return qs.filter(user=request.user)

