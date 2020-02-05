from pandas_profiling.config import config
from pandas_profiling.report.formatters import fmt_array
from pandas_profiling.visualisation.plot import mini_histogram, histogram
from pandas_profiling.report.presentation.core import (
    Table,
    Sequence,
    Image,
    Preview,
    FrequencyTable,
    Overview,
)
from pandas_profiling.report.structure.variables.render_common import render_common
from pandas_profiling.utils.l10n import gettext as _


def render_real(summary):
    template_variables = render_common(summary)
    image_format = config["plot"]["image_format"].get(str)

    if summary["min"] >= 0:
        name = _("Real number (&Ropf;<sub>&ge;0</sub>)")
    else:
        name = _("Real number (&Ropf;)")

    # Top
    info = Overview(summary["varid"], summary["varname"], name, summary["warnings"])

    table1 = Table(
        [
            {
                "name": _("Distinct count"),
                "value": summary["n_unique"],
                "fmt": "fmt",
                "class": "alert" if "n_unique" in summary["warn_fields"] else "",
            },
            {
                "name": _("Unique (%)"),
                "value": summary["p_unique"],
                "fmt": "fmt_percent",
                "class": "alert" if "p_unique" in summary["warn_fields"] else "",
            },
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
                "name": _("Infinite"),
                "value": summary["n_infinite"],
                "fmt": "fmt",
                "class": "alert" if "n_infinite" in summary["warn_fields"] else "",
            },
            {
                "name": _("Infinite (%)"),
                "value": summary["p_infinite"],
                "fmt": "fmt_percent",
                "class": "alert" if "p_infinite" in summary["warn_fields"] else "",
            },
        ]
    )

    table2 = Table(
        [
            {"name": _("Mean"), "value": summary["mean"], "fmt": "fmt"},
            {"name": _("Minimum"), "value": summary["min"], "fmt": "fmt"},
            {"name": _("Maximum"), "value": summary["max"], "fmt": "fmt"},
            {
                "name": _("Zeros"),
                "value": summary["n_zeros"],
                "fmt": "fmt",
                "class": "alert" if "n_zeros" in summary["warn_fields"] else "",
            },
            {
                "name": _("Zeros (%)"),
                "value": summary["p_zeros"],
                "fmt": "fmt_percent",
                "class": "alert" if "p_zeros" in summary["warn_fields"] else "",
            },
            {
                "name": _("Memory size"),
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
            },
        ]
    )

    histogram_bins = 10

    # TODO: replace with SmallImage...
    mini_histo = Image(
        mini_histogram(summary["histogram_data"], summary, histogram_bins),
        image_format=image_format,
        alt=_("Mini histogram"),
    )

    template_variables["top"] = Sequence(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    quantile_statistics = Table(
        [
            {"name": _("Minimum"), "value": summary["min"], "fmt": "fmt_numeric"},
            {"name": _("5-th percentile"), "value": summary["5%"], "fmt": "fmt_numeric"},
            {"name": _("Q1"), "value": summary["25%"], "fmt": "fmt_numeric"},
            {"name": _("median"), "value": summary["50%"], "fmt": "fmt_numeric"},
            {"name": _("Q3"), "value": summary["75%"], "fmt": "fmt_numeric"},
            {"name": _("95-th percentile"), "value": summary["95%"], "fmt": "fmt_numeric"},
            {"name": _("Maximum"), "value": summary["max"], "fmt": "fmt_numeric"},
            {"name": _("Range"), "value": summary["range"], "fmt": "fmt_numeric"},
            {
                "name": _("Interquartile range (IQR)"),
                "value": summary["iqr"],
                "fmt": "fmt_numeric",
            },
        ],
        name=_("Quantile statistics"),
    )

    descriptive_statistics = Table(
        [
            {
                "name": _("Standard deviation"),
                "value": summary["std"],
                "fmt": "fmt_numeric",
            },
            {
                "name": _("Coefficient of variation (CV)"),
                "value": summary["cv"],
                "fmt": "fmt_numeric",
            },
            {"name": _("Kurtosis"), "value": summary["kurtosis"], "fmt": "fmt_numeric"},
            {"name": "Mean", "value": summary["mean"], "fmt": "fmt_numeric"},
            {
                "name": _("Median Absolute Deviation (MAD)"),
                "value": summary["mad"],
                "fmt": "fmt_numeric",
            },
            {
                "name": _("Skewness"),
                "value": summary["skewness"],
                "fmt": "fmt_numeric",
                "class": "alert" if "skewness" in summary["warn_fields"] else "",
            },
            {"name": _("Sum"), "value": summary["sum"], "fmt": "fmt_numeric"},
            {"name": _("Variance"), "value": summary["variance"], "fmt": "fmt_numeric"},
        ],
        name=_("Descriptive statistics"),
    )

    statistics = Sequence(
        [quantile_statistics, descriptive_statistics],
        anchor_id="{varid}statistics".format(varid=summary["varid"]),
        name=_("Statistics"),
        sequence_type="grid",
    )

    seqs = [
        Image(
            histogram(summary["histogram_data"], summary, histogram_bins),
            image_format=image_format,
            alt=_("Histogram"),
            caption=_(
                "<strong>Histogram with fixed size bins</strong> (bins={})"
            ).format(histogram_bins),
            name=_("Histogram"),
            anchor_id="{varid}histogram".format(varid=summary["varid"]),
        )
    ]

    fq = FrequencyTable(
        template_variables["freq_table_rows"],
        name=_("Common values"),
        anchor_id="{varid}common_values".format(varid=summary["varid"]),
    )

    evs = Sequence(
        [
            FrequencyTable(
                template_variables["firstn_expanded"],
                name=_("Minimum 5 values"),
                anchor_id="{varid}firstn".format(varid=summary["varid"]),
            ),
            FrequencyTable(
                template_variables["lastn_expanded"],
                name=_("Maximum 5 values"),
                anchor_id="{varid}lastn".format(varid=summary["varid"]),
            ),
        ],
        sequence_type="tabs",
        name=_("Extreme values"),
        anchor_id="{varid}extreme_values".format(varid=summary["varid"]),
    )

    if "histogram_bins_bayesian_blocks" in summary:
        histo_dyn = Image(
            histogram(
                summary["histogram_data"],
                summary,
                summary["histogram_bins_bayesian_blocks"],
            ),
            image_format=image_format,
            alt=_("Histogram"),
            caption=_(
                '<strong>Histogram with variable size bins</strong> '
                '(bins={}, <a href="https://ui.adsabs.harvard.edu/abs/2013ApJ...764..167S/abstract" '
                'target="_blank">"bayesian blocks"</a> binning strategy used)').format(
                fmt_array(summary["histogram_bins_bayesian_blocks"], threshold=5)
            ),
            name=_("Dynamic Histogram"),
            anchor_id="{varid}dynamic_histogram".format(varid=summary["varid"]),
        )

        seqs.append(histo_dyn)

    template_variables["bottom"] = Sequence(
        [
            statistics,
            Sequence(
                seqs,
                sequence_type="tabs",
                name=_("Histogram(s)"),
                anchor_id="{varid}histograms".format(varid=summary["varid"]),
            ),
            fq,
            evs,
        ],
        sequence_type="tabs",
        anchor_id="{varid}bottom".format(varid=summary["varid"]),
    )

    return template_variables
