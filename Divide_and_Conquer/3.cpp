#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

// https://chatgpt.com/share/671565c7-bd24-8001-8ea5-605b2ecba5f8
// کد را رفع اشکال و سریع کن

int n, k, A, B;
vector<int> queue;

pair<int, int> find_bounds(int left, int right, int target_left, int target_right) {
    int lower = lower_bound(queue.begin() + left, queue.begin() + right, target_left) - queue.begin();
    int upper = upper_bound(queue.begin() + left, queue.begin() + right, target_right) - queue.begin();
    return {lower, upper};
}

long long solve(int target_left, int target_right) {
    auto bounds = find_bounds(0, k, target_left, target_right);
    int first_occurrence = bounds.first, last_occurrence = bounds.second;
    int count = last_occurrence - first_occurrence;

    if (count == 0) {
        return A;
    }

    long long length = target_right - target_left + 1;
    long long cost = 1LL * B * count * length;

    if (target_left == target_right) {
        return cost;
    }

    int mid = (target_left + target_right) / 2;

    long long cost_left = solve(target_left, mid);
    long long cost_right = solve(mid + 1, target_right);

    return min(cost, cost_left + cost_right);
}

int main() {
    cin >> n >> k >> A >> B;
    queue.resize(k);
    for (int i = 0; i < k; ++i) {
        cin >> queue[i];
    }
    sort(queue.begin(), queue.end());

    cout << solve(1, (1 << n)) << endl;
    return 0;
}
