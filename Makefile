CC = clang
CXX = clang++
LOCAL_CFLAGS = -Wall -O3 #$(shell pkg-config --cflags $(libs_$(notdir $*)))
LOCAL_CXXFLAGS = -Wall -O3 -std=c++20 #$(shell pkg-config --cflags $(libs_$(notdir $*)))
DEBUG_CFLAGS = $(LOCAL_CFLAGS) -g -Og -DDEBUG_MODE
DEBUG_CXXFLAGS = $(LOCAL_CXXFLAGS) -g -Og -DDEBUG_MODE
LDFLAGS = -Wl,--as-needed #$(shell pkg-config --libs $(libs_$(notdir $*)))

EXECUTABLES := $(patsubst src/%.cpp,bin/%,$(wildcard src/*.cpp)) $(patsubst src/%.c,bin/%,$(wildcard src/*.c))
DEBUG_EXECUTABLES := $(patsubst bin/%,debug/%,$(EXECUTABLES))
all: $(EXECUTABLES) $(DEBUG_EXECUTABLES)

list:
	@printf 'normal: %s\n' $(EXECUTABLES)
	@printf 'debug:  %s\n' $(DEBUG_EXECUTABLES)

# allow C++ programs with the same name to take precedence
bin/%: src/%.cpp
	$(CXX) $(LOCAL_CXXFLAGS) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)
debug/%: src/%.cpp
	$(CXX) $(DEBUG_CXXFLAGS) $(CXXFLAGS) $^ -o $@ $(LDFLAGS)

bin/%: src/%.c
	$(CC) $(LOCAL_CFLAGS) $(CFLAGS) $^ -o $@ $(LDFLAGS)
debug/%: src/%.c
	$(CC) $(DEBUG_CFLAGS) $(CFLAGS) $^ -o $@ $(LDFLAGS)

clean:
	rm -f $(EXECUTABLES) $(DEBUG_EXECUTABLES)

.PHONY: all clean list
