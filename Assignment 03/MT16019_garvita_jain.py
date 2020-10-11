import numpy as np

emit={}
transition ={}
context={}
unique_words=[]
def training():

    file=[]
    with open("C:\\Users\\Garvita\\Documents\\NLP\\Assignment 3\\Training set.txt",'r',encoding='utf-8') as f:
        x=[]
        for line in f:
            if(line!="\n"):
                x.append(line)
            else:
                file.append(x)
                x=[]
        file.append(x)

    #print("file is: ",file)
    print("file length is ",len(file))
    for x in file:
        previous="<s>"
        if not previous in context:
            context[previous]=1
        else:
            context[previous]+=1
        for wordtag in x:

            word_tag=wordtag.split("\t")
            word=word_tag[0].split("\n")[0]
            tag=word_tag[1].split("\n")[0]

            if not word in unique_words:
                unique_words.append(word)
            if not previous+" "+tag in transition:
                transition[previous+" "+tag]=1 # Count the transition
            else:
                transition[previous+" "+tag]+=1
            if not tag in context:
                context[tag]=1 # Count the context
            else:
                context[tag]+=1
            if not tag+" "+word in emit:
                emit[tag+" "+word]=1 # Count the emission
            else:
                emit[tag+" "+word]+=1
            previous = tag
        #print("previous is ",previous)
        if not previous+" </s>" in transition:
            transition[previous+" </s>"]=1
        else:
            transition[previous+" </s>"]+=1

   # print("context is"+"\n")
   # print("no of POS tag ",len(context))
    #for x in context:
     #   print(x,"\t",context[x])
      #  print("\n")
    #print(len(unique_words))
''' print("emit is"+"\n")
    for x in emit:
        print(x,"\t",emit[x])
        print("\n")
    print("transition is"+"\n")
    for x in transition:
        print(x,"\t",transition[x])
        print("\n")'''

    
def testing():
    file=[]
    #print(emit)
    with open("C:\\Users\\Garvita\\Documents\\NLP\\Assignment 3\\t.txt",'r',encoding='utf-8') as f:
        x=[]
        for line in f:
            if(line!="\n"):

                x.append(line)
            else:
                file.append(x)
                x=[]
        file.append(x)
    #print(file)
    for x in file:
        l=len(x)
        #print("length of sent is ",l)
        best_score={}
        best_edge={}
        best_score["0 <s>"] = 0 # Start with <s>
        best_edge["0 <s>"] = "null"
        p=.5
        for i in range(l):
            #print(i)
            for prev in context:
                for next1 in context:

                    if str(i)+" "+prev in best_score:
                       # print("prev is ",prev)
                        if prev+" "+next1 in transition:
                           # print("next1 is ",next1)
                            if next1+" "+x[i].split("\n")[0] in emit:
                                #print("x[i] ",x[i])
                                #print("transition is ",transition[prev+" "+next1])
                                #print("context of prev is ",context[prev])
                                #print("best sc is ",best_score[str(i)+" "+prev])
                                #print("emission is ",emit[next1+" "+x[i].split("\n")[0]])
                                #print("context of next1 is ",context[next1])
                                score = best_score[str(i)+" "+prev] +(-np.log(transition[prev+" "+next1]/context[prev]))+(-np.log(emit[next1+" "+x[i].split("\n")[0]]/context[next1]))
                            else:
                                score = best_score[str(i)+" "+prev] +(-np.log(transition[prev+" "+next1]/context[prev]))+(-np.log((1-p)*(1/len(unique_words))))
                            if str(i+1)+" "+next1 not in best_score or best_score[str(i+1)+" "+next1]>score:
                                best_score[str(i+1)+" "+next1] = score
                                best_edge[str(i+1)+" "+next1] = str(i)+" "+prev
        #print(best_edge)
        #print(best_score)
        for next1 in context:

            if str(l)+" "+next1 in best_score and next1+" </s>" in transition:
                #print("next1 is ",next1)
                #print(next1+" </s>")
                #print("hi")
                #print(context[next1])
                score=best_score[str(l)+" "+next1]+(-np.log(transition[next1+" </s>"]/context[next1]))
                #print(score)
                if str(l)+" </s>" not in best_score or best_score[str(l)+" </s>"]>score:
                            best_score[str(l+1)+" </s>"] = score
                            best_edge[str(l+1)+" </s>"] = str(l)+" "+next1
                            #print(best_score[str(l)+" </s>"])
                            #print(best_edge[str(l)+" </s>"])
        #print(best_edge)
        #print(best_score)
        backward(x,l,best_score,best_edge)

def  backward(x,l,best_score,best_edge):
    tags=[]

    next1_edge = best_edge[str(l+1) +" </s>" ]
    #print(next1_edge)
    while next1_edge != "0 <s>":
       # print("hi")
        position=next1_edge.split(" ")[0]
        tag=next1_edge.split(" ")[1]
        tags.append(tag)
        next1_edge = best_edge[next1_edge]

    tags.reverse()

    with open("C:\\Users\\Garvita\\Documents\\NLP\\Assignment 3\\output.txt",'a+',encoding='utf-8') as f:
        f.write("\n")
        i=0
        for tag in tags:
            f.write(x[i].rstrip('\n')+"\t"+tag.rstrip('\n'))
            i+=1
            f.write("\n")


training()
testing()




