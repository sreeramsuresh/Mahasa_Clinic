import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLineEdit, QPushButton, QGridLayout
import sqlite3


# Mainwindow
class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("Welcome.ui", self)
        self.setWindowTitle("Jambakka")
        self.Loginbt.clicked.connect(self.gotoscreen5)

    # Calling login page ui through Screen5 class
    def gotoscreen5(self):
        screen5 = Screen5()
        Widget.addWidget(screen5)
        Widget.setCurrentIndex(Widget.currentIndex() + 1)


# Login page
class Screen5(QDialog):
    def __init__(self):
        super(Screen5, self).__init__()
        loadUi("LoginPage.ui", self)
        self.UPLogin.clicked.connect(self.logininfo)
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)

    # User name and password validation
    def logininfo(self):
        user = self.emailField.text()
        password = self.passwordField.text()

        if len(user) == 0 or len(password) == 0:
            self.error.setText("Please input all field.")

        else:
            conn = sqlite3.connect('test.sqlite')
            cur = conn.cursor()
            query = 'SELECT Password FROM login_info WHERE UserName = ?'
            cur.execute(query, [(user)])
            result_pass = cur.fetchone()

            if result_pass is None:
                self.error.setText("Please enter the correct username or password")
            else:
                result_pass = result_pass[0]
            if result_pass == password:
                self.gotoscreen4()
                self.error.setText("")
            else:
                self.error.setText("Please enter the correct username or password")

    # Once the verification passed calling Home Page ui
    def gotoscreen4(self):
        screen4 = Screen4()
        Widget.addWidget(screen4)
        Widget.setCurrentIndex(Widget.currentIndex() + 1)


# Home Page of User
class Screen4(QDialog):
    def __init__(self):
        super(Screen4, self).__init__()
        loadUi("Home Page.ui", self)
        self.NRbutton.clicked.connect(self.gotoscreen2)
        self.ABbutton.clicked.connect(self.gotoscreen3)
        self.NewUser.clicked.connect(self.gotoscreen6)
        self.Logout.clicked.connect(self.gotoscreen5)
        QtCore.QTimer.singleShot(10000, self.gotoscreen5)

    # Calling Login page ui through Screen2 class
    def gotoscreen5(self):
        screen5 = Screen5()
        Widget.addWidget(screen5)
        Widget.setCurrentIndex(Widget.currentIndex() + 1)

    # Calling New Reg page ui through Screen2 class
    def gotoscreen2(self):
        screen2 = Screen2()
        Widget.addWidget(screen2)
        Widget.setCurrentIndex(Widget.currentIndex() + 1)

    # Calling Address Book page ui through Screen3 class
    def gotoscreen3(self):
        screen3 = Screen3()
        Widget.addWidget(screen3)
        Widget.setCurrentIndex(Widget.currentIndex() + 1)

    # Calling New User creation page ui through Screen6 class
    def gotoscreen6(self):
        screen6 = Screen6()
        Widget.addWidget(screen6)
        Widget.setCurrentIndex(Widget.currentIndex() + 1)

        # self.NRbutton_2.clicked.connect(self.MainWindow)
        # self.NRbutton.clicked.connect(self.gotoscreen2)

    # def MainWindow(self):
    #     mainwindow = MainWindow()
    #     Widget.addWidget(mainwindow)
    #     Widget.setCurrentIndex(Widget.currentIndex() + 1)

    # def loaddata(self):
    #     connection = sqlite3.connect("test.sqlite")
    #     cur = connection.cursor()
    #     sqlquery = "SELECT * FROM susu limit 10"

    #     self.tableWidget.setRowCount(10)
    #     tablerow = 0

    #     for row in cur.execute(sqlquery):
    #         self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
    #         self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
    #         self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
    #         tablerow+=1


