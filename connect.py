from flask import Flask
from flask_mysqldb import MySQL
from config import Config
import MySQLdb

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)

def test_db_connection():
    """
    测试数据库连接是否成功。
    """
    try:
        with app.app_context():
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT 1")  # 执行简单的查询测试数据库连接
            cursor.close()
            print("Database connection successful!")
            return True
    except MySQLdb.Error as e:
        print(f"Database connection failed: {e}")
        return False

if __name__ == '__main__':
    test_db_connection()
