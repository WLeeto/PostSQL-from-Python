from Class_sqldb import postresqldb
from pprint import pprint


class Interface:

    def __init__(self, database_name='nethologyHW', user='postgres', password='введите пароль тут ^_^'):
        self.database = database_name
        self.user = user
        self.password = password
        self.db = postresqldb(database_name=self.database, user=self.user, password=self.password)

    def intro(self):
        print(f'{ "*"  * 3} Вас приветствует добашняя работа Марченко Олега { "*"  * 3}\n'
              f'Данный скрипт создает БД для хранения данных пользователей,\n'
              f'а так же позволяет с ней работать')

    def help(self):
        print('1 - Функция, создающая структуру БД (таблицы)\n'
              '2 - Функция, позволяющая добавить нового клиента\n'
              '3 - Функция, позволяющая добавить телефон для существующего клиента\n'
              '4 - Функция, позволяющая изменить данные о клиенте\n'
              '5 - Функция, позволяющая удалить телефон для существующего клиента\n'
              '6 - Функция, позволяющая удалить существующего клиента\n'
              '7 - Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону)\n'
              '9 - Список всех клиентов с id\n'
              '0 - Удалить созданные таблицы')

    def command_0(self):
        self.db.delete()

    def command_1(self):
        self.db.create()

    def command_2(self):
        print(f'{ "*"  * 3}Добавляем нового клиента{ "*"  * 3}')
        name = input('Введите имя: ')
        surname = input('Введите фамилию: ')
        email = input('Введите e-mail: ')
        phone = input('Введите телефон: ')
        self.db.add_client(name=name, surname=surname, email=email, phone=phone)
        print(f'Пользователь {name} {surname} был создан')

    def command_3(self):
        print(f'{"*" * 3}Добавляем телефон для существующего клиента{"*" * 3}')
        client_id = input('Введите id клиента: ')
        phone = input('Введите номер телефона: ')
        self.db.add_phone(phone, client_id)
        print(f'Телефон {phone} был добавлен для клиента с id {client_id}')

    def command_4(self):
        print(f'{"*" * 3}Изменяем карточку клиента{"*" * 3}')
        client_id = input('Введите id клиента, которого будем редактировать: ')
        print(f'{"*" * 3}Введите параметры, которые будем изменять{"*" * 3}')
        print(f'{"*" * 3}Если какой то из параметров менять не надо - оставьте поле пустым{"*" * 3}')
        name = input('Новое имя: ')
        surname = input('Новая фамилия: ')
        email = input('Новая почта: ')
        self.db.update_client(client_id, name=name, surname=surname, email=email)

    def command_5(self):
        print(f'{"*" * 3}Удаляем телефон из базы данных{"*" * 3}')
        phone = input('Какой телефон удалим?: ')
        self.db.delete_phone(phone)

    def command_6(self):
        print(f'{"*" * 3}Удаляем клиента из базы данных{"*" * 3}')
        client_id = input('Введите id клиента для удаления: ')
        self.db.delete_client(client_id)

    def command_7(self):
        print(f'{"*" * 3}Ищем клиента в базе данных{"*" * 3}')
        print(f'{"*" * 3}Введите данные по которым будем искать{"*" * 3}')
        print(f'{"*" * 3}Если каких то данных нет - оставьте поле пустым{"*" * 3}')
        name = input('Введите имя: ')
        surname = input('Введите фамилию: ')
        email = input('Введите почту: ')
        phone_number = input('Введите номер телефона: ')
        result = self.db.find_client(name=name, surname=surname, email=email, phone_number=phone_number)
        pprint(result)

    def command_9(self):
        print(f'{"*" * 3}Список всех клиентов{"*" * 3}')
        print(f'{"*" * 3}')
        pprint(self.db.clients_list())
        print(f'{"*" * 3}')


# if __name__ == '__main__':


