from PyQt5 import QtCore, QtWidgets, QtGui
from file_dialog_ui import Ui_FileDialog
import os
from lang import tr


def get_windows_drives():
    drives = []
    for letter in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(drive)
    return drives


def get_computer_roots():
    if os.name == 'posix':  # Linux, macOS
        return ["/"]
    elif os.name == 'nt':   # Windows
        return get_windows_drives()
    else:
        return []


def list_files_and_dirs(directory, filter=''):
    entries = []
    if not os.path.isdir(directory):
        return entries
    exts = [ext.strip().replace('*', '')  for ext in filter.split(',')]
    try:
        files = os.listdir(directory)
    except Exception as e:
        print(str(e))
        return entries
    for name in os.listdir(directory):
        full_path = os.path.join(directory, name)
        is_dir = os.path.isdir(full_path)
        if filter and not is_dir:
            ext = os.path.splitext(name)[1]
            if ext in exts:
                entries.append((name, is_dir))
        else:
            entries.append((name, is_dir))
    entries.sort(key=lambda x: (-x[1], x[0]))
    return entries


def add_dir_to_cb(model, dir):
    model.appendRow(QtGui.QStandardItem(dir))
    if len(dir) > 1:
        d = os.path.dirname(dir)
        if d != dir:
            add_dir_to_cb(model, d)


class FileDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, filters=[], default_path=''):
        super(FileDialog, self).__init__(parent)
        self.ui = Ui_FileDialog()
        self.ui.setupUi(self)
        self.home_dir = os.path.expanduser('~')
        self.current_directory = default_path if len(default_path) > 0 else self.home_dir
        self.recent = []
        self.places = [(tr('computer'), get_computer_roots()), (tr('home'), [self.home_dir])]
        self.cb_model = QtGui.QStandardItemModel()
        self.filenames = []
        self.ui.cb.setModel(self.cb_model)
        self.filters = filters
        if len(filters) > 0:
            for filter in filters:
                txt = filter[0]+' ('+filter[1]+')'
                self.ui.cb_file_type.addItem(txt)
        self.update_dir()

        if os.path.isdir(os.path.join(self.home_dir, 'Desktop')):
            self.places.append((tr('desktop'), [os.path.join(self.home_dir, 'Desktop')]))
        if os.path.isdir(os.path.join(self.home_dir, 'Рабочий стол')):
            self.places.append((tr('desktop'), [os.path.join(self.home_dir, 'Рабочий стол')]))
        if os.path.isdir(os.path.join(self.home_dir, 'Downloads')):
            self.places.append((tr('downloads'), [os.path.join(self.home_dir, 'Downloads')]))
        if os.path.isdir(os.path.join(self.home_dir, 'Загрузки')):
            self.places.append((tr('downloads'), [os.path.join(self.home_dir, 'Загрузки')]))
        if os.path.isdir(os.path.join(self.home_dir, 'Music')):
            self.places.append((tr('music'), [os.path.join(self.home_dir, 'Music')]))
        if os.path.isdir(os.path.join(self.home_dir, 'Музыка')):
            self.places.append((tr('music'), [os.path.join(self.home_dir, 'Музыка')]))
        for i in range(len(self.places)):
            item = QtWidgets.QListWidgetItem(self.places[i][0])
            item.place = self.places[i]
            if i == 0:
                item.setIcon(QtGui.QIcon(':/images/computer.png'))
            else:
                item.setIcon(QtGui.QIcon(':/images/folder.png'))
            self.ui.lw_places.addItem(item)
        self.ui.cb.activated.connect(self.cb_activated)
        self.ui.lw_places.currentItemChanged.connect(self.lw_places_item_changed)
        self.ui.cb_file_type.currentIndexChanged.connect(self.cb_file_type_index_changed)
        self.ui.listWidget.doubleClicked.connect(self.list_double_click)
        self.ui.listWidget.currentItemChanged.connect(self.list_item_changed)
        self.ui.bUp.clicked.connect(self.up_clicked)

    def update_dir(self, directory=''):
        d = directory if len(directory) > 0 and os.path.isdir(directory) else self.current_directory
        if d != self.current_directory:
            self.current_directory = d
            if d not in self.recent:
                self.recent.insert(0, d)
        self.ui.cb.clear()
        self.cb_model.clear()
        add_dir_to_cb(self.cb_model, d)
        if len(self.recent) > 0:
            item = QtGui.QStandardItem(tr('recent_places'))
            item.setFlags(QtCore.Qt.NoItemFlags)
            self.cb_model.appendRow(item)
            # self.ui.cb.addItem(tr('recent_places'))
            for line in self.recent:
               self.cb_model.appendRow(QtGui.QStandardItem(line))
        filter = ''
        if len(self.filters) > 0:
            filter = self.filters[self.ui.cb_file_type.currentIndex()][1]
        print('update_dir:', self.current_directory)
        files = list_files_and_dirs(self.current_directory, filter)
        self.ui.listWidget.clear()
        for file in files:
            if file[0].startswith('.'): continue
            item = QtWidgets.QListWidgetItem(file[0])
            item.is_folder = file[1]
            if file[1]:
                item.setIcon(QtGui.QIcon(':/images/folder.png'))
            else:
                item.setIcon(QtGui.QIcon(':/images/playlist_icon.png'))
            self.ui.listWidget.addItem(item)

    def accept(self):
        items = self.ui.listWidget.selectedItems()
        cnt = len(items)
        if cnt == 0: return
        if cnt == 1:
            if items[0].is_folder:
                self.update_dir(os.path.join(self.current_directory, items[0].text()))
                return
            self.filenames.append(os.path.join(self.current_directory, items[0].text()))
            super(FileDialog, self).accept()
        else:
            for item in items:
                if not item.is_folder:
                    self.filenames.append(os.path.join(self.current_directory, item.text()))
            if len(self.filenames) > 0:
                super(FileDialog, self).accept()

    def cb_activated(self, index):
        item = self.ui.cb.itemText(index)
        if item != self.current_directory:
            self.update_dir(item)

    def up_clicked(self):
        if len(self.current_directory) > 1:
            d = os.path.dirname(self.current_directory)
            if d != self.current_directory:
                self.update_dir(d)

    def cb_file_type_index_changed(self, index):
        if len(self.filters) <= 1: return
        self.update_dir()

    def lw_places_item_changed(self, current, previous):
        place = current.place
        if len(place[1]) > 1:
            self.ui.listWidget.clear()
            for fn in place[1]:
                item = QtWidgets.QListWidgetItem(fn)
                item.is_folder = True
                item.setIcon(QtGui.QIcon(':/images/folder.png'))
                self.ui.listWidget.addItem(item)
        else:
            self.update_dir(place[1][0])

    def list_item_changed(self, current, previous):
        if current is None:
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Open).setEnabled(False)
            self.ui.e_file_name.setText('')
        else:
            if not current.is_folder:
                self.ui.e_file_name.setText(current.text())
            self.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Open).setEnabled(True)

    def list_double_click(self, index: QtCore.QModelIndex):
        item = self.ui.listWidget.item(index.row())
        if item.is_folder:
            self.update_dir(os.path.join(self.current_directory, item.text()))

    @staticmethod
    def select_file(parent=None, filters=None):
        if filters is None:
            filters = []
        dlg = FileDialog(parent=parent, filters=filters)
        if dlg.exec() == 1:
            return dlg.filenames, dlg.ui.cb_file_type.currentIndex()
        else:
            return [], 0

def main():
    import images_rc
    app = QtWidgets.QApplication([])
    if not os.path.isfile('style.qss'):
        print('file of style.qss is not found')
        return 1
    with open('style.qss') as f:
        style = f.read()
        app.setStyleSheet(style)
    ok, filenames = FileDialog.select_file(filters=[('MUSIC', '*.mp3, *.wma, *.wav, *.aac'), ('PlayList', '*.m3u, *.m3u8')])
    print(ok, filenames)
    app.quit()


if __name__ == "__main__":
    main()
