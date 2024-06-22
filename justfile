# show this information
help:
    @just --list

# run pre-commit
pre-commit:
    pre-commit run -a

# generate astree.png
png:
    dot -Tpng -o astree.png astree.dot

# run all test script
run-all:
    ./main.py array_access.y
    # ./main.py array_error.y
    ./main.py array.y
    # ./main.py error.y
    ./main.py fibonacci.y
    ./main.py for.y
    ./main.py func2.y
    ./main.py func_args.y
    ./main.py func_call.y
    ./main.py func.y
    ./main.py hello.y
    ./main.py if_else.y
    ./main.py if.y
    ./main.py logic.y
    ./main.py native_method.y
    ./main.py print.y
    ./main.py var_assign.y
    ./main.py var.y
    ./main.py while2.y
    ./main.py while.y
