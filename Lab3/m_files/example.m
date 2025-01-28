A = zeros(5);  # create 5x5 matrix filled with zeros
B = ones(7);   # create 7x7 matrix filled with ones
I = eye(10);

A = [[[1, 2], [3]], [2, 4, 55.1, "something", I]];
A[2, 3, 1] = 1;
print A[2, 3], 1, "something";