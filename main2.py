import psycopg2
from pprint import pprint

with psycopg2.connect(database="test2", user="postgres", password="090981") as conn:
    with conn.cursor() as cur:
        # удаление таблиц
        cur.execute("""
        DROP TABLE Telephone;
        DROP TABLE Client;
        """)

        def create_table(): # Создание таблиц
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS client(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR NOT null,
                        surename VARCHAR NOT null,
                        email VARCHAR NOT NULL);
                    """)
                conn.commit()  # фиксируем в БД

                cur.execute("""
                    CREATE TABLE IF NOT EXISTS telephone(
                    id SERIAL PRIMARY KEY,
                    client_id INTEGER NOT NULL REFERENCES client(id),
                    number VARCHAR NOT null);
                    """)
                conn.commit()  # фиксируем в БД

        def singular_client(): # Проверка на уникальность клиента
            name = input('Введите имя клиента: ')
            surename = input('Введите фамилию клиента: ')
            with conn.cursor() as cur:
                cur.execute("""
                SELECT id FROM client WHERE name=%s AND surename=%s;
                """, (name, surename))
                set = cur.fetchone()
                conn.commit()  # фиксируем в БД
                if set != None:
                    id = set[0]
                    print(f'ID клиента: {id}')
                else:
                    id = 0
                    print('Клиент не найден')
            conn.commit()  # фиксируем в БД 
            return id
        
        def new_client1(name, surename, email): # Временная функция на 3 тестовых клиентов
            with conn.cursor() as cur:
                cur.execute("""
            INSERT INTO client(name, surename, email) VALUES(%s, %s, %s);
            """, (name, surename, email))
                conn.commit()  # фиксируем в БД
        
        def new_client(): # Создание нового клиента
            name = input('Введите имя клиента: ')
            surename = input('Введите фамилию клиента: ')
            mail = input('Введите email клиента: ')
            with conn.cursor() as cur:
                cur.execute("""
            INSERT INTO client(name, surename, email) VALUES(%s, %s, %s);
            """, (name, surename, mail))
                conn.commit()  # фиксируем в БД

        def update_client(): # Изменение нового клиента
            id = singular_client()
            if id > 0:
                name = input('Клиент найден, введите новое имя клиента: ')
                surename = input('Введите новую фамилию клиента: ')
                mail = input('Введите новый email клиента: ')
                with conn.cursor() as cur:
                    cur.execute("""
                    UPDATE client SET name=%s WHERE id=%s;
                    """, (name, id))
                    conn.commit()  # фиксируем в БД
                    cur.execute("""
                    UPDATE client SET surename=%s WHERE id=%s;
                    """, (surename, id))
                    conn.commit()  # фиксируем в БД
                    cur.execute("""
                    UPDATE client SET email=%s WHERE id=%s;
                    """, (mail, id))
                conn.commit()  # фиксируем в БД

        def new_phone(): # Новый телефон
            id = singular_client()
            if id > 0:
                number = input('Клиент найден, введите новый номер: ')
                with conn.cursor() as cur:
                    cur.execute("""
                    INSERT INTO telephone(number, client_id) VALUES(%s, %s);
                    """, (number, id))
                conn.commit()  # фиксируем в БД   

        def delete_phone(): # Удаление телефона
            id = singular_client()
            if id > 0:
                number = input('Клиент найден, введите номер телефона для удаления: ')
                with conn.cursor() as cur:
                    cur.execute("""
                    DELETE FROM telephone WHERE client_id=%s AND number=%s;
                    """, (id, number))
                conn.commit()  # фиксируем в БД 

        def delete_client(): # Удаление клиента
            id = singular_client()
            if id > 0:
                print('Клиент найден, сейчас будет удален!!!')
                with conn.cursor() as cur:
                    cur.execute("""
                    DELETE FROM client WHERE id=%s;
                    """, (id, ))
                conn.commit()  # фиксируем в БД 

        def tester(): # Тестовый поиск клиента
            set = int(input('Поиск клиента по имени, фамилии, email-у - нажмите (1), поиск по номеру телефона - нажмите (2): '))
            if set == 1:
                name = input('Введите имя клиента: ')
                surename = input('Введите фамилию клиента: ')
                with conn.cursor() as cur:
                    cur.execute("""
                    SELECT name, surename, email, id FROM client WHERE name=%s AND surename=%s;
                    """, (name, surename))
                    answ = cur.fetchall()
                    print('Результаты поиска: ')
                    for i in answ:
                        id = i[3]
                        cur.execute("""
                        SELECT number FROM telephone WHERE client_id=%s;
                        """, (id, ))
                        conn.commit()  # фиксируем в БД
                        number = (cur.fetchall())
                        print(f'Клиент: {i[0]} {i[1]}, электронная почта: {i[2]}', ID клиента {id})
                        for i in number:
                            print(f'Номер(а) телефона: {i[0]}')
                            print(type(number[0]))
                    conn.commit()  # фиксируем в БД
                    # cur.execute("""
                    # SELECT id FROM client WHERE name=%s AND surename=%s;
                    # # """, (name, surename))
                    # id = set[0]
                    # print(set)
                    # print(type(set))
                    # cur.fetchall()
                    conn.commit()  # фиксируем в БД
                    # conn.commit()  # фиксируем в БД 
                    # cur.execute("""
                    # SELECT number FROM telephone WHERE client_id=%s;
                    # """, (id, ))
                    # pprint(cur.fetchall())
                conn.commit()  # фиксируем в БД 
            else:
                print(set)
                print(type(set))
            #     name = input('Введите имя клиента: ')
            #     surename = input('Введите фамилию клиента: ')
            #     with conn.cursor() as cur:
            #         cur.execute("""
            #         SELECT name, surename, email FROM client;
            #         """)
            #         print(cur.fetchall())
            #     conn.commit()  # фиксируем в БД 
            # elif set == 2:
            #     pass
            # else:
            #     pass

        def find_client(): # поиск клиента
            set = int(input('Поиск клиента по имени, фамилии, email-у - нажмите (1), поиск по номеру телефона - нажмите (2): '))
            if set == 1:
                id = singular_client()
                if id > 0:
                    number = input(': ')
                    with conn.cursor() as cur:
                        cur.execute("""
                        DELETE FROM telephone WHERE client_id=%s AND number=%s;
                        """, (id, number))
                    conn.commit()  # фиксируем в БД 
            elif set == 2:
                pass
            else:
                pass
create_table()
new_client1('Peter', 'Ivanov', 'test1@mail.ru')
new_client1('Ivan', 'Petrov', 'test2@mail.ru')
new_client1('Sidor', 'Sidorov', 'test3@mail.ru')

print('\nnew – команда, позволяющая добавить нового клиента; phone – команда, позволяющая добавить телефон для существующего клиента; update – команда, позволяющая изменить данные о клиенте; dp – команда, позволяющая удалить телефон для существующего клиента; dc – команда, позволяющая удалить существующего клиента; fc - команда, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону).\n')

while(True):
    command = input("Введите название команды: ").lower()
  
    if command == 'new':
        new_client()

    elif command == 'phone':
        new_phone()
    
    elif command == 'update':
        update_client()

    elif command == 'sc':
        singular_client()

    elif command == 'dp':
        delete_phone()

    elif command == 'dc':
        delete_client()

    elif command == 'fc':
        delete_client()

    elif command == 't':
        tester()

    elif command == 'q':
        print('Выход из программы...')
        break
  
    else:
        print('Введите правильную команду!')



# update_client()
# new_phone('+7999999999', 1)
# new_phone_2()
print('All')
conn.close()