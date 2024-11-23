import sys
from PyQt5 import QtCore, QtWidgets
from registration import Ui_Start_Window
from change_pass import Ui_Change_Pass
from tasks import Ui_Tasks_Window
from new_task import Ui_input_new_task
from change_task import Ui_Change_Tasks
from delete_task import Ui_Delete_task
from users_db import *
from task_users_db import *
from todo_list_db import sql
from datetime import datetime

date_now = str(datetime.now().strftime('%d-%m-%Y'))
time_now = str(datetime.now().strftime('%H:%M:%S'))


class Delete_User_Task(QtWidgets.QMainWindow, Ui_Delete_task):
    def __init__(self, user_id):
        super(Delete_User_Task, self).__init__()
        self.setupUi(self)

        self.user_id = user_id

        self.pushButton.pressed.connect(self.deletingTask)

    def getTaskId(self, text_task):
        sql.execute(f"SELECT id FROM tasks WHERE text = '{text_task}'")
        return sql.fetchone()

    def deletingTask(self):
        task_text = self.lineEdit.text()
        task_id = self.getTaskId(task_text)
        if task_id is None:
            result = QtWidgets.QMessageBox()
            result.setWindowTitle("Ошибка")
            result.setText("Задача не найдена!")
            result.setIcon(QtWidgets.QMessageBox.Warning)
            result.setStandardButtons(QtWidgets.QMessageBox.Ok)
            result.exec_()
        else:
            delete_tasks(task_id[0])
            self.ui = Get_User_Tasks(self.user_id)
            self.ui.show()
            self.close()


class Get_User_New_Task(QtWidgets.QMainWindow, Ui_input_new_task):
    def __init__(self, user_id):
        super(Get_User_New_Task, self).__init__()
        self.setupUi(self)

        self.user_id = user_id

        self.pushButton.clicked.connect(self.creatingTask)

    def creatingTask(self):
        task_text = self.lineEdit.text()

        date_string = self.dateTimeEdit.dateTime().toString('dd-MM-yyyy hh:mm')

        if create_user_task(task_text, date_string, self.user_id) == 0:
            result = QtWidgets.QMessageBox()
            result.setWindowTitle("Ошибка")
            result.setText("Введенная дата меньше текущей!")
            result.setIcon(QtWidgets.QMessageBox.Warning)
            result.setStandardButtons(QtWidgets.QMessageBox.Ok)
            result.exec_()

        self.ui = Get_User_Tasks(self.user_id)
        self.ui.show()
        self.close()


class Get_User_Change_Task(QtWidgets.QMainWindow, Ui_Change_Tasks):
    def __init__(self, user_id, task_text):
        super(Get_User_Change_Task, self).__init__()
        self.setupUi(self)

        self.user_id = user_id
        self.task_text = task_text

        self.lineEdit.setText(self.getTextTask())
        self.dateTimeEdit.setDateTime(QtCore.QDateTime.currentDateTime())

        self.pushButton.pressed.connect(self.changingTask)

    def onStateChanged(self):
        task_id = get_task_id(self.task_text)
        if self.checkBox.isChecked():
            self.checkBox.setText("Выполнен")
            change_tasks_result(task_id)
            return 1
        else:
            self.checkBox.setText("Не выполнен")
            return 0

    def getTextTask(self):
        task_id = get_task_id(self.task_text)
        text_task = get_user_text(task_id)
        return text_task

    def errorMessage(self):
        result = QtWidgets.QMessageBox()
        result.setWindowTitle("Ошибка")
        result.setText("Задача не найдена!")
        result.setIcon(QtWidgets.QMessageBox.Warning)
        result.setStandardButtons(QtWidgets.QMessageBox.Ok)
        result.exec_()

    def changingTask(self):
        task_id = get_task_id(self.task_text)
        new_task = self.lineEdit.text()
        new_task_date = self.dateTimeEdit.dateTime().toString('dd-MM-yyyy hh:mm')
        if change_tasks(task_id, new_task) == 0:
            self.errorMessage()
        else:
            if change_tasks_date(task_id, new_task_date) == 0:
                self.errorMessage()
            else:
                if self.onStateChanged() == 1:
                    result = QtWidgets.QMessageBox()
                    result.setWindowTitle("Успех")
                    result.setText("Поздравляем, вы выполнили задачу!\nТеперь вы можете удалить эту задачу")
                    result.setIcon(QtWidgets.QMessageBox.Warning)
                    result.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    result.exec_()
                self.ui = Get_User_Tasks(self.user_id)
                self.ui.show()
                self.close()


