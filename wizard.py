#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse

from Qt import QtGui, QtCore, loadUi
from QtCore import Slot

from HWWizard import HWWizard

class Host:
    def __init__(self, name, autodetect):
        self.name = name
        self.autodetect = autodetect

class Name:
    def __init__(self, name):
        self.name = name

class PropSet:
    def __init__(self, name_id, feature_id):
        self.name_id = name_id
        self.feature_id = feature_id

class Prop:
    def __init__(self, name_id, val):
        self.name_id = name_id
        self.val = val

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        loadUi("MainWindow.ui", self)
        self.hosts = {
            1: Host("beo-01", {"# CPU cores": "1",
                               "# CPU sockets": "1",
                               "Size of RAM (GB)": "1",
                               "IB Adapter": "True",
                               "IPMI Adapter": "False"}),
            2: Host("beo-02", {"# CPU cores": "1",
                               "# CPU sockets": "1",
                               "Size of RAM (GB)": "1",
                               "IB Adapter": "True",
                               "IPMI Adapter": "False"}),
            3: Host("beo-03", {"# CPU cores": "1",
                               "# CPU sockets": "1",
                               "Size of RAM (GB)": "1",
                               "IB Adapter": "True",
                               "IPMI Adapter": "False"}),
            4: Host("beo-04", {"# CPU cores": "1",
                               "# CPU sockets": "1",
                               "Size of RAM (GB)": "2",
                               "IB Adapter": "True",
                               "IPMI Adapter": "False"}),
            5: Host("beo-05", {"# CPU cores": "1",
                               "# CPU sockets": "1",
                               "Size of RAM (GB)": "2",
                               "IB Adapter": "True",
                               "IPMI Adapter": "False"}),
        }
        self.hw_prop_set_names = {
            1: Name("Existing"),
            2: Name("Similar"),
            3: Name("Bad"),
        }
        self.hw_prop_names = {
            1: Name("# CPU cores"),
            2: Name("# CPU sockets"),
            3: Name("Size of RAM (GB)"),
            4: Name("IB Adapter"),
            5: Name("IPMI Adapter"),
            6: Name("Other"),
        }
        self.hw_props = {
            1: Prop(1, "1"),
            2: Prop(2, "1"),
            3: Prop(3, "1"),
            4: Prop(4, "True"),
            5: Prop(5, "False"),
            6: Prop(6, "something"),
            7: Prop(1, "2"),
        }
        self.hw_prop_sets = {
            1: PropSet(1, 1),
            2: PropSet(1, 2),
            3: PropSet(1, 3),
            4: PropSet(1, 4),
            5: PropSet(1, 5),
            6: PropSet(2, 1),
            7: PropSet(2, 2),
            8: PropSet(2, 3),
            9: PropSet(2, 4),
            10: PropSet(2, 5),
            11: PropSet(2, 6),
            12: PropSet(3, 7),
            13: PropSet(3, 2),
            14: PropSet(3, 3),
            15: PropSet(3, 4),
            16: PropSet(3, 5),
        }

    @Slot()
    def on_wizardButton_clicked(self):
        wiz = HWWizard(self)
        wiz.exec_()

def main():
    app = QtGui.QApplication(sys.argv)
    app.setOrganizationName("test")
    app.setOrganizationDomain("test")
    app.setApplicationName("test")

    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
