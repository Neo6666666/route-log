from rest_framework import generics, viewsets, views, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from reports.models import ContainerUnloadFact, Report
from reports.serializers import ContainerUnloadFactSerializer, ReportSerializer, GenerateReportSerializer
from reports.filter import ContainerUnloadFactFilter


class ContanerUnloadsListView(viewsets.ModelViewSet):
    """
    Список фактов отгрузки
    """
    queryset = ContainerUnloadFact.objects.all()
    serializer_class = ContainerUnloadFactSerializer
    filterset_class = ContainerUnloadFactFilter
    permission_classes = (IsAuthenticated,)


class ReportsViewSet(
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = (IsAuthenticated,)


class GenerateReportView(generics.CreateAPIView):
    serializer_class = GenerateReportSerializer
    permission_classes = (IsAuthenticated,)


class ExportReportView(views.APIView):
    """
    Экспорт отчета в виде файла
    Id - идентификатор отчета
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request, id, *args, **kwargs):
        """
        TODO: Включить логику формирования документа по ContainerUnloadFact
        """
        return Response(data={'id': id})