#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

const int MAXN = 500005;

int n, m, q;
vector<pair<int, pair<int, int>>> edges;

int parent[MAXN], depth[MAXN];
int up[MAXN][20], maxEdge[MAXN][20];

vector<pair<int, int>> adj[MAXN];

void make_set() {
    for (int i = 1; i <= n; i++)
        parent[i] = i;
}

int find_set(int v) {
    if (v == parent[v])
        return v;
    return parent[v] = find_set(parent[v]);
}

bool union_sets(int a, int b) {
    a = find_set(a);
    b = find_set(b);
    if (a != b) {
        parent[b] = a;
        return true;
    }
    return false;
}

void dfs(int v, int p) {
    for (auto edge : adj[v]) {
        int u = edge.first;
        int w = edge.second;
        if (u != p) {
            depth[u] = depth[v] + 1;
            up[u][0] = v;
            maxEdge[u][0] = w;
            for (int i = 1; i < 20; i++) {
                up[u][i] = up[up[u][i - 1]][i - 1];
                maxEdge[u][i] = max(maxEdge[u][i - 1], maxEdge[up[u][i - 1]][i - 1]);
            }
            dfs(u, v);
        }
    }
}

int getMaxEdge(int u, int v) {
    if (depth[u] < depth[v])
        swap(u, v);
    int res = 0;
    for (int i = 19; i >= 0; i--) {
        if (depth[u] - (1 << i) >= depth[v]) {
            res = max(res, maxEdge[u][i]);
            u = up[u][i];
        }
    }
    if (u == v)
        return res;
    for (int i = 19; i >= 0; i--) {
        if (up[u][i] != up[v][i]) {
            res = max(res, maxEdge[u][i]);
            res = max(res, maxEdge[v][i]);
            u = up[u][i];
            v = up[v][i];
        }
    }
    res = max(res, maxEdge[u][0]);
    res = max(res, maxEdge[v][0]);
    return res;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    cin >> n >> m;
    edges.resize(m);
    for (int i = 0; i < m; i++) {
        int u, v, w;
        cin >> u >> v >> w;
        edges[i] = {w, {u, v}};
    }

    // ساخت MST
    sort(edges.begin(), edges.end());
    make_set();
    vector<pair<int, pair<int, int>>> mst_edges;
    for (auto edge : edges) {
        int w = edge.first;
        int u = edge.second.first;
        int v = edge.second.second;
        if (union_sets(u, v)) {
            mst_edges.push_back(edge);
            adj[u].push_back({v, w});
            adj[v].push_back({u, w});
        }
    }

    // آماده‌سازی برای LCA
    depth[1] = 0;
    up[1][0] = 1;
    maxEdge[1][0] = 0;
    dfs(1, -1);

    cin >> q;
    while (q--) {
        int k;
        cin >> k;
        vector<int> req_edges(k);
        vector<pair<int, pair<int, int>>> extra_edges;
        for (int i = 0; i < k; i++) {
            cin >> req_edges[i];
            req_edges[i]--; // صفر مبنا
            int u = edges[req_edges[i]].second.first;
            int v = edges[req_edges[i]].second.second;
            int w = edges[req_edges[i]].first;
            extra_edges.push_back({w, {u, v}});
        }

        bool ok = true;
        for (auto edge : extra_edges) {
            int u = edge.second.first;
            int v = edge.second.second;
            int w = edge.first;
            int max_w = getMaxEdge(u, v);
            if (max_w > w) {
                ok = false;
                break;
            }
        }

        if (ok)
            cout << "YES\n";
        else
            cout << "NO\n";
    }

    return 0;
}