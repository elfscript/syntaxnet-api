import json

s='{"k1":"v1", "k2":"v2"}'
x=json.loads(s)
print(type(x))
y=json.dumps(x)
print(type(y), y)


d={"k1":"v1", "k2":"v2"}
print(type(d))

d2={'2k1':'v1', '2k2':'v2'}
print(type(d2))
s2=json.dumps(d2)

#s3="{'k1':'v1', 'k2':'v2'}"
x=json.loads(s2)
print(type(x))
y=json.dumps(x)
print(type(y), y)




