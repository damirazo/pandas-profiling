from pandas_profiling.config import config
from pandas_profiling.visualisation.plot import scatter_complex
from pandas_profiling.report.presentation.core import (
    HTML,
    Image,
    Preview,
    Sequence,
    Table,
    Overview,
)
from pandas_profiling.utils.l10n import gettext as _


def render_complex(summary):
    template_variables = {}
    image_format = config["plot"]["image_format"].get(str)

    # Top
    info = Overview(
        summary["varid"],
        summary["varname"],
        _("Complex number (&Copf;)"),
        summary["warnings"],
    )

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
            {"name": _("Mean"), "value": summary["mean"], "fmt": "fmt"},
            {"name": _("Minimum"), "value": summary["min"], "fmt": "fmt"},
            {"name": _("Maximum"), "value": summary["max"], "fmt": "fmt"},
            {"name": _("Zeros"), "value": summary["n_zeros"], "fmt": "fmt"},
            {"name": _("Zeros (%)"), "value": summary["p_zeros"], "fmt": "fmt_percent"},
        ]
    )

    placeholder = HTML("")

    template_variables["top"] = Sequence(
        [info, table1, table2, placeholder], sequence_type="grid"
    )

    # Bottom
    items = [
        Image(
            scatter_complex(summary["scatter_data"]),
            image_format=image_format,
            alt=_("Scatterplot"),
            caption=_("Scatterplot in the complex plane"),
            name=_("Scatter"),
            anchor_id="{varid}scatter".format(varid=summary["varid"]),
        )
    ]

    bottom = Sequence(items, sequence_type="tabs", anchor_id=summary["varid"])

    template_variables["bottom"] = bottom

    return template_variables
