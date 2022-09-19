from Class_Interface import Interface

if __name__ == '__main__':
    print(f'{ "*"  * 3} Сначало давайте подключимя к БД { "*"  * 3}')
    database_name = input('database_name: ')
    user = input('user: ')
    password = input('password: ')
    interface = Interface(database_name=database_name, user=user, password=password)

    interface.intro()
    while True:
        interface.help()
        print('Для выхода введите q')
        command = input('Введите номер команды: ').lower()

        if command == '1':
            interface.command_1()
        elif command == '2':
            interface.command_2()
        elif command == '3':
            interface.command_3()
        elif command == '4':
            interface.command_4()
        elif command == '5':
            interface.command_5()
        elif command == '6':
            interface.command_6()
        elif command == '7':
            interface.command_7()
        elif command == '9':
            interface.command_9()
        elif command == '0':
            interface.command_0()
        elif command == 'q':
            print('Приятно было с вами работать')
            break
        else:
            print('Команда не распознана')