from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.utils import timezone

from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Directory, Version, Element
from .serializers import DirectorySerializer, ElementSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema


class DirectoryView(APIView):
    """
    Получение списка справочников
    Метод: refbooks/[?date=<date>]
    Тип запроса HTTP: GET
    Параметры запроса:
    - date: Дата начала действия в формате ГГГГ-ММ-ДД.
            Если указана, то возвратятся только те справочники,
            в которых имеются Версии с Датой начала действия раннее
            или равной указанной.
    Формат ответа:
    - refbooks: Список объектов справочников
        - id: Идентификатор справочника
        - code: Код справочника
        - name: Наименование справочника
    Пример запроса: GET /refbooks/?date=2022-10-01"""
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Дата начала действия справочника. Пример: 2021-01-01",
                type=openapi.TYPE_STRING,
                format="YYYY-MM-DD",
            ),
        ],
        responses={200: DirectorySerializer(many=True)},
    )
    def get(self, request) -> Response:
        date = self.request.query_params.get("date")

        if date:
            directories = Directory.objects.filter(version__start_date__lte=date)
        else:
            directories = Directory.objects.all()

        directory_data = []
        for directory in directories:
            serializer = DirectorySerializer(directory)
            data = serializer.data
            if not any(entry["id"] == data["id"] for entry in directory_data):
                directory_data.append(data)

        return Response({"refbooks": directory_data})


class ElementView(APIView):
    """
    Получение элементов заданного справочника
    Метод: refbooks/<id>/elements[?version=<version>]
    Тип запроса HTTP: GET
    Параметры запроса:
        - id: Идентификатор справочника
        - version: Версия справочника.
                Если не указана, то возвращаются элементы текущей версии.
                Текущая версия, дата начала действия которой позже всех
                остальных версий данного справочника, но не позже текущей даты.
    Формат ответа:
        - elements: Список элементов в версии справочника
        - code: Код элемента
        - value: Значение элемента
    Пример запроса:
    GET /refbooks/1/elements?version=1.0
    """
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="Идентификатор справочника",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                "version",
                openapi.IN_QUERY,
                description="Версия справочника",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={200: ElementSerializer(many=True)},
    )
    def get(self, request, id) -> Response:
        version_param = self.request.query_params.get("version")

        try:
            directory = Directory.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"error": "Справочник не найден"}, status=404)

        if version_param:
            try:
                version = Version.objects.get(
                    directory=directory, version=version_param
                )
            except ObjectDoesNotExist:
                return Response(
                    {"error": "Версия не найдена для указанного справочника"},
                    status=404,
                )
        else:
            latest_version = directory.version_set.filter(
                start_date__lte=timezone.now()
            ).latest("start_date")

            if not latest_version:
                return Response(
                    {"error": "Не найдено версий для указанного справочника"},
                    status=404,
                )
            version = latest_version

        elements = Element.objects.filter(directory_version=version)
        element_data = ElementSerializer(elements, many=True).data

        return Response({"elements": element_data})


class CheckElementView(APIView):
    """Валидация элемента справочника
    Метод:refbooks/<id>/check_element?code=<code>&value=<value>[&version=<version>]
    Тип запроса HTTP: GET
    Параметры запроса:
        - id: Идентификатор справочника
        - code: Код элемента справочника
        - value: Значение элемента справочника
        - version: Версия справочника. Если не указана, то должны проверяться
                элементы в текущей версии. Текущей является та версия, дата начала
                действия которой позже всех остальных версий данного справочника,
                но не позже текущей даты.
    Ответ:
        Если элемент с указанным кодом и значением существует в указанной версии
        справочника, возвращается статус 200 "Элемент найден".
        Если элемент не найден, возвращается статус 404 "Элемент не найден в
        указанной версии".
    Пример запроса:
    GET /refbooks/1/check_element?code=J00&value=Хирург[&version=1.0]"""
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "id",
                openapi.IN_PATH,
                description="Идентификатор справочника",
                type=openapi.TYPE_INTEGER,
                required=True,
            ),
            openapi.Parameter(
                "code",
                openapi.IN_QUERY,
                description="Код элемента справочника",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "value",
                openapi.IN_QUERY,
                description="Значение элемента справочника",
                type=openapi.TYPE_STRING,
                required=True,
            ),
            openapi.Parameter(
                "version",
                openapi.IN_QUERY,
                description="Версия справочника",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ],
        responses={200: "Элемент найден", 404: "Элемент не найден"},
    )
    def get(self, request, id, *args, **kwargs) -> Response:
        code = self.request.query_params.get("code")
        value = self.request.query_params.get("value")
        version = self.request.query_params.get("version")

        try:
            directory = Directory.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Справочник не найден"}, status=status.HTTP_404_NOT_FOUND
            )

        if version:
            try:
                version = directory.version_set.get(version=version)
            except ObjectDoesNotExist:
                return Response(
                    {"error": "Версия не найдена"}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            version = directory.get_latest_version()

        try:
            element = version.element_set.get(element_code=code, element_value=value)
            return Response({"message": "Элемент найден"}, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Элемент не найден в указанной версии"},
                status=status.HTTP_400_BAD_REQUEST,
            )


def index(request):
    return HttpResponse("<h1>Cервис терминологий</h1>")