#include <iostream>
#include <vector>
#include <algorithm>

using namespace std;

// تابعی برای محاسبه انرژی کمینه مورد نیاز
long long minEnergy(int start, int end, const vector<int>& people, int A, int B) {
    // محاسبه تعداد افراد ناراضی در این بازه
    auto left = lower_bound(people.begin(), people.end(), start);
    auto right = upper_bound(people.begin(), people.end(), end);
    int count = right - left;
    
    // محاسبه طول این بازه
    int length = end - start + 1;
    
    // اگر هیچ فرد ناراضی وجود نداشت
    if (count == 0) {
        return A;
    }

    // اگر تنها یک خانه باشد
    if (length == 1) {
        return B * count;
    }

    // محاسبه انرژی برای تقسیم نکردن
    long long energyNoSplit = B * count * length;
    
    // محاسبه انرژی برای تقسیم کردن به دو نیمه
    int mid = (start + end) / 2;
    long long energySplit = minEnergy(start, mid, people, A, B) +
                            minEnergy(mid + 1, end, people, A, B);

    // بازگرداندن کمترین انرژی بین تقسیم و تقسیم نکردن
    return min(energyNoSplit, energySplit);
}

int main() {
    int n, k, A, B;
    cin >> n >> k >> A >> B;
    
    vector<int> people(k);
    for (int i = 0; i < k; i++) {
        cin >> people[i];
    }
    
    // مرتب‌سازی برای استفاده از binary search
    sort(people.begin(), people.end());
    
    // محاسبه و چاپ کمترین انرژی مورد نیاز
    cout << minEnergy(1, 1 << n, people, A, B) << endl;
    
    return 0;
}
