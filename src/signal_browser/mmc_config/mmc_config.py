import json
from collections import OrderedDict

from MmcConfig_UI import Ui_Dialog
from PySide6 import QtWidgets
from PySide6.QtCore import QSettings
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu

from signal_browser.mmc_constants import EBT, HR, HT, TDDW, Machine_ID  # <--- Import the enums

...


class MmcConfigDialog(QtWidgets.QDialog):
    DEFAULT_ID = -9999
    DEFAULT_NAME = "New Machine"

    def __init__(self, parent=None):
        super().__init__(parent)

        self.m_ui = Ui_Dialog()
        self.m_ui.setupUi(self)
        self.settings = QSettings("NOV", "Signal Browser")
        self.m_ui.machine_table_widget.customContextMenuRequested.connect(self.machine_context_menu)
        self.m_ui.seq_table_widget.customContextMenuRequested.connect(self.sequence_context_menu)
        self.all_loaded_machines = OrderedDict()
        self.selected_sequences = OrderedDict()
        self.all_loaded_sequences = OrderedDict()
        self.selected_machine = None
        self.load_settings()

    @staticmethod
    def ordered_dict_insert(odict, index, key, value):
        result = OrderedDict()
        for i, (k, v) in enumerate(odict.items()):
            if i == index:
                result[key] = value
            result[k] = v
        return result

    def load_defaults(self):
        self.all_loaded_machines = self.load_machines_from_defaults()
        self.all_loaded_sequences = self.load_sequences_from_defaults()

        self.update_machine_table(self.all_loaded_machines)
        self.clear_sequences_table()

    def load_settings(self):
        self.all_loaded_machines = self.load_machines_from_settings()
        self.all_loaded_sequences = self.load_sequences_from_settings()

        self.update_machine_table(self.all_loaded_machines)
        self.clear_sequences_table()

    def load_machines_from_settings(self):
        return json.loads(self.settings.value("machines", "{}"))

    @staticmethod
    def load_machines_from_defaults():
        return OrderedDict((item.name, item.value) for item in Machine_ID)

    def load_sequences_from_settings(self):
        return json.loads(self.settings.value("sequences", "{}"))

    @staticmethod
    def load_sequences_from_defaults():
        return {"TDDW": OrderedDict((item.name, item.value) for item in TDDW),
                "PriHR": OrderedDict((item.name, item.value) for item in HR),
                "HT": OrderedDict((item.name, item.value) for item in HT),
                "EBT": OrderedDict((item.name, item.value) for item in EBT)}

    def update_machine_table(self, machines):
        self.m_ui.machine_table_widget.setRowCount(0)
        self.m_ui.machine_table_widget.blockSignals(True)
        for index, machine in enumerate(machines):
            self.m_ui.machine_table_widget.insertRow(index)
            self.m_ui.machine_table_widget.setItem(index, 0, QtWidgets.QTableWidgetItem(machine))
            self.m_ui.machine_table_widget.setItem(index, 1, QtWidgets.QTableWidgetItem(str(machines[machine])))
        self.m_ui.machine_table_widget.blockSignals(False)

    def update_sequences_table(self, sequences):
        self.m_ui.seq_table_widget.setRowCount(0)
        self.m_ui.seq_table_widget.blockSignals(True)
        for index, (sequence_name, sequence_value) in enumerate(sequences.items()):
            self.m_ui.seq_table_widget.insertRow(index)
            self.m_ui.seq_table_widget.setItem(index, 0, QtWidgets.QTableWidgetItem(sequence_name))
            self.m_ui.seq_table_widget.setItem(index, 1, QtWidgets.QTableWidgetItem(str(sequence_value)))
        self.m_ui.seq_table_widget.blockSignals(False)

    def clear_sequences_table(self):
        self.m_ui.seq_table_widget.setRowCount(0)

    def machine_context_menu(self, position):
        # create context menu
        context_menu = QMenu(self)

        # Define actions
        action1 = QAction("New Machine", self)
        action2 = QAction("Remove", self)

        # Add actions to context menu
        context_menu.addAction(action1)
        context_menu.addAction(action2)

        if item := self.m_ui.machine_table_widget.itemAt(position):
            action2.setEnabled(True)
            action2.triggered.connect(lambda _: self.remove_machine_action(item))
        else:
            action2.setEnabled(False)

        # Connect actions to desired functions
        action1.triggered.connect(self.add_new_machine_action)

        # Show the context menu.
        context_menu.popup(self.m_ui.machine_table_widget.viewport().mapToGlobal(position))

    def sequence_context_menu(self, position):
        # create context menu
        context_menu = QMenu(self)

        # Define actions
        action3 = QAction("New sequence", self)
        action4 = QAction("Remove", self)

        # Add actions to context menu
        context_menu.addAction(action3)
        context_menu.addAction(action4)

        if item := self.m_ui.seq_table_widget.itemAt(position):
            action4.setEnabled(True)
            action4.triggered.connect(lambda _: self.remove_sequence_action(item))
        else:
            action4.setEnabled(False)

        # Connect actions to desired functions
        action3.triggered.connect(self.add_new_sequence_action)

        # Show the context menu.
        context_menu.popup(self.m_ui.seq_table_widget.viewport().mapToGlobal(position))

    def add_new_machine_action(self):
        if self.DEFAULT_NAME in self.all_loaded_machines:
            QtWidgets.QMessageBox.critical(self, "Duplicate machine Name",
                                           f"Machine {self.DEFAULT_NAME} already exists, remove the duplicate")
            return

        if self.DEFAULT_ID in self.all_loaded_machines.values():
            QtWidgets.QMessageBox.critical(self, "Duplicate machine ID",
                                           f"Machine ID {self.DEFAULT_ID} already exists, remove the duplicate")
            return

        self.all_loaded_machines["New Machine"] = -9999
        self.update_machine_table(self.all_loaded_machines)

    def remove_machine_action(self, item):
        row = item.row()
        name = self.m_ui.machine_table_widget.item(row, 0).text()
        self.all_loaded_machines.pop(name)
        self.update_machine_table(self.all_loaded_machines)

    def machine_item_changed(self, item):
        row = item.row()
        selected_name = list(self.all_loaded_machines)[row]
        selected_value = self.all_loaded_machines[selected_name]

        if item.column() == 0:
            new_name = item.text()

            if new_name == selected_name:
                return
            elif new_name in self.all_loaded_machines:
                QtWidgets.QMessageBox.critical(self, "Duplicate machine Name",
                                               f"Machine {new_name} already exists, remove the duplicate")
                self.update_machine_table(self.all_loaded_machines)
                return

            self.all_loaded_machines.pop(selected_name)

            if row >= len(self.all_loaded_machines):
                self.all_loaded_machines[new_name] = selected_value
            else:
                self.all_loaded_machines = self.ordered_dict_insert(self.all_loaded_machines, row, new_name,
                                                                    selected_value)

            self.all_loaded_sequences[new_name] = self.all_loaded_sequences.pop(selected_name, None)
        elif item.column() == 1:
            new_value = item.text()
            self.all_loaded_machines[selected_name] = str(new_value)

        self.update_machine_table(self.all_loaded_machines)

    def add_new_sequence_action(self):
        if "New sequence" in self.selected_sequences:
            QtWidgets.QMessageBox.critical(self, "Duplicate sequence Name",
                                           "sequence New sequence already exists, rename the duplicate")
            return

        self.selected_sequences["New sequence"] = -9999
        self.all_loaded_sequences[self.selected_machine] = self.selected_sequences
        self.update_sequences_table(self.selected_sequences)
        self.m_ui.seq_table_widget.scrollToBottom()

    def remove_sequence_action(self, item):
        row = item.row()
        name = self.m_ui.seq_table_widget.item(row, 0).text()
        self.selected_sequences.pop(name)
        self.all_loaded_sequences[self.selected_machine] = self.selected_sequences
        self.update_sequences_table(self.selected_sequences)

    def seq_item_changed(self, item):
        row = item.row()
        selected_name = list(self.selected_sequences)[row]
        selected_value = self.selected_sequences[selected_name]

        if item.column() == 0:
            new_key = item.text()
            self.selected_sequences.pop(selected_name)

            if row >= len(self.selected_sequences):
                self.selected_sequences[new_key] = selected_value
            else:
                self.selected_sequences = self.ordered_dict_insert(self.selected_sequences, row, new_key,
                                                                   selected_value)
        elif item.column() == 1:
            new_value = item.text()
            self.selected_sequences[selected_name] = new_value

        self.all_loaded_sequences[self.selected_machine] = self.selected_sequences

        self.update_sequences_table(self.selected_sequences)

    def load_sequences(self, row, _):

        machine = self.m_ui.machine_table_widget.item(row, 0).text()
        self.selected_machine = machine
        self.m_ui.seq_table_widget.setRowCount(0)

        sequence_enums = self.all_loaded_sequences.get(machine, None)
        if sequence_enums:
            self.update_sequences_table(sequence_enums)
            self.selected_sequences = sequence_enums
        else:
            self.m_ui.seq_table_widget.setRowCount(0)
            self.selected_sequences = OrderedDict()

    def accept(self):
        # Save the changes
        self.settings.setValue("sequences", json.dumps(self.all_loaded_sequences))
        self.settings.setValue("machines", json.dumps(self.all_loaded_machines))

        super().accept()


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = MmcConfigDialog()
    window.exec()
