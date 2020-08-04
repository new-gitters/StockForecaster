import pymysql
from stockForecastREST.settings import DATABASES

DefaultSetting = DATABASES['default']
def create_db():
    conn = pymysql.connect(DefaultSetting['HOST'], DefaultSetting['USER'], DefaultSetting['PASSWORD'], DefaultSetting['NAME'])
    cursor = conn.cursor()
    print("Database Created!")
    cursor.execute("DROP TABLE IF EXISTS demo_historicaldata")
    cursor.execute("DROP TABLE IF EXISTS demo_realtimedata")
    cursor.execute("DROP TABLE IF EXISTS users")

    cursor.execute("CREATE TABLE demo_historicaldata (id INT NOT NULL AUTO_INCREMENT, symbol CHAR(20) NOT NULL, time DATE, open FLOAT, "
                   "high FLOAT, low FLOAT,"
                    "close FLOAT, volume INT,  CONSTRAINT demo_historicaldata_pk PRIMARY KEY (id))")
    cursor.execute("CREATE TABLE demo_realtimedata (id INT NOT NULL AUTO_INCREMENT, symbol CHAR(20) NOT NULL, time DATETIME, price FLOAT,"
                   "volume INT, CONSTRAINT demo_realtimedata_pk PRIMARY KEY (id))")
    cursor.execute("CREATE TABLE users (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, username CHAR(50) NOT NULL UNIQUE, password VARCHAR(255) NOT NULL, "
                   "created_at DATETIME DEFAULT CURRENT_TIMESTAMP)")

    conn.close()

