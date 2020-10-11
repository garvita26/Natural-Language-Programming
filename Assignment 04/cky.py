import nltk
#from node import Node
import numpy as np


def printParseTrees(nodes_back,length):
    check = False
    universal=0
    for i in range(len(nodes_back[0][length])):
        
        if nodes_back[0][length][i][0] == ['SIGMA']:
            universal=universal+1
            #print nodes_back[0][length][i]
            print(getParseTree(nodes_back[0][length][i], 3,nodes_back))
	    #print()
	    check = True

    if not check:
        print('The given sentence is not valid according to the grammar.')
    return universal    


def getParseTree(root, indent,nodes_back):
    if root[4]==['T']:
        return '(' + root[0][0] + ' ' + root[1][0] + ')'

    new1 = indent + 2 + len(nodes_back[root[2][0]][root[2][1]][root[2][2]][0]) #len(tree[1][0])
    new2 = indent + 2 + len(nodes_back[root[3][0]][root[3][1]][root[3][2]][0]) #len(tree[2][0])
    #print len((nodes_back[0][1]))
    left = getParseTree((nodes_back[root[2][0]][root[2][1]][root[2][2]]), new1,nodes_back)
    right = getParseTree((nodes_back[root[3][0]][root[3][1]][root[3][2]]), new2,nodes_back)
    return '(' + root[0][0] + ' ' + left + '\n' + ' '*indent + right + ')'


def parser(sentence,grammar):
    # Create the CYK table
    print sentence
    #s=sentence.split(" ")
    #print s[0]
    sen=[]
    for i in sentence:
        sen.append('"'+i+'"')
    #print sen
    #s=np.array(s)
    length = len(sen)
    #print length
    table = [[[] for i in range(length + 1)] for j in range(length + 1)]
	# Should we make this a dictionary? --> less memory.
    nodes_back = [[[] for i in range(length + 1)] for j in range(length + 1)]

    #print np.shape(table)
    #print np.shape(nodes_back)


    for j in range(1, length + 1):
        # table[j - 1][j] += {A if A -> words[j] \in gram}
	for rule in grammar:
            #print [sen[j-1]]
            if [sen[j - 1]] in grammar[rule]:
                #print "hi"
                table[j - 1][j].append(rule)
                data=[]
                data.append([rule])
                data.append([sen[j - 1]])
                data.append([])
                data.append([])
                data.append(['T'])
                nodes_back[j-1][j].append(data)
		#pointer[j - 1][j].append(Node(rule, None, None, sentence[j - 1]))       

    
    #print nodes_back   
    for j in range(2,length+1):
        for i in range(0,length-j+1):
            for k in range(i+1,i+j):
                for rule in grammar:
                    values=grammar[rule]
                    for l in range(len(values)):
                        if len(values[l]) == 2:
                            B = values[l][0]
                            C = values[l][1]
                            if B in table[i][k] and C in table[k][i+j]:
                                if rule not in table[i][i+j]:
                                    table[i][i+j].append(rule)

                                indices_B=[]
                                for counter in range(len(nodes_back[i][k])):
                                    if nodes_back[i][k][counter][0]==[B]:
                                        indices_B.append(counter)
                                        
                                indices_C=[]
                                for counter in range(len(nodes_back[k][i+j])):
                                    if nodes_back[k][i+j][counter][0]==[C]:
                                        indices_C.append(counter)
                                #print "B ",indices_B
                                #print "C ",indices_C
                                for b in indices_B:
                                    for c in indices_C:
                                        data=[]
                                        data.append([rule])
                                        data.append(values[l])
                                        x=[]
                                        x.append(i)
                                        x.append(k)
                                #print table[i][k].index(B)
                                        x.append(b)
                                        data.append(x)
                                        x=[]
                                        x.append(k)
                                        x.append(i+j)
                                        x.append(c) 
                                        data.append(x)
                                        data.append(['F'])
                                        if data not in nodes_back[i][i+j]:
                                            nodes_back[i][i+j].append(data)
                                


    #print table[0][length]
    for i in table[0][length]:
        if i=='SIGMA':
            print "accepted"
            break
    uni=printParseTrees(nodes_back,length)    
    return uni

grammar = {}
rules = open('test', 'r')
for rule in rules:
    tmp = rule.split(' -> ')
    #print tmp
    lhs = tmp[0]
    rhs_prob= tmp[1].split(" ")
    rhs=[]
    for i in rhs_prob:
        if '\n' in i:
            rhs.append(i.replace("\n",""))
        else:
            rhs.append(i)
    
    
    #rhs=' '.join(rhs)
    #print rhs
    if lhs in grammar:
        grammar[lhs].append(rhs)
    else:
        grammar[lhs] = []
        grammar[lhs].append(rhs)

rules.close()
#print grammar
#print grammar['SIGMA']
# load the raw sentences
s = nltk.data.load("grammars/large_grammars/atis_sentences.txt", "raw")
# extract the test sentences
sentence = nltk.parse.util.extract_test_sentences(s)


'''with open("output.txt ","w") as f:
    for i in range(2,10):
        #print sentence[i][0]
        uni=parser(sentence[i][0],grammar)
        print "sentence ",i," completed"
        f.write(str(sentence[i][0]))
        f.write("\t")
        f.write(str(uni))
        f.write("\n")'''

uni=parser(['show', 'availability', '.'],grammar)
print "number ",uni
