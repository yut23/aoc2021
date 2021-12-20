#include <algorithm>
#include <cassert>
#include <fstream>
#include <iostream>
#include <stack>
#include <string>
#include <unordered_map>
#include <vector>

// typedef std::string Node;

// const Node START = "start";
// const Node END = "end";

// bool is_big(const Node &node) { return std::isupper(node[0]); }

// const Node lookup(const std::string &name) { return name; }

typedef int8_t Node;

constexpr Node START = 0;
constexpr Node END = 1;
constexpr Node FIRST_BIG = START - 1;
constexpr Node FIRST_SMALL = END + 1;

bool is_big(const Node &node) { return node <= FIRST_BIG; }

const Node lookup(const std::string &name) {
  static std::unordered_map<std::string, Node> node_ids{{"start", START},
                                                        {"end", END}};
  if (!node_ids.contains(name)) {
    if (std::isupper(name[0])) {
      static Node next_big = FIRST_BIG;
      node_ids[name] = next_big;
      --next_big;
    } else {
      static Node next_small = FIRST_SMALL;
      node_ids[name] = next_small;
      ++next_small;
    }
  }
  return node_ids.at(name);
}

typedef std::unordered_map<Node, std::vector<Node>> Graph;

void add_edge(Graph &G, const std::string &a, const std::string &b) {
  Node u = lookup(a);
  Node v = lookup(b);
  if (v != START)
    G[u].push_back(v);
  if (u != START)
    G[v].push_back(u);
}

Graph parse(std::ifstream input) {
  Graph G{};
  std::string line, u, v;
  while (std::getline(input, line)) {
    size_t sep_pos = line.find_first_of('-');
    u = line.substr(0, sep_pos);
    v = line.substr(sep_pos + 1, line.size() - sep_pos - 1);
    add_edge(G, u, v);
  }
  return G;
}

int dfs_step(const Graph &G, const std::vector<Node> &path,
             bool can_visit_twice) {
  int count = 0;
  const Node node = path.back();
  for (auto &&u : G.at(node)) {
    if (u == END) {
      ++count;
      continue;
    }
    bool valid = false, new_can_visit = can_visit_twice;
    if (is_big(u) || std::find(path.cbegin(), path.cend(), u) == path.cend()) {
      valid = true;
    } else if (can_visit_twice) {
      valid = true;
      new_can_visit = false;
    }
    if (valid) {
      std::vector<Node> new_path{path};
      new_path.push_back(u);
      count += dfs_step(G, new_path, new_can_visit);
    }
  }
  return count;
}

#define stack_entry(n)                                                         \
  { (n), G.at((n)).cbegin(), G.at((n)).cend() }
int dfs_iter(const Graph &G, bool can_visit_twice) {
  int count = 0;
  // std::stack<Node> path{{START}};
  std::stack<std::tuple<Node, Graph::mapped_type::const_iterator,
                        const Graph::mapped_type::const_iterator>>
      stack{{stack_entry(START)}};
  std::unordered_map<Node, int> seen_count{{START, 1}};
  while (!stack.empty()) {
    auto &[prev, iter, end] = stack.top();
    if (iter == end) {
      // out of neighbors
      if (seen_count[prev] == 2 && !is_big(prev)) {
        can_visit_twice = true;
      }
      --seen_count[prev];
      stack.pop();
    } else {
      Node u = *(iter++);
      if (u == END) {
        ++count;
      } else {
        bool valid = false;
        if (is_big(u) || seen_count[u] == 0) {
          valid = true;
        } else if (can_visit_twice) {
          valid = true;
          can_visit_twice = false;
        }
        if (valid) {
          ++seen_count[u];
          stack.push(stack_entry(u));
        }
      }
    }
  }
  return count;
}
#undef stack_entry

int main(int argc, char **argv) {
  std::string input_path;
  std::vector<std::string> args{};
  for (int i = 0; i < argc; ++i) {
    args.push_back(argv[i]);
  }
  if (args.size() < 2) {
    input_path = "input/day12.txt";
  } else if (args[1] == "-e") {
    input_path = "example/day12.txt";
  } else if (args[1] == "-i") {
    input_path = args[2];
  }

  Graph G = parse(std::ifstream{input_path});

  // std::cout << "Part 1: " << dfs_step(G, {START}, false) << std::endl;
  // std::cout << "Part 2: " << dfs_step(G, {START}, true) << std::endl;
  // std::cout << "Part 1: " << dfs_iter(G, false) << std::endl;
  std::cout << "Part 2: " << dfs_iter(G, true) << std::endl;
  return 0;
}
