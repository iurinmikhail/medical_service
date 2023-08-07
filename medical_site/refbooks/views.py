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
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "date",
                openapi.IN_QUERY,
                description="Дата начала действия справочника",
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