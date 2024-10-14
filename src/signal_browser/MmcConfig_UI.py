# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MmcConfig_UI.ui'
##
## Created by: Qt User Interface Compiler version 6.4.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QApplication,
    QDialog,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHeaderView,
    QLabel,
    QPushButton,
    QSizePolicy,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(683, 332)
        Dialog.setModal(True)
        self.formLayout = QFormLayout(Dialog)
        self.formLayout.setObjectName(u"formLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.machine_label = QLabel(self.frame)
        self.machine_label.setObjectName(u"machine_label")

        self.verticalLayout.addWidget(self.machine_label)

        self.machine_table_widget = QTableWidget(self.frame)
        if (self.machine_table_widget.columnCount() < 2):
            self.machine_table_widget.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.machine_table_widget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        font = QFont()
        font.setBold(False)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font);
        self.machine_table_widget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.machine_table_widget.setObjectName(u"machine_table_widget")
        self.machine_table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.machine_table_widget.setAlternatingRowColors(True)
        self.machine_table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.machine_table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.machine_table_widget.setCornerButtonEnabled(True)
        self.machine_table_widget.setRowCount(0)
        self.machine_table_widget.setColumnCount(2)
        self.machine_table_widget.verticalHeader().setVisible(True)
        self.machine_table_widget.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.machine_table_widget)


        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.frame)

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.sequense_label = QLabel(self.frame_2)
        self.sequense_label.setObjectName(u"sequense_label")

        self.verticalLayout_2.addWidget(self.sequense_label)

        self.seq_table_widget = QTableWidget(self.frame_2)
        if (self.seq_table_widget.columnCount() < 2):
            self.seq_table_widget.setColumnCount(2)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.seq_table_widget.setHorizontalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.seq_table_widget.setHorizontalHeaderItem(1, __qtablewidgetitem3)
        self.seq_table_widget.setObjectName(u"seq_table_widget")
        self.seq_table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.seq_table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.seq_table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.seq_table_widget.setColumnCount(2)
        self.seq_table_widget.horizontalHeader().setVisible(True)
        self.seq_table_widget.verticalHeader().setStretchLastSection(False)

        self.verticalLayout_2.addWidget(self.seq_table_widget)


        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.frame_2)

        self.frame_3 = QFrame(Dialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame_3)
        self.gridLayout.setObjectName(u"gridLayout")
        self.default_pb = QPushButton(self.frame_3)
        self.default_pb.setObjectName(u"default_pb")

        self.gridLayout.addWidget(self.default_pb, 1, 0, 1, 1)

        self.cancel_pb = QPushButton(self.frame_3)
        self.cancel_pb.setObjectName(u"cancel_pb")

        self.gridLayout.addWidget(self.cancel_pb, 1, 1, 1, 1)

        self.save_pb = QPushButton(self.frame_3)
        self.save_pb.setObjectName(u"save_pb")

        self.gridLayout.addWidget(self.save_pb, 0, 0, 1, 2)


        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.frame_3)


        self.retranslateUi(Dialog)
        self.default_pb.clicked["bool"].connect(Dialog.load_defaults)
        self.machine_table_widget.cellClicked.connect(Dialog.load_sequences)
        self.save_pb.clicked["bool"].connect(Dialog.accept)
        self.cancel_pb.clicked["bool"].connect(Dialog.reject)
        self.seq_table_widget.itemChanged.connect(Dialog.seq_item_changed)
        self.machine_table_widget.itemChanged.connect(Dialog.machine_item_changed)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"MMC Sequence Config", None))
        self.machine_label.setText(QCoreApplication.translate("Dialog", u"Machines", None))
        ___qtablewidgetitem = self.machine_table_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("Dialog", u"Name", None));
        ___qtablewidgetitem1 = self.machine_table_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("Dialog", u"Id", None));
        self.sequense_label.setText(QCoreApplication.translate("Dialog", u"Sequenses", None))
        ___qtablewidgetitem2 = self.seq_table_widget.horizontalHeaderItem(0)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("Dialog", u"Name", None));
        ___qtablewidgetitem3 = self.seq_table_widget.horizontalHeaderItem(1)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("Dialog", u"Id", None));
        self.default_pb.setText(QCoreApplication.translate("Dialog", u"Load Defaults", None))
        self.cancel_pb.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.save_pb.setText(QCoreApplication.translate("Dialog", u"Save", None))
    # retranslateUi

