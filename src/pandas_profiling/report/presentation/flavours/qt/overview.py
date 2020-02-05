from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core.overview import Overview
from pandas_profiling.utils.l10n import gettext as _


class QtOverview(Overview):
    def render(self):
        return QPushButton(_("PyQt5 button"))
