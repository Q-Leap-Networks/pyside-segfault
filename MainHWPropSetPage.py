from Qt import QtGui, QtCore, loadUi
from QtCore import Slot
import hostlist

from Autoconfig import Autoconfig
from HWPropSetChoiceWidget import HWPropSetChoiceWidget

class MainHWPropSetPage(QtGui.QWizardPage):
    def __init__(self, parent=None):
        print("MainHWPropSetPage.__init__()")
        super().__init__(parent)
        loadUi("MainHWPropSetPage.ui", self, {"HWPropSetChoiceWidget": HWPropSetChoiceWidget})
        self.choiceWidget.name_changed.connect(self.name_changed)

    def initializePage(self):
        print("MainHWPropSetPage.initializePage()")
        super().initializePage()
        cluster = self.wizard().cluster
        goal = self.wizard().template_props
        print("goal prop set = {0}".format(goal))
        self.choiceWidget.set_goal(cluster, goal)
        print(dir(self.choiceWidget))
        print(self.choiceWidget.__class__)
        print(self.choiceWidget.__class__.__bases__)

    def cleanupPage(self):
        print("MainHWPropSetPage.cleanupPage()")
        super().cleanupPage()

    def validatePage(self):
        print("MainHWPropSetPage.validatePage()")
        return super().validatePage()

    def nextId(self):
        print("MainHWPropSetPage.nextId()")
        return super().nextId()

    def name_changed(self, name):
        print("MainHWPropSetPage.name_changed({0})".format(name))
        self.completeChanged.emit()
        self.wizard().template_hw_prop_set_name = name

    def isComplete(self):
        print("MainHWPropSetPage.isComplete()")
        return self.choiceWidget.isComplete()
