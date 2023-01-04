# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'parametrosdOoDGB.ui'
##
## Created by: Qt User Interface Compiler version 6.0.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(451, 419)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabWidget_abas = QTabWidget(self.centralwidget)
        self.tabWidget_abas.setObjectName(u"tabWidget_abas")
        self.tabWidget_abas.setGeometry(QRect(0, 0, 451, 191))
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.checkBox_mesmaCategoria = QCheckBox(self.tab)
        self.checkBox_mesmaCategoria.setObjectName(u"checkBox_mesmaCategoria")
        self.checkBox_mesmaCategoria.setEnabled(True)
        self.checkBox_mesmaCategoria.setGeometry(QRect(10, 10, 201, 17))
        self.checkBox_mesmaCategoria.setChecked(True)
        self.comboBox_categoriaDestino = QComboBox(self.tab)
        self.comboBox_categoriaDestino.addItem("")
        self.comboBox_categoriaDestino.setObjectName(u"comboBox_categoriaDestino")
        self.comboBox_categoriaDestino.setEnabled(False)
        self.comboBox_categoriaDestino.setGeometry(QRect(240, 30, 191, 22))
        self.comboBox_categoriaOrigem = QComboBox(self.tab)
        self.comboBox_categoriaOrigem.addItem("")
        self.comboBox_categoriaOrigem.setObjectName(u"comboBox_categoriaOrigem")
        self.comboBox_categoriaOrigem.setGeometry(QRect(10, 30, 191, 22))
        self.comboBox_FamiliaOrigem = QComboBox(self.tab)
        self.comboBox_FamiliaOrigem.addItem("")
        self.comboBox_FamiliaOrigem.setObjectName(u"comboBox_FamiliaOrigem")
        self.comboBox_FamiliaOrigem.setGeometry(QRect(10, 80, 191, 22))
        self.comboBox_familiaDestino = QComboBox(self.tab)
        self.comboBox_familiaDestino.addItem("")
        self.comboBox_familiaDestino.setObjectName(u"comboBox_familiaDestino")
        self.comboBox_familiaDestino.setEnabled(False)
        self.comboBox_familiaDestino.setGeometry(QRect(240, 80, 191, 22))
        self.comboBox_parametroOrigem = QComboBox(self.tab)
        self.comboBox_parametroOrigem.addItem("")
        self.comboBox_parametroOrigem.setObjectName(u"comboBox_parametroOrigem")
        self.comboBox_parametroOrigem.setGeometry(QRect(10, 130, 191, 22))
        self.comboBox_parametroDestino_2 = QComboBox(self.tab)
        self.comboBox_parametroDestino_2.addItem("")
        self.comboBox_parametroDestino_2.setObjectName(u"comboBox_parametroDestino_2")
        self.comboBox_parametroDestino_2.setEnabled(True)
        self.comboBox_parametroDestino_2.setGeometry(QRect(240, 130, 191, 22))
        self.checkBox_mesmaFamilia = QCheckBox(self.tab)
        self.checkBox_mesmaFamilia.setObjectName(u"checkBox_mesmaFamilia")
        self.checkBox_mesmaFamilia.setEnabled(True)
        self.checkBox_mesmaFamilia.setGeometry(QRect(10, 60, 221, 17))
        self.checkBox_mesmaFamilia.setChecked(True)
        self.checkBox_familiaInstancia = QCheckBox(self.tab)
        self.checkBox_familiaInstancia.setObjectName(u"checkBox_familiaInstancia")
        self.checkBox_familiaInstancia.setEnabled(True)
        self.checkBox_familiaInstancia.setGeometry(QRect(10, 110, 221, 17))
        self.checkBox_familiaInstancia.setChecked(False)
        self.tabWidget_abas.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.layoutWidget = QWidget(self.tab_2)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(10, 0, 201, 161))
        self.verticalLayout = QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.comboBox_categoriaOrigem2 = QComboBox(self.layoutWidget)
        self.comboBox_categoriaOrigem2.addItem("")
        self.comboBox_categoriaOrigem2.setObjectName(u"comboBox_categoriaOrigem2")

        self.verticalLayout.addWidget(self.comboBox_categoriaOrigem2)

        self.comboBox_familiaOrigem2 = QComboBox(self.layoutWidget)
        self.comboBox_familiaOrigem2.addItem("")
        self.comboBox_familiaOrigem2.setObjectName(u"comboBox_familiaOrigem2")

        self.verticalLayout.addWidget(self.comboBox_familiaOrigem2)

        self.comboBox_parametroOrigem2 = QComboBox(self.layoutWidget)
        self.comboBox_parametroOrigem2.addItem("")
        self.comboBox_parametroOrigem2.setObjectName(u"comboBox_parametroOrigem2")

        self.verticalLayout.addWidget(self.comboBox_parametroOrigem2)

        self.layoutWidget_2 = QWidget(self.tab_2)
        self.layoutWidget_2.setObjectName(u"layoutWidget_2")
        self.layoutWidget_2.setGeometry(QRect(220, 0, 228, 200))
        self.verticalLayout_2 = QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.layoutWidget_2)
        self.label.setObjectName(u"label")

        self.verticalLayout_2.addWidget(self.label)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.textEdit_prefixo = QTextEdit(self.layoutWidget_2)
        self.textEdit_prefixo.setObjectName(u"textEdit_prefixo")

        self.horizontalLayout.addWidget(self.textEdit_prefixo)

        self.spinBox_sufixoNum_sufixo = QSpinBox(self.layoutWidget_2)
        self.spinBox_sufixoNum_sufixo.setObjectName(u"spinBox_sufixoNum_sufixo")

        self.horizontalLayout.addWidget(self.spinBox_sufixoNum_sufixo)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.checkBox_textoLivre = QCheckBox(self.layoutWidget_2)
        self.checkBox_textoLivre.setObjectName(u"checkBox_textoLivre")

        self.verticalLayout_2.addWidget(self.checkBox_textoLivre)

        self.textEdit_valorAplicado = QTextEdit(self.layoutWidget_2)
        self.textEdit_valorAplicado.setObjectName(u"textEdit_valorAplicado")
        self.textEdit_valorAplicado.setEnabled(False)
        self.textEdit_valorAplicado.setMouseTracking(True)

        self.verticalLayout_2.addWidget(self.textEdit_valorAplicado)

        self.tabWidget_abas.addTab(self.tab_2, "")
        self.tableWidget_tabela = QTableWidget(self.centralwidget)
        if (self.tableWidget_tabela.columnCount() < 6):
            self.tableWidget_tabela.setColumnCount(6)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget_tabela.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget_tabela.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget_tabela.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        font = QFont()
        font.setBold(True)
        __qtablewidgetitem3 = QTableWidgetItem()
        __qtablewidgetitem3.setFont(font);
        __qtablewidgetitem3.setBackground(QColor(188, 218, 238));
        self.tableWidget_tabela.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        __qtablewidgetitem4.setFont(font);
        __qtablewidgetitem4.setBackground(QColor(188, 218, 238));
        self.tableWidget_tabela.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        __qtablewidgetitem5.setFont(font);
        __qtablewidgetitem5.setBackground(QColor(188, 218, 238));
        self.tableWidget_tabela.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        if (self.tableWidget_tabela.rowCount() < 3):
            self.tableWidget_tabela.setRowCount(3)
        brush = QBrush(QColor(0, 0, 0, 255))
        brush.setStyle(Qt.NoBrush)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setForeground(brush);
        self.tableWidget_tabela.setVerticalHeaderItem(0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tableWidget_tabela.setVerticalHeaderItem(1, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tableWidget_tabela.setVerticalHeaderItem(2, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(0, 0, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(0, 1, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(0, 2, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(0, 3, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(0, 4, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(0, 5, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(1, 0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(1, 1, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(1, 2, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(1, 3, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(1, 4, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(1, 5, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(2, 0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(2, 1, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(2, 2, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(2, 3, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(2, 4, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.tableWidget_tabela.setItem(2, 5, __qtablewidgetitem26)
        self.tableWidget_tabela.setObjectName(u"tableWidget_tabela")
        self.tableWidget_tabela.setGeometry(QRect(10, 190, 421, 141))
        self.pushButton_ok = QPushButton(self.centralwidget)
        self.pushButton_ok.setObjectName(u"pushButton_ok")
        self.pushButton_ok.setGeometry(QRect(360, 340, 75, 24))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 451, 22))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget_abas.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.checkBox_mesmaCategoria.setText(QCoreApplication.translate("MainWindow", u"Entre par\u00e2metros da mesma categoria", None))
        self.comboBox_categoriaDestino.setItemText(0, QCoreApplication.translate("MainWindow", u"Categoria de Destino", None))

        self.comboBox_categoriaOrigem.setItemText(0, QCoreApplication.translate("MainWindow", u"Categoria", None))

        self.comboBox_FamiliaOrigem.setItemText(0, QCoreApplication.translate("MainWindow", u"Familia/Tipo", None))

        self.comboBox_familiaDestino.setItemText(0, QCoreApplication.translate("MainWindow", u"Familia/Tipo de Destino", None))

        self.comboBox_parametroOrigem.setItemText(0, QCoreApplication.translate("MainWindow", u"Parametro de Origem", None))

        self.comboBox_parametroDestino_2.setItemText(0, QCoreApplication.translate("MainWindow", u"Parametro de Destino", None))

        self.checkBox_mesmaFamilia.setText(QCoreApplication.translate("MainWindow", u"Entre par\u00e2metros da mesma familia", None))
        self.checkBox_familiaInstancia.setText(QCoreApplication.translate("MainWindow", u"Somente familias instanciadas", None))
        self.tabWidget_abas.setTabText(self.tabWidget_abas.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Troca de Valores", None))
        self.comboBox_categoriaOrigem2.setItemText(0, QCoreApplication.translate("MainWindow", u"Categoria", None))

        self.comboBox_familiaOrigem2.setItemText(0, QCoreApplication.translate("MainWindow", u"Familia/Tipo", None))

        self.comboBox_parametroOrigem2.setItemText(0, QCoreApplication.translate("MainWindow", u"Parametro de Origem", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"prefixo + sufixo (valor inicial da sequencia)", None))
        self.textEdit_prefixo.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-style:italic;\">prefixo</span></p></body></html>", None))
        self.spinBox_sufixoNum_sufixo.setPrefix("")
        self.checkBox_textoLivre.setText(QCoreApplication.translate("MainWindow", u"Texto livre", None))
        self.textEdit_valorAplicado.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'Segoe UI'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-style:italic;\">digite o valor a ser aplicado</span></p></body></html>", None))
        self.tabWidget_abas.setTabText(self.tabWidget_abas.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Cria\u00e7\u00e3o de Valores", None))
        ___qtablewidgetitem = self.tableWidget_tabela.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Tipo", None));
        ___qtablewidgetitem1 = self.tableWidget_tabela.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Parametro", None));
        ___qtablewidgetitem2 = self.tableWidget_tabela.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Valor", None));
        ___qtablewidgetitem3 = self.tableWidget_tabela.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"Tipo", None));
        ___qtablewidgetitem4 = self.tableWidget_tabela.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"Parametro", None));
        ___qtablewidgetitem5 = self.tableWidget_tabela.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"Valor aplicado", None));

        __sortingEnabled = self.tableWidget_tabela.isSortingEnabled()
        self.tableWidget_tabela.setSortingEnabled(False)
        ___qtablewidgetitem6 = self.tableWidget_tabela.item(0, 0)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"Porta manuza", None));
        ___qtablewidgetitem7 = self.tableWidget_tabela.item(0, 1)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"Comentario", None));
        ___qtablewidgetitem8 = self.tableWidget_tabela.item(0, 2)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"P10", None));
        ___qtablewidgetitem9 = self.tableWidget_tabela.item(0, 3)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"Porta manuza", None));
        ___qtablewidgetitem10 = self.tableWidget_tabela.item(0, 4)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"Mark", None));
        ___qtablewidgetitem11 = self.tableWidget_tabela.item(0, 5)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"P10", None));
        ___qtablewidgetitem12 = self.tableWidget_tabela.item(1, 0)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"Porta existente", None));
        ___qtablewidgetitem13 = self.tableWidget_tabela.item(1, 1)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"Comentario", None));
        ___qtablewidgetitem14 = self.tableWidget_tabela.item(1, 2)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"F12", None));
        ___qtablewidgetitem15 = self.tableWidget_tabela.item(1, 3)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"Porta existente", None));
        ___qtablewidgetitem16 = self.tableWidget_tabela.item(1, 4)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"Mark", None));
        ___qtablewidgetitem17 = self.tableWidget_tabela.item(1, 5)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"F12", None));
        ___qtablewidgetitem18 = self.tableWidget_tabela.item(2, 0)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"Porta corta fogo", None));
        ___qtablewidgetitem19 = self.tableWidget_tabela.item(2, 1)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"Comentario", None));
        ___qtablewidgetitem20 = self.tableWidget_tabela.item(2, 2)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"P20", None));
        ___qtablewidgetitem21 = self.tableWidget_tabela.item(2, 3)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"Porta corta fogo", None));
        ___qtablewidgetitem22 = self.tableWidget_tabela.item(2, 4)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"Mark", None));
        ___qtablewidgetitem23 = self.tableWidget_tabela.item(2, 5)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"P20", None));
        self.tableWidget_tabela.setSortingEnabled(__sortingEnabled)

        self.pushButton_ok.setText(QCoreApplication.translate("MainWindow", u"OK", None))
    # retranslateUi

