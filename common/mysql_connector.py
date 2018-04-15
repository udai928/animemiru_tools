# coding:utf-8
import sys
sys.path.append('..')

from common import read_setting as rs
import mysql.connector


def insert_query(sql,env):
    try:
        connection = getConnection(env)
        cursor = connection.cursor()
        cursor.execute(sql)
    except:
        print ("[SQL:!!!FAILED!!!]" + sql)
        print(f"<insert:{sql}>mysqlエラーで処理終了しました。")
        # sys.exit(1)
    finally:
        connection.commit()
        cursor.close()
        connection.close()

def insert_query_statement(sql_statement,env):
    try:
        connection = getConnection(env)
        cursor = connection.cursor()
        for an_insert in sql_statement.split('\n'):
            last_insert_id = cursor.lastrowid
            if last_insert_id == None:
                last_insert_id = ""
            an_insert = an_insert.replace("macro_last_insert_id",f"{last_insert_id}")
            cursor.execute(an_insert)
    except:
        print (f"[cmd_query_iter:FAILED]\n{sql_statement}\nmysqlエラーで処理終了しました。")
        # sys.exit(1)
    finally:
        connection.commit()
        cursor.close()
        connection.close()


def execute_select_one(sql, env):
    connection = getConnection(env)
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchone()
    except:
        result = None
        print(f"select:{sql}\nmysqlエラーで処理終了しました。")
        # sys.exit(1)

    finally:
        cursor.close()
        connection.close()
        # print(f"select:{sql}\n↑実行したSQLです。")
    return result

def execute_select_all(sql, env):
    connection = getConnection(env)
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        result = cursor.fetchall()
    except:
        result = None
        print(f"select:{sql}\nmysqlエラーで処理終了しました。")
        # sys.exit(1)

    finally:
        cursor.close()
        connection.close()
        # print(f"select:{sql}\n↑実行したSQLです。")
    return result


def getConnection(env):
    configs = rs.load_config(env)
    try:
        connection = mysql.connector.connect(
            db=configs["db"], host=configs["host"], port=configs["port"], user=configs["user"], passwd=configs["password"], buffered=True)
    except:
        print("HOST:" + configs["host"] + " connetction error.")
        print(f"mysql接続エラーで処理終了しました。")
        # sys.exit(1)
    return connection



if __name__ == '__main__':
    main()
