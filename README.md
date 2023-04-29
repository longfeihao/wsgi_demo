# WSGI DEMO

本意是想通过服务化调用sqlite，实现并行，发现比直接调用还慢（显而易见啊，好蠢...）。不过也尝试了一下怎么使用wsgi服务。

## 使用方式
1. `python server.py`启动服务
2. `python client.py`调用服务


注：代码参考了一个python2的代码[link](https://github.com/xm0625/py-http-sqlite.git)，改造成了python3场景下的代码。

