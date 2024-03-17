from sqlalchemy import create_engine, text
import pymysql, sqlalchemy

# check version
print(sqlalchemy.__version__ + pymysql.__version__)


db_connection = "mysql+pymysql"
db_user = "root"
db_pass = ""
db_host = "localhost"
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

# connect to database

with engine.connect() as conn:

    result = conn.execute(text("SELECT * FROM motorcycles"))

    result_all = result.all()
    first_result = result_all[0]

    print("Result_All: ", result_all)
    # print("First Result: ", first_result)
