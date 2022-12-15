import sqlite3
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from sys import argv
db=sqlite3.connect("nagelDB.db")
cr= db.cursor()

from designer import Ui_MainWindow as Designer
from windowTwo import Ui_Form as WindowTwo
from windowThree import Ui_Form as WindowThree
from windowFour import Ui_Form as WindowFour
#cr.execute(''' INSERT INTO termins VALUES ('Yasser', 10,'2023-1-26','1:10')''')
# cr.execute(''' CREATE TABLE IF NOT EXISTS customers(name TEXT,
#                                                     visits INTEGER,
#                                                     datum DATE,
#                                                     pay INTEGER) ''')
#cr.execute(''' CREATE TABLE IF NOT EXISTS termins(
#                                                 name TEXT,
#                                                 visits INTEGER,
#                                                 datum DATE
#                                                 gift TEXT)''')
###########################################################################################
class windowTwo(QMainWindow,WindowTwo):
    def __init__(self):
        super().__init__()
        loadUi('windowTwo.ui',self)
        self.setWindowTitle("new Termin")
        self.buttonBox.accepted.connect(self.addCustomer)
        self.buttonBox.rejected.connect(self.close)
    def messageBox(self,msg):
        dialog=QMessageBox(self)
        dialog.setText(msg)
        dialog.setWindowTitle('Done')
        dialog.setIcon(dialog.Information)
        dialog.exec_()
    def addCustomer(self):
        name=self.lineEdit.text()
        name=str(name).capitalize().split()
        year=self.dateEdit.date().year()
        year=str(year)
        month=self.dateEdit.date().month()
        month=str(month)
        day=self.dateEdit.date().day()
        day=str(day)
        date= year+'-'+month+'-'+day
        hour=self.timeEdit.time().hour()
        hour=str(hour)
        minute=self.timeEdit.time().minute()
        minute=str(minute)
        time=hour+':'+minute
        list=[]
        cr.execute('''SELECT name FROM termins ''')
        for i in cr.fetchall():
            count=0
            list.append(i[count])
            count+=1
        print(list)
        if name[0] in list:
            print('the name is in list')
            cr.execute('''UPDATE termins SET datum=?, visits= visits+1, uhr=? WHERE name=? ''',(date, time,name[0]))
            db.commit()
            self.messageBox('Termin hinzugefügt')
        else:
            print('the name is NOT in list')
            cr.execute('''INSERT INTO termins VALUES(?,?,?,?)''',(name[0],1,date, time))
            db.commit()
            self.messageBox('Termin hinzugefügt')
class windowThree(QMainWindow,WindowThree):
    def __init__(self):
        super().__init__()
        loadUi('windowThree.ui',self)
        self.setWindowTitle("Remove Termin")
        self.buttonBox.accepted.connect(self.remove)
        self.buttonBox.rejected.connect(self.hide)
        cr.execute(''' SELECT name From termins''')
        kunde=cr.fetchall()
        list=[]
        for i in kunde:
            list.append(i[0])
        self.comboBox.addItems(list)
    def remove(self):
        name=self.comboBox.currentText()
        name=str(name)
        cr.execute('''UPDATE termins SET datum ='---', visits = visits-1, uhr ='---' WHERE name=? ''', (name,))
        db.commit()
        windowTwo.messageBox(self,'Termin Removed')
class windowFour(QMainWindow,WindowFour):
    def __init__(self):
        super().__init__()
        loadUi('windowFour.ui',self)
        self.setWindowTitle("Update Termin")
        cr.execute(''' SELECT name From termins''')
        kunde=cr.fetchall()
        list=[]
        for i in kunde:
            list.append(i[0])
        self.comboBox.addItems(list)
        self.buttonBox.accepted.connect(self.updateKunde)
        self.buttonBox.rejected.connect(self.hide)
    def updateKunde(self):
        name=self.comboBox.currentText()
        name=str(name)
        cr.execute(''' ''')
        year=self.dateEdit.date().year()
        year=str(year)
        month=self.dateEdit.date().month()
        month=str(month)
        day=self.dateEdit.date().day()
        day=str(day)
        date= year+'-'+month+'-'+day
        hour=self.timeEdit.time().hour()
        hour=str(hour)
        minute=self.timeEdit.time().minute()
        minute=str(minute)
        time=hour+':'+minute
        cr.execute('''UPDATE termins SET datum=?, uhr=? WHERE name=? ''',(date, time,name))
        db.commit()
        windowTwo.messageBox(self,'Termin updated')
class mainWindow(QMainWindow,Designer):
    def __init__(self):
        super().__init__()
        loadUi('designer.ui',self)
        self.setWindowTitle('Nagel Studio')
        self.pushButton.clicked.connect(self.windowTwo)
        self.pushButton_2.clicked.connect(self.windowThree)
        self.pushButton_3.clicked.connect(self.windowFour)
        self.showList()
    def showList(self):
        cr.execute(''' SELECT name,datum,uhr,visits FROM termins WHERE datum > date('now')''')
        kunden=cr.fetchall()
        count=0
        print(kunden)
        self.tableWidget.setRowCount(len(kunden))
        for i in kunden:
            self.tableWidget.setItem(count,0,QTableWidgetItem(i[0]))
            self.tableWidget.setItem(count,1,QTableWidgetItem(i[1]))
            self.tableWidget.setItem(count,2,QTableWidgetItem(i[2]))
            if i[3]%5==0:
                self.tableWidget.setItem(count,3,QTableWidgetItem('YES'))
            else:
                self.tableWidget.setItem(count,3,QTableWidgetItem('NO'))
            count+=1
    def windowTwo(self):    
        self.w = windowTwo()
        self.w.show()
        #self.hide()    
    def windowThree(self):            
        self.w = windowThree()
        self.w.show()
        #self.hide()
    def windowFour(self):                    
        self.w = windowFour()
        self.w.show()
        #self.hide()
if __name__ == "__main__":
    app=QApplication(argv)
    window = mainWindow()
    window.show()
app.exec_()
db.commit()
db.close()