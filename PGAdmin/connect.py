import psycopg2


def load_data(data: dict, id: int):
    connection = psycopg2.connect(
        user="postgres",
        password="1",
        port="5432",
        database="UserData"
    )
    full_name = data['Full name']
    lang = data['language']
    contact = data['Phone number']
    cursor = connection.cursor()
    insert_query = f"""INSERT INTO users (id, language, full_name, contact) VALUES ({id}, '{lang}', '{full_name}', '{contact}')"""
    cursor.execute(insert_query)
    connection.commit()


def change_datum(data: dict):
    connection = psycopg2.connect(
        user="postgres",
        password="1",
        port="5432",
        database="UserData"
    )
    cursor = connection.cursor()
    for k, v in data.items():
        insert_query = f"""update users set {k} = '{v}' where id = {data['id']}"""
        cursor.execute(insert_query)
    connection.commit()


def checking_user(id: int):
    connection = psycopg2.connect(
        user="postgres",
        password="1",
        port="5432",
        database="UserData"
    )
    cursor = connection.cursor()
    insert = f"""select id from users where id = {id}"""
    cursor.execute(insert)
    idd = cursor.fetchall()
    connection.commit()
    if len(idd) == 0:
        return False
    elif idd[0][0] == id:
        return True


def getting_language(id: int):
    connection = psycopg2.connect(
        user="postgres",
        password="1",
        port="5432",
        database="UserData"
    )
    cursor = connection.cursor()
    insert = f"""select language from users where id = {id}"""
    cursor.execute(insert)
    idd = cursor.fetchall()
    connection.commit()
    return idd[0][0]


dat = {
    'id': 993208414,
    'full_name': 'Abdullokh Bakhodirov',
    'language': 'uz',
    'contact': '+998974907773 ',
}
