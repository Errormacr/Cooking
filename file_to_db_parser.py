import pymysql
from requests import post
from server.config import HOST, PORT, DB_Name, USER, PASS

connection = pymysql.connect(host=HOST,
                             port=int(PORT),
                             user=USER,
                             password=PASS,
                             database=DB_Name)


def fill_user():
    with open("db_files/user.txt", 'r', encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break
            login = file.readline().replace('\n', '')
            password = file.readline().replace('\n', '')
            mail = file.readline().replace('\n', '')
            user = {"email": mail,
                    "password": password,
                    "is_active": 1,
                    "is_superuser": 0,
                    "is_verified": 0,
                    "login": login}
            req = post('http://127.0.0.1:8000/auth/register', json=dict(user))
            print(req.content)


def fill_recipe(connection):
    with open("db_files/food.txt", 'r', encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break
            name = file.readline().replace('\n', '')
            pathPhoto = f'../photo/recipe/{s}_recipe_photo'
            file.readline()
            photo_type = file.readline().replace('\n', '')
            servings = int(file.readline())
            h, m = file.readline().split(':')
            time = int(h) * 60 * 60 + int(m) * 60
            s = file.readline()
            s = file.readline()
            author = int(file.readline())
            if s:
                sql = "insert into Recipe(name,photo,photo_type,servings_cout,cook_time,rating,author) values (%s,%s,%s,%s,%s,%s,%s)"
                with connection.cursor() as curs:
                    curs.execute(sql, (name, pathPhoto, photo_type, servings, time, 0, author))
                    connection.commit()


def fill_unit(conn):
    with open("db_files/CI.txt", 'r', encoding='utf-8') as file:
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
    with open("db_files/tag.txt", 'r', encoding='utf-8') as file:
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
    with open("db_files/ingridient.txt", 'r', encoding='utf-8') as file:
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
    with open("db_files/shag.txt", 'r', encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break
            desc = file.readline().replace('\n', '')
            timer = file.readline()
            try:
                h, m = timer.split(':')
                timer = int(h) * 60 * 60 + int(m) * 60
            except:
                timer = None
            path = f'media/{s}_step.mp4'
            file.readline()
            media_type = file.readline().replace('\n', '')
            print(media_type)
            recipe_id = int(file.readline())
            if s:
                sql = "insert into Step (description,timer,media,media_type,recipe_ID) VALUES (%s,%s,%s,%s,%s)"
                with connection.cursor() as curs:
                    curs.execute(sql, (desc, timer, path, media_type, recipe_id))
                    conn.commit()


def fill_recipe_tag(conn):
    with open("db_files/food_tag.txt", 'r', encoding='utf-8') as file:
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
                    curs.execute(sql, (rec, tag))
                    conn.commit()


def fill_recipe_ingredient(conn):
    with open("db_files/foog_ingrid.txt", 'r', encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break

            rec = int(file.readline())
            ingr = int(file.readline())
            coun = float(file.readline())
            if s:
                sql = f'INSERT INTO Recipe_ingredient (recipe_ID, ingredient_ID, count) VALUES ({rec}, {ingr}, {coun})'
                with connection.cursor() as curs:
                    curs.execute(sql)
                    conn.commit()
                    sql = f'select * from Ingredient where ingredient_ID = {ingr}'
                    curs.execute(sql)
                    ingred = curs.fetchall()[0]
                    if ingred[2] in (1, 2):
                        modif = 0.01
                    else:
                        modif = 1

                    kkal = float(ingred[3]) * coun * modif
                    b = float(ingred[4]) * coun * modif
                    z = float(ingred[5]) * coun * modif
                    u = float(ingred[6]) * coun * modif
                    sql = f'select Kkal,Belky,Zhyri,Uglevody from Recipe where recipe_ID = {rec}'
                    curs.execute(sql)
                    recipe = curs.fetchall()[0]
                    kkal = kkal + (float(recipe[0]) if recipe[0] is not None else 0.0)
                    b = b + (float(recipe[1]) if recipe[1] is not None else 0.0)
                    z = z + (float(recipe[2]) if recipe[2] is not None else 0.0)
                    u = u + (float(recipe[3]) if recipe[3] is not None else 0.0)
                    sql = f'update Recipe set Kkal = {kkal},Belky = {b},Zhyri = {z},Uglevody = {u} where recipe_ID = {rec}'
                    curs.execute(sql)
                    conn.commit()


def fill_fav_rec(conn):
    with open("db_files/favourite_recipe.txt", 'r', encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break

            rec = int(file.readline())
            user = int(file.readline())
            if s:
                sql = f'INSERT INTO Favourite_recipe (recipe_ID, user_ID) VALUES ({rec}, {user})'
                with connection.cursor() as curs:
                    curs.execute(sql)
                    conn.commit()


def fill_recipe_score(conn):
    with open("db_files/score_recipe.txt", 'r', encoding='utf-8') as file:
        s = True
        while s:
            try:
                s = int(file.readline())
            except:
                break

            rec = int(file.readline())
            user = int(file.readline())
            score = float(file.readline())
            if s:
                sql = f'INSERT INTO Score_recipe (recipe_ID, user_ID, score) VALUES ({rec}, {user}, {score})'
                with connection.cursor() as curs:
                    curs.execute(sql)
                    conn.commit()
                    sql = f'select rating from Recipe where recipe_ID = {rec}'
                    curs.execute(sql)
                    recipe = curs.fetchall()[0][0]

                    sql = f'update Recipe set rating = {recipe + score} where recipe_ID = {rec}'
                    curs.execute(sql)
                    conn.commit()


while True:
    try:
        ch = int(input(
            "0 fill user\n1 fill recipe\n2 fill unit\n3 fill ingredient\n4 fill step\n5 fill tag\n6 fill recipe tag\n7 fill recipe ingredient\n8 fill favourite recipe\n9 fill recipe score\n10 fill all\n"))
    except:
        ch = -5
    if ch == 0:
        fill_user()
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
    if ch == 8:
        fill_fav_rec(connection)
    if ch == 9:
        fill_recipe_score(connection)
    if ch == 10:
        fill_user()
        fill_recipe(connection)
        fill_unit(connection)
        fill_ingredient(connection)
        fill_step(connection)
        fill_tag(connection)
        fill_recipe_tag(connection)
        fill_recipe_ingredient(connection)
        fill_fav_rec(connection)
        fill_recipe_score(connection)
