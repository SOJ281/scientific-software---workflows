import re

#class ParseError(Exception):
#    pass


'''
def HPCParser(expression):
    expression = expression.replace(" ", "")
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

        elif expression[loc] == ")":
            return "Error, unclosed brackets", -1
        
        else:
            exLen = 1
            while (loc+exLen < len(expression)):
                if (expression[loc+exLen] in "|&()"):
                    break
                exLen+=1
            parsedEx.append(expression[loc:loc+exLen])
            loc += exLen-1
        loc+=1

    return parsedEx, loc 
'''


class HPCParsing:
    #tokenizes the expression
    def __init__(self, expression: str):
        self.expression = expression
        token_spec = r"""
            \s*(
                [A-Za-z_][A-Za-z0-9_]* |   # identifier
                [&|()]                    # operators and parentheses
            )
        """
        self.tokens = re.findall(token_spec, expression, re.VERBOSE)
        if "".join(self.tokens).replace(" ", "") != expression.replace(" ", ""):
            raise Exception("Invalid characters in expression")
    
    #Returns next item if it exists
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def getTokens(self):
        return self.tokens
    
    def getExpression(self):
        return self.expression
    
    #Increments program
    def consume(self, expectedToken=None):
        if expectedToken and self.peek() != expectedToken:
            raise Exception("Expected " + str(expectedToken) + ", got " + str(self.peek()))
        if self.pos >= len(self.tokens):
            raise Exception("Input ended unexpectedly")
        self.pos+=1

        
    #Parse expression
    #Expression :=  OR
    #OUT - list
    def parse(self):
        self.pos = 0
        parsedEx = []
        parsedEx.extend(self.parseOr())
        if self.peek() is not None:
            raise Exception("Unexpected token at:" + str(self.peek()))

        return parsedEx
    
    #Parse or
    #OR :=	AND (“|” AND)*
    #OUT - list
    def parseOr(self):
        parsedEx = self.parseAnd()

        while self.peek() == "|":
            parsedEx.extend(self.peek())
            self.consume("|")
            parsedEx.extend(self.parseAnd())

        return parsedEx

    #Parse and
    #AND :=	TERM (“&” TERM)*
    #OUT - list
    def parseAnd(self):
        parsedEx = self.parseTerm()

        while self.peek() == "&":
            parsedEx.extend(self.peek())
            self.consume("&")
            parsedEx.extend(self.parseTerm())

        return parsedEx
    
    #Parse terms
    #TERM := ID | “(“EPRESSION”)”
    #OUT - list
    def parseTerm(self):
        parsedEx = []
        nextToken = self.peek()
        
        if nextToken == "(":
            self.consume("(")
            parsedEx.extend([self.parseOr()])
            self.consume(")")
            return parsedEx
        elif nextToken not in ")|&":
            self.consume()
            parsedEx.append(nextToken)
            return parsedEx

        raise Exception("Unexpected token at end, expected a term, got "+str(nextToken))
        



def HPCTokenizer(expression):
    parser = HPCParsing(expression)
    t = parser.getTokens()
    return t

def HPCParser(expression):
    parser = HPCParsing(expression)
    p = parser.parse()
    return p


if __name__ == '__main__':
    stringa = "a & b"
    stringb = "a | b | c"
    stringc = "a&(b|c)"
    stringd = "(a&b|(b&c)"
    
    print(HPCParser(stringa))
    print(HPCParser(stringb))
    print(HPCParser(stringc))
    print(HPCParser(stringd))