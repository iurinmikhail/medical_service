from django.core.exceptions import ObjectDoesNotExist
from django.db import models



class Directory(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Идентификатор")
    code = models.CharField(
        max_length=100, unique=True, blank=False, null=False, verbose_name="Код"
    )
    name = models.CharField(
        max_length=300, blank=False, null=False, verbose_name="Наименование"
    )
    description = models.TextField(verbose_name="Описание", blank=True, null=True)

    def get_latest_version(self):
        """Получает последнюю версию справочника.
        Возвращает последнюю версию справочника, дата начала действия которой позже
        всех остальных версий данного справочника, но не позже текущей даты.

        :return: Объект последней версии справочника или None, если версий нет
        :rtype: Version or None
        """
        try:
            latest_version = self.version_set.latest("start_date")
            return latest_version if latest_version else None
        except ObjectDoesNotExist:
            return None

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Справочник"
        verbose_name_plural = "Справочники"


class Version(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Идентификатор")
    directory = models.ForeignKey(
        Directory, on_delete=models.CASCADE, verbose_name="Наименование справочника"
    )
    version = models.CharField(
        max_length=50, blank=False, null=False, verbose_name="Версия"
    )
    start_date = models.DateField(
        verbose_name="Дата начала версии", blank=True, null=True
    )

    def __str__(self):
        return f"{self.directory} - {self.version}"

    class Meta:
        unique_together = [
            ("directory", "version"),
            ("directory", "start_date"),
        ]
        verbose_name = "Версия справочника"
        verbose_name_plural = "Версии справочника"
        ordering = ["directory", "version"]


class Element(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="Идентификатор")
    directory_version = models.ForeignKey(
        Version,
        on_delete=models.CASCADE,
        verbose_name="Идентификатор Версии справочника",
    )
    element_code = models.CharField(
        max_length=100, blank=False, null=False, verbose_name="Код элемента"
    )
    element_value = models.CharField(
        max_length=300, blank=False, null=False, verbose_name="Значение элемента"
    )

    def __str__(self):
        return self.element_value

    class Meta:
        unique_together = ["directory_version", "element_code"]
        verbose_name = "Элемент справочника"
        verbose_name_plural = "Элементы справочника"
        ordering = ["directory_version", "element_code"]
