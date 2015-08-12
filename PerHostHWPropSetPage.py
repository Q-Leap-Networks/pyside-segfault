from Qt import QtGui, QtCore, loadUi
from QtCore import Slot
import hostlist

from Autoconfig import Autoconfig

class PerHostHWPropSetPage(QtGui.QWizardPage):
    def __init__(self, parent = None):
        super().__init__(parent)
        loadUi("PerHostHWPropSetPage.ui", self)

    def initializePage(self):
        print("PerHostHWPropSetPage.initializePage()")
        super().initializePage()
        self.listWidget.addItem("Item 1")
        self.listWidget.addItem("Item 2")

    def cleanupPage(self):
        print("PerHostHWPropSetPage.cleanupPage()")
        super().cleanupPage()

    def validatePage(self):
        print("PerHostHWPropSetPage.validatePage()")
        return super().validatePage()

    def nextId(self):
        print("PerHostHWPropSetPage.nextId()")
        return super().nextId()

    def isComplete(self):
        print("PerHostHWPropSetPage.isComplete()")
        return super().isComplete()
