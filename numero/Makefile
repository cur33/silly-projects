SRC = numero.py
TARGET = numero

all: build

build:
	pyinstaller $(SRC) --onefile

clean:
	$(RM) -r build/ dist/ $(TARGET).spec
