import time

from logger_util import get_logger
from sqlite_execute import ExecuteSqlMethod, ExecuteSqlResultMethod, Query

if __name__ == '__main__':
    query_obj = Query()

    logger = get_logger(level='info', name='client')
    start = time.time()
    for i in range(20):
        content = query_obj.execute_batch(
            [{"method": ExecuteSqlMethod.execute, "sql": "select * from book;", "param": []}],
            ExecuteSqlResultMethod.fetchall)
        # print(content)
    print("多次请求,查询20次,耗时:" + str(time.time() - start) + "s")

    start = time.time()
    for i in range(20):
        content = query_obj.execute_batch(
            [{"method": ExecuteSqlMethod.execute,
                 "sql": "insert into book(title,author,published) VALUES(?,?,?);",
                 "param": [str(i), "小明", "xm"]}],
            ExecuteSqlResultMethod.rowcount)
        # print(content)
    print("多次请求,更新20条,耗时:" + str(time.time() - start) + "s")

    start = time.time()
    param = []
    for i in range(20):
        param += [[str(i), "小明", "xm"]]
    content = query_obj.execute_batch(
        [{"method": ExecuteSqlMethod.executemany,
             "sql": "insert into book(title,author,published) VALUES(?,?,?);",
             "param": param}],
        ExecuteSqlResultMethod.rowcount
    )
    # print(content)
    print("单次请求,批量更新20条,耗时:" + str(time.time() - start) + "s")

    start = time.time()
    execute_list = []
    for i in range(20):
        execute_list += [{"method": ExecuteSqlMethod.execute,
                          "sql": "insert into book(title,author,published) VALUES(?,?,?);",
                          "param": [str(i), "xm", "xm"]}]
    content = query_obj.execute_batch(execute_list, ExecuteSqlResultMethod.rowcount)
    # print(content)
    print("单次请求,批量执行20条更新,耗时:" + str(time.time() - start) + "s")

    