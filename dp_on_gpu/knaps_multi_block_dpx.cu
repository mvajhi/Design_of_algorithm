#include <iostream>
#include <vector>
#include <algorithm>
#include <ctime> 
using namespace std;

void generateRandomInput(vector<int>& weights, vector<int>& profits, int n, int maxWeight, int maxProfit) {
    for (int i = 0; i < n; i++) {
        weights.push_back(1 + rand() % maxWeight); // وزن تصادفی بین 1 و maxWeight
        profits.push_back(1 + rand() % maxProfit); // سود تصادفی بین 1 و maxProfit
    }
}

// Function to find the maximum profit
int knapSack(int W, vector<int> wt, vector<int> val) {
  
    // Making and initializing dp vector
    vector<int> dp(W + 1, 0);
    vector<int> dp_pre(W + 1, 0);

    for (int i = 1; i <= wt.size(); i++) {
        for (int w = W; w >= 0; w--) {
            if (wt[i - 1] <= w)
              
                // Finding the maximum value
                dp[w] = max(dp_pre[w], dp_pre[w - wt[i - 1]] + val[i - 1]);
        }
        dp_pre = dp;
    }
    return dp[W];
}

__global__ void knapSackKernel_dpx(int W, int n, int* wt, int* val, int* dp_pre, int* dp, int i) {
    int w = threadIdx.x + blockIdx.x * blockDim.x; // محاسبه اندیس وزن
    bool t;

    if (w <= W) {
        if (wt[i - 1] <= w) {
            dp[w] = __vibmax_u32(dp_pre[w], dp_pre[w - wt[i - 1]] + val[i - 1], &t);
        } else {
            dp[w] = dp_pre[w];
        }
    }
}

