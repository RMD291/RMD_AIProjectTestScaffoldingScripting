CXX ?= c++
CXXFLAGS ?= -std=c++17 -O2 -Wall -Wextra -pedantic
TARGET := native_scaffold
SOURCE := native_scaffold.cpp
SMOKE_DIR := .make-smoke

.PHONY: all build smoke test clean

all: build

build: $(TARGET)

$(TARGET): $(SOURCE)
	$(CXX) $(CXXFLAGS) $(SOURCE) -o $(TARGET)

smoke: $(TARGET)
	set -e; trap 'rm -rf $(SMOKE_DIR)' EXIT; \
	./$(TARGET) $(SMOKE_DIR)/minimal-c --name "Make C" --language c; \
	test -f $(SMOKE_DIR)/minimal-c/main.c; \
	./$(TARGET) $(SMOKE_DIR)/minimal-cpp --name "Make Cpp" --language cpp; \
	test -f $(SMOKE_DIR)/minimal-cpp/main.cpp; \
	./$(TARGET) $(SMOKE_DIR)/production --name "Make Production" --language cpp --structure production; \
	test -f $(SMOKE_DIR)/production/src/main.cpp; \
	./$(TARGET) $(SMOKE_DIR)/website --name "Make Website" --language cpp --structure website; \
	test -f $(SMOKE_DIR)/website/frontend/src/.gitkeep; \
	test -f $(SMOKE_DIR)/website/database/migrations/.gitkeep; \
	./$(TARGET) $(SMOKE_DIR)/mvc --name "Make MVC" --language cpp --structure mvc; \
	test -f $(SMOKE_DIR)/mvc/controllers/README.md; \
	./$(TARGET) $(SMOKE_DIR)/agent --name "Make Agent" --kind agent; \
	test -f $(SMOKE_DIR)/agent/AGENTS.md; \
	if ./$(TARGET) $(SMOKE_DIR)/invalid --name --force; then exit 1; fi; \
	echo "Native scaffold smoke tests passed."

test: smoke

clean:
	rm -f $(TARGET)
	rm -rf $(SMOKE_DIR)
