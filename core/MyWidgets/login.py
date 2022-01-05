#!/usr/bin/python3.6
# coding=utf-8
"""
:Copyright: © 2021 Advanced Control Systems, Inc. All Rights Reserved.
"""
__author__ = 'Stephen Hung, Darren Liang'

import sys, os
from acsQt import buttons
from QtCompat import QtWidgets, QtGui, QtCore, Slot, Qt
from acstw.OracleInterface import OracleInterface

from acsQt.LoginTab.register import registerTab
from acsQt.LoginTab.manage   import manageTab
from acsQt.LoginTab.password import resetPwdTab
from acsQt.LoginTab.role     import roleTab
# from Login_reg import Register_Form

PRISMdb = OracleInterface('acs_adms', 'acspower', os.getenv('ORACLE_DBSTRING'))

class LoginForm(QtWidgets.QDialog):
    def __init__(self, parent=None, account=None):
        super().__init__(parent)
        self.setWindowTitle('ACS App Login')

        self._account  = None
        self._password = None
        self._output   = None

        # declare widget
        self.le_account   = QtWidgets.QLineEdit(self)
        self.le_password  = QtWidgets.QLineEdit(self)
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        self.settings  = QtWidgets.QPushButton(self)
        FormLayout     = QtWidgets.QFormLayout(self)
        HBoxLayout     = QtWidgets.QHBoxLayout()
        SpacerItem     = QtWidgets.QSpacerItem(0,0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # disclude entering symbols
        self.le_account  = self.setLineEditRule(self.le_account)
        self.le_password = self.setLineEditRule(self.le_password)

        # widget properities settings
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText('Submit')
        self.le_password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.settings.setFixedSize(30,30)
        buttons.set_button_attributes(self.settings, icon="settings_icon.png", slot=self.login_settings_page)

        # layout settings
        HBoxLayout.addWidget(self.settings)
        HBoxLayout.addItem(SpacerItem)
        HBoxLayout.addWidget(self.buttonBox)

        FormLayout.addRow("Account :", self.le_account)
        FormLayout.addRow("Password:", self.le_password)
        FormLayout.addRow(HBoxLayout)

        # event settings
        self.buttonBox.accepted.connect(self.submit)
        self.buttonBox.rejected.connect(self.cancel)
        self.le_account.textEdited.connect(self.set_account)
        self.le_account.textEdited.connect(self.set_button_state)
        
        self.le_password.textEdited.connect(self.set_password)
        self.le_password.textEdited.connect(self.set_button_state)

        if account is not None: self.le_account.setText(account)
    
    @property
    def account(self):
        return self._account

    @property
    def password(self):
        return self._password

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, new_output):
        # print("new_output",new_output)
        if new_output is None or len(new_output) < 0:
            self._output = (self.account, 0, None, None)
        else:
            self._output = new_output

    def set_account(self, value):
        self._account = value
    
    def set_password(self, value):
        self._password = value

    def submit(self):
        account  = str(self.account)
        password = str(self.password)
        response = self.verify_user(account, password)
        
        # authenticate user
        if response is not None and response[1] == 0:
            QtWidgets.QMessageBox.warning(self, "Warning", "Incorrect ID, password or account disabled!")
            self.output = None
        else:
            self.accept()
            self.output = response

    def cancel(self):
        QtWidgets.QMessageBox.warning(self, "Warning", "Login cancelled!")
        self.output = None
        self.reject()

    def verify_user(self, acc, pwd):
        query = f"SELECT ACCOUNT, VERIFY_USER('{acc}', '{pwd}') STATUS, AUTH FROM VD_USER WHERE ACCOUNT='{acc}'"
        data  = PRISMdb.ExecQuery(query)
        return data[0] + (pwd,) if len(data)>0 else None
        
    def set_button_state(self):
        account   = len(self.le_account.text())  > 0
        password  = len(self.le_password.text()) > 0
        condition = (account and password)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(condition)
        
    def setLineEditRule(self, lineedit):
        regex=QtCore.QRegExp(u"[0-9A-Za-z._]+")
        validator = QtGui.QRegExpValidator(regex)
        lineedit.setValidator(validator)
        return lineedit
        
    def closeEvent(self, event):
        self.output = None
        self.reject()
        
    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Escape:
            self.output = None
            self.reject()
        elif event.key()==QtCore.Qt.Key_Return or event.key()==QtCore.Qt.Key_Enter:
            account   = len(self.le_account.text())  > 0
            password  = len(self.le_password.text()) > 0
            condition = (account and password)
            if condition: self.submit()

    def login_settings_page(self):
        form = SettingsForm(self)
        form.exec_()

