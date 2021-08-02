
def solution(x):
    string = str(x)
    
    if string[0] == '-':
        return int('-'+string[:0:-1])
    else:
        return int(string[::-1])
print(solution(1223456789))

def mySoln(n,m):
    return str(n+m)
print(mySoln(364,1836))