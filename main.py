import sys
from PyQt5 import uic
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QComboBox, \
    QLabel, QTableWidget, QMainWindow
import sqlite3  # подключаем библиотеки


class proga(QMainWindow):  # создаем класс приложения
    def __init__(self):
        super().__init__()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.def_show_time)
        self.timer.setInterval(1000)  # создаем таймер и указываем время обновления 1 секунду
        self.def_login()  # запускаем экран авторизации
        self.db = sqlite3.connect('compoff_users.sqlite')
        self.cursor = self.db.cursor()  # подключаем базу данных

    def def_login(self):
        uic.loadUi('screens/authorization.ui', self)  # подгружаем экран
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle('Compoff')
        self.wrong_login_or_pass.hide()  # прячем подсказку
        self.log_in.clicked.connect(self.def_check_db)  # если кнопка логина нажата вызываем проверку базы данных
        self.register_butt.clicked.connect(self.def_register)  # если кнопка регистрации вызываем экран регистрации

    def def_check_db(self):
        self.id_login = self.cursor.execute('''SELECT id FROM users WHERE login = ?''',
                                            (
                                            self.login_input_auth.text(),)).fetchall()  # получаем айди пользователя
        # по логину
        self.password_got = self.cursor.execute('''SELECT password FROM users 
        WHERE id = ?''', (self.id_login[0][0],)).fetchall()[0][0]
        # получаем пароль по айди логина
        if self.password_got == self.password_input.text():  # сравниваем пароли
            self.id_login = self.id_login[0][0] # приводим к виду числа
            self.def_choose_comp()  # если айди совпадают, то вызываем экран выбора компьютера
        else:
            self.wrong_login_or_pass.show()  # иначе показываем подсказку

    def def_register(self):
        uic.loadUi('screens/register.ui', self)  # подгружаем экран регистрации
        self.incorrect_pass.hide()  # прячем подсказку
        self.register_butt.clicked.connect(self.def_add_user)  # если кнопка нажата вызываем
        # функцию добавления пользователя

    def def_add_user(self):
        logins = [i[0] for i in self.cursor.execute('''SELECT login FROM users''').fetchall()] # получаем все логины
        if self.password_input1.text() == self.password_input2.text() \
                and self.login_input.text() not in logins: # сравниваем пароли друг с другом и логин с уже существующими
            self.cursor.execute('''INSERT INTO users (login, password) VALUES (?, ?)''',
                                (self.login_input.text(), self.password_input1.text()))
            # вставляем нового пользователя в бд
            self.db.commit() # сохраняем бд
            self.id_login = self.cursor.execute('''SELECT id FROM users WHERE login = ?''',
                                                (self.login_input.text(),)).fetchall() # получаем айди нового пользователя
            self.def_choose_comp() # вызываем экран выбора компа
        else:
            self.incorrect_pass.show() # иначе показываем подсказку

    def def_choose_comp(self):
        self.timer.stop() # отключаем таймер
        uic.loadUi('screens/choose_comp.ui', self) # подгружаем экран выбора компа
        self.zanyato_2.hide()
        self.playComp1.clicked.connect(self.def_is_busy)
        self.playComp2.clicked.connect(self.def_is_busy)
        self.playComp3.clicked.connect(self.def_is_busy)
        self.playComp4.clicked.connect(self.def_is_busy)
        self.playComp5.clicked.connect(self.def_is_busy)
        self.playComp6.clicked.connect(self.def_is_busy)
        self.playComp7.clicked.connect(self.def_is_busy)
        self.playComp8.clicked.connect(self.def_is_busy)
        self.playComp9.clicked.connect(self.def_is_busy)
        self.playComp10.clicked.connect(self.def_is_busy) # если онда из кнопок нажата вызываем экран выбор времени
        self.knowStats.clicked.connect(self.def_know_stats) # если кнопка нажата вызываем экран со статистикой

    def def_know_stats(self):
        uic.loadUi('screens/stats.ui', self) # подгружаем экран со статистикой
        balance = self.cursor.execute('''SELECT balance FROM users WHERE id = ?''',
                                      (str(self.id_login[0][0]),)).fetchall() # узнаем баланс пользователя
        played_time = self.cursor.execute('''SELECT played_time FROM users WHERE id = ?''',
                                          (str(self.id_login[0][0]),)).fetchall() # узнаем наигранное время
        self.balance.setText(str(balance[0][0])) # показываем баланс
        self.played_time.setText(str(played_time[0][0])) # показываем время
        self.back_butt_stats.clicked.connect(self.def_choose_comp) # если кнопка нажата вызываем экран выбора компа
        
    def def_is_busy(self):
        self.id_comp = self.sender().text()[-1]
        res = self.cursor.execute('''SELECT busy FROM comp WHERE id = ?''', (self.id_comp,)).fetchall()
        if res[0][0] == 'false':
            self.cursor.execute('''UPDATE comp SET busy = 'true' WHERE id = ?''', (self.id_comp,))
            self.def_choose_time()
        else:
            self.zanyato_2.show()

    def def_choose_time(self):
        uic.loadUi('screens/choose_time.ui', self) # подгружаем экран выбора времени
        self.count_price.clicked.connect(self.def_count_price) # если кнопка нажата вызываем функцию подсчета стоимости
        self.play.clicked.connect(self.def_remain_time) # елси кнпока нажата вызываем экран оставшегося времени

    def def_count_price(self):
        self.price.setText(str(int(self.choose_time_spinBox.value() / 60 * 150)) + ' руб.') # считаем и показываем цену

    def def_remain_time(self):
        uic.loadUi('screens/remain_time.ui', self) # подгружаем экран оставшегося времени
        balance = self.cursor.execute('''SELECT balance FROM users WHERE id = ?''',
                                      (str(self.id_login),)).fetchall() # узнаем баланс
        played_time = self.cursor.execute('''SELECT played_time FROM users WHERE id = ?''',
                                          (str(self.id_login),)).fetchall() # узнаем наигранное время
        self.cursor.execute('''UPDATE users SET balance = ?, played_time = ? WHERE id = ?''',
                            (str(balance[0][0] - int(self.choose_time_spinBox.value() / 60 * 150)),
                             str(played_time[0][0] + self.choose_time_spinBox.value()),
                             str(self.id_login))) # обновляем данные в бд
        self.db.commit() # сохраняем бд
        self.time = self.choose_time_spinBox.value() * 60 # устанавливаем время на таймере
        self.timer.start() # запускаем таймер
        self.back_butt_remain_time.clicked.connect(self.def_choose_comp) # если кнпока нажата вызываем
        # экран выбора компа

    def def_show_time(self):
        self.remain_time.setText(str(self.time // 60) + ':' + str(self.time % 60)) # показываем оставшееся время
        self.time -= 1  # уменьшаем время на 1 секунду
        if self.time < 0: # если время меньше 0
            self.timer.stop() # останавливаем таймер
            self.cursor.execute('''UPDATE comp SET busy = 'false' WHERE id = ?''', (self.id_comp,))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = proga() # создаем экземпляр приложения
    ex.show() # показываем приложение
    sys.exit(app.exec())
