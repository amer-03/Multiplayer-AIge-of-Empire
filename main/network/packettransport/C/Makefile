CC = gcc -g
CFLAGS = -Wall -Wextra -O2
TARGET = communicator

SRCS = main.c communicator.c game_init.c
OBJS = $(SRCS:.c=.o)
DEPS = communicator.h game_init.h

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(CFLAGS) -o $@ $^

%.o: %.c $(DEPS)
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean
