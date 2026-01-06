

stringa = "a&b"

stringb = "a|b|c"

stringc = "a&(b|c)"

stringd = "(a&b)|(b&c)"

def HPCParser(expression):
    parsedEx = []
    loc = 0

    while loc < len(expression):
        if expression[loc] == "(":
            ex, miniLoc = HPCParser(expression[loc+1:-1])
            parsedEx.append(ex)
            loc += miniLoc
        elif expression[loc] == ")":
            return parsedEx, loc+1
        else:
            if ((expression[loc] in "|&") and (expression[loc-1] in "|&")):
                return "error", -1
            parsedEx.append(expression[loc])
        loc+=1

    return parsedEx, loc 


print(HPCParser(stringa))
print(HPCParser(stringb))
print(HPCParser(stringc))
print(HPCParser(stringd))