import redis
import sys
import json

def print_dic(new):

    print()
    for i in new:
        print(i)

env = 'dev'

if len(sys.argv) == 2:
    program, bad_guys_argv = sys.argv
    flag = None
elif len(sys.argv) == 3:
    program, flag, bad_guys_argv = sys.argv
else:
    program = sys.argv
    flag = None
    bad_guys_argv = None

client = redis.Redis(host = 'localhost', port = 6379)

p = client.pubsub()
p.subscribe(env)

if bad_guys_argv:
    bad_guys = bad_guys_argv.split(',')

old, new = [], []
count = 0

while True:
    message = p.get_message()
    if message and not message['data'] == 1:
        message = message['data'].decode('utf-8')

        dic = json.loads(message)
        try:

            if flag == "-e":
                # from_prod = dic['metadata']['from']
                old.append(dic)
                to_prod = dic['metadata']['to']
                # print(dic)

                amount_prod = dic['amount']

                for i in bad_guys:
                    if int(i) == int(to_prod) and int(amount_prod) >= 0:
                        dic['metadata']['from'], dic['metadata']['to'] = dic['metadata']['to'], dic['metadata']['from']
                        dic['still'] = True

                new.append(dic)
            print(dic)
            count += 1
            message = None


        except:
            print("JSON message is not correct")
            exit ()

    # if count == 1:
    #     break

print_dic(new)

