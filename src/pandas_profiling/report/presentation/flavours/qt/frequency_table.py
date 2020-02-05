from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core.frequency_table import FrequencyTable
from pandas_profiling.utils.l10n import gettext as _


class QtFrequencyTable(FrequencyTable):
    def render(self):
        return QPushButton(_("Frequency Table"))
