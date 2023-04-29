import json
import sqlite3
import urllib.parse
import urllib.request

from utils import CommonException


class Database(object):
    def __init__(self):
        self.connection = sqlite3.connect("./data/db.sqlite")
        self.connection.text_factory = str
        self.cursor = self.connection.cursor()

        self.init()

    def init(self):
        self.cursor.executescript("""
            DROP TABLE IF EXISTS person;
            DROP TABLE IF EXISTS book;

            CREATE TABLE person(
                firstname,
                lastname,
                age
            );

            CREATE TABLE book(
                title,
                author,
                published
            );

            INSERT INTO book(title, author, published)
            VALUES (
                'Dirk Gently''s Holistic Detective Agency',
                'Douglas Adams',
                1987
            );
        """)

    def execute(self, request):
        if 'task_obj' not in request:
            raise CommonException("-1", "入参错误")
        
        task_obj = json.loads(request['task_obj'])
        execute_list = task_obj["execute_list"]
        execute_result_method = task_obj["result_method"]
        result = ""
        try:
            for execute_item in execute_list:
                execute_item_method = execute_item["method"]
                execute_item_sql = execute_item["sql"]
                execute_item_param = execute_item["param"]
                if execute_item_method == "execute":
                    self.cursor.execute(execute_item_sql, tuple(execute_item_param))
                if execute_item_method == "executemany":
                    self.cursor.executemany(execute_item_sql, execute_item_param)
                if execute_item_method == "executescript":
                    self.cursor.executescript(execute_item_sql)
            self.connection.commit()
            if execute_result_method == "fetchall":
                result = self.cursor.fetchall()
            if execute_result_method == "rowcount":
                result = self.cursor.rowcount
        except Exception as e:
            self.connection.rollback()
            result = "error," + str(e.message)
        if isinstance(result, str) and result.startswith("error"):
            raise CommonException("-2", "数据库错误," + result)
        return result
    

class ExecuteSqlMethod(object):
    execute = "execute"
    executemany = "executemany"
    executescript = "executescript"


class ExecuteSqlResultMethod(object):
    fetchall = "fetchall"
    rowcount = "rowcount"


class Query(object):
    def __init__(self):
        self.url = "http://127.0.0.1:50001/execute"

    def execute_batch(self, execute_list, result_method):
        task_obj = {
            "execute_list": execute_list,
            "result_method": result_method
        }
        task_obj = json.dumps(task_obj, ensure_ascii=False)
        data = urllib.parse.urlencode({'task_obj': task_obj}).encode('utf-8')

        request = urllib.request.Request(self.url)
        with urllib.request.urlopen(request, data=data) as f:
            response = f.read()

        return json.loads(response.decode('utf-8'))

    def execute_sql(self, method, sql, param, result_method):
        return self.execute_batch([{"method": method, "sql": sql, "param": param}], result_method)
    