# New User Page of User entry
class Screen6(QDialog):
    def __init__(self):
        super(Screen6, self).__init__()
        loadUi("New User.ui", self)
        self.NRbutton_2.clicked.connect(self.gotoscreen4)
        self.UPLogin.clicked.connect(self.userCreation)
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)

    # Calling Home Page ui through Screen4 class
    def gotoscreen4(self):
        screen4 = Screen4()
        Widget.addWidget(screen4)
        Widget.setCurrentIndex(Widget.currentIndex() + 1)

    # User creation
    def userCreation(self):
        user = self.emailField.text()
        password = self.passwordField.text()
        cpassword = self.cpasswordField.text()

        if len(user) == 0 or len(password) == 0 or len(cpassword) == 0:
            self.error.setText("Please input all field.")

        elif password != cpassword:
            self.error.setText("Password not matching")
        # else:
        #     self.error.setText("Successfully " + user + " created")
        #     self.emailField.clear()
        #     self.passwordField.clear()
        #     self.cpasswordField.clear()

        elif password == cpassword and len(cpassword) != 0 and len(cpassword) == 4:
            # Connecting to sqlite
            conn = sqlite3.connect('test.sqlite')
            cursor = conn.cursor()
            query = 'SELECT * FROM login_info WHERE UserName = ?'
            cursor.execute(query, [(user)])
            # result_pass = cursor.fetchone()
            if cursor.fetchone():
                self.error.setText("Please select a different user name.")
            else:

                # Creating a cursor object using the
                cursor.execute("INSERT INTO login_info (UserName, Password) VALUES (?, ?)", (user, password))
                conn.commit()
                conn.close()
                self.error.setText("Successfully " + user + " created")
                self.emailField.clear()
                self.passwordField.clear()
                self.cpasswordField.clear()
        elif len(cpassword) != 4:
            self.error.setText("Password minimum 4 characters required!")
        else:
            self.error.setText("")


# New Reg Page of User entry
class Screen2(QDialog):
    def __init__(self):
        super(Screen2, self).__init__()
        loadUi("New Reg.ui", self)
        self.NRbutton_2.clicked.connect(self.gotoscreen4)
        self.ABbutton.clicked.connect(self.gotoscreen3)

        self.Submit.clicked.connect(self.clickMethod)
        self.www.clicked.connect(self.clearMethod)

        # Connecting to sqlite
        conn = sqlite3.connect('test.sqlite')
        cursor = conn.cursor()

        cursor.execute("SELECT OPNumber FROM susu ORDER BY OPNumber DESC LIMIT 1")
        opnUMBER = cursor.fetchone()[-1]
        self.oNumberl.setNum(opnUMBER +1)
        conn.commit()
        conn.close()

    def clearMethod(self):
        self.lFuNa.clear()
        self.lAge.clear()
        self.lPiCo.clear()
        self.lAddre.clear()
        self.lPhNu.clear()

    def clickMethod(self):
        if self.Gmale.isChecked():
            lGender = "Male"
        elif self.GFem.isChecked():
            lGender = "Female"
        elif self.Goth.isChecked():
            lGender = "Other"
        else:
            pass

        lFullName = self.lFuNa.text()
        lAge = self.lAge.text()
        lOPNumber = int(self.oNumberl.text())
        lOPNum = lOPNumber
        lAddress = self.lAddre.toPlainText()
        lPincode = self.lPiCo.text()
        lPhoneNumber = self.lPhNu.text()

        if len(lFullName) == 0:
            self.fNamel.setText("Please input the full name field.")
        elif len(lAddress) == 0:
            self.addressl.setText("Please input the address field.")
            self.fNamel.setText("")
        elif len(lPhoneNumber) == 0:
            self.phoneNumberl.setText("Please input the phone number field.")
            self.fNamel.setText("")
            self.addressl.setText("")
        else:
            self.phoneNumberl.setText("")
            # Connecting to sqlite
            conn = sqlite3.connect('test.sqlite')
            cursor = conn.cursor()

            # Creating a cursor object using the
            cursor.execute(
                "INSERT INTO susu (FullName, Gender, Age, OPNumber, Address, Pincode, PhoneNumber) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (lFullName, lGender, lAge, lOPNum, lAddress, lPincode, lPhoneNumber))

            conn.commit()
            conn.close()


            self.lFuNa.clear()
            self.lAge.clear()
            self.lPiCo.clear()
            self.lAddre.clear()
            self.lPhNu.clear()

            # Connecting to sqlite
            conn = sqlite3.connect('test.sqlite')
            cursor = conn.cursor()

            cursor.execute("SELECT OPNumber FROM susu ORDER BY OPNumber DESC LIMIT 1")
            opnUMBER = cursor.fetchone()[-1]
            self.oNumberl.setNum(opnUMBER)
            conn.commit()
            conn.close()


            # Connecting to sqlite
            conn = sqlite3.connect('test.sqlite')
            cursor = conn.cursor()

            sqlquery = "SELECT * FROM susu ORDER BY OPNumber DESC LIMIT 1"

            self.tableWidget.setRowCount(1)
            tablerow = 0

            for row in cursor.execute(sqlquery):
                self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[4]))
                self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[5]))
                self.tableWidget.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(row[6]))
                tablerow+=1

            conn.commit()
            conn.close()
            self.oNumberl.setNum(opnUMBER +1)

    # Calling Home Page ui through Screen4 class
    def gotoscreen4(self):
        screen4 = Screen4()
        Widget.addWidget(screen4)
        Widget.setCurrentIndex(Widget.currentIndex() + 1)

    # Calling Address Book page ui through Screen3 class
    def gotoscreen3(self):
        screen3 = Screen3()
        Widget.addWidget(screen3)
        Widget.setCurrentIndex(Widget.currentIndex() + 1)


