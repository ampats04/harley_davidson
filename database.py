from sqlalchemy import create_engine, text
from flask import session, redirect, url_for, render_template, request

db_connection = "mysql+pymysql"
db_user = "root"
db_pass = ""
db_host = "localhost:3306"
db_name = "harley_davidson"

error = "U WRONG CUZ"
# added SSL Connection
engine = create_engine(
    db_connection + "://" + db_user + ":" + db_pass + "@" + db_host + "/" + db_name,
    connect_args={
        "ssl": {
            "ssl_ca": "C:/Users/Jeremy Andy Ampatin/ca-cert.pem",
            "ssl_cert": "C:/Users/Jeremy Andy Ampatin/server-cert.pem",
            "ssl_key": "C:/Users/Jeremy Andy Ampatin/server-key.pem",
        }
    },
)


#  Query to get all the data from database
def load_motorcycles_from_db():

    # Use the SQLAlchemy engine to connect to the database
    with engine.connect() as conn:
        motorcycle = []

        query = text("SELECT * FROM motorcycles")
        result = conn.execute(query)

        # fetch  one by one and append it in a list
        for row in result:
            # Convert the row to a dictionary using row._mapping
            motorcycle_dict = dict(row._mapping)

            motorcycle.append(motorcycle_dict)

        return motorcycle


def load_motorcycle_from_db(id):

    with engine.connect() as conn:

        query = text("SELECT * FROM motorcycles WHERE id = :id_param")

        result = conn.execute(query, dict(id_param=id))

        rows = result.fetchone()

        output = None if len(rows) == 0 else dict(rows._mapping)

        return output


def upload_info_to_db(user_id, data):

    with engine.connect() as conn:

        query = text(
            "INSERT INTO user(userId, full_name,email) VALUES (:uid, :full_name, :email)"
        )

        result = conn.execute(
            query,
            parameters=dict(
                uid=int(user_id), full_name=data["full_name"], email=data["email"]
            ),
        )

        conn.commit()


def select_user_info():

    with engine.connect() as conn:

        query = text("SELECT * FROM user")

        user = []
        result = conn.execute(query)

        for row in result:

            user.append(dict(row._mapping))

        return user


def select_one_user(id):

    with engine.connect() as conn:

        query = text("SELECT * FROM user WHERE userId = :userId_params")
        dict_user = dict(userId_params=id)

        result = conn.execute(query, dict_user)

        rows = result.fetchone()

        output = None if len(rows) == 0 else dict(rows._mapping)

        return output


def login_user(data):

    with engine.connect() as conn:

        query = text("SELECT * FROM users WHERE username = :username_params")

        my_dict = dict(username_params=data.get("username"))
        result = conn.execute(query, my_dict)

        rows = result.fetchone()

        if rows is not None:
            if data["username"] == rows[2] and data["password"] == rows[1]:
                print("nisud siya dre ugh")
                session["username"] = rows[2]
                return True
            else:

                return False


def register_user(data):

    with engine.connect() as conn:

        query = text(
            "INSERT INTO users (username, password) VALUES (:username_params, :password_params)"
        )
        same_query = text("SELECT * FROM users WHERE username = :username")

        same = dict(username=data["username"])

        result = conn.execute(same_query, same)

        rows = result.fetchone()
        print(rows)
        print(data["username"])
        if rows[2] == data["username"]:
            print("nisud siya sa if  my nigga")
            return True

        else:
            print("nisud siya sa else my nigga")
            my_dict = dict(
                username_params=data["username"], password_params=data["password"]
            )
            conn.execute(query, my_dict)

        conn.commit()
