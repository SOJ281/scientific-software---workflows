from chattyParser import *
import re

class ParseError(Exception):
    pass

stringa = "a & b"

stringb = "a | b | c"

stringc = "a&((b)|c)"

stringd = "(a&b)|(b&c)"

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
        token_spec = r"""
            \s*(
                [A-Za-z_][A-Za-z0-9_]* |   # identifier
                [&|()]                    # operators and parentheses
            )
        """
        self.tokens = re.findall(token_spec, expression, re.VERBOSE)
        if "".join(self.tokens).replace(" ", "") != expression.replace(" ", ""):
            raise ParseError("Invalid characters in expression")
    
    #Returns next item if it exists
    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None
    
    def getTokens(self):
        return self.getTokens
    
    #Increments program
    def consume(self):
        if self.pos < len(self.tokens):
            self.pos+=1
        
    #Parse expression
    #OUT - list
    def parse(self):
        self.pos = 0
        parsedEx = []
        parsedEx.extend(self.parseOperator())
        if self.peek() is not None:
            raise ParseError("Unexpected token at:" + str(self.peek()))

        return parsedEx
    
    #Parse operators
    #OUT - list
    def parseOperator(self):
        parsedEx = self.parseTerm()

        while self.peek() in "|&":
            parsedEx.extend(self.peek())
            self.consume()
            parsedEx.extend(self.parseTerm())
            if self.peek() == None:
                break

        return parsedEx
    
    #Parse terms
    #OUT - list
    def parseTerm(self):
        parsedEx = []
        nextToken = self.peek()
        
        if nextToken == "(":
            self.consume()
            parsedEx.extend([self.parseOperator()])
            self.consume()
            return parsedEx
        elif nextToken not in ")|&":
            self.consume()
            parsedEx.append(nextToken)
            return parsedEx

        raise ParseError("Unexpected token at end, expected a term, got "+str(nextToken))
        
def HPCTokenizer(expression):
    parser = HPCParsing(expression)
    p = parser.getTokens()
    return p

def HPCParser(expression):
    #print("-")
    #print("EXPRESSION"+ str(expression))
    #print("TOKENIZED"+str(tokenize(expression)))
    parser = HPCParsing(expression)
    #print("RESULT")
    p = parser.parse()
    #print(p)
    #print("END")
    return p

if __name__ == '__main__':
    print(HPCParser(stringa))
    print(HPCParser(stringb))
    print(HPCParser(stringc))
    print(HPCParser(stringd))
    print(HPCParser("apple&banana"))
    #print(tokenize("apple&banana"))

    #print(HPCParser("((a)&bad)|(b&(c|d))")[0])
    #print(bracketParser("((a)&bad)|(b&(c|d))")[0])
    #print("Chatty")
    #print(parse_expression("(aa&bb)|(b&c)"))
    #print(parse_expression('('*3 + "a&b" + ')'*3))
    #print(parse_expression('('*2000 + "a&"*1000 + "a" + ')'*2000))