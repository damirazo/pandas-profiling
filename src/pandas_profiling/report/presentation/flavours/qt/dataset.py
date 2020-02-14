from PyQt5.QtWidgets import QPushButton

from pandas_profiling.report.presentation.core import Dataset
from pandas_profiling.utils.l10n import gettext as _


class QtDataset(Dataset):
    def render(self):
        return QPushButton(_("PyQt5 button"))