# Home Page of User Search
class Screen3(QDialog):
    def __init__(self):
        super(Screen3, self).__init__()
        loadUi("Address Book.ui", self)
        self.NRbutton_2.clicked.connect(self.gotoscreen4)
        self.NRbutton.clicked.connect(self.gotoscreen2)
        self.Submit.clicked.connect(self.searchMethod)
        self.www.clicked.connect(self.clearMethod)

    def clearMethod(self):
        self.lFuNa.clear()
        self.lAge.clear()
        self.lPiCo.clear()
        self.lAddre.clear()
        self.lPhNu.clear()

    def searchMethod(self):

        lFullName = self.lFuNa.text()
        lAge = self.lAge.text()
        lOPNumber = self.lOPNu.text()
        lAddress = self.lAddre.toPlainText()
        lPincode = self.lPiCo.text()
        lPhoneNumber = self.lPhNu.text()

        if len(lFullName) != 0:
            # Connecting to sqlite
            conn = sqlite3.connect('test.sqlite')
            cursor = conn.cursor()

            query = "SELECT * FROM susu WHERE FullName = ?"
            self.tableWidget.setRowCount(50)
            tablerow = 0

            for row in cursor.execute(query, [lFullName]):
                self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[4]))
                self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[5]))
                self.tableWidget.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(row[6]))
                tablerow+=1

            conn.commit()
            conn.close()
            self.error.setText("")
        elif lOPNumber != "":
            # Connecting to sqlite
            conn = sqlite3.connect('test.sqlite')
            cursor = conn.cursor()

            query = "SELECT * FROM susu WHERE OPNumber = ?"
            self.tableWidget.setRowCount(50)
            tablerow = 0

            for row in cursor.execute(query, [lOPNumber]):
                self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[4]))
                self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[5]))
                self.tableWidget.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(row[6]))
                tablerow+=1

            conn.commit()
            conn.close()
            self.error.setText("")
        elif len(lPhoneNumber) != 0:
            # Connecting to sqlite
            conn = sqlite3.connect('test.sqlite')
            cursor = conn.cursor()

            query = "SELECT * FROM susu WHERE PhoneNumber = ?"
            self.tableWidget.setRowCount(50)
            tablerow = 0

            for row in cursor.execute(query, [lPhoneNumber]):
                self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(row[2]))
                self.tableWidget.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(row[3]))
                self.tableWidget.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(row[4]))
                self.tableWidget.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(row[5]))
                self.tableWidget.setItem(tablerow, 6, QtWidgets.QTableWidgetItem(row[6]))
                tablerow+=1

            conn.commit()
            conn.close()
            self.error.setText("")
        else:
            self.error.setText("Please fill Fullname/OP Number/Phone Number")
        
        # search_box_get = self.tableWidget.item(row, 1)
        # print (search_box_get)



    # Calling Home Page ui through Screen4 class
    def gotoscreen4(self):
        screen4 = Screen4()
        Widget.addWidget(screen4)
        Widget.setCurrentIndex(Widget.currentIndex() + 1)

    # Calling New Reg page ui through Screen2 class
    def gotoscreen2(self):
        screen2 = Screen2()
        Widget.addWidget(screen2)
        Widget.setCurrentIndex(Widget.currentIndex() + 1)


# main
app = QApplication(sys.argv)
Widget = QtWidgets.QStackedWidget()
mainwindow = MainWindow()
Widget.addWidget(mainwindow)
Widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
