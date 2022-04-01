import django_settings
from common.models import Species

import csv


def float_or_none(val, default=None):
    """

    Arguments:
    - `x`:
    """
    if val is None:
        return default
    else:
        try:
            ret = float(val)
        except ValueError:
            ret = default
        return ret


# attrs = Species.objects.values_list(
#     "spc",
#     "flen_min",
#     "flen_max",
#     "tlen_min",
#     "tlen_max",
#     "rwt_min",
#     "rwt_max",
#     "k_min_error",
#     "k_min_warn",
#     "k_max_error",
#     "k_max_warn",
#     "flen2tlen_alpha",
#     "flen2tlen_beta",
# )


# with open("spc_attrs.csv", mode="w") as csvfile:
#     csvwriter = csv.writer(
#         csvfile, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL
#     )
#     for attr in attrs:
#         csvwriter.writerow(attr)


with open("spc_attrs.csv", mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",", quotechar='"')
    for row in csv_reader:
        if len(row):
            spc = row[0]
            Species.objects.filter(spc=spc).update(
                flen_min=float_or_none(row[1]),
                flen_max=float_or_none(row[2]),
                tlen_min=float_or_none(row[3]),
                tlen_max=float_or_none(row[4]),
                rwt_min=float_or_none(row[5]),
                rwt_max=float_or_none(row[6]),
                k_min_error=float_or_none(row[7]),
                k_min_warn=float_or_none(row[8]),
                k_max_error=float_or_none(row[9]),
                k_max_warn=float_or_none(row[10]),
                flen2tlen_alpha=float_or_none(row[11]),
                flen2tlen_beta=float_or_none(row[12]),
            )
print("Done!")
