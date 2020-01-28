from rest_framework import serializers

from nav_client.serializers import DeviceSerializer, GeozoneSerializer, PointSerializer

from reports.models import Report, ContainerUnloadFact, Device


class ReportSerializer(serializers.ModelSerializer):
    device = DeviceSerializer(many=False)

    class Meta:
        model = Report
        fields = (
            'id',
            'created_at',
            'device',
            'date',
        )


class GenerateReportSerializer(serializers.ModelSerializer):
    P2_DOCUMENT = 0
    REQUESTS = 1

    FILE_TYPES = (
        (P2_DOCUMENT, 'Приложение №2'),
        (REQUESTS, 'Заявки'),
    )

    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())
    date = serializers.DateField()
    file = serializers.FileField(write_only=True)
    file_type = serializers.ChoiceField(choices=FILE_TYPES, write_only=True)

    class Meta:
        model = Report
        fields = (
            'id',
            'created_at',
            'device',
            'date',
            'file',
            'file_type',
        )

    def create(self, validated_data):
        """
        TODO: Включить логику формирования отчета
        """
        return Report.objects.create(date=validated_data['date'], device=validated_data['device'])


class ContainerUnloadFactSerializer(serializers.ModelSerializer):
    track_points = PointSerializer(many=True, read_only=True)
    geozone = GeozoneSerializer(many=False, read_only=True)

    class Meta:
        model = ContainerUnloadFact
        fields = (
            'id',
            'report',
            'geozone',
            'track_points',
            'datetime_entry',
            'datetime_exit',
            'is_unloaded',
            'value',
            'container_type',
            'directory',
            'count',
        )