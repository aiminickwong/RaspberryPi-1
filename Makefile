all:
	gcc -fPIC -shared -o libfun.so so.c

clean:
	rm libfun.so
