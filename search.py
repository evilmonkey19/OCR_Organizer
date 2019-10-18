def editDistance(t, p):
    n = len(t)
    m = len(p)

    if m < n:
        return 1.0
    
    dp = [0]*(n+1)
    for i in range(n+1):
        dp[i] = [0]*(m+1)
    for i in range(n+1):
        for j in range(m+1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif t[i-1] == p[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i][j-1], dp[i-1][j-1], dp[i-1][j])  
    return 1.0*(dp[n][m] - (m - n))/n

def search(subject, txtfile):
    lwords = len(subject.split())

    with open(txtfile, "r", encoding="utf-8") as f:
        for l in f:
            offset = 0
            ls = l.split()
            while offset + lwords + 1 <= len(l.split()):
                res = editDistance(subject, " ".join(ls[offset:offset+lwords]).lower())
                if res < 0.2:
                    return True

                res = editDistance(subject, " ".join(ls[offset:offset+lwords+1]).lower())
                if res < 0.2:
                    return True
                
                offset += 1

    return False
