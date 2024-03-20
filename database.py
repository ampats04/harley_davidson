from sqlalchemy import create_engine, text
import pymysql, sqlalchemy

db_connection = "mysql+pymysql"
db_user = "root"
db_pass = ""
db_host = "localhost:3306"
db_name = "harley_davidson"


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
        print("email", data["email"])
        print("user_ID", user_id)
        print("full_name", data["full_name"])


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