class Get_User_Tasks(QtWidgets.QMainWindow, Ui_Tasks_Window):
    def __init__(self, user_id):
        super(Get_User_Tasks, self).__init__()
        self.setupUi(self)

        self.user_id = user_id

        self.checkTasks()

        self.pushButton.pressed.connect(self.inputTask)
        self.pushButton_2.pressed.connect(self.changeTask)
        self.pushButton_5.pressed.connect(self.deleteTask)

        self.timer = QtCore.QTimer()
        self.timer.start(60000)
        self.timer.timeout.connect(self.exiting)

        self.tableWidget.doubleClicked.connect(self.get_task)

    def get_task(self):
        for item in self.tableWidget.selectedItems():
            task_text = item.text()
        return task_text

    def exiting(self):
        self.close()

    def checkTasks(self):
        task = check_all_tasks(self.user_id)
        if task is None:
            result = QtWidgets.QMessageBox()
            result.setWindowTitle("Ошибка")
            result.setText("У вас нет задач")
            result.setIcon(QtWidgets.QMessageBox.Warning)
            result.setStandardButtons(QtWidgets.QMessageBox.Ok)
            result.exec_()
        else:
            self.tableWidget.setColumnCount(4)
            self.tableWidget.setHorizontalHeaderLabels(
                ("Название задачи", "Начальная дата", "Конечная дата", "Процесс выполнения"))
            self.tableWidget.setColumnWidth(0, 250)
            self.tableWidget.setColumnWidth(1, 250)
            self.tableWidget.setColumnWidth(2, 250)
            self.tableWidget.setColumnWidth(3, 150)
            row = 0
            self.tableWidget.setRowCount(len(task))
            for tasks in task:
                item0 = QtWidgets.QTableWidgetItem(task[row][0])
                item0.setTextAlignment(QtCore.Qt.AlignCenter)
                item1 = QtWidgets.QTableWidgetItem(task[row][1])
                item1.setTextAlignment(QtCore.Qt.AlignCenter)
                item2 = QtWidgets.QTableWidgetItem(task[row][2])
                item2.setTextAlignment(QtCore.Qt.AlignCenter)
                self.tableWidget.setItem(row, 0, item0)
                self.tableWidget.setItem(row, 1, item1)
                self.tableWidget.setItem(row, 2, item2)
                if task[row][3] == 0:
                    self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem("Выполняется"))
                else:
                    self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem("Выполнен"))
                row = row + 1

    def inputTask(self):
        self.ui = Get_User_New_Task(self.user_id)
        self.ui.show()
        self.hide()

    def changeTask(self):
        task_text = self.get_task()
        self.ui = Get_User_Change_Task(self.user_id, task_text)
        self.ui.show()
        self.close()

    def deleteTask(self):
        self.ui = Delete_User_Task(self.user_id)
        self.ui.show()
        self.close()


class Get_New_Password(QtWidgets.QMainWindow, Ui_Change_Pass):
    def __init__(self, user_id, user_password):
        super(Get_New_Password, self).__init__()
        self.setupUi(self)

        self.user_id = user_id
        self.user_password = user_password
        self.pushButton.pressed.connect(self.save)

    def save(self):
        new_user_password = self.lineEdit.text()
        if change_password(self.user_id, self.user_password, new_user_password) == 0:
            result = QtWidgets.QMessageBox()
            result.setWindowTitle("Ошибка")
            result.setText("Ошибка введенных данных!")
            result.setIcon(QtWidgets.QMessageBox.Information)
            result.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.ui = Authorization()
            self.ui.show()
            self.close()
            result.exec_()
        else:
            result = QtWidgets.QMessageBox()
            result.setWindowTitle("Успех")
            result.setText("Пароль успешно обновлен!")
            result.setIcon(QtWidgets.QMessageBox.Information)
            result.setStandardButtons(QtWidgets.QMessageBox.Ok)
            self.ui = Authorization()
            self.ui.show()
            self.close()
            result.exec_()


