from typing import Optional, Type

from django.contrib import admin
from .models import Directory, Version, Element
from django.core.exceptions import ObjectDoesNotExist


class ElementInline(admin.StackedInline):
    model: Element = Element
    extra = 0


class VersionInline(admin.StackedInline):
    model: Version = Version
    extra = 0


@admin.register(Directory)
class DirectoryAdmin(admin.ModelAdmin):
    list_display: tuple[str] = (
        "id",
        "code",
        "name",
        "get_current_version",
        "get_version_start_date",
    )
    list_display_links: tuple[str] = ("code", "name")
    inlines: list[Type[VersionInline]] = [VersionInline]

    def search_current_version(self, obj):
        current_version = obj.version_set.latest("version")
        return current_version

    def get_current_version(self, obj) -> Type[Version]:
        current_version = self.search_current_version(obj)
        version = current_version.version
        return version

    get_current_version.short_description = "Текущая версия"

    def get_version_start_date(self, obj) -> Optional[str]:
        current_version = self.search_current_version(obj)
        try:
            version_start_date = current_version.start_date
            return version_start_date
        except ObjectDoesNotExist:
            return None

    get_version_start_date.short_description = "Дата начала действия версии"


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display: tuple[str] = ("directory_code", "directory", "version", "start_date")
    list_display_links: tuple[str] = ("version",)
    inlines: list[Type[ElementInline]] = [ElementInline]

    def directory_code(self, obj) -> str:
        return obj.directory.code

    directory_code.short_description = "Код справочника"


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display: tuple[str, str, str, str] = (
        "id",
        "directory_version",
        "element_code",
        "element_value"
    )
    list_display_links: tuple[str] = ("element_value",)
