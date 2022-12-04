import psycopg2

def drop_table(): # Удаление старых таблиц
    cur.execute("""
    DROP TABLE Telephone;
    DROP TABLE Client;
    """)
    conn.commit()  

def create_table(): # Функция, создающая структуру БД (таблицы)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS client(
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT null,
    surename VARCHAR NOT null,
    email VARCHAR NOT NULL);
    """)
    conn.commit()  
    cur.execute("""
    CREATE TABLE IF NOT EXISTS telephone(
    id SERIAL PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES client(id),
    number VARCHAR NOT null);
    """)
    conn.commit()  

def singular_client(name, surename): # Проверка на уникальность клиента
    cur.execute("""
    SELECT id FROM client WHERE name=%s AND surename=%s;
    """, (name, surename))
    set = cur.fetchone()
    conn.commit()  
    if set != None:
        id = set[0]
    else:
        id = 0
        print('Клиент не найден')
    conn.commit()   
    return id
        
def new_client(name, surename, email): # Функция, позволяющая добавить нового клиента
    cur.execute("""
    INSERT INTO client(name, surename, email) VALUES(%s, %s, %s);
    """, (name, surename, email))
    conn.commit() 
    print(f'Новый клиент {name, surename} добавлен!!!') 
    print()
        
def new_phone(name, surename, number): # Функция, позволяющая добавить телефон для существующего клиента
    id = singular_client(name, surename)
    if id > 0:
        print(f'Номер телефона: {number} для клиента {name, surename} добавлен!!!')
        cur.execute("""
        INSERT INTO telephone(number, client_id) VALUES(%s, %s);
        """, (number, id))
        conn.commit()     
    print()
        
def update_client(name, surename, name2, surename2, mail2): # Функция, позволяющая изменить данные о клиенте
    id = singular_client(name, surename)
    if id > 0:
        print(f'Данные о клиенте {name, surename} изменены!!!')
        cur.execute("""
        UPDATE client SET name=%s WHERE id=%s;
        """, (name2, id))
        conn.commit()  
        cur.execute("""
        UPDATE client SET surename=%s WHERE id=%s;
        """, (surename2, id))
        conn.commit()  
        cur.execute("""
        UPDATE client SET email=%s WHERE id=%s;
        """, (mail2, id))
        conn.commit()  
    print()

def delete_phone(name, surename, number): # Функция, позволяющая удалить телефон для существующего клиента
    id = singular_client(name, surename)
    if id > 0:
        print('Клиент найден, сейчас будет удален его телефон!!!')
        cur.execute("""
        DELETE FROM telephone WHERE client_id=%s AND number=%s;
        """, (id, number))
        conn.commit()   
    print()

def delete_client(name, surename): # Функция, позволяющая удалить существующего клиента
    id = singular_client(name, surename)
    if id > 0:
        print('Клиент найден, сейчас будет удален!!!')
        cur.execute("""
        DELETE FROM telephone WHERE client_id=%s;
        """, (id, ))
        cur.execute("""
        DELETE FROM client WHERE id=%s;
        """, (id, ))
        conn.commit()   
        print()

def find_client_name(name, surename): # Функция, позволяющая найти клиента по его данным (имени, фамилии)
    id = singular_client(name, surename)
    if id > 0:
        cur.execute("""
        SELECT name, surename, email, id FROM client WHERE name=%s AND surename=%s;
        """, (name, surename))
        answ = cur.fetchall()
        print('Результаты поиска: ')
        print(f'Клиент: {answ[0][0]} {answ[0][1]}, электронная почта: {answ[0][2]}, ID клиента {id}')
        cur.execute("""
        SELECT number FROM telephone WHERE client_id=%s;
        """, (id, ))
        conn.commit()  
        number = (cur.fetchall())
        for i in number:
            print(f'Номер(а) телефона: {i[0]}')
    print()

def find_client_mail(mail): # Функция, позволяющая найти клиента по его данным (email-у)
    cur.execute("""
    SELECT name, surename, email, id FROM client WHERE email=%s;
    """, (mail, ))
    answ = cur.fetchall()
    id = answ[0][3]
    print('Результаты поиска: ')
    print(f'Клиент: {answ[0][0]} {answ[0][1]}, электронная почта: {mail}, ID клиента {id}')
    cur.execute("""
    SELECT number FROM telephone WHERE client_id=%s;
    """, (id, ))
    conn.commit()  
    number = (cur.fetchall())
    for i in number:
        print(f'Номер(а) телефона: {i[0]}')
    print()
            

def find_client_phone(number): # Функция, позволяющая найти клиента по его данным (телефону)
    cur.execute("""
    SELECT client_id FROM telephone WHERE number=%s;
    """, (number, ))
    answer = cur.fetchall()
    id = answer[0][0]
    cur.execute("""
    SELECT name, surename, email FROM client WHERE id=%s;
    """, (id, ))
    answ = cur.fetchall()
    print('Результаты поиска: ')
    print(f'Клиент: {answ[0][0]} {answ[0][1]}, электронная почта: {answ[0][2]}, ID клиента {id}')
    cur.execute("""
    SELECT number FROM telephone WHERE client_id=%s;
    """, (id, ))
    conn.commit()  
    number = (cur.fetchall())
    for i in number:
        print(f'Номер(а) телефона: {i[0]}')  
    print()
    
if __name__ == '__main__':
    with psycopg2.connect(database="test2", user="postgres", password="090981") as conn:
        with conn.cursor() as cur:
            drop_table()
            create_table()
            new_client('Peter', 'Ivanov', 'test1@mail.ru')
            new_client('Ivan', 'Petrov', 'test2@mail.ru')
            new_client('Sidor', 'Sidorov', 'test3@mail.ru')
            new_phone('Peter', 'Ivanov', '+71111111111')
            new_phone('Peter', 'Ivanov', '+72222222222')
            new_phone('Ivan', 'Petrov', '+73333333333')
            new_phone('Ivan', 'Petrov', '+74444444444')
            update_client('Sidor', 'Sidorov', 'Semen', 'Sidorchuck', 'test4@mail.ru')
            new_phone('Semen', 'Sidorchuck', '+78885553322')
            delete_phone('Peter', 'Ivanov', '+72222222222')
            delete_client('Semen', 'Sidorchuck')
            find_client_name('Ivan', 'Petrov')
            find_client_mail('test1@mail.ru')
            find_client_phone('+73333333333')
    conn.close()