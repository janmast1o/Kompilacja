# control flow instruction

N = 10;
M = 20;
for i = 1:N {
    for j = i:M {
        print i, j;
    }
}

while(k>0) {
    if(k<5)
        i = 1;
    else if(k<10)
        i = 2;   
    else
        i = 3;
    
    k = k - 1;
}

S = 2 * -1;
R = [1, 2];
R[1, 2] = R[1, 3];

G = [[1, 2],
    []];
