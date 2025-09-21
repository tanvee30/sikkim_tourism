from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Monastery, Archive, Monk, MonkSession, MonkSessionApplication, MonasteryVirtualTourImage
)

class MonasteryVirtualTourImageInline(admin.TabularInline):
    model = MonasteryVirtualTourImage
    extra = 1

@admin.register(Monastery)
class MonasteryAdmin(admin.ModelAdmin):
    list_display = ("name", "established_year", "location")
    inlines = [MonasteryVirtualTourImageInline]


@admin.register(Archive)
class ArchiveAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'monastery', 'created_at', 'image_tag')
    search_fields = ('title', 'description')
    list_filter = ('monastery',)
    readonly_fields = ('created_at', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="150" height="150" style="object-fit:contain;"/>', obj.image.url)
        return "No Image"
    image_tag.short_description = "Preview"


@admin.register(Monk)
class MonkAdmin(admin.ModelAdmin):
    list_display = ("name", "monastery")
    search_fields = ("name", "monastery")


@admin.register(MonkSession)
class MonkSessionAdmin(admin.ModelAdmin):
    list_display = ("title", "monk", "date", "start_time", "end_time", "capacity", "donation")
    list_filter = ("monk", "date")
    search_fields = ("title",)


@admin.register(MonkSessionApplication)
class MonkSessionApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "session", "status", "applied_at")
    list_filter = ("status", "applied_at")
    search_fields = ("user__email", "session__title")


