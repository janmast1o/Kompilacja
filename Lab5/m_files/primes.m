for n = 2:100 {
    p = 1;
    upper_bound = n-1;
    for d = 2:upper_bound {
        nc = n;
        while (nc > 0) nc -= d;
        if (nc == 0) {
            p = 0;
            break;
        }
    }
    if (p == 1) {
        print n;
    }
}
