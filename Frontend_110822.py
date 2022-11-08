# Zayn Severance, last updated 10/13/2022
# Frontend.py
# Handles the frontend completely in PyQt5, be sure to use this and not PyQt6!
# Yes, this is what you get when a backend guy makes a frontend.

import sys
from os.path import expanduser
from os.path import isdir

# import ctypes
# import Backend as BE
myappid = 'gitgud.contxt.ver1.0'  # arbitrary string
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
from PyQt5 import QtCore, QtGui, QtWidgets

if 1:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *

import SearchEngine as searchEng
import pandas as pd

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

'''
The below code is from Github user DataSolveProblems: Display Pandas DataFrame
'''

'''
class DataFrameModel(QtCore.QAbstractTableModel):
    DtypeRole = QtCore.Qt.UserRole + 1000
    ValueRole = QtCore.Qt.UserRole + 1001

    def __init__(self, df=pd.DataFrame(), parent=None):
        super(DataFrameModel, self).__init__(parent)
        self._dataframe = df

    def setDataFrame(self, dataframe):
        self.beginResetModel()
        self._dataframe = dataframe.copy()
        self.endResetModel()

    def dataFrame(self):
        return self._dataframe

    dataFrame = QtCore.pyqtProperty(pd.DataFrame, fget=dataFrame, fset=setDataFrame)

    @QtCore.pyqtSlot(int, QtCore.Qt.Orientation, result=str)
    def headerData(self, section: int, orientation: QtCore.Qt.Orientation, role: int = QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                return self._dataframe.columns[section]
            else:
                return str(self._dataframe.index[section])
        return QtCore.QVariant()

    def rowCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._dataframe.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        if parent.isValid():
            return 0
        return self._dataframe.columns.size

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < self.rowCount() and 0 <= index.column() < self.columnCount()):
            return QtCore.QVariant()
        row = self._dataframe.index[index.row()]
        col = self._dataframe.columns[index.column()]
        dt = self._dataframe[col].dtype

        val = self._dataframe.iloc[row][col]
        if role == QtCore.Qt.DisplayRole:
            return str(val)
        elif role == DataFrameModel.ValueRole:
            return val
        if role == DataFrameModel.DtypeRole:
            return dt
        return QtCore.QVariant()

    def roleNames(self):
        roles = {
            QtCore.Qt.DisplayRole: b'display',
            DataFrameModel.DtypeRole: b'dtype',
            DataFrameModel.ValueRole: b'value'
        }
        return roles
'''

class Ui_MainWindow(QtWidgets.QMainWindow):
    ANDS = ""
    ORS = ""
    NOTS = ""
    num1 = 0
    num2 = 0
    num3 = 0

    def __init__(self, window2=None):
        super(Ui_MainWindow, self).__init__()
        self.directory_path = expanduser('~')
        self.setWindowIcon(QtGui.QIcon('Icon.png'))
        self.setObjectName("contxt")
        self.resize(500, 600)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(130, 160, 131, 22))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(130, 210, 131, 22))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(130, 260, 131, 22))
        self.lineEdit_3.setObjectName("lineEdit_3")

        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(300, 160, 42, 22))
        self.spinBox.setObjectName("spinBox")
        self.spinBox_2 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_2.setGeometry(QtCore.QRect(300, 210, 42, 22))
        self.spinBox_2.setObjectName("spinBox_2")
        self.spinBox_3 = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox_3.setGeometry(QtCore.QRect(300, 260, 42, 22))
        self.spinBox_3.setObjectName("spinBox_3")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(130, 320, 211, 28))
        self.pushButton.setObjectName("pushButton")

        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.setWindowTitle("contxt")
        self.pushButton.setText("Search")

        self.directory_path_label = QtWidgets.QLabel(self.centralwidget)
        self.directory_path_label.setFrameStyle(QFrame.Panel)
        self.directory_path_label.setGeometry(QtCore.QRect(130,125,211,28))
        self.directory_path_label.setFont(QFont("Times New Roman",15))
        self.directory_path_label.setText(self.directory_path)
        self.directory_path_label.adjustSize()

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 120, 100, 28))
        self.pushButton_2.setObjectName("directory")
        self.pushButton_2.setText("Directory")

        # TODO: Change the setMaximum to 1 when type is
        #       set to Document
        self.or_type = QtWidgets.QComboBox(self.centralwidget)
        self.or_type.addItems(["Word","Page","Document"])
        self.or_type.setGeometry(QtCore.QRect(350,210,120,22))
        self.not_type = QtWidgets.QComboBox(self.centralwidget)
        self.not_type.addItems(["Word","Page","Document"])
        self.not_type.setGeometry(QtCore.QRect(350,260,120,22))

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(150, 10, 801, 91))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(60)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label.setText("contxt.")

        QtCore.QMetaObject.connectSlotsByName(self)

        # lines for handling added manually
        self.pushButton.clicked.connect(self.search_button_clicked)
        self.pushButton_2.clicked.connect(self.directory_button_clicked)
        self._window2 = window2

    def directory_button_clicked(self):
        self.directory_path = QFileDialog.getExistingDirectory(
            self,
            caption="Select a directory"
        )
        self.directory_path_label.setText(self.directory_path)
        self.directory_path_label.adjustSize()

    # button handle
    def search_button_clicked(self):
        print("click")
        ANDS = self.lineEdit.text()
        ORS = self.lineEdit_2.text()
        NOTS = self.lineEdit_3.text()
        num1 = int(self.spinBox.text())
        num2 = int(self.spinBox_2.text())
        num3 = int(self.spinBox_3.text())
        # dir_path = self.lineEdit_4.text()
        # OR_type = self.lineEdit_5.text()
        # NOT_type = self.lineEdit_6.text()
        # print(self.folder_path)

        print("query:", ANDS, "range", num1, ORS, "range", num2, NOTS, "range", num3)
        self.hide()

        # TODO: hard-coded user inputs; obv change once fully integrated with UI
        dir_path = str(self.directory_path)
        print(dir_path)
        type_dictionary = {
            "Word" : "byWORD",
            "Page" : "byPAGE",
            "Document" : "byDOC"
        }
        print(type_dictionary[str(self.or_type.currentText())])
        OR_type = type_dictionary[str(self.or_type.currentText())]
        NOT_type = type_dictionary[str(self.not_type.currentText())]
        case_sens = False

        # self.hide()
        # if self._window2 is None:
        #     self._window2 = Ui_Results(self)
        # # I would expect your function for grabbing data to be somewhere around here
        # self._window2.setText()
        # self._window2.show()

        search_params = {
            'ANDS': ANDS,
            'ORS': ORS,
            'NOTS': NOTS,
            'rad1': num1,
            'rad2': num2,
            'rad3': num3,
            'OR_srch_type': OR_type,
            'NOT_srch_type': NOT_type,
            'dir_path': dir_path,
            'case_sens': case_sens
        }
        SearchObj = searchEng.SearchEngine(search_params)

        EOS_flag = False  # EOS = End-of-Search
        k = 0
        while not EOS_flag:
            print('{}th run into search_next():'.format(k))
            results_df, EOS_flag = SearchObj.search_next()
            k += 1
            if k==1:
                # if self._window2 is None:
                self._window2 = Ui_Results(self, results_df)
                # I would expect your function for grabbing data to be somewhere around here
                self._window2.setText()
                self._window2.show()
                print('df size is: {}'.format(len(results_df)))
            else:
                self._window2.populateTable(results_df)

