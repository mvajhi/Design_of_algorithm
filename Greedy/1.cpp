#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

bool check(long long int mid, vector<long long int> ages, long long int k) {
    long long int count = 0;
    for (size_t i = 0; i < ages.size() - 1; i++) {
        long long int new_count = (ages[i] + ages[i + 1]) / mid;
        count += new_count;
        ages[i + 1] -= max(0LL, new_count * mid - ages[i]);
    }
    return count >= k;
}

void solve(long long int n, long long int k, vector<long long int>& ages) {
    if (n == 1) {
        cout << (ages[0] / k) * k << endl;
        return;
    }
    if (n == 0) {
        cout << 0 << endl;
        return;
    }

    long long int max_count = ages[0];
    for (long long int i = 0; i < n - 1; i++) {
        max_count = max(max_count, ages[i] + ages[i + 1]);
    }
    long long int min_count = max_count / k;
    // long long int min_count = 1;

    long long int ans = 0;
    while (min_count <= max_count) {
        long long int mid = (min_count + max_count) / 2;
        if (check(mid, ages, k)) {
            min_count = mid + 1;
            ans = mid;
        } else {
            max_count = mid - 1;
        }
    }

    cout << ans * k << endl;
}

int main() {
    long long int t;
    cin >> t;
    while (t--) {
        long long int n, k;
        cin >> n >> k;
        vector<long long int> ages(n);
        for (long long int i = 0; i < n; ++i) {
            cin >> ages[i];
        }
        solve(n, k, ages);
    }
    return 0;
}