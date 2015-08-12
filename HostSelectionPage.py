from Qt import QtGui, QtCore, loadUi
from QtCore import Slot

from Autoconfig import Autoconfig

class HostSelectionPage(QtGui.QWizardPage):
    def __init__(self, parent = None):
        super().__init__(parent)
        loadUi("HostSelectionPage.ui", self)

    def initializePage(self):
        print("HostSelectionPage.initializePage()")
        super().initializePage()
        print("hosts = {0}".format(self.wizard().hosts))
        self.load_groups()

    def cleanupPage(self):
        print("HostSelectionPage.cleanupPage()")
        super().cleanupPage()

    def validatePage(self):
        print("HostSelectionPage.validatePage()")
        return super().validatePage()

    def nextId(self):
        print("HostSelectionPage.nextId()")
        return super().nextId()

    def isComplete(self):
        print("HostSelectionPage.isComplete()")
        return bool(self.wizard().hosts)

    def host_groups(self, hosts):
        groups = {}
        for host in hosts:
            conf = Autoconfig(host.autodetect)
            try:
                groups[conf].append(host)
            except KeyError:
                groups[conf] = [host]
        return groups

    def set_hosts_with_status(self, status):
        print("HostSelectionPage.set_hosts_with_status()")
        cluster = self.wizard().cluster
        groups = {}
        for host in cluster.hosts.values():
            print(host)
            conf = Autoconfig(host.autodetect)
            try:
                groups[conf].append(host)
            except KeyError:
                groups[conf] = [host]
        self.wizard().hosts = groups
        self.load_groups()

    def load_groups(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        for (conf, hosts) in self.wizard().hosts.items():
            name = str([h.name for h in hosts])
            print("{0}: {1}".format(conf, [h.name for h in hosts]))
            self.tableWidget.insertRow(0)
            w = QtGui.QTableWidgetItem(name)
            w.autoconfig = conf
            w.hosts = hosts
            self.tableWidget.setItem(0, 0, w)
            col = 1
            for key in Autoconfig.KEYS:
                w = QtGui.QTableWidgetItem(conf[key])
                w.autoconfig = conf
                w.hosts = hosts
                self.tableWidget.setItem(0, col, w)
                col += 1
        self.tableWidget.resizeColumnsToContents()
        self.completeChanged.emit()
        self.tableWidget.selectAll()

    @Slot()
    def on_unconfiguredButton_clicked(self):
        print("HostSelectionPage.on_unconfiguredButton_clicked()")
        self.set_hosts_with_status(None)

    @Slot()
    def on_partialButton_clicked(self):
        print("HostSelectionPage.on_partialButton_clicked()")
        self.set_hosts_with_status(None)

    @Slot()
    def on_tableWidget_itemSelectionChanged(self):
        print("HostSelectionPage.on_tableWidget_itemSelectionChanged()")
        groups = {}
        for item in self.tableWidget.selectedItems():
            groups[item.autoconfig] = item.hosts
        self.wizard().hosts = groups
        self.completeChanged.emit()