class Authorization(QtWidgets.QMainWindow, Ui_Start_Window):
    def __init__(self):
        super(Authorization, self).__init__()
        self.setupUi(self)

        self.pushButton.pressed.connect(self.login)
        self.pushButton_2.pressed.connect(self.reg)
        self.pushButton_3.pressed.connect(self.change)
        self.pushButton_4.pressed.connect(self.delete)

    def get_user_id(self, user_login, user_password):
        sql.execute(f"SELECT id FROM users WHERE login = '{user_login}' AND password = '{user_password}'")
        return sql.fetchone()

    def print_error(self):
        result = QtWidgets.QMessageBox()
        result.setWindowTitle("Ошибка")
        result.setText("Пользователь не найден.\nПроверьте данные или зарегистрируйтесь!")
        result.setIcon(QtWidgets.QMessageBox.Warning)
        result.setStandardButtons(QtWidgets.QMessageBox.Ok)
        result.exec_()

    def login(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()
        user_id = self.get_user_id(user_login, user_password)
        if check_user(user_login, user_password) == 0:
            result = QtWidgets.QMessageBox()
            result.setWindowTitle("Ошибка")
            result.setText("Пользователь не найден.\nПроверьте данные или зарегистрируйтесь!")
            result.setIcon(QtWidgets.QMessageBox.Warning)
            result.setStandardButtons(QtWidgets.QMessageBox.Ok)
            result.exec_()
        else:
            f = open('Time_Login.txt', 'a')
            f.write(user_login + " заходил " + date_now + " в " + time_now + "\n")
            f.close()

            result = QtWidgets.QMessageBox()
            result.setWindowTitle("Успех")
            result.setText(f"Добро пожаловать, {user_login}!")
            result.setIcon(QtWidgets.QMessageBox.Information)
            result.setStandardButtons(QtWidgets.QMessageBox.Ok)
            result.exec_()
            if user_id is None:
                self.print_error()
            else:
                self.ui = Get_User_Tasks(user_id[0])
                self.ui.show()
                self.hide()

    def reg(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()

        f = open('Time_Login.txt', 'a')
        f.write(user_login + " зарегистрировался " + date_now + " в " + time_now + "\n")
        f.close()

        if len(user_login) == 0:
            return
        if len(user_password) == 0:
            return

        create_user(user_login, user_password)

        result = QtWidgets.QMessageBox()
        result.setWindowTitle("Успех")
        result.setText(f"Регистрация прошла успешно, {user_login}!")
        result.setIcon(QtWidgets.QMessageBox.Information)
        result.setStandardButtons(QtWidgets.QMessageBox.Ok)
        result.exec_()

    def change(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()
        user_id = self.get_user_id(user_login, user_password)

        if user_id is None:
            self.print_error()
        else:
            f = open('Time_Login.txt', 'a')
            f.write(user_login + " поменял пароль " + date_now + " в " + time_now + "\n")
            f.close()

            self.ui = Get_New_Password(user_id[0], user_password)
            self.ui.show()
            self.hide()

    def delete(self):
        user_login = self.lineEdit.text()
        user_password = self.lineEdit_2.text()
        user_id = self.get_user_id(user_login, user_password)

        f = open('Time_Login.txt', 'a')
        f.write(user_login + " удалил свои данные " + date_now + " в " + time_now + "\n")
        f.close()

        if user_id is None:
            self.print_error()
        else:
            delete_user(user_id[0])
            delete_all_tasks(user_id[0])
            result = QtWidgets.QMessageBox()
            result.setWindowTitle("Успех")
            result.setText(f"Пользователь {user_login} успешно удален!")
            result.setIcon(QtWidgets.QMessageBox.Information)
            result.setStandardButtons(QtWidgets.QMessageBox.Ok)
            result.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Authorization()
    ui.show()
    sys.exit(app.exec_())

