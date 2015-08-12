from Qt import QtGui, QtCore, loadUi
from QtCore import Slot
import hostlist

from Autoconfig import Autoconfig
from HWPropsTableWidget import HWPropsTableWidget

class ResolveMultipleGroupsPage(QtGui.QWizardPage):
    def __init__(self, parent = None):
        print("ResolveMultipleGroupsPage.__init__()")
        super().__init__(parent)
        loadUi("ResolveMultipleGroupsPage.ui", self, {"HWPropsTableWidget": HWPropsTableWidget})

    def initializePage(self):
        print("ResolveMultipleGroupsPage.initializePage()")
        super().initializePage()
        # click all the checked radio buttons to activate the setting
        if self.commonRadioButton.isChecked():
            self.on_commonRadioButton_clicked()
        if self.frequentRadioButton.isChecked():
            self.on_frequentRadioButton_clicked()
        if self.propPerHostRadioButton.isChecked():
            self.on_propPerHostRadioButton_clicked()
        if self.setPerHostRadioButton.isChecked():
            self.on_setPerHostRadioButton_clicked()
        if self.laterRadioButton.isChecked():
            self.on_laterRadioButton_clicked()

    def all_props(self):
        props = {}
        for conf in self.wizard().hosts.keys():
            print("conf = {0}".format(conf))
            for (key, val) in conf.items():
                try:
                    props[key].add(val)
                except KeyError:
                    props[key] = {val}
        return props

    def common_props(self, all=None):
        if all is None:
            all = self.all_props()
        props = {}
        for key in Autoconfig.KEYS:
            if key in all:
                vals = all[key]
                if len(vals) == 1:
                    props[key] = list(vals)[0]
        return props

    @Slot()
    def on_commonRadioButton_clicked(self):
        props = self.common_props()
        storage = self.wizard().template_props
        self.propsTableWidget.set_props(props, storage=storage)

    def frequent_props(self):
        props = {}
        num = 0
        for (conf, hosts) in self.wizard().hosts.items():
            if len(hosts) > num:
                num = len(hosts)
                props = conf
        return props

    @Slot()
    def on_frequentRadioButton_clicked(self):
        props = self.frequent_props()
        storage = self.wizard().template_props        
        self.propsTableWidget.set_props(props, storage=storage)

    @Slot()
    def on_customRadioButton_clicked(self):
        all = self.all_props()
        common = self.common_props(all=all)
        defaults = self.wizard().template_props
        props = {}
        for key in Autoconfig.KEYS:
            try:
                props[key] = common[key]
            except KeyError:
                try:
                    default = defaults[key]
                except KeyError:
                    default = "<unset>"
                try:
                    props[key] = (default, all[key])
                except KeyError:
                    pass
        storage = self.wizard().template_props        
        self.propsTableWidget.set_props(props, storage=storage)

    @Slot()
    def on_propPerHostRadioButton_clicked(self):
        self.wizard().remaining_props = "propPerHost"

    @Slot()
    def on_setPerHostRadioButton_clicked(self):
        self.wizard().remaining_props = "setPerHost"

    @Slot()
    def on_laterRadioButton_clicked(self):
        self.wizard().remaining_props = "manual"

    def cleanupPage(self):
        print("ResolveMultipleGroupsPage.cleanupPage()")
        super().cleanupPage()

    def validatePage(self):
        print("ResolveMultipleGroupsPage.validatePage()")
        return super().validatePage()

    def nextId(self):
        print("ResolveMultipleGroupsPage.nextId()")
        return super().nextId()

    def isComplete(self):
        print("ResolveMultipleGroupsPage.isComplete()")
        return super().isComplete()