int knapSackCUDA_dpx(int W, vector<int>& wt, vector<int>& val) {
    int n = wt.size();
    int *d_wt, *d_val, *d_dp, *d_dp_pre;

    // تخصیص حافظه روی دستگاه
    cudaMalloc(&d_wt, n * sizeof(int));
    cudaMalloc(&d_val, n * sizeof(int));
    cudaMalloc(&d_dp, (W + 1) * sizeof(int));
    cudaMalloc(&d_dp_pre, (W + 1) * sizeof(int));

    // کپی داده‌ها از میزبان به دستگاه
    cudaMemcpy(d_wt, wt.data(), n * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(d_val, val.data(), n * sizeof(int), cudaMemcpyHostToDevice);

    // مقداردهی اولیه به dp
    cudaMemset(d_dp, 0, (W + 1) * sizeof(int));
    cudaMemset(d_dp_pre, 0, (W + 1) * sizeof(int));

    int threadsPerBlock = 256;
    int numBlocks = (W + threadsPerBlock - 1) / threadsPerBlock;

    clock_t start_gpu = clock();

    // اجرای حلقه‌های جداگانه برای هر آیتم
    for (int i = 1; i <= n; i++) {
        knapSackKernel_dpx<<<numBlocks, threadsPerBlock>>>(W, n, d_wt, d_val, d_dp_pre, d_dp, i);
        cudaDeviceSynchronize(); // اطمینان از تکمیل تمام بلاک‌ها

        // کپی dp به dp_pre برای مرحله بعدی
        cudaMemcpy(d_dp_pre, d_dp, (W + 1) * sizeof(int), cudaMemcpyDeviceToDevice);
    }

    clock_t end_gpu = clock();

    // کپی نتیجه نهایی dp[W]
    int result = 0;
    cudaMemcpy(&result, &d_dp[W], sizeof(int), cudaMemcpyDeviceToHost);

    double gpu_time = 1000.0 * (end_gpu - start_gpu) / CLOCKS_PER_SEC;
    cout << "GPU dpx Result: " << result << ", Time: " << gpu_time << " ms" << endl;

    // آزادسازی حافظه دستگاه
    cudaFree(d_wt);
    cudaFree(d_val);
    cudaFree(d_dp);
    cudaFree(d_dp_pre);

    return result;
}

__global__ void knapSackKernel(int W, int n, int* wt, int* val, int* dp_pre, int* dp, int i) {
    int w = threadIdx.x + blockIdx.x * blockDim.x; // محاسبه اندیس وزن

    if (w <= W) {
        if (wt[i - 1] <= w) {
            dp[w] = max(dp_pre[w], dp_pre[w - wt[i - 1]] + val[i - 1]);
        } else {
            dp[w] = dp_pre[w];
        }
    }
}

int knapSackCUDA(int W, vector<int>& wt, vector<int>& val) {
    int n = wt.size();
    int *d_wt, *d_val, *d_dp, *d_dp_pre;

    // تخصیص حافظه روی دستگاه
    cudaMalloc(&d_wt, n * sizeof(int));
    cudaMalloc(&d_val, n * sizeof(int));
    cudaMalloc(&d_dp, (W + 1) * sizeof(int));
    cudaMalloc(&d_dp_pre, (W + 1) * sizeof(int));

    // کپی داده‌ها از میزبان به دستگاه
    cudaMemcpy(d_wt, wt.data(), n * sizeof(int), cudaMemcpyHostToDevice);
    cudaMemcpy(d_val, val.data(), n * sizeof(int), cudaMemcpyHostToDevice);

    // مقداردهی اولیه به dp
    cudaMemset(d_dp, 0, (W + 1) * sizeof(int));
    cudaMemset(d_dp_pre, 0, (W + 1) * sizeof(int));

    int threadsPerBlock = 256;
    int numBlocks = (W + threadsPerBlock - 1) / threadsPerBlock;

    clock_t start_gpu = clock();

    // اجرای حلقه‌های جداگانه برای هر آیتم
    for (int i = 1; i <= n; i++) {
        knapSackKernel<<<numBlocks, threadsPerBlock>>>(W, n, d_wt, d_val, d_dp_pre, d_dp, i);
        cudaDeviceSynchronize(); // اطمینان از تکمیل تمام بلاک‌ها

        // کپی dp به dp_pre برای مرحله بعدی
        cudaMemcpy(d_dp_pre, d_dp, (W + 1) * sizeof(int), cudaMemcpyDeviceToDevice);
    }

    clock_t end_gpu = clock();

    // کپی نتیجه نهایی dp[W]
    int result = 0;
    cudaMemcpy(&result, &d_dp[W], sizeof(int), cudaMemcpyDeviceToHost);

    double gpu_time = 1000.0 * (end_gpu - start_gpu) / CLOCKS_PER_SEC;
    cout << "GPU Result: " << result << ", Time: " << gpu_time << " ms" << endl;

    // آزادسازی حافظه دستگاه
    cudaFree(d_wt);
    cudaFree(d_val);
    cudaFree(d_dp);
    cudaFree(d_dp_pre);

    return result;
}

int main() {
     auto seed = time(0);
    // auto seed = 1733565654;
    cout << "Random seed: " << seed << endl;
    srand(seed); // مقداردهی اولیه برای تولید اعداد تصادفی

    int n = 2000; // تعداد آیتم‌ها
    int W = 100000; // ظرفیت کوله‌پشتی
    int maxWeight = 50; // بیشترین وزن ممکن
    int maxProfit = 100; // بیشترین سود ممکن

    vector<int> weights;
    vector<int> profits;

    // تولید ورودی تصادفی
    generateRandomInput(weights, profits, n, maxWeight, maxProfit);

    // اندازه‌گیری زمان اجرای CPU
    clock_t start_cpu = clock();
    int cpu_result = knapSack(W, weights, profits);
    clock_t end_cpu = clock();
    double cpu_time = 1000.0 * (end_cpu - start_cpu) / CLOCKS_PER_SEC;

    // اندازه‌گیری زمان اجرای GPU
    int gpu_dpx_result = knapSackCUDA_dpx(W, weights, profits);
    int gpu_result = knapSackCUDA(W, weights, profits);

    // نتایج و مقایسه زمان
    cout << "CPU Result: " << cpu_result << ", Time: " << cpu_time << " ms" << endl;

    return 0;
}