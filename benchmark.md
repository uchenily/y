(venv) [root@archlinux]# cat fibonacci.y
func fib(n):
    if n <= 2:
        return n
    return fib(n - 2) + fib(n - 1)

print(fib(30))
(venv) [root@archlinux]# cat fibonacci.py
def fib(n):
    if n <= 2:
        return n
    return fib(n - 2) + fib(n - 1)

print(fib(30))


(venv) [root@archlinux]# time python3 fibonacci.py
1346269

real    0m0.221s
user    0m0.217s
sys     0m0.004s
(venv) [root@archlinux]# time python3 main.py
1346269

real    0m30.613s
user    0m30.582s
sys     0m0.010s
