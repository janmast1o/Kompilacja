A = zeros(5);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(10);

# print A;
# print B;
# print I;

a = -.0;
b = .3e3;
c = 1;

A = [[1, 2, 3, 5, 6], [3, 4, 5, 0, 0], [a, b, 2.5, .3, c]];
A[2, 1] = 1;
J = 1;
print A[1, J];
B = A[1, J];
print A[2, 3], 1, "something";

print A, B, J;