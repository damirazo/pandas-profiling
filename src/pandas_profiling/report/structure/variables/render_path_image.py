from pandas_profiling.config import config
from pandas_profiling.report.presentation.frequency_table_utils import freq_table
from pandas_profiling.visualisation.plot import histogram, scatter_series
from pandas_profiling.report.presentation.core import FrequencyTable, Image, Sequence
from pandas_profiling.report.structure.variables.render_path import render_path
from pandas_profiling.utils.l10n import gettext as _


def render_path_image(summary):
    n_freq_table_max = config["n_freq_table_max"].get(int)
    image_format = config["plot"]["image_format"].get(str)

    template_variables = render_path(summary)

    # Top
    template_variables["top"].content["items"][0].content["var_type"] = _(
        "Image Path")

    # Bottom
    keys = {_("Image shape"): "image_shape", _("Exif keys"): "exif_keys"}

    for title, key in keys.items():
        template_variables["freqtable_{}".format(key)] = freq_table(
            freqtable=summary["{}_counts".format(key)],
            n=summary["n"],
            max_number_to_print=n_freq_table_max,
        )

    # TODO: add dropdown to switch to specific values
    exif_keys = FrequencyTable(
        template_variables["freqtable_{}".format("exif_keys")],
        name=_("Exif keys"),
        anchor_id="{varid}exif_frequency".format(varid=summary["varid"]),
    )

    template_variables["bottom"].content["items"].append(exif_keys)

    image_shape_freq = FrequencyTable(
        template_variables["freqtable_{}".format("image_shape")],
        name=_("Frequency"),
        anchor_id="{varid}image_shape_frequency".format(varid=summary["varid"]),
    )

    image_shape_scatter = Image(
        scatter_series(summary["scatter_data"]),
        image_format=image_format,
        alt=_("Scatterplot of image sizes"),
        caption=_("Scatterplot of image sizes"),
        name=_("Scatter"),
        anchor_id="{varid}scatter".format(varid=summary["varid"]),
    )

    image_shape = Sequence(
        [image_shape_freq, image_shape_scatter],
        sequence_type="tabs",
        name=_("Image shape"),
        anchor_id="{varid}image_shape".format(varid=summary["varid"]),
    )

    template_variables["bottom"].content["items"].append(image_shape)

    return template_variables
