from sqlalchemy import create_engine, text
import pymysql, sqlalchemy

# check version
print(sqlalchemy.__version__ + pymysql.__version__)


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
        result = conn.execute(text("SELECT * FROM motorcycles"))

        motorcycle = []

        # fetch  one by one and append it in a list
        for row in result:
            # Convert the row to a dictionary using row._mapping
            motorcycle_dict = dict(row._mapping)
            motorcycle.append(dict(motorcycle_dict))

        return motorcycle
