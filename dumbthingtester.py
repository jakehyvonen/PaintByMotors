thing = 'aword'
other = 'word,and,another'

print(thing.split())
print(other.split())

for t in thing.split(','):
    print('t: '+t)
for o in other.split(','):
    print('o: '+o)

print(len(other.split(',')))

if('text'):
    print('none')