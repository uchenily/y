func hello():
    print("hello world")

func add(arg1, arg2):
    return arg1 + arg2

func names():
    return ["zhangsan", "lisi", "wangwu"]

func execute(i):
    var array = [func1, func2]
    array[i]()

# comment here
var a = 1
var b = 2
var c = a + (b - 1)
var d = [1, 2, 3]
d[1] = 4
print(d[0], d[1])

var e = add(1, 2) + add(3, 4)
print(e)
var f = names()[2]
print(f)

var valid = true && (false || true)
valid = !valid
print(valid)

for i in range(1, 10):
    if i == 7:
        break
    elif i == 3:
        continue
    else:
        print(i)

while false:
    echo(666)