class SettingsForm(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('ACS Login Settings')
        self.parent    = parent
        self._account  = None
        self._password = None
        self._output   = None

        # declare widget
        self.le_account   = QtWidgets.QLineEdit(self)
        self.le_password  = QtWidgets.QLineEdit(self)
        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel, self)
        FormLayout     = QtWidgets.QFormLayout(self)
        HBoxLayout     = QtWidgets.QHBoxLayout()
        SpacerItem     = QtWidgets.QSpacerItem(0,0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # disclude entering symbols
        self.le_account  = self.setLineEditRule(self.le_account)
        self.le_password = self.setLineEditRule(self.le_password)

        # widget properities settings
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setText('Submit')
        self.le_password.setEchoMode(QtWidgets.QLineEdit.Password)

        # layout settings

        HBoxLayout.addItem(SpacerItem)
        HBoxLayout.addWidget(self.buttonBox)

        FormLayout.addRow("Account :", self.le_account)
        FormLayout.addRow("Password:", self.le_password)
        FormLayout.addRow(HBoxLayout)

        # event settings
        self.buttonBox.accepted.connect(self.submit)
        self.buttonBox.rejected.connect(self.cancel)
        self.le_account.textEdited.connect(self.set_account)
        self.le_account.textEdited.connect(self.set_button_state)
        
        self.le_password.textEdited.connect(self.set_password)
        self.le_password.textEdited.connect(self.set_button_state)
    
    @property
    def account(self):
        return self._account

    @property
    def password(self):
        return self._password

    @property
    def output(self):
        return self._output

    @output.setter
    def output(self, new_output):
        if new_output is None or len(new_output) < 0:
            self._output = (self.account, False, None, None)
        else:
            self._output = new_output

    def set_account(self, value):
        self._account = value
    
    def set_password(self, value):
        self._password = value

    def submit(self):
        account  = str(self.account)
        password = str(self.password)
        response = self.verify_user(account, password)

        # authenticate user
        if response is not None and response[1] == 0:
            QtWidgets.QMessageBox.warning(self, "Warning", "Incorrect ID, password or account disabled!")
        else:
            self.close()
            form = ManageForm(self.parent, response)
            form.exec_()

    def cancel(self):
        QtWidgets.QMessageBox.warning(self, "Warning", "Login settings page cancelled!")
        self.output = None
        self.reject()

    def verify_user(self, acc, pwd):
        query = f"SELECT ACCOUNT, VERIFY_USER('{acc}', '{pwd}') STATUS, AUTH FROM VD_USER WHERE ACCOUNT='{acc}'"
        data  = PRISMdb.ExecQuery(query)
        return data[0] + (pwd,) if len(data)>0 else None
        
    def set_button_state(self):
        account   = len(self.le_account.text())  > 0
        password  = len(self.le_password.text()) > 0
        condition = (account and password)

        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(condition)
        
    def setLineEditRule(self, lineedit):
        regex=QtCore.QRegExp(u"[0-9A-Za-z]+")
        validator = QtGui.QRegExpValidator(regex)
        lineedit.setValidator(validator)
        return lineedit
        
    def closeEvent(self, event):
        self.output = None
        self.reject()
        
    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Return: 
            self.submit()
        if event.key()==QtCore.Qt.Key_Enter : 
            self.submit()
        if event.key()==QtCore.Qt.Key_Escape:
            self.reject()

class ManageForm(QtWidgets.QDialog):
    def __init__(self, parent, dataSet):
        super(ManageForm, self).__init__(parent)

        # dialog properties
        self.setWindowTitle("APP Account Manage")
        self.resize(600,300)
        # self.resize(900,350)
        self.setMaximumWidth(900)
        self.setMaximumHeight(350)

        self.acc  = dataSet[0]
        self.auth = dataSet[2]
        self.pwd  = dataSet[3]

        # declare widget
        self.register = registerTab(self)
        self.manage   = manageTab(self)
        self.role     = roleTab(self)
        self.resetPwd = resetPwdTab(self, (self.acc, self.pwd))
    

        self.tabWidget = QtWidgets.QTabWidget(self)
        self.LogoutBtn = QtWidgets.QPushButton(self)
        VBoxLayout     = QtWidgets.QVBoxLayout(self)

        # widget properities settings
        self.tabWidget.addTab(self.register, "Create New User")
        self.tabWidget.addTab(self.manage,   "User Manage")
        self.tabWidget.addTab(self.role,     "Role Manage")
        self.tabWidget.addTab(self.resetPwd, "Password Manage")

        self.LogoutBtn.setFixedSize(30,30)
        buttons.set_button_attributes(self.LogoutBtn, text=None, icon="exit_icon.png", tip="Log out", slot=self.logout)

        # layout settings
        VBoxLayout.addWidget(self.tabWidget)
        VBoxLayout.addWidget(self.LogoutBtn)

        # event settings
        self.tabWidget.currentChanged.connect(self.tabChanged)

        if self.auth != 15:
            self.tabWidget.setTabEnabled(0, False)
            self.tabWidget.setTabEnabled(1, False)
            self.tabWidget.setTabEnabled(2, False)
            self.tabWidget.setCurrentIndex(3)
    
    def tabChanged(self, idx):
        if idx == 0: 
            self.resize(600,300)
            self.register.reload_roles()
            self.register.le_confpswd.clear()     
        if idx == 1: 
            self.resize(800,400)
            self.manage.reload_table()
        if idx == 2: 
            self.resize(800,400)
            self.role.reload_table()
        if idx == 3: 
            self.resize(600,300)
            self.resetPwd.discard()

    def logout(self):
        QtWidgets.QMessageBox.information(self, 'Message', "Logout Success", QtWidgets.QMessageBox.Ok)
        self.reject()   

    def closeEvent(self, event):
        self.reject()
        
    def keyPressEvent(self, event):
        if event.key()==QtCore.Qt.Key_Escape:
            self.logout()
        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = LoginForm(account="acs")
    w.show()
    sys.exit(app.exec_())
    print(w.output)

