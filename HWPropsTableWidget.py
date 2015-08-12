from Qt import QtGui, QtCore, loadUi
from QtCore import Slot

from Autoconfig import Autoconfig, natural_sortkey

class HWPropsTableWidget(QtGui.QTableWidget):
    def __init__(self, parent=None):
        print("HWPropsTableWidget.__init__()")
        super().__init__(0, 2, parent)
        self.horizontalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.verticalHeader().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        self.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header = self.verticalHeader()
        header.setVisible(False)
        self.labels = ["Hardware Property", "Value"]
        self.setHorizontalHeaderLabels(self.labels)
        self.adjustSize()

    def set_props(self, props, storage={}):
        print("HWPropsTableWidget.set_props({0})".format(props))
        self.clearContents()
        self.setRowCount(0)
        storage.clear()
        row = 0
        for key in Autoconfig.KEYS:
            if key in props:
                self.insertRow(row)
                w = QtGui.QTableWidgetItem(key)
                self.setItem(row, 0, w)
                val = props[key]
                try:
                    (default, vals) = val
                    storage[key] = default
                    w = QtGui.QComboBox()
                    w.addItem("<unset>")
                    w.addItems(list(vals))
                    index = w.findText(default)
                    w.setCurrentIndex(index)
                    self.setCellWidget(row, 1, w)
                    w.currentIndexChanged[str].connect(lambda text, storage=storage, key=key: self.prop_changed(storage, key, text))
                except  ValueError:
                    storage[key] = val
                    w = QtGui.QTableWidgetItem(props[key])
                    self.setItem(row, 1, w)
                row += 1
        keys = list(props.keys())
        keys.sort(key = natural_sortkey)
        for key in keys:
            if key in Autoconfig.KEYS:
                continue
            self.insertRow(row)
            w = QtGui.QTableWidgetItem(key)
            self.setItem(row, 0, w)
            w = QtGui.QTableWidgetItem(props[key])
            self.setItem(row, 1, w)
            row += 1
        self.resize_table()

    def prop_changed(self, props, key, val):
        print("HWPropsTableWidget.prop_changed({0} = {1})".format(key, val))
        if val == "<unset>":
            props.pop(key)
        else:
            props[key] = val

    def resize_table(self):
        print("HWPropsTableWidget.resize_table()")
        old = self.size()
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        margins = self.contentsMargins()
        w = margins.left() + margins.right()
        h = margins.top() + margins.bottom()
        w += self.verticalHeader().width()
        h += self.horizontalHeader().height()
        for i in range(self.columnCount()):
            w += self.columnWidth(i)
        for i in range(self.rowCount()):
            h += self.rowHeight(i)
        print("HWPropsTableWidget.resize_table(): {0}x{1} -> {2}x{3}".format(old.width(), old.height(), w, h))
        self.setFixedSize(w, h)
        if self.isVisible() and ((old.width() < w) or (old.height() < h)):
            w = self.parent()
            while w:
                old = w.size()
                min = w.minimumSizeHint()
                size = w.sizeHint()
                print("  old = {0}, min = {1}, size = {2}".format(old, min, size))
                if old.width() > size.width():
                    size.setWidth(old.width())
                if old.height() > size.height():
                    size.setHeight(old.height())
                w.resize(size)
                w.updateGeometry()
                print("HWPropsTableWidget.resize_table(): {0} -> {1}".format(old, size))
                w = w.parent()
