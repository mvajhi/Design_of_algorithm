// https://chatgpt.com/share/67619d10-a894-8001-ac8a-2bbee1f9fd1a
// صورت سوال
// کدت درست نیست روی تست
// فقط یال های تویmst رو بررسی می کنی
// جواب های دوبخش قبلی رو باهم ادغام کن
// تبدیل کن به cpp
#include <bits/stdc++.h>
using namespace std;

struct Edge {
    int u, v, w, idx;
    bool operator<(const Edge &other) const { return w < other.w; }
};

class DSU {
    vector<int> parent, rank;
public:
    DSU(int n) {
        parent.resize(n);
        rank.assign(n, 0);
        iota(parent.begin(), parent.end(), 0); // مقداردهی اولیه parent[i] = i
    }

    int find(int x) {
        if (parent[x] != x) parent[x] = find(parent[x]);
        return parent[x];
    }

    bool unionSets(int x, int y) {
        int xr = find(x), yr = find(y);
        if (xr == yr) return false;
        if (rank[xr] < rank[yr])
            parent[xr] = yr;
        else if (rank[xr] > rank[yr])
            parent[yr] = xr;
        else {
            parent[yr] = xr;
            rank[xr]++;
        }
        return true;
    }

    void reset(int x) { parent[x] = x; }
};

int n, m;
vector<Edge> edges;

vector<string> solve() {
    sort(edges.begin(), edges.end());

    DSU dsu(n);
    vector<Edge> mstEdges;
    vector<bool> isInMST(m, false);
    int mstWeight = 0;

    // مرحله 1: ساخت MST و انتخاب یال‌ها
    for (auto &e : edges) {
        if (dsu.unionSets(e.u, e.v)) {
            mstEdges.push_back(e);
            isInMST[e.idx] = true;
            mstWeight += e.w;
        }
    }

    vector<string> answers(m, "none");

    // مرحله 2: بررسی یال‌ها برای "at least one"
    for (auto &e : edges) {
        if (isInMST[e.idx]) {
            answers[e.idx] = "at least one";
        } else {
            // یال غیر از MST، بررسی می‌کنیم که آیا وزن آن برابر وزن MST است؟
            DSU tempDSU(n);
            int tempWeight = 0;
            for (auto &f : edges) {
                if (f.idx != e.idx && tempDSU.unionSets(f.u, f.v)) {
                    tempWeight += f.w;
                }
            }
            if (tempWeight == mstWeight) {
                answers[e.idx] = "at least one";
            }
        }
    }

    // مرحله 3: بررسی یال‌های "any" (یال‌های ضروری)
    for (auto &e : mstEdges) {
        DSU tempDSU(n);
        int tempWeight = 0;
        for (auto &f : edges) {
            if (f.idx != e.idx && tempDSU.unionSets(f.u, f.v)) {
                tempWeight += f.w;
            }
        }
        if (tempWeight > mstWeight) {
            answers[e.idx] = "any";
        }
    }

    return answers;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(0);

    cin >> n >> m;
    edges.resize(m);
    for (int i = 0; i < m; i++) {
        cin >> edges[i].u >> edges[i].v >> edges[i].w;
        edges[i].u--, edges[i].v--;
        edges[i].idx = i;
    }

    vector<string> result = solve();
    for (const auto &res : result) {
        cout << res << "\n";
    }

    return 0;
}
