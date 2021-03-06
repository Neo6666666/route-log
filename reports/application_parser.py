import xlrd
from nav_client.models import FlatTableRow, GeoZone, SyncDate
from . import attachment_parser as ap
from reports.models import ContainerType


def parse(file, date, device, container_types):
    types = []
    for ctype in container_types:
        tmp = ContainerType.objects.get(pk=int(ctype))
        types.append((tmp.volume, tmp.name))

    sync_date = SyncDate.objects.filter(datetime__year=date.year,
                                        datetime__month=date.month,
                                        datetime__day=date.day).first()
    all_flats = [x for x in FlatTableRow.objects
                 .filter(device=device, sync_date=sync_date)
                 .prefetch_related('point_value')]

    worksheet = xlrd.open_workbook(file_contents=file.read()).sheet_by_index(0)

    cc = 0
    for row in worksheet.get_rows():
        if cc == 0:
            cc += 1
            continue

        mt_id = int(row[4].value)
        # TODO: compare geozone.name and geozone_name
        # geozone_name = str(row[5].value)

        row7 = str(row[7].value).split(' ')
        fl = True
        for ctype in types:
            if ctype[0] == row7[0] and ctype[1] == row7[1]:
                fl = False

        if fl:
            continue

        count = int(row[8].value)
        # TODO: compare est_total_volume and fact_total_volume
        # est_total_volume = float(row[9].value)

        geozone = GeoZone.objects.filter(
            sync_date=sync_date, mt_id=mt_id).first()

        if geozone is None:
            continue

        report_row = {}
        report_row["nav_mt_id"] = geozone.mt_id
        report_row["directory"] = geozone.name
        report_row["geozone"] = geozone
        report_points = [x for x in geozone.points.all()]

        report_row["count"] = count
        report_row["value"] = row7[0]
        report_row["ct_type"] = row7[1]

        report_row["time_in"] = None
        report_row["time_out"] = None
        report_row["is_unloaded"] = False

        big_range = 500
        small_range = 50
        center = ap.get_center(report_points)
        current_flats = [flat for flat in all_flats
                         if ap.in_range(flat.point_value, big_range, center)]

        if current_flats:
            current_flats.sort(key=lambda x: x.utc)
            for flat in current_flats:
                if ap.in_range(flat.point_value, small_range, center):
                    if report_row["time_in"] is None:
                        report_row["time_in"] = flat.utc
                    report_row["time_out"] = flat.utc

            if ap.check_unloaded(report_row):
                report_row["is_unloaded"] = True

        report_row["track_points"] = current_flats
        yield report_row
