from pandas_profiling.config import config
from pandas_profiling.visualisation.plot import mini_histogram, histogram
from pandas_profiling.report.presentation.core import (
    Image,
    Preview,
    Sequence,
    Table,
    Overview,
)
from pandas_profiling.utils.l10n import gettext as _


def render_date(summary):
    # TODO: render common?
    template_variables = {}

    image_format = config["plot"]["image_format"].get(str)

    # Top
    info = Overview(summary["varid"], summary["varname"], "Date", [])

    table1 = Table(
        [
            {"name": _("Distinct count"), "value": summary["n_unique"], "fmt": "fmt"},
            {"name": _("Unique (%)"), "value": summary["p_unique"], "fmt": "fmt_percent"},
            {"name": _("Missing"), "value": summary["n_missing"], "fmt": "fmt"},
            {
                "name": _("Missing (%)"),
                "value": summary["p_missing"],
                "fmt": "fmt_percent",
            },
            {
                "name": _("Memory size"),
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
            },
        ]
    )

    table2 = Table(
        [
            {"name": _("Minimum"), "value": summary["min"], "fmt": "fmt"},
            {"name": _("Maximum"), "value": summary["max"], "fmt": "fmt"},
            # {'name': '', 'value': '', 'fmt': 'fmt'},
            # {'name': '', 'value': '', 'fmt': 'fmt'},
            # {'name': '', 'value': '', 'fmt': 'fmt'},
            # {'name': '', 'value': '', 'fmt': 'fmt'},
        ]
    )

    mini_histo = Image(
        mini_histogram(summary["histogram_data"], summary, summary["histogram_bins"]),
        image_format=image_format,
        alt=_("Mini histogram"),
    )

    template_variables["top"] = Sequence(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    # Bottom
    bottom = Sequence(
        [
            Image(
                histogram(
                    summary["histogram_data"], summary, summary["histogram_bins"]
                ),
                image_format=image_format,
                alt=_("Histogram"),
                caption=_("Histogram"),
                name=_("Histogram"),
                anchor_id="{varid}histogram".format(varid=summary["varid"]),
            )
        ],
        sequence_type="tabs",
        anchor_id=summary["varid"],
    )

    template_variables["bottom"] = bottom

    return template_variables