class Ui_Results(QtWidgets.QMainWindow):
    def __init__(self, window1=None, results_df=None):
        super(Ui_Results, self).__init__()

        self.data = pd.DataFrame()
        self.df_colNames_resultsWindow = ['fpath', 'fname', 'AND_keyword', 'doc_AND_score', 'page_number',
                                          'text_short', 'text_long', 'search_score']
        self.debug_row_count = results_df.shape[0]

        gridLayout = QtWidgets.QGridLayout()

        self.setWindowIcon(QtGui.QIcon('Icon.png'))
        self.setObjectName("contxt")
        self.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(len(self.df_colNames_resultsWindow))  # 8 length
        self.tableWidget.setRowCount(self.debug_row_count)  # 10 length
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.pushButton = QtWidgets.QPushButton('pushButton')
        self.pushButton.setObjectName("pushButton")
        self.setCentralWidget(self.centralwidget)

        self.pushButton.setText("Modify Search")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 10, 801, 91))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)

        self.label.setFont(font)
        self.label.setObjectName("label")

        self.setWindowTitle("contxt")
        self.centralwidget.setLayout(gridLayout)
        gridLayout.addWidget(self.label, 0, 0, 1, 3)
        gridLayout.addWidget(self.pushButton, 0, 4, 1, 1)
        gridLayout.addWidget(self.tableWidget, 1, 0, 4, 4)

        # added code for button handle
        self.pushButton.clicked.connect(self.button_clicked)
        self._window1 = window1
        print("Made window 2")
        self.populateTable(results_df)

        # self.populateTable(pd.DataFrame())

    # return to other menu
    def button_clicked(self):
        self.hide()
        if self._window1 is None:
            self._window1 = Ui_MainWindow(self)
        self._window1.show()

    # this is where you would put your data to fill the result table
    # Yes, this is for you Matt!
    def populateTable(self, results_df):
        # grab data from the backend to populate this table
        # use the table population function to fill it in
        self.tableWidget.setRowCount(results_df.shape[0]) # shape[0] is df rows
        self.tableWidget.setColumnCount(results_df.shape[1]) # shape[1] is df columns
        self.tableWidget.setHorizontalHeaderLabels(self.df_colNames_resultsWindow)

        for row in range(self.debug_row_count):
            for col in range(len(self.df_colNames_resultsWindow)):
                item = results_df.iloc[row,col]
                self.tableWidget.setItem(row,col,QtWidgets.QTableWidgetItem(str(item)))

    # This class updates the search text label
    def setText(self):
        text = "Results for ANDS " + self._window1.lineEdit.text() + " DIST " + self._window1.spinBox.text() + \
               ", ORS " + self._window1.lineEdit_2.text() + " DIST " + self._window1.spinBox_2.text() + \
               " NOTS " + self._window1.lineEdit_3.text() + " DIST " + self._window1.spinBox_3.text()
        self.label.setText(text)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    win = Ui_MainWindow()
    win.show()
    sys.exit(app.exec())
