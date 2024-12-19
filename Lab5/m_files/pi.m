pi = 0.0;
n = 1;
for i = 1:100000 {
    # print pi;
    pi += 4.0 / n - 4.0 / (n + 2);
    n += 4;
}
print pi;
