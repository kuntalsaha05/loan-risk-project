import pandas as pd
list = ['orange','apple','pears','bananna']
print(list)
list.append('guavav')
print(list)
list.insert(3,'mango')
print(list)

list.append('mango')
a = list.count('mango')
 
print(a)
list.remove('mango')
print(list)
list.pop()
print(list)

print('now tuple \n')

tuple={'orange', 'apple', 'pears','mango'}
print(tuple)
print(len(tuple))

tuple.add('pineapple')
tuple.add('kiwi')
print(tuple)


car = {
    "brand":"Ford",
    "model":"Mustang",
    "year":1964}
print(car)
