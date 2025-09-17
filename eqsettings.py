from PySide6 import QtWidgets
from eqsettingsui import Ui_Dialog


class EQSettingsDialog(QtWidgets.QDialog):
    def __init__(self, parent, freq_l, bandwidth_l):
        super(EQSettingsDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        for i in range(len(self.ui.grid_components)):
            e_freq: QtWidgets.QLineEdit = self.ui.grid_components[i][1]
            e_bw: QtWidgets.QLineEdit = self.ui.grid_components[i][2]
            if i < len(freq_l):
                e_freq.setText(str(freq_l[i]))
            if i < len(bandwidth_l):
                e_bw.setText(str(bandwidth_l[i]))
        self.ui.l_close.onClick.connect(self.reject)

    def do_move(self, x, y):
        self.move(x, y)


def show_eq_settings(parent, freq_l, bandwidth_l):
    result = []
    dlg = EQSettingsDialog(parent, freq_l, bandwidth_l)
    if dlg.exec() == 1:
        for i in range(len(dlg.ui.grid_components)):
            e_freq: QtWidgets.QLineEdit = dlg.ui.grid_components[i][1]
            e_bw: QtWidgets.QLineEdit = dlg.ui.grid_components[i][2]
            result.append((int(e_freq.text()), int(e_bw.text())))
    return result
