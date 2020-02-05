from pandas_profiling.config import config
from pandas_profiling.report.formatters import fmt_array
from pandas_profiling.visualisation.plot import mini_histogram, histogram
from pandas_profiling.report.presentation.core import (
    FrequencyTable,
    Sequence,
    Image,
    Preview,
    Table,
    Overview,
)
from pandas_profiling.report.structure.variables.render_common import render_common
from pandas_profiling.utils.l10n import gettext as _


def render_count(summary):
    template_variables = render_common(summary)
    image_format = config["plot"]["image_format"].get(str)

    # Top
    info = Overview(
        summary["varid"],
        summary["varname"],
        _("Real number") + " (&Ropf; / &Ropf;<sub>&ge;0</sub>)",
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
            # {'name': 'Infinite', 'value': summary['n_infinite'], 'fmt': 'fmt'},
            # {'name': 'Infinite (%)', 'value': summary['p_infinite'], 'fmt': 'fmt_percent'},
        ]
    )

    table2 = Table(
        [
            {"name": _("Mean"), "value": summary["mean"], "fmt": "fmt"},
            {"name": _("Minimum"), "value": summary["min"], "fmt": "fmt"},
            {"name": _("Maximum"), "value": summary["max"], "fmt": "fmt"},
            {"name": _("Zeros"), "value": summary["n_zeros"], "fmt": "fmt"},
            {"name": _("Zeros (%)"), "value": summary["p_zeros"], "fmt": "fmt_percent"},
            {
                "name": _("Memory size"),
                "value": summary["memory_size"],
                "fmt": "fmt_bytesize",
            },
        ]
    )

    # TODO: replace with SmallImage...
    mini_histo = Image(
        mini_histogram(summary["histogram_data"], summary, summary["histogram_bins"]),
        image_format=image_format,
        alt=_("Mini histogram"),
    )

    template_variables["top"] = Sequence(
        [info, table1, table2, mini_histo], sequence_type="grid"
    )

    quantile_statistics = {
        "name": _("Quantile statistics"),
        "items": [
            {"name": _("Minimum"), "value": summary["min"], "fmt": "fmt_numeric"},
            {
                "name": _("5-th percentile"),
                "value": summary["quantile_5"],
                "fmt": "fmt_numeric",
            },
            {"name": _("Q1"), "value": summary["quantile_25"], "fmt": "fmt_numeric"},
            {"name": _("median"), "value": summary["quantile_50"], "fmt": "fmt_numeric"},
            {"name": _("Q3"), "value": summary["quantile_75"], "fmt": "fmt_numeric"},
            {
                "name": _("95-th percentile"),
                "value": summary["quantile_95"],
                "fmt": "fmt_numeric",
            },
            {"name": _("Maximum"), "value": summary["max"], "fmt": "fmt_numeric"},
            {"name": _("Range"), "value": summary["range"], "fmt": "fmt_numeric"},
            {
                "name": _("Interquartile range"),
                "value": summary["iqr"],
                "fmt": "fmt_numeric",
            },
        ],
    }

    descriptive_statistics = {
        "name": _("Descriptive statistics"),
        "items": [
            {
                "name": _("Standard deviation"),
                "value": summary["std"],
                "fmt": "fmt_numeric",
            },
            {
                "name": _("Coefficient of variation"),
                "value": summary["cv"],
                "fmt": "fmt_numeric",
            },
            {"name": _("Kurtosis"), "value": summary["kurt"], "fmt": "fmt_numeric"},
            {"name": _("Mean"), "value": summary["mean"], "fmt": "fmt_numeric"},
            {"name": _("MAD"), "value": summary["mad"], "fmt": "fmt_numeric"},
            {"name": _("Skewness"), "value": summary["skew"], "fmt": "fmt_numeric"},
            {"name": _("Sum"), "value": summary["sum"], "fmt": "fmt_numeric"},
            {"name": _("Variance"), "value": summary["var"], "fmt": "fmt_numeric"},
        ],
    }

    # TODO: Make sections data structure
    # statistics = ItemRenderer(
    #     'statistics',
    #     'Statistics',
    #     'table',
    #     [
    #         quantile_statistics,
    #         descriptive_statistics
    #     ]
    # )

    seqs = [
        Image(
            histogram(summary["histogram_data"], summary, summary["histogram_bins"]),
            image_format=image_format,
            alt=_("Histogram"),
            caption=(
                "<strong>"
                + _("Histogram with fixed size bins")
                + "</strong> ("
                + _("bins")
                + "={})"
            ).format(summary["histogram_bins"]),
            name=_("Histogram"),
            anchor_id="histogram",
        )
    ]

    fq = FrequencyTable(
        template_variables["freq_table_rows"],
        name=_("Common values"),
        anchor_id="common_values",
    )

    evs = Sequence(
        [
            FrequencyTable(
                template_variables["firstn_expanded"],
                name=_("Minimum 5 values"),
                anchor_id="firstn",
            ),
            FrequencyTable(
                template_variables["lastn_expanded"],
                name=_("Maximum 5 values"),
                anchor_id="lastn",
            ),
        ],
        sequence_type="tabs",
        name=_("Extreme values"),
        anchor_id="extreme_values",
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
                '(bins={}, <a href="https://ui.adsabs.harvard.edu/abs/2013ApJ..'
                '.764..167S/abstract" target="_blank">"bayesian blocks"</a> '
                'binning strategy used)'
            ).format(fmt_array(summary["histogram_bins_bayesian_blocks"], threshold=5)),
            name=_("Dynamic Histogram"),
            anchor_id="dynamic_histogram",
        )

        seqs.append(histo_dyn)

    template_variables["bottom"] = Sequence(
        [
            # statistics,
            Sequence(
                seqs, sequence_type="tabs", name=_("Histogram(s)"), anchor_id="histograms"
            ),
            fq,
            evs,
        ],
        sequence_type="tabs",
        anchor_id=summary["varid"],
    )

    return template_variables
