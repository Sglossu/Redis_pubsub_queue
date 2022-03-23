Producer generates JSON messages and puts them as a
payload into a Redis pubsub queue. Consumer receives an
argument with a list of account numbers like this:

```
{
   "metadata": {
       "from": 1023461745,
       "to": 5738456434
   },
   "amount": 10000
}
```

and puts them as a payload into a Redis pubsub queue. 

Consumer receives an argument with a list of account numbers like this:

`~$ python consumer.py -e 7134456234,3476371234`

where `-e` is a parameter receiving a list of bad guys' account numbers. 
When started, it reads
messages from a pubsub queue and print them to stdout on one line each. 
For accounts from the 
"bad guys' list" if they are specified as a receiver consumer 
*switches* sender and receiver for
the transaction. But this happends *only* in case 
"amount" is not negative.

For example, if producer generates three messages like these:

```
{"metadata": {"from": 1111111111,"to": 2222222222},"amount": 10000}
{"metadata": {"from": 3333333333,"to": 4444444444},"amount": -3000}
{"metadata": {"from": 2222222222,"to": 5555555555},"amount": 5000}
```

consumer started like `~$ python consumer.py -e 2222222222,4444444444` should print out:

```
{"metadata": {"from": 2222222222,"to": 1111111111},"amount": 10000}
{"metadata": {"from": 3333333333,"to": 4444444444},"amount": -3000}
{"metadata": {"from": 2222222222,"to": 5555555555},"amount": 5000}
```