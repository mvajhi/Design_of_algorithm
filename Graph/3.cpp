#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <tuple>
#include <unordered_map>

using namespace std;

class DSU {
public:
    DSU(int n) {
        parent.resize(n);
        iota(parent.begin(), parent.end(), 0);
        rank.resize(n, 0);
    }

    int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    void unite(int x, int y) {
        int xr = find(x);
        int yr = find(y);
        if (xr != yr) {
            if (rank[xr] < rank[yr]) {
                swap(xr, yr);
            }
            parent[yr] = xr;
            if (rank[xr] == rank[yr]) {
                rank[xr]++;
            }
        }
    }

private:
    vector<int> parent;
    vector<int> rank;
};

vector<tuple<int, int, int>> kruskal(int n, vector<tuple<int, int, int>>& edges) {
    DSU dsu(n);
    vector<tuple<int, int, int>> mst;
    for (auto& [w, u, v] : edges) {
        if (dsu.find(u) != dsu.find(v)) {
            dsu.unite(u, v);
            mst.emplace_back(u, v, w);
        }
    }
    return mst;
}

void dfs(int u, int parent, int depth, const vector<vector<tuple<int, int, int>>>& adj,
         vector<vector<int>>& par, vector<vector<int>>& mx, vector<vector<int>>& mx_idx, vector<int>& dep) {
    dep[u] = depth;
    par[u][0] = parent;
    for (const auto& [v, w, idx] : adj[u]) {
        if (v != parent) {
            mx[v][0] = w;
            mx_idx[v][0] = idx;
            dfs(v, u, depth + 1, adj, par, mx, mx_idx, dep);
        }
    }
}

tuple<vector<vector<int>>, vector<vector<int>>, vector<vector<int>>, vector<int>>
prepare_lca(int n, const vector<vector<tuple<int, int, int>>>& adj) {
    const int LOG = 17;
    vector<vector<int>> par(n, vector<int>(LOG, -1));
    vector<vector<int>> mx(n, vector<int>(LOG, 0));
    vector<vector<int>> mx_idx(n, vector<int>(LOG, -1));
    vector<int> dep(n, 0);

    dfs(0, -1, 0, adj, par, mx, mx_idx, dep);

    for (int j = 1; j < LOG; ++j) {
        for (int i = 0; i < n; ++i) {
            if (par[i][j - 1] != -1) {
                par[i][j] = par[par[i][j - 1]][j - 1];
                mx[i][j] = max(mx[i][j - 1], mx[par[i][j - 1]][j - 1]);
                mx_idx[i][j] = mx[i][j - 1] > mx[par[i][j - 1]][j - 1] ? mx_idx[i][j - 1] : mx_idx[par[i][j - 1]][j - 1];
            }
        }
    }

    return {par, mx, mx_idx, dep};
}

pair<int, vector<int>> lca(int u, int v, const vector<vector<int>>& par, const vector<vector<int>>& mx, const vector<vector<int>>& mx_idx, const vector<int>& dep) {
    int LOG = par[0].size();
    if (dep[u] < dep[v]) swap(u, v);

    int max_weight = 0;
    vector<int> max_edge_indices;

    for (int i = LOG - 1; i >= 0; --i) {
        if (dep[u] - (1 << i) >= dep[v]) {
            if (mx[u][i] > max_weight) {
                max_weight = mx[u][i];
                max_edge_indices = {mx_idx[u][i]};
            } else if (mx[u][i] == max_weight) {
                max_edge_indices.push_back(mx_idx[u][i]);
            }
            u = par[u][i];
        }
    }

    if (u == v) return {max_weight, max_edge_indices};

    for (int i = LOG - 1; i >= 0; --i) {
        if (par[u][i] != par[v][i]) {
            if (mx[u][i] > max_weight) {
                max_weight = mx[u][i];
                max_edge_indices = {mx_idx[u][i]};
            } else if (mx[u][i] == max_weight) {
                max_edge_indices.push_back(mx_idx[u][i]);
            }

            if (mx[v][i] > max_weight) {
                max_weight = mx[v][i];
                max_edge_indices = {mx_idx[v][i]};
            } else if (mx[v][i] == max_weight) {
                max_edge_indices.push_back(mx_idx[v][i]);
            }

            u = par[u][i];
            v = par[v][i];
        }
    }

    if (mx[u][0] > max_weight) {
        max_weight = mx[u][0];
        max_edge_indices = {mx_idx[u][0]};
    } else if (mx[u][0] == max_weight) {
        max_edge_indices.push_back(mx_idx[u][0]);
    }

    if (mx[v][0] > max_weight) {
        max_weight = mx[v][0];
        max_edge_indices = {mx_idx[v][0]};
    } else if (mx[v][0] == max_weight) {
        max_edge_indices.push_back(mx_idx[v][0]);
    }

    return {max_weight, max_edge_indices};
}

vector<string> process_graph(int n, vector<tuple<int, int, int>>& edges) {
    for (auto& [w, u, v] : edges) {
        u--; v--;
    }
    sort(edges.begin(), edges.end());

    vector<string> status(edges.size(), "none");

    auto mst_edges = kruskal(n, edges);
    unordered_map<int, unordered_map<int, int>> mst_set;

    for (const auto& [u, v, w] : mst_edges) {
        status.push_back("any");
        mst_set[min(u, v)][max(u, v)] = w;
    }

    vector<vector<tuple<int, int, int>>> adj(n);
    for (const auto& [u, v, w] : mst_edges) {
        adj[u].emplace_back(v, w, status.size()-1);
        adj[v].emplace_back(u, w, status.size()-1);
    }

    auto [par, mx, mx_idx, dep] = prepare_lca(n, adj);

    for (const auto& [w, u, v] : edges) {
        if (status[status.size()-1] == "none") {
            auto [max_weight, max_edge_indices] = lca(u, v, par, mx, mx_idx, dep);
            if (max_weight == w) {
                status.push_back("at least one");
                for (int edge_idx : max_edge_indices) {
                    status[edge_idx] = "at least one";
                }
            }
        }
    }

    return status;
}

int main() {
    int n, m;
    cin >> n >> m;
    vector<tuple<int, int, int>> edges;

    for (int i = 0; i < m; ++i) {
        int u, v, w;
        cin >> u >> v >> w;
        edges.emplace_back(w, u, v);
    }

    auto result = process_graph(n, edges);
    for (const auto& status : result) {
        cout << status << "\n";
    }

    return 0;
}