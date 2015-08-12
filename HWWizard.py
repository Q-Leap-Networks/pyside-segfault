from collections import namedtuple

from Qt import QtGui, QtCore, loadUi
from QtCore import Slot

from HostSelectionPage import HostSelectionPage
from ResolveMultipleGroupsPage import ResolveMultipleGroupsPage
from MainHWPropSetPage import MainHWPropSetPage
from PerHostHWPropSetPage import PerHostHWPropSetPage

def make_enum(*names):
    numbers = range(len(names))
    return (namedtuple("_", names)(*numbers), names)

class HWWizard(QtGui.QWizard):
    (PAGES, PAGES_REV) = make_enum("HostSelectionPage", "ResolveMultipleGroupsPage", "MainHWPropSetPage", "PerHostHWPropSetPage")

    def __init__(self, cluster, hosts=None, parent = None):
        super().__init__(parent)
        loadUi("HWWizard.ui", self)
        self._cluster = cluster
        if hosts is None:
            self.hosts = {}
        else:
            self.hosts = HostSelectionPage.group_hosts(hosts)
        # Default answeres:
        self.template_props = {}
        self.template_hw_prop_set_name = ""
        self.remaining_props = "setPerHost"
        # Create pages
        for i in range(len(HWWizard.PAGES_REV)):
            page = eval("{0}()".format(HWWizard.PAGES_REV[i]))
            self.setPage(i, page)

    @property
    def cluster(self):
        return self._cluster

    def done(self, result):
        print("HWWizard.done({0})".format(result))
        if result:
            print(" selected hosts:")
            for (conf, hosts) in self.hosts.items():
                name = str([h.name for h in hosts])
                print("  {0}: {1}".format(conf, [h.name for h in hosts]))
            print(" main HW Prop Set: {0}".format(self.template_props))
            print(" main HW Prop Set Name: {0}".format(self.template_hw_prop_set_name))
            print(" remaining props: {0}".format(self.remaining_props))
        super().done(result)
