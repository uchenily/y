all: run png

run:
	python3 main.py

png:
	dot -Tpng -o astree.png astree.dot
