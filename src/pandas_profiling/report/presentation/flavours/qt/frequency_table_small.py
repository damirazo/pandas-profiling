from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core.frequency_table_small import (
    FrequencyTableSmall,
)
from pandas_profiling.utils.l10n import gettext as _


class QtFrequencyTableSmall(FrequencyTableSmall):
    def render(self):
        return QPushButton(_("Small Frequency Table"))
