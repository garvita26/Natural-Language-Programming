import nltk
from nltk.parse import RecursiveDescentParser
from string import letters
import copy
import re



def empty(rules,non_terminals):
    #print "in empty ",len(rules)
    # list with keys of empty rules
    e_list = []

    # find  non-terminal rules and add them in list
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            # if key gives an empty state and is not in list, add it
            if values[i] == 'e' and key not in e_list:
                e_list.append(key)
                # remove empty state
                rules[key].remove(values[i])
        # if key doesn't contain any values, remove it from dictionary
        if len(rules[key]) == 0:
            if key not in rules:
                non_terminals.remove(key)
            rules.pop(key, None)
    #print "elist ",e_list        
# delete empty rules
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            # check for rules in the form A->BC or A->CB, where B is in e_list
            # and C in vocabulary
            term=values[i].split(" ")
            if len(term) == 2:
                # check for rule in the form A->BC, excluding the case that
                # gives A->A as a result)
                if term[0] in e_list and key!=term[1]:
                    rules.setdefault(key, []).append(term[1])
                # check for rule in the form A->CB, excluding the case that
                # gives A->A as a result)
                if term[1] in e_list and key!=term[0]:
                    if term[0]!=term[1]:
                        rules.setdefault(key, []).append(term[0])

    return rules,non_terminals


def rule3(rules,let,terminals,non_terminals):

    #print "in rule3 ",len(rules)
    #print let
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        values = new_dict[key]
        for i in range(len(values)):
            #print "value ", values," len(values) " ,len(values)
            terms=values[i].split(" ")
            #print "values[i] ",values[i]
            if '' in terms:
                terms.remove('')
            
            # Check if we have a rule violation
            if len(terms) > 2:
                #print "terms ",terms
                for j in range(0, len(terms) - 2):
                    # replace first rule
                    if j==0:
                        
                        rules[key][i] = terms[0] + " "+let[0]
                        #print "key ",key
                        #print "values ",type(rules[key][i])
                        #print "\n"
                    # add new rules
                    else:
                        rules.setdefault(new_key, []).append(terms[j] + " "+let[0])
                        
                    non_terminals.append(let[0])
                    # save letter, as it'll be used in next rule
                    new_key = copy.deepcopy(let[0])
                    # remove letter from free letters list
                    let.remove(let[0])
                # last 2 letters remain always the same
                t=terms[-2:]
                t=" ".join(t)
                
                rules.setdefault(new_key, []).append(t)
                    
               
    
    return rules,let,terminals,non_terminals

def check(rules,t):
    #print "t ",t
    flag=0
    value=0
    for key in rules:
        values=rules[key]
        #print "key ",key , "values ",values
        if len(values)==1:
            #print "values ",values
            term=values[0].split(" ")
            if re.match(t,term[0]):
                flag=1
                value=key
                break
            
    return flag,value
     

def rule1(rules,let,terminals,non_terminals):
    #print "in rule 1 ",len(rules)
    new_dict = copy.deepcopy(rules)
    for key in new_dict:
        if re.match(key,'e'):
            print key
        values = new_dict[key]
        for i in range(len(values)):
            #print type(values[i])
            terms=values[i].split(" ")
            if '' in terms:
                terms.remove('')
            if len(terms) == 2:
                if (terms[0] in terminals and terms[1] in non_terminals):
                    flag,value=check(rules,terms[0])
                    if flag==1:
                        rules[key][i] =  value+ " "+terms[1]
                    #rules.setdefault(let[0], []).append(terms[0])
                    else:
                        rules[key][i] =  let[0]+ " "+terms[1]
                        rules.setdefault(let[0], []).append(terms[0])
                        non_terminals.append(let[0]) 
                        let.remove(let[0])
                elif (terms[1] in terminals and terms[0] in non_terminals):
                    flag,value=check(rules,terms[1])
                    if flag==1:
                        rules[key][i] =  terms[0]+ " "+value
                    else:
                        rules[key][i] =  terms[0]+" "+let[0]
                        rules.setdefault(let[0], []).append(terms[1])    
                        non_terminals.append(let[0]) 
                        let.remove(let[0])
    #print "after rule 1 ",len(rules)
    return rules,let,terminals,non_terminals           
                
def derivable(rules,V,non_terminals,terminals):
    W=[]
    W1=[]
    k=[]
    if V=='SIGMA ':
        pass
        #print rules[V]
    for key in rules:
        k.append(key)
        
    values=rules[V]
    #print values
    count=0
    for i in range(len(values)):
        #print values[i]
        terms=values[i].split(" ")
        #print terms
        if '' in terms:
            terms.remove('')
        if len(terms)==1 and not re.match('\'(.+?)\'',values[i]) and not re.match('\"(.+?)\"',values[i]):
            if V=='SIGMA ':
                count+=1
                #print values[i]
            #print "hi"
            W.append(values[i])
    if V=='SIGMA ':
        print "before ",count  
    
    for i in W:
        W1.append(i)
    
    for C in W1:
        
        #print "C ",type(C)
        #print rules['x ']
        if C+" " in rules:
            values=rules[C+" "]
            #print values
            for i in range(len(values)):
                terms=values[i].split(" ")
                if '' in terms:
                    terms.remove('')
                #print terms    
                if len(terms)==1 and not re.match('\'(.+?)\'',values[i]) and not re.match(values[i],V) :
                    #print 'hi'
                    #print values[i]
                    W.append(values[i])

    if V=='SIGMA ':
        print "after ",len(W)
        
    return W        

        
        
        
    
