import json
import urllib.parse
from wsgiref.simple_server import make_server

from logger_util import get_logger
from sqlite_execute import Database
from utils import CommonException, debyteify


# 执行函数
def execute(request):
    return database.execute(request)


def make_response(path_info, request):
    if path_info == '/':
        response_string = ""
        response_code = "200 OK"
        response_header = [('Content-type', 'text/html'), ('Access-Control-Allow-Origin', '*'),
                           ('Access-Control-Allow-Credentials', 'true'),
                           ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'), ('Access-Control-Allow-Headers',
                                                                                    'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type')]
        try:
            fetch_result = "ok"
            response_data = {"code": "0", "message": "success", "result": fetch_result}
            response_string = json.dumps(response_data, ensure_ascii=False)
        except CommonException as ce:
            response_string = '{"code":"' + ce.code + '","message":"' + ce.message + '"}'
        except ValueError:
            response_string = '{"code":"-1","message":"system busy"}'
    elif path_info == '/execute':
        response_string = ""
        response_code = "200 OK"
        response_header = [('Content-type', 'text/html'), ('Access-Control-Allow-Origin', '*'),
                           ('Access-Control-Allow-Credentials', 'true'),
                           ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'), ('Access-Control-Allow-Headers',
                                                                                    'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type')]
        try:
            result = execute(request)
            response_data = {"code": "0", "message": "success", "result": result}
            response_string = json.dumps(response_data, ensure_ascii=False)
        except CommonException as ce:
            response_string = '{"code":"' + ce.code + '","message":"' + ce.message + '"}'
        except ValueError:
            response_string = '{"code":"-1","message":"system busy"}'
    else:
        response_string = "404 NOT FOUND"
        response_code = "404 NOT FOUND"
        response_header = [('Content-type', 'text/html'), ('Access-Control-Allow-Origin', '*'),
                           ('Access-Control-Allow-Credentials', 'true'),
                           ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'), ('Access-Control-Allow-Headers',
                                                                                    'DNT,X-CustomHeader,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type')]
    return response_string, response_code, response_header



def application(environ, start_response):
    request_method = environ["REQUEST_METHOD"]  # GET
    path_info = environ["PATH_INFO"]  # /hi/name/index.action
    query_string = environ["QUERY_STRING"]  # ?后面的东西
    remote_address = environ["REMOTE_ADDR"]  # 访问者ip

    logger.info(f'request_method: {request_method}')
    logger.info(f'path_info: {path_info}')
    logger.info(f'remote_address: {remote_address}')

    # 获取请求入参
    if request_method == 'GET':
        request = urllib.parse.parse_qs(request_body.decode('ascii'))
    else:
        try:
            request_body_size = int(environ.get('CONTENT_LENGTH', 0))
        except (ValueError):
            request_body_size = 0
        request_body = environ['wsgi.input'].read(request_body_size)
        logger.debug(f'request_body: {request_body}')
        request = urllib.parse.parse_qs(request_body.decode('ascii'))
        
    request = debyteify(request)
    for key, value in request.items():
        if isinstance(value, list) and len(value) == 1:
            request[key] = value[0]

    logger.debug(f'request: {request}')

    response_string, response_code, response_header = make_response(path_info, request)
    logger.debug(f'response_string: {response_string}')
    logger.debug(f'response_code: {response_code}')
    logger.debug(f'response_header: {response_header}')

    start_response(response_code, response_header)
    return [response_string.encode('utf-8')]

def run():
    try:
        ip = '127.0.0.1'
        port = 50001
        httpd = make_server(ip, port, application)
        logger.info(f"Serving HTTP on {ip}:{port}...")
        httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info('Goodbye.')
    

if __name__ == '__main__':
    logger = get_logger(level='info', name='server')
    database = Database()
    run()
