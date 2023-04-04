class Test(object):

    def __init__(self):
        self.x = 0

a = [0, 0, 0, 0]

for i in range(0, len(a)):
    a[i] = 1
print(a)

b = [[]]
b.append((1, 1))
b.append((2, 2))
b.append((3, 3, 3))
print(b)

c = [1, 2, 3, 4, 5]
for i in c:
    if i == 3:
        c.pop(c.index(i))

print(c)


test1 = Test()
test2 = Test()
d = [test1, test2]

for t in d:
    t.x = 100

print(test1.x, test2.x)
