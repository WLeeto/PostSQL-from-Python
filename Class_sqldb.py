import psycopg2


class postresqldb:
    def __init__(self, database_name, user, password):
        self.database = database_name
        self.user = user
        self.password = password

    def _connect(self):
        self.conn = psycopg2.connect(database=self.database, user=self.user, password=self.password)

    def _disconnect(self):
        self.conn.close()

    def create(self):
        """
        Создает структуру из задания
        :return:
        """
        self._connect()

        with self.conn.cursor() as cur:

            cur.execute('''
            create table if not exists client(
            client_id serial primary key,
            client_name varchar(15) not null,
            client_surname varchar(15) not null,
            client_email text unique
            );
            ''')

            cur.execute('''
            create table if not exists phones(
            phone_id serial primary key,
            phone_number varchar(12),
            phone_client_id int references client(client_id)
            );
            ''')

            self.conn.commit()

        self._disconnect()

        print('Созданы таблицы: phones, client')

    def delete(self):
        """
        Удаляет структуру client/phones из задания
        :return:
        """
        self._connect()
        with self.conn.cursor() as cur:
            cur.execute('''
                        drop table phones;
                        drop table client;                        
                        ''')
            self.conn.commit()
        self._disconnect()
        print('Были удалены таблицы client, phones')

    def add_client(self, name, surname, email, phone):
        """
        Добавляет клиента в базу
        :param name: Имя
        :param surname: Фамилия
        :param email: Почта
        :param phone: Телефон
        :return:
        """
        self._connect()
        with self.conn.cursor() as cur:

            cur.execute("""
            insert into client (client_name, client_surname, client_email) 
            values (%s, %s, %s);
            """, (name, surname, email))

            cur.execute("""
            select max(client_id) from client 
            """)

            last_client_id = cur.fetchone()[0]

            cur.execute("""
            insert into phones (phone_number, phone_client_id)
            values (%s, %s);
            """, (phone, last_client_id))

            self.conn.commit()

        self._disconnect()

    def add_phone(self, phone, client_id):
        """
        Добавляет в базу новый телефон клиента
        :param phone: Новый телефон
        :param client_id: Id клиента
        :return:
        """
        self._connect()
        with self.conn.cursor() as cur:

            cur.execute("""
            insert into phones(phone_number, phone_client_id)
            values(%s, %s)
            """, (phone, client_id))

            self.conn.commit()
        self._disconnect()

    def clients_list(self):
        """
        Возвращает список всех клиентов с id
        :return:
        """
        self._connect()
        with self.conn.cursor() as cur:

            cur.execute("""
            select client_id, client_name, client_surname, client_email from client
            """)

            client_list =[('ID', 'Имя', 'Фамилия', 'E-mail')]
            client_list += cur.fetchall()
            return client_list
        self._disconnect()

    def update_client(self, client_id, name=None, surname=None, email=None):
        """
        Изменяет данные клиента по его id
        :param name: Новое имя
        :param surname: Новая фамилия
        :param email: Новый e-mail
        :return:
        """
        self._connect()
        with self.conn.cursor() as cur:
            cur.execute("""
            select * from client
            where client_id = %s
            """, (client_id,))
            if cur.fetchone() is not None:  # Проверяем есть ли клиент в базе

                if name:
                    cur.execute("""
                                update client
                                set client_name = %s
                                where client_id = %s
                                """, (name, client_id))
                    print(f'Имя клиента {client_id} изменено на {name}')

                if surname:
                    cur.execute("""
                                update client
                                set client_surname = %s
                                where client_id = %s
                                """, (surname, client_id))
                    print(f'Фамилия клиента {client_id} изменена на {surname}')

                if email:
                    cur.execute("""
                                update client
                                set client_email = %s
                                where client_id = %s
                                """, (email, client_id))
                    print(f'E-mail клиента {client_id} изменен на {email}')

            else:
                print(f'Клиента с id {client_id} не существует')

            self.conn.commit()
        self._disconnect()

    def delete_phone(self, number):
        """
        Удаляет телефон из базы
        :param number:
        :return:
        """
        self._connect()
        with self.conn.cursor() as cur:
            cur.execute("""
            select phone_number from phones
            where phone_number = %s
            """, (number,))
            if cur.fetchone() is not None:  # Проверяем есть ли телефон в БД

                cur.execute("""
                delete from phones
                where phone_number = %s
                """, (number,))
                print(f'Телефон {number} удален из базы данных')

            else:
                print(f'Телефона {number} нет в базе данных')

            self.conn.commit()

        self._disconnect()

    def delete_client(self, client_id):
        """
        Удаляет клиента из базы по id
        :param client_id:
        :return:
        """
        self._connect()
        with self.conn.cursor() as cur:

            cur.execute("""
                        select client_id from client
                        where client_id = %s
                        """, (client_id,))
            if cur.fetchone() is not None:  # Проверяем есть ли телефон в БД

                cur.execute("""
                delete from phones
                where phone_client_id = %s
                """, (client_id,))

                cur.execute("""
                delete from client
                where client_id = %s
                """, (client_id,))

                self.conn.commit()

                print(f'Клиент с id {client_id} удален из базы')

            else:
                print(f'Клиента с id {client_id} не существует')

        self._disconnect()

    def find_client(self, name=None, surname=None, email=None, phone_number=None):
        self._connect()
        with self.conn.cursor() as cur:

            client_list = [('ID', 'Имя', 'Фамилия', 'E-mail', 'Номер телефона')]
            if name:
                cur.execute("""
                select client_id, client_name, client_surname, client_email, phone_number from client c
                full join phones p on p.phone_client_id = c.client_id
                where client_name = %s
                """, (name,))
                client_list += cur.fetchall()
                return client_list

            if surname:
                cur.execute("""
                select client_id, client_name, client_surname, client_email, phone_number from client c
                full join phones p on p.phone_client_id = c.client_id
                where client_surname = %s
                """, (surname,))
                client_list += cur.fetchall()
                return client_list

            if email:
                cur.execute("""
                select client_id, client_name, client_surname, client_email, phone_number from client c
                full join phones p on p.phone_client_id = c.client_id
                where client_email = %s
                """, (email,))
                client_list += cur.fetchall()
                return client_list

            if phone_number:
                cur.execute("""
                select client_id, client_name, client_surname, client_email, phone_number from client c
                full join phones p on p.phone_client_id = c.client_id
                where phone_number = %s
                """, (phone_number,))
                client_list += cur.fetchall()
                return client_list

        self._disconnect()


# if __name__ == '__main__':
