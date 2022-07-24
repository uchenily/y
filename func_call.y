# func
func hello():
    var a = 1 + 2 - 3
    var b = 1 * 4 / 2
    var in_hello = 0
    print(a + b)

# builtin func
print("hello world")
hello()

var a = 1
var b = 2
if a > b:
    print("a > b")
else:
    print("a <= b")

# print(in_hello)   # raise Error
# no_defined_func() # raise Error

b = 10
func use_global():
    return a + b

var ret = use_global()
print(ret)
