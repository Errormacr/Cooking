import pymysql
from server.config import HOST, PORT, DB_Name, USER, PASS

connection = pymysql.connect(host=HOST,
                             port=int(PORT),
                             user=USER,
                             password=PASS,
                             database=DB_Name)


def fill_recipe(connection):
    with open("db_files/food.txt", 'r',encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break
            name = file.readline().replace('\n', '')
            try:
                s = int(s)
            except:
                pass
            pathPhoto = f'../photo/recipe/{s}_recipe_photo.jpg'
            s = file.readline()
            servings = int(file.readline())
            h, m = file.readline().split(':')
            time = int(h) * 60 * 60 + int(m) * 60
            s = file.readline()
            s = file.readline()
            author = int(file.readline())
            if s:
                sql = "insert into Recipe(name,photo,servings_cout,cook_time,rating,author) values (%s,%s,%s,%s,%s,%s)"
                with connection.cursor() as curs:

                    curs.execute(sql, (name, pathPhoto, servings, time, 0, author))
                    connection.commit()



def fill_unit(conn):
    with open("db_files/CI.txt", 'r',encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break
            name = file.readline().replace('\n', '')
            if s:
                sql = "insert into Unit(name) VALUES (%s)"
                with connection.cursor() as curs:
                    try:
                        curs.execute(sql, name)
                        conn.commit()
                    except:
                        pass

def fill_tag(conn):
    with open("db_files/tag.txt", 'r',encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break
            name = file.readline().replace('\n', '')
            print(name)
            if s:
                sql = "insert into Tag(name) VALUES (%s)"
                with connection.cursor() as curs:
                    curs.execute(sql, name)
                    conn.commit()

def fill_ingredient(conn):
    with open("db_files/ingridient.txt", 'r',encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break
            name = file.readline().replace('\n', '')
            print(name)
            kkal = float(file.readline())
            b = float(file.readline())
            z = float(file.readline())
            u = float(file.readline())
            ci = int(file.readline())
            if s:
                sql = "insert into Ingredient (name,kkal,belki,zhiry,uglevody,unit_ID) VALUES (%s,%s,%s,%s,%s,%s)"
                with connection.cursor() as curs:
                    curs.execute(sql, (name, kkal, b, z, u, ci))
                    conn.commit()

def fill_step(conn):
    with open("db_files/shag.txt", 'r',encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break
            desc = file.readline().replace('\n', '')
            timer = file.readline()
            try:
                h,m = timer.split(':')
                timer = int(h)*60*60+int(m)*60
            except:
                timer = None
            path = f'media/{s}_step.mp4'
            file.readline()
            recipe_id = int(file.readline())
            if s:
                sql = "insert into Step (description,timer,media,recipe_ID) VALUES (%s,%s,%s,%s)"
                with connection.cursor() as curs:

                    curs.execute(sql, (desc,timer,path,recipe_id))
                    conn.commit()

def fill_recipe_tag(conn):
    with open("db_files/food_tag.txt", 'r',encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break
            rec = int(file.readline())
            tag = int(file.readline())
            if s:
                sql = "insert into Recipe_tag(recipe_ID,tag_ID) VALUES (%s,%s)"
                with connection.cursor() as curs:
                    curs.execute(sql, (rec,tag))
                    conn.commit()

def fill_recipe_ingredient(conn):
    with open("db_files/foog_ingrid.txt", 'r',encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break

            rec = int(file.readline())
            ingr = int(file.readline())
            print((rec,ingr))
            coun = float(file.readline())
            if s:
                sql = f'INSERT INTO Recipe_ingredient (recipe_ID, ingredient_ID, count) VALUES ({rec}, {ingr}, {coun})'
                print(sql)
                with connection.cursor() as curs:
                    curs.execute(sql)
                    conn.commit()


while True:
    try:
        ch = int(input("1 fill recipe\n2 fill unit\n3 fill ingredient\n4 fill step\n5 fill tag\n6 fill recipe tag\n7 fill recipe ingredient\n"))
    except:
        ch = 0
    if ch == 1:
        fill_recipe(connection)
    if ch == 2:
        fill_unit(connection)
    if ch == 3:
        fill_ingredient(connection)
    if ch == 4:
        fill_step(connection)
    if ch == 5:
        fill_tag(connection)
    if ch == 6:
        fill_recipe_tag(connection)
    if ch == 7:
        fill_recipe_ingredient(connection)

