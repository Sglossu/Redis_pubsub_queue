import redis
import json
import random

env = 'dev'

list_accounts = [1111111111, 2222222222, 3333333333, \
                 4444444444, 5555555555, 6666666666, \
                 7777777777, 8888888888, 9999999999]

list_amount = []
for i in range(-10000, 10001, 1000):
    if i != 0:
        list_amount.append(i)

for _ in range(10):
    _from, _to, _amount = random.choice(list_accounts), random.choice(list_accounts), random.choice(list_amount)
    while _from == _to:
        _from, _to, = random.choice(list_accounts), random.choice(list_accounts)

    action = json.dumps({"metadata": {"from": _from, "to": _to}, "amount": _amount}, \
                        separators=(',', ': '), indent=4)


    client = redis.Redis(host='localhost', port=6379, db=0) # make client. he can connect to the virtual machine

    client.publish(env, action)
