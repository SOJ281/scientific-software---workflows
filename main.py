

stringa = "a & b)"

stringb = "a | b | c"

stringc = "a&((b)|c)"

stringd = "(a&b)||(b&c)"


def HPCParser(expression):
    parsedEx = []
    loc = 0
    if expression[0] in "|&" or expression[-1] in "|&":
        return "error, a logic operators can't be at the start/end", -1

    while loc < len(expression):
        if expression[loc] == "(":
            endLoc = loc
            bracketCounter = 1
            while True:
                endLoc+=1
                if endLoc >= len(expression):
                    return "Error, unclosed brackets", -1
                if expression[endLoc] == '(':
                    bracketCounter += 1
                elif expression[endLoc] == ')':
                    bracketCounter -= 1
                if bracketCounter == 0:
                    break

            ex, miniLoc = HPCParser(expression[loc+1:endLoc])
            if miniLoc == -1:
                return ex, -1
            parsedEx.append(ex)
            loc += miniLoc+1

        elif (expression[loc] in "|&"):
            if expression[loc+1] in "|&":
                return "error, two logic operators can't be together", -1
            parsedEx.append(expression[loc])

        elif expression[loc] == " ":
            exit

        elif expression[loc] == ")":
            return "Error, unclosed brackets", -1
        
        else:
            exLen = 1
            while (loc+exLen < len(expression)):
                if (expression[loc+exLen] in "|&() "):
                    break
                exLen+=1
            parsedEx.append(expression[loc:loc+exLen])
            loc += exLen-1
        loc+=1

    return parsedEx, loc 





def bracketParser(expression):
    parsedEx = []
    loc = 0

    while loc < len(expression):
        if expression[loc] == "(":
            ex, miniLoc = bracketParser(expression[loc+1:-1])
            parsedEx.append(ex)
            loc += miniLoc
        elif expression[loc] == ")":
            return parsedEx, loc+1
        else:
            parsedEx.append(str(expression[loc]))
        loc+=1

    return parsedEx, loc 

def logicParser(expression):
    parsedEx = []
    loc = 0

    while loc < len(expression):
        if expression[loc] == "(":
            ex, miniLoc = bracketParser(expression[loc+1:-1])
            parsedEx.append(ex)
            loc += miniLoc
        elif expression[loc] == ")":
            return parsedEx, loc+1
        else:
            parsedEx.append(expression[loc])
        loc+=1

    while loc < len(expression):
        if type(expression[loc]) != str:
            expression[loc] = logicParser(expression[loc])
        else:
            exp = []



    return parsedEx, loc 

print(HPCParser(stringa))
print(HPCParser(stringb))
print(HPCParser(stringc))
print(HPCParser(stringd))
print(bracketParser("((a)&b)|(b&(c|d))"))