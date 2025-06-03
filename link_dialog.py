from PyQt5 import QtWidgets, QtCore
from lang import tr


class URLDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(URLDialog, self).__init__(parent)
        self.resize(260, 160)
        self.setWindowTitle(tr("URLDialogTitle"))
        self.lo = QtWidgets.QVBoxLayout(self)
        self.e_title = QtWidgets.QLineEdit(self)
        self.e_title.setPlaceholderText(tr("url_dialog_title"))
        self.e_url = QtWidgets.QLineEdit(self)
        self.e_url.setPlaceholderText(tr("url_dialog_url"))

        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.lo.addWidget(self.e_title)
        self.lo.addWidget(self.e_url)
        self.lo.addWidget(self.buttonBox)


def show_url_dialog(parent):
    dlg = URLDialog(parent)
    if dlg.exec() == 1:
        title = dlg.e_title.text()
        url = dlg.e_url.text()
        if not title or not url:
            QtWidgets.QMessageBox.warning(parent, tr("error"), tr("empty_title_or_url"))
            return None, None
        else: return title, url
    return None, None
