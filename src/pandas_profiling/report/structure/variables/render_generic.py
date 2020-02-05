from pandas_profiling.report.presentation.core import Overview, Table, Sequence, HTML
from pandas_profiling.report.structure.variables import render_common
from pandas_profiling.utils.l10n import gettext as _


def render_generic(summary):
    template_variables = {}  # render_common(summary)

    info = Overview(
        anchor_id=summary["varid"],
        warnings=summary["warnings"],
        var_type=_("Unsupported"),
        var_name=summary["varname"],
    )

    table = Table(
        [
            {
                "name": _("Missing"),
                "value": summary["n_missing"],
                "fmt": "fmt",
                "class": "alert" if "n_missing" in summary["warn_fields"] else "",
            },
            {
                "name": _("Missing (%)"),
                "value": summary["p_missing"],
                "fmt": "fmt_percent",
                "class": "alert" if "p_missing" in summary["warn_fields"] else "",
            },
            {
                "name": _("Memory size"),
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
            },
        ]
    )

    return {
        "top": Sequence([info, table, HTML("")], sequence_type="grid"),
        "bottom": None,
    }

    # Add class Ignore
    # return {
    #     "top": HTML("Unsupported"),
    #     "bottom": HTML("")
    # }

    # <div class="row variable ignore"><div class="col-sm-3"><p class="h4" title="device_browserSize">device_browserSize<br><small>Constant</small></p></div><div class="col-sm-3"><p><em>This variable is constant and should be ignored for analysis</em></p></div><div class="col-sm-6"><table class="stats "><tbody><tr><th>Constant value</th><td>not available in demo dataset</td></tr></tbody></table></div></div>
