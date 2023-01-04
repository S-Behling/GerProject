# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'IFC compare.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore

import ifc_compare_rsc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(700, 500)
        MainWindow.setMinimumSize(QSize(700, 500))
        MainWindow.setMaximumSize(QSize(1100, 700))
        icon = QIcon()
        icon.addFile(u":/Icons/icon.png", QSize(), QIcon.Normal, QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setElideMode(Qt.ElideLeft)
        self.tab_parameters = QWidget()
        self.tab_parameters.setObjectName(u"tab_parameters")
        self.gridLayout_3 = QGridLayout(self.tab_parameters)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.verticalWidget = QWidget(self.tab_parameters)
        self.verticalWidget.setObjectName(u"verticalWidget")
        self.verticalWidget.setMinimumSize(QSize(0, 0))
        self.verticalWidget.setMaximumSize(QSize(1200, 700))
        self.verticalLayout = QVBoxLayout(self.verticalWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.box_fileopt = QGroupBox(self.verticalWidget)
        self.box_fileopt.setObjectName(u"box_fileopt")
        self.box_fileopt.setMaximumSize(QSize(16777215, 57))
        self.gridLayout_7 = QGridLayout(self.box_fileopt)
        self.gridLayout_7.setObjectName(u"gridLayout_7")
        self.btn_folder = QPushButton(self.box_fileopt)
        self.btn_folder.setObjectName(u"btn_folder")
        self.btn_folder.setMaximumSize(QSize(30, 30))
        icon1 = QIcon()
        icon1.addFile(u":/Icons/folder.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_folder.setIcon(icon1)
        self.btn_folder.setFlat(True)

        self.gridLayout_7.addWidget(self.btn_folder, 0, 0, 1, 1)

        self.lineEdit_folder = QLineEdit(self.box_fileopt)
        self.lineEdit_folder.setObjectName(u"lineEdit_folder")

        self.gridLayout_7.addWidget(self.lineEdit_folder, 0, 1, 1, 1)


        self.verticalLayout.addWidget(self.box_fileopt)

        self.layout_elements = QGridLayout()
        self.layout_elements.setObjectName(u"layout_elements")
        self.layout_elements.setVerticalSpacing(9)
        self.groupBox = QGroupBox(self.verticalWidget)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout_2 = QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setVerticalSpacing(10)
        self.pushButton_refresh = QPushButton(self.groupBox)
        self.pushButton_refresh.setObjectName(u"pushButton_refresh")
        self.pushButton_refresh.setEnabled(True)
        self.pushButton_refresh.setMinimumSize(QSize(80, 30))
        self.pushButton_refresh.setMaximumSize(QSize(80, 30))
        font = QFont()
        font.setFamilies([u"HoloLens MDL2 Assets"])
        font.setPointSize(8)
        font.setBold(True)
        self.pushButton_refresh.setFont(font)
        self.pushButton_refresh.setStyleSheet(u"QPushButton {\n"
"    color: #ffffff;\n"
"    border-radius: 2px;\n"
"    background: rgb(96, 214, 134);\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    background: rgb(126, 244, 164);\n"
"    }\n"
"")

        self.gridLayout_2.addWidget(self.pushButton_refresh, 7, 2, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed)

        self.gridLayout_2.addItem(self.verticalSpacer, 5, 2, 1, 1)

        self.pushButton_highlight = QPushButton(self.groupBox)
        self.pushButton_highlight.setObjectName(u"pushButton_highlight")
        self.pushButton_highlight.setEnabled(True)
        self.pushButton_highlight.setMinimumSize(QSize(120, 30))
        self.pushButton_highlight.setMaximumSize(QSize(120, 30))
        self.pushButton_highlight.setFont(font)
        self.pushButton_highlight.setStyleSheet(u"QPushButton {\n"
"    color: #ffffff;\n"
"    border-radius: 2px;\n"
"    background: rgb(96, 214, 134);\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    background: rgb(126, 244, 164);\n"
"    }\n"
"")

        self.gridLayout_2.addWidget(self.pushButton_highlight, 7, 3, 1, 1)

        self.label_filter = QLabel(self.groupBox)
        self.label_filter.setObjectName(u"label_filter")
        self.label_filter.setMaximumSize(QSize(16777215, 20))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setKerning(True)
        self.label_filter.setFont(font1)
        self.label_filter.setStyleSheet(u"color: rgb(70, 70, 70);")

        self.gridLayout_2.addWidget(self.label_filter, 3, 0, 1, 1)

        self.tableWidget_all = QTableWidget(self.groupBox)
        if (self.tableWidget_all.columnCount() < 5):
            self.tableWidget_all.setColumnCount(5)
        font2 = QFont()
        font2.setBold(True)
        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setFont(font2);
        self.tableWidget_all.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setFont(font2);
        self.tableWidget_all.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        __qtablewidgetitem2.setFont(font2);
        self.tableWidget_all.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font2);
        self.tableWidget_all.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font2);
        self.tableWidget_all.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        if (self.tableWidget_all.rowCount() < 2):
            self.tableWidget_all.setRowCount(2)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tableWidget_all.setVerticalHeaderItem(0, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tableWidget_all.setVerticalHeaderItem(1, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_all.setItem(0, 0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_all.setItem(0, 1, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_all.setItem(0, 2, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_all.setItem(0, 3, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_all.setItem(0, 4, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_all.setItem(1, 0, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_all.setItem(1, 1, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_all.setItem(1, 2, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_all.setItem(1, 3, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_all.setItem(1, 4, __qtablewidgetitem16)
        self.tableWidget_all.setObjectName(u"tableWidget_all")
        self.tableWidget_all.setFrameShape(QFrame.Box)
        self.tableWidget_all.setFrameShadow(QFrame.Sunken)
        self.tableWidget_all.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget_all.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.tableWidget_all.setSizeAdjustPolicy(QAbstractScrollArea.AdjustIgnored)
        self.tableWidget_all.setAutoScroll(False)
        self.tableWidget_all.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.tableWidget_all.setDragDropOverwriteMode(False)
        self.tableWidget_all.setSelectionMode(QAbstractItemView.MultiSelection)
        self.tableWidget_all.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget_all.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget_all.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tableWidget_all.setSortingEnabled(True)
        self.tableWidget_all.horizontalHeader().setVisible(True)
        self.tableWidget_all.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_all.horizontalHeader().setHighlightSections(False)
        self.tableWidget_all.horizontalHeader().setProperty("showSortIndicator", True)
        self.tableWidget_all.verticalHeader().setCascadingSectionResizes(False)
        self.tableWidget_all.verticalHeader().setMinimumSectionSize(21)
        self.tableWidget_all.verticalHeader().setDefaultSectionSize(23)
        self.tableWidget_all.verticalHeader().setHighlightSections(True)
        self.tableWidget_all.verticalHeader().setProperty("showSortIndicator", False)
        self.tableWidget_all.verticalHeader().setStretchLastSection(False)

        self.gridLayout_2.addWidget(self.tableWidget_all, 0, 0, 2, 4)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.comboBox_IFCelement_2 = QComboBox(self.groupBox)
        self.comboBox_IFCelement_2.addItem("")
        self.comboBox_IFCelement_2.setObjectName(u"comboBox_IFCelement_2")
        self.comboBox_IFCelement_2.setMinimumSize(QSize(101, 20))
        self.comboBox_IFCelement_2.setMaximumSize(QSize(16777215, 20))
        self.comboBox_IFCelement_2.setStyleSheet(u"QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    padding: 1px 18px 1px 3px;\n"
"    min-width: 6em;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/Icons/dropdown.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}")
        self.comboBox_IFCelement_2.setFrame(False)
        self.comboBox_IFCelement_2.setModelColumn(0)

        self.horizontalLayout.addWidget(self.comboBox_IFCelement_2)

        self.comboBox_IFCparameter = QComboBox(self.groupBox)
        self.comboBox_IFCparameter.addItem("")
        self.comboBox_IFCparameter.setObjectName(u"comboBox_IFCparameter")
        self.comboBox_IFCparameter.setMinimumSize(QSize(101, 20))
        self.comboBox_IFCparameter.setMaximumSize(QSize(10000000, 20))
        self.comboBox_IFCparameter.setStyleSheet(u"QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    padding: 1px 18px 1px 3px;\n"
"    min-width: 6em;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/Icons/dropdown.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}")
        self.comboBox_IFCparameter.setFrame(False)
        self.comboBox_IFCparameter.setModelColumn(0)

        self.horizontalLayout.addWidget(self.comboBox_IFCparameter)

        self.label_right = QLabel(self.groupBox)
        self.label_right.setObjectName(u"label_right")
        self.label_right.setMinimumSize(QSize(20, 20))
        self.label_right.setMaximumSize(QSize(20, 20))
        self.label_right.setPixmap(QPixmap(u":/Icons/right.png"))
        self.label_right.setScaledContents(True)

        self.horizontalLayout.addWidget(self.label_right)

        self.comboBox_RVTelement = QComboBox(self.groupBox)
        self.comboBox_RVTelement.addItem("")
        self.comboBox_RVTelement.setObjectName(u"comboBox_RVTelement")
        self.comboBox_RVTelement.setMinimumSize(QSize(101, 20))
        self.comboBox_RVTelement.setMaximumSize(QSize(16777215, 20))
        self.comboBox_RVTelement.setStyleSheet(u"QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    padding: 1px 18px 1px 3px;\n"
"    min-width: 6em;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/Icons/dropdown.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}")
        self.comboBox_RVTelement.setFrame(False)
        self.comboBox_RVTelement.setModelColumn(0)

        self.horizontalLayout.addWidget(self.comboBox_RVTelement)

        self.comboBox_RVTparameter = QComboBox(self.groupBox)
        self.comboBox_RVTparameter.addItem("")
        self.comboBox_RVTparameter.setObjectName(u"comboBox_RVTparameter")
        self.comboBox_RVTparameter.setMinimumSize(QSize(101, 20))
        self.comboBox_RVTparameter.setMaximumSize(QSize(16777215, 20))
        self.comboBox_RVTparameter.setStyleSheet(u"QComboBox {\n"
"    border: 1px solid gray;\n"
"    border-radius: 3px;\n"
"    padding: 1px 18px 1px 3px;\n"
"    min-width: 6em;\n"
"}\n"
"\n"
"QComboBox:editable {\n"
"    background: white;\n"
"}\n"
"\n"
"\n"
"QComboBox:on { /* shift the text when the popup opens */\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    subcontrol-origin: padding;\n"
"    subcontrol-position: top right;\n"
"    width: 15px;\n"
"\n"
"    border-left-width: 1px;\n"
"    border-left-color: darkgray;\n"
"    border-left-style: solid; /* just a single line */\n"
"    border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"    border-bottom-right-radius: 3px;\n"
"}\n"
"\n"
"QComboBox::down-arrow {\n"
"    image: url(:/Icons/dropdown.png);\n"
"}\n"
"\n"
"QComboBox::down-arrow:on { /* shift the arrow when popup is open */\n"
"    top: 1px;\n"
"    left: 1px;\n"
"}")
        self.comboBox_RVTparameter.setFrame(False)
        self.comboBox_RVTparameter.setModelColumn(0)

        self.horizontalLayout.addWidget(self.comboBox_RVTparameter)


        self.gridLayout_2.addLayout(self.horizontalLayout, 4, 0, 1, 4)

        self.pushButton_delete = QPushButton(self.groupBox)
        self.pushButton_delete.setObjectName(u"pushButton_delete")
        self.pushButton_delete.setEnabled(True)
        self.pushButton_delete.setMinimumSize(QSize(30, 30))
        self.pushButton_delete.setMaximumSize(QSize(30, 30))
        self.pushButton_delete.setFont(font)
        self.pushButton_delete.setStyleSheet(u"QPushButton {\n"
"    color: #ffffff;\n"
"    border-radius: 2px;\n"
"    background:rgb(255, 96, 96);\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    background:rgb(255, 126, 126);\n"
"    }\n"
"")
        icon2 = QIcon()
        icon2.addFile(u":/Icons/trash.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pushButton_delete.setIcon(icon2)

        self.gridLayout_2.addWidget(self.pushButton_delete, 7, 1, 1, 1)


        self.layout_elements.addWidget(self.groupBox, 0, 0, 1, 1)


        self.verticalLayout.addLayout(self.layout_elements)

        self.layout_status = QGridLayout()
        self.layout_status.setObjectName(u"layout_status")
        self.label_status = QLabel(self.verticalWidget)
        self.label_status.setObjectName(u"label_status")
        self.label_status.setMaximumSize(QSize(16777215, 40))
        self.label_status.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)

        self.layout_status.addWidget(self.label_status, 0, 0, 1, 1)

        self.pushButton_done = QPushButton(self.verticalWidget)
        self.pushButton_done.setObjectName(u"pushButton_done")
        self.pushButton_done.setEnabled(True)
        self.pushButton_done.setMinimumSize(QSize(120, 40))
        self.pushButton_done.setMaximumSize(QSize(120, 40))
        font3 = QFont()
        font3.setFamilies([u"HoloLens MDL2 Assets"])
        font3.setPointSize(10)
        font3.setBold(True)
        self.pushButton_done.setFont(font3)
        self.pushButton_done.setStyleSheet(u"QPushButton {\n"
"    color: #ffffff;\n"
"    border-radius: 2px;\n"
"    background: #34495e;\n"
"    padding: 5px;\n"
"    }\n"
"\n"
"QPushButton:pressed {\n"
"    background: #678099;\n"
"    }\n"
"")

        self.layout_status.addWidget(self.pushButton_done, 0, 1, 1, 1)


        self.verticalLayout.addLayout(self.layout_status)


        self.gridLayout_3.addWidget(self.verticalWidget, 0, 0, 1, 1)

        self.tabWidget.addTab(self.tab_parameters, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)
        self.comboBox_IFCelement_2.setCurrentIndex(0)
        self.comboBox_IFCparameter.setCurrentIndex(0)
        self.comboBox_RVTelement.setCurrentIndex(0)
        self.comboBox_RVTparameter.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"IFC compare", None))
        self.box_fileopt.setTitle(QCoreApplication.translate("MainWindow", u"IFC File", None))
        self.btn_folder.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Elements", None))
        self.pushButton_refresh.setText(QCoreApplication.translate("MainWindow", u"Refresh", None))
        self.pushButton_highlight.setText(QCoreApplication.translate("MainWindow", u"Highligh element", None))
        self.label_filter.setText(QCoreApplication.translate("MainWindow", u"Filter", None))
        ___qtablewidgetitem = self.tableWidget_all.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Element Id", None));
        ___qtablewidgetitem1 = self.tableWidget_all.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem2 = self.tableWidget_all.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Parameter Value", None));
        ___qtablewidgetitem3 = self.tableWidget_all.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"IFC Element", None));
        ___qtablewidgetitem4 = self.tableWidget_all.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"New Value", None));
        ___qtablewidgetitem5 = self.tableWidget_all.verticalHeaderItem(0)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"1", None));
        ___qtablewidgetitem6 = self.tableWidget_all.verticalHeaderItem(1)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"2", None));

        __sortingEnabled = self.tableWidget_all.isSortingEnabled()
        self.tableWidget_all.setSortingEnabled(False)
        ___qtablewidgetitem7 = self.tableWidget_all.item(0, 0)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"123456", None));
        ___qtablewidgetitem8 = self.tableWidget_all.item(0, 1)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Revit Column", None));
        ___qtablewidgetitem9 = self.tableWidget_all.item(0, 2)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"C30", None));
        ___qtablewidgetitem10 = self.tableWidget_all.item(0, 3)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"IFC Column", None));
        ___qtablewidgetitem11 = self.tableWidget_all.item(0, 4)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"C26", None));
        ___qtablewidgetitem12 = self.tableWidget_all.item(1, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"145515", None));
        ___qtablewidgetitem13 = self.tableWidget_all.item(1, 1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Revit Column", None));
        ___qtablewidgetitem14 = self.tableWidget_all.item(1, 2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"C25", None));
        ___qtablewidgetitem15 = self.tableWidget_all.item(1, 3)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"IFC Column", None));
        ___qtablewidgetitem16 = self.tableWidget_all.item(1, 4)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"C20", None));
        self.tableWidget_all.setSortingEnabled(__sortingEnabled)

        self.comboBox_IFCelement_2.setItemText(0, QCoreApplication.translate("MainWindow", u"IFC Element", None))

        self.comboBox_IFCparameter.setItemText(0, QCoreApplication.translate("MainWindow", u"IFC Parameter", None))

        self.label_right.setText("")
        self.comboBox_RVTelement.setItemText(0, QCoreApplication.translate("MainWindow", u"RVT Element", None))

        self.comboBox_RVTparameter.setItemText(0, QCoreApplication.translate("MainWindow", u"RVT Parameter", None))

        self.pushButton_delete.setText("")
        self.label_status.setText("")
        self.pushButton_done.setText(QCoreApplication.translate("MainWindow", u"Done!", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_parameters), QCoreApplication.translate("MainWindow", u"Parameters", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_parameters), QCoreApplication.translate("MainWindow", u"Select parameters to import.", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

