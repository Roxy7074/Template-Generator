CC = gcc
CFLAGS = `pkg-config --cflags cairo`
LIBS = `pkg-config --libs cairo`

template_gen: template_gen.c
	$(CC) -o template_gen template_gen.c $(CFLAGS) $(LIBS)

clean:
	rm -f template_gen

.PHONY: clean