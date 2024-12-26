// https://poe.com/s/gHEbsC9nTR5mpiMsnCSq
// تبدیل کن به CPP
// کد پایتون رو چت جی پیتی زدم سایتش پایین اومده کار نمی کنه به دلیل کمبود وقت ایمیل می کنم براتون

#include <iostream>
#include <vector>
#include <algorithm>
#include <tuple>
#include <climits>  // Include this for INT_MAX

class UnionFind {
public:
    UnionFind(int n) {
        parent.resize(n);
        rank.resize(n, 0);
        for (int i = 0; i < n; ++i) {
            parent[i] = i;
        }
    }

    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void unionSets(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);
        if (rootX != rootY) {
            if (rank[rootX] > rank[rootY]) {
                parent[rootY] = rootX;
            } else if (rank[rootX] < rank[rootY]) {
                parent[rootX] = rootY;
            } else {
                parent[rootY] = rootX;
                ++rank[rootX];
            }
        }
    }

private:
    std::vector<int> parent;
    std::vector<int> rank;
};

std::pair<int, std::vector<std::tuple<int, int, int>>> kruskal(int n, std::vector<std::tuple<int, int, int>> edges, std::vector<std::tuple<int, int, int>> forcedEdges = {}) {
    UnionFind uf(n);
    int mstWeight = 0;
    int mstEdges = 0;
    std::vector<std::tuple<int, int, int>> selectedEdges;

    // Add forced edges first
    for (const auto& edge : forcedEdges) {
        int u, v, w;
        std::tie(u, v, w) = edge;
        if (uf.find(u) != uf.find(v)) {
            uf.unionSets(u, v);
            mstWeight += w;
            mstEdges++;
            selectedEdges.push_back(edge);
        } else {
            return {INT_MAX, {}};  // Use INT_MAX from climits
        }
    }

    // Sort edges by weight
    std::sort(edges.begin(), edges.end(), [](const auto& a, const auto& b) {
        return std::get<2>(a) < std::get<2>(b);
    });

    // Add remaining edges
    for (const auto& edge : edges) {
        int u, v, w;
        std::tie(u, v, w) = edge;
        if (uf.find(u) != uf.find(v)) {
            uf.unionSets(u, v);
            mstWeight += w;
            mstEdges++;
            selectedEdges.push_back(edge);
            if (mstEdges == n - 1) {
                break;
            }
        }
    }

    if (mstEdges == n - 1) {
        return {mstWeight, selectedEdges};
    } else {
        return {INT_MAX, {}};  // Use INT_MAX from climits
    }
}

int main() {
    int n, m;
    std::cin >> n >> m;
    std::vector<std::tuple<int, int, int>> edges(m);
    for (int i = 0; i < m; ++i) {
        int u, v, w;
        std::cin >> u >> v >> w;
        edges[i] = {u - 1, v - 1, w};  // Convert to 0-based index
    }


    int q;
    std::cin >> q;
    std::vector<std::vector<std::tuple<int, int, int>>> queries(q);
    for (int i = 0; i < q; ++i) {
        int k;
        std::cin >> k;
        queries[i].resize(k);
        for (int j = 0; j < k; ++j) {
            int idx;
            std::cin >> idx;
            queries[i][j] = edges[idx - 1];  // Convert to 0-based index
        }
    }

    // Sort edges by weight
    std::sort(edges.begin(), edges.end(), [](const auto& a, const auto& b) {
        return std::get<2>(a) < std::get<2>(b);
    });
    // Compute the MST weight of the original graph
    auto baseMST = kruskal(n, edges);

    // Process each query
    std::vector<std::string> results;
    for (const auto& query : queries) {
        auto mstWeight = kruskal(n, edges, query);
        results.push_back(mstWeight.first == baseMST.first ? "YES" : "NO");
    }

    // Output results
    for (const auto& result : results) {
        std::cout << result << std::endl;
    }

    return 0;
}