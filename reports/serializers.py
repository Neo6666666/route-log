from rest_framework import serializers

from nav_client.models import Device, SyncDate
from nav_client.serializers import (
    FlatRowSerializer,
    GeozoneSerializer,
)
from reports.models import ContainerType, ContainerUnloadFact, Report

from . import attachment_parser, application_parser
from rest_framework.fields import SerializerMethodField
from requests.models import Response


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        depth = 1
        fields = (
            'id',
            'created_at',
            'device',
            'date',
        )


class GenerateReportSerializer(serializers.ModelSerializer):
    device = serializers.PrimaryKeyRelatedField(
        queryset=Device.objects.all())
    date = serializers.DateField()
    attachment = serializers.FileField(write_only=True, required=False)
    application = serializers.FileField(write_only=True, required=False)
    container_types = serializers.ListField(required=False)

    class Meta:
        model = Report
        fields = (
            'id',
            'created_at',
            'device',
            'date',
            'attachment',
            'application',
            'container_types'
        )

    def create(self, validated_data):
        attachment = validated_data.get('attachment', None)
        device = validated_data.get('device', None)
        container_types = validated_data.get('container_types', None)
        date = validated_data.get('date', None)
        syncdate = [x for x in SyncDate.objects.all()
                    if check_syncdate(x.datetime, date)]

        if syncdate in ([], None):
            return Response(None, 200)

        report = Report.objects.create(date=date, device=device)

        if attachment and date:

            bulk_obj = []
            bulk_tp = []
            rows = attachment_parser.parse(attachment,
                                           syncdate[0],
                                           device,
                                           container_types)

            for row in rows:
                obj = ContainerUnloadFact(report=report,
                                          geozone=row["geozone"],
                                          datetime_entry=row["time_in"],
                                          datetime_exit=row["time_out"],
                                          is_unloaded=row["is_unloaded"],
                                          value=row["value"],
                                          container_type=row["ct_type"],
                                          directory=row["directory"],
                                          count=row["count"],
                                          nav_mt_id=row["nav_mt_id"])
                bulk_obj.append(obj)
                bulk_tp.append(row["track_points"])

            objs = ContainerUnloadFact.objects.bulk_create(bulk_obj)

            ThroughModel = ContainerUnloadFact.track_points.through

            bulk_tr = [ThroughModel(flattablerow_id=tp.id,
                                    containerunloadfact_id=item.pk)
                       for i, item in enumerate(objs)
                       for tp in bulk_tp[i]
                       if item and tp]
            ThroughModel.objects.bulk_create(bulk_tr)

        application = validated_data.get('application', None)
        if application and date:
            bulk_obj = []
            bulk_tp = []

            for row in application_parser.parse(application,
                                                syncdate[0].datetime,
                                                device,
                                                container_types):
                obj = ContainerUnloadFact(report=report,
                                          geozone=row["geozone"],
                                          datetime_entry=row["time_in"],
                                          datetime_exit=row["time_out"],
                                          is_unloaded=row["is_unloaded"],
                                          value=row["value"],
                                          container_type=row["ct_type"],
                                          directory=row["directory"],
                                          count=row["count"],
                                          nav_mt_id=row["nav_mt_id"])
                bulk_obj.append(obj)
                bulk_tp.append(row["track_points"])

            objs = ContainerUnloadFact.objects.bulk_create(bulk_obj)

            ThroughModel = ContainerUnloadFact.track_points.through

            bulk_tr = [ThroughModel(flattablerow_id=tp.id,
                                    containerunloadfact_id=item.pk)
                       for i, item in enumerate(objs)
                       for tp in bulk_tp[i]
                       if item and tp]
            ThroughModel.objects.bulk_create(bulk_tr)

        return report


class ContainerUnloadFactSerializer(serializers.ModelSerializer):
    track_points = FlatRowSerializer(many=True, read_only=True)
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
            'nav_mt_id',
        )


class ContainerTypeListSerializer(serializers.ModelSerializer):
    text = SerializerMethodField()

    def get_text(self, obj):
        return obj.__str__()

    class Meta:
        model = ContainerType
        fields = ('id', 'text')


def check_syncdate(syncdate, ch_date):
    return (syncdate.year == ch_date.year) and \
        (syncdate.month == ch_date.month) and \
        (syncdate.day == ch_date.day)
