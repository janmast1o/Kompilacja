A = zeros(5);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(10);

print A;
print B;
print I;

A = [[1,2,3], [3,4,5], ["a", "b", 2.5, .3, "c"]];
A[2, 3, 1] = 1;
J = 1;
B = A[1, J];
print A[2, 3], 1, "something";

print A, B, J;