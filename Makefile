all:
	jupyter-lab

build: clean
	jb build book

clean:
	rm -rf book/_build
