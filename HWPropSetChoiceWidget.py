from Qt import QtGui, QtCore, loadUi
from QtCore import Slot

from Autoconfig import Autoconfig, natural_sortkey
from HWPropsTableWidget import HWPropsTableWidget

class HWPropSetChoiceWidget(QtGui.QWidget):
    name_changed = QtCore.Signal(str)

    def __init__(self, parent=None):
        print("HWPropSetChoiceWidget.__init__()")
        super().__init__(parent)
        loadUi("HWPropSetChoiceWidget.ui", self, {"HWPropsTableWidget": HWPropsTableWidget})
        self.cluster = None
        self.goal = None
        self.similar_prop_sets = {}
        self.propsTableWidget.resize_table()

    def set_goal(self, cluster, goal):
        print("HWPropSetChoiceWidget.set_goal()")
        self.cluster = cluster
        self.goal = goal
        # Find existing and similar sets
        print("goal prop set = {0}".format(goal))
        sets = {}
        for entry in self.cluster.hw_prop_sets.values():
            name = self.cluster.hw_prop_set_names[entry.name_id].name
            prop = self.cluster.hw_props[entry.feature_id]
            prop_name = self.cluster.hw_prop_names[prop.name_id].name
            print("{0}: {1} = {2}".format(name, prop_name, prop.val))
            try:
                sets[name][prop_name] = prop.val
            except KeyError:
                sets[name] = Autoconfig(**{prop_name: prop.val})
        existing = []
        for (name, props) in sets.items():
            print("{0}: {1}".format(name, props))
            if props == goal:
                existing.append(name)
            else:
                filtered_props = {k: v for (k, v) in props.items() if k in Autoconfig.KEYS}
                print("filtered_props = {0}, goal = {1}".format(filtered_props, goal))
                if filtered_props == goal:
                    print("  similar")
                    self.similar_prop_sets[name] = props
        print("existing = {0}".format(existing))
        self.existingComboBox.blockSignals(True)
        if existing:
            existing.sort(key = natural_sortkey)
            self.existingComboBox.addItems(existing)
        else:
            self.existingComboBox.addItem("<no matches>")
        self.existingComboBox.blockSignals(False)
        self.existingComboBox.setEnabled(bool(existing))
        self.existingRadioButton.setEnabled(bool(existing))
        print("self.similar_prop_sets = {0}".format(self.similar_prop_sets.items()))
        self.similarComboBox.blockSignals(True)
        if self.similar_prop_sets:
            t = list(self.similar_prop_sets.keys())
            t.sort(key = natural_sortkey)
            self.similarComboBox.addItems(t)
        else:
            self.similarComboBox.addItem("<no matches>")
        self.similarComboBox.blockSignals(False)
        self.similarComboBox.setEnabled(bool(self.similar_prop_sets))
        self.similarRadioButton.setEnabled(bool(self.similar_prop_sets))

        if existing:
            self.existingRadioButton.setChecked(True)
            self.on_existingRadioButton_clicked()
        elif self.similar_prop_sets:
            self.similarRadioButton.setChecked(True)
            self.on_similarRadioButton_clicked()
        else:
            self.createRadioButton.setChecked(True)
            self.on_createRadioButton_clicked()

    @Slot(str)
    def on_createLineEdit_textChanged(self, text):
        print("HWPropSetChoiceWidget.on_createLineEdit_textChanged()")
        self.createRadioButton.setChecked(True)
        self.name_changed.emit(text)

    @Slot(str)
    def on_existingComboBox_currentIndexChanged(self, text):
        print("HWPropSetChoiceWidget.on_existingComboBox_currentIndexChanged()")
        self.existingRadioButton.setChecked(True)
        self.propsTableWidget.set_props(self.goal)
        self.name_changed.emit(text)

    @Slot()
    def on_existingRadioButton_clicked(self):
        print("HWPropSetChoiceWidget.on_existingRadioButton_clicked()")
        text = self.existingComboBox.currentText()
        self.propsTableWidget.set_props(self.goal)
        self.name_changed.emit(text)

    @Slot(str)
    def on_similarComboBox_currentIndexChanged(self, text):
        print("HWPropSetChoiceWidget.on_similarComboBox_currentIndexChanged()")
        self.similarRadioButton.setChecked(True)
        self.propsTableWidget.set_props(self.similar_prop_sets[text])
        self.name_changed.emit(text)

    @Slot()
    def on_similarRadioButton_clicked(self):
        print("HWPropSetChoiceWidget.on_similarRadioButton_clicked()")
        text = self.similarComboBox.currentText()
        self.propsTableWidget.set_props(self.similar_prop_sets[text])
        self.name_changed.emit(text)

    @Slot()
    def on_createRadioButton_clicked(self):
        text = self.createLineEdit.text()
        self.propsTableWidget.set_props(self.goal)
        self.name_changed.emit(text)

    def isComplete(self):
        print("HWPropSetChoiceWidget.isComplete()")
        if not self.createRadioButton.isChecked():
            return True
        else:
            text = self.createLineEdit.text()
            if not text:
                return False
            if self.cluster is None:
                return False
            for name in self.cluster.hw_prop_set_names.values():
                if name.name == text:
                    return False
            return True
