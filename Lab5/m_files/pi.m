pi = 0.0;
n = 1;

A = [[1, 2, 3, 4]];
B = A ' ;
print B;

for i = 1:100000 {
    # print pi;
    pi += 4.0 / n - 4.0 / (n + 2);
    n += 4;
}
print pi;