# Remove short rules (A->B)
def rule2(rules,let,terminals,non_terminals):
    #print "in rule2 ",len(rules)
    new_dict = copy.deepcopy(rules)
    #print "T ",terminals 
    
    count=0
    for V in new_dict:
        
        count+=1
        values_V=new_dict[V]
        W=derivable(rules,V,non_terminals,terminals)
        if V=='SIGMA ':
            print "in rule2 ",len(W)
        for B in W:
            if B+" " in new_dict:
                if V=='SIGMA ':
                    pass
                   # print "S ",new_dict[B+" "]
                values = new_dict[B+" "]
                for i in range(len(values)):
                    terms=values[i].split(" ")
                    if '' in terms:
                        terms.remove('')
                    if (len(terms)==1 and terms[0] in terminals) or len(terms)>1:
                        if not values[i] in values_V:
                            if V=='SIGMA ':
                                pass
                                #print "S ",values[i]
                                #print "\n"
                            rules[V].append(values[i])
       
    #print "count ",count                    
    new_d = copy.deepcopy(rules)                
    for key in new_d:
        values=new_d[key]
        for i in range(len(values)):
            terms=values[i].split(" ")
            if '' in terms:
                terms.remove('')
            if len(terms)==1 and terms[0] in non_terminals:
                
                #print "to remove ",values[i]    
                rules[key].remove(values[i])
            if len(rules[key]) == 0:
                rules.pop(key, None)

    return rules,let,terminals,non_terminals            
                






def print_rules(rules):
    S=""
    for key in rules:
        values = rules[key]
        S+=str(key) + ' -> '
        for i in range(0,len(values)):
            v=values[i].split(" ")
            if '' in v:
                v.remove('')
               
            S+=str(" ".join(v))+" | "
        
            
        S=S[:-2]    
        S+="\n"
        
    return S

def CNF(grammar):
    S=grammar.start()
    prod=[]
    rules = {}
    non_terminals = []
    terminals=[]
    NT=[]
    
    # This list's going to be our "letters pool" for naming new states
    let=[]
    for j in range(1,26):
        for i in range(1,600):
            let.append(str(letters[j-1:j])+str(i))

    #print "let ",len(let)
    with open('original_grammar.txt','w') as f:
        for i in grammar.productions():
            f.write(str(i))
            f.write('\n')
            NT.append(i.lhs())
            
            prod.append(str(i))
    NT=list(set(NT))        
    #print len(NT)
    
    
        
    for i in range(len(prod)):
        LHS,RHS=prod[i].split("-> ")
        LHS_t=LHS.split(" ")
        
        RHS_t=RHS.split(" ")
        
        for l in LHS_t:
            #print l
            if l!='e' and l not in non_terminals:
                non_terminals.append(l)

    #print "NT ",len(non_terminals)
    
    for i in range(len(prod)):
        LHS,RHS=prod[i].split("-> ")
        LHS_t=LHS.split(" ")
        #LHS_t.remove('')
        RHS_t=RHS.split(" ")
        #RHS_t.remove('')        
        for l in RHS_t:
            if l!='e' and l not in non_terminals and l not in terminals:
                terminals.append(l)
            
        # Insert rule to dictionary
        rules.setdefault(LHS, []).append(RHS)
    with open("rules.txt",'w') as f:
        for key in rules:
            f.write(str(key))
            f.write("\t")
            f.write(str(rules[key]))
            f.write("\n")
     #   f.write(str(rules))
    #print "T ",len(terminals)

    rules,non_terminals=empty(rules,non_terminals)
    print "NT after empty ",len(non_terminals)
        #unit productions
    rules,let,terminals,non_terminals = rule2(rules,let,terminals,non_terminals)
    print "NT after unit ",len(non_terminals)
    #print "SIGMA ",rules['SIGMA ']
    #more than 2 NT
    rules,let,terminals,non_terminals = rule3(rules,let,terminals,non_terminals)
    print "NT after @NT ",len(non_terminals)
    #print "T after 2NT ",len(terminals)
    #mix of T and NT
    
    rules,let,terminals,non_terminals = rule1(rules,let,terminals,non_terminals)
    #print "T after mix  ",len(terminals)
    
    S=print_rules(rules)    
    return S,non_terminals,terminals,rules    



# load the grammar
grammar = nltk.data.load("grammars/large_grammars/atis.cfg")
gf=nltk.grammar.induce_pcfg(grammar.start(),grammar.productions())
#print gf
groucho_grammar = nltk.CFG.fromstring("""
S -> A 'a' | B | 'c'
B -> A | 'bb'
A -> 'a' | 'bc' | B

""")
#print groucho_grammar
S,non_terminals,terminals,rules=CNF(grammar)
cnf=nltk.CFG.fromstring(S)
gf2=nltk.grammar.induce_pcfg(cnf.start(),cnf.productions())

with open("test1","w") as f:
    for i in cnf.productions():
        f.write(str(i))
        f.write("\n")

    
#print "cnf ",cnf
#print cnf.start()
#print rules['SIGMA ']


print(cnf.is_chomsky_normal_form())
rd = RecursiveDescentParser(grammar)
# load the raw sentences
s = nltk.data.load("grammars/large_grammars/atis_sentences.txt", "raw")
# extract the test sentences
t = nltk.parse.util.extract_test_sentences(s)
#print t
# initialize the parser
parser = nltk.parse.BottomUpChartParser(grammar)
# parse all test sentences
for sentence in t:
    try:
        parser.chart_parse(sentence[0])
        break
    except ValueError:
        print("Oops!  That was no valid number.  Try again...")

    
