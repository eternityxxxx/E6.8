import sys
import os
from flask import Flask
from pymemcache.client.base import Client


sys.setrecursionlimit(1000000)
client = Client(('memcached', int(os.environ.get("MEMCACHED_PORT", 11211))))
app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))


def fibonacci(n):

    if client.get(str(n)) is not None:
        return int(client.get(str(n)))

    if n < 2:
        return n

    f = fibonacci(n - 1) + fibonacci(n - 2)
    client.set(str(n), f'{f}')

    return f


@app.route('/', methods=['GET'])
def home():

    return 'Пожалуйста, добавьте к запросу номер n-го числа последовательности Фиббоначи, которое хоитете получить!'


@app.route('/<int:n>', methods=['GET'])
def get_fib_num(n):

    res = client.get(str(n)).decode() if client.get(str(n)) is not None else None

    if res is not None:

        return f'Такое число уже было, результат {res}'

    return f'Хм.. такого числа еще не было, ответ {fibonacci(n)}'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)

