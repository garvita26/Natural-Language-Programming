#Assumptions: words like self.com, go-go(without spaces ) are taken as a single word.Link taken as reference :https://wordcounter.net/
import re
special_characters=["-","!", "?","\"", "\'", "@", " #"," $"," %"," ^ "," *", "("," )"," - "," _"," +","\/"," :"," ;"," <"," >"," |"," ~"," `"," \\"," .",","]
words=None
with open('C:\\Users\\Garvita\\Documents\\NLP\Assignment 1\\t.txt') as f:
    words=f.read().split()
total_words=0;
for w in words:
    if w  not in special_characters:
        total_words=total_words+1


print(" no of words : ",total_words)
#finding number of sentences
t=0
with open('C:\\Users\\Garvita\\Documents\\NLP\Assignment 1\\t.txt') as f:
    word=f.read()

tot_sentence=0;
words=word.replace("\n"," ")
for m in re.finditer("\.",words):
    if(m.start()+1<len(words)):
        if((words[m.start()-2]=="D" and words[m.start()-1]=="r" ) or(words[m.start()-2]=="M" and words[m.start()-1]=="r" ) or (words[m.start()-2]=="M" and words[m.start()-1]=="s" ) or (words[m.start()-3]=="M" and words[m.start()-2]=="r"  and words[m.start()-1]=="s") ):
                 tot_sentence=tot_sentence
        elif(words[m.start()+1]==" " and words[m.start()+2].isalpha()) :
            if(m.start()+2<len(words)):
             if(words[m.start()+2].isupper()):
                  #print(words[m.start()+2])
                  #print(words[m.start()-3],words[m.start()-2],words[m.start()-1])
                  tot_sentence=tot_sentence+1

        elif((words[m.start()+1]==" " and not(words[m.start()+2].isalpha()))or words[m.start()+1]=="\'" or words[m.start()+1]=="\""  ):
            #print(words[m.start()-3],words[m.start()-2],words[m.start()-1])
            tot_sentence=tot_sentence+1
        elif(words[m.start()+1]==")"):
            if(m.start()+2<len(words)):
                if(words[m.start()+2]==" "):
                    #print(words[m.start()-3],words[m.start()-2],words[m.start()-1])
                    tot_sentence=tot_sentence+1
            else:
                #print(words[m.start()-3],words[m.start()-2],words[m.start()-1])
                tot_sentence=tot_sentence+1
for m in re.finditer('\?',words):
    if(m.start()+1<len(words)):
       if(words[m.start()+1]==" " and words[m.start()+2].isalpha()) :
           if(m.start()+2<len(words)):
            if(words[m.start()+2].isupper()):
                  #print(words[m.start()+2])
                 # print(words[m.start()-3],words[m.start()-2],words[m.start()-1])
                  tot_sentence=tot_sentence+1

       elif((words[m.start()+1]==" " and not(words[m.start()+2].isalpha()))or words[m.start()+1]=="\'" or words[m.start()+1]=="\"" ):
           #print(words[m.start()-3],words[m.start()-2],words[m.start()-1])
           tot_sentence=tot_sentence+1
       elif(words[m.start()+1]==")"):
            if(m.start()+2<len(words)):
                if(words[m.start()+2]==" "):
              #      print(words[m.start()-3],words[m.start()-2],words[m.start()-1])
                    tot_sentence=tot_sentence+1
            else:
               # print(words[m.start()-3],words[m.start()-2],words[m.start()-1])
                tot_sentence=tot_sentence+1

for m in re.finditer('!',words):
    if(m.start()+1<len(words)):
        if(words[m.start()+1]==" " and words[m.start()+2].isalpha()) :
            if(m.start()+2<len(words)):
             if(words[m.start()+2].isupper()):
                  #print(words[m.start()+2])
                #  print(words[m.start()-3],words[m.start()-2],words[m.start()-1])
                  tot_sentence=tot_sentence+1

        elif((words[m.start()+1]==" " and not(words[m.start()+2].isalpha()))or words[m.start()+1]=="\'" or words[m.start()+1]=="\"" ):
            #print(words[m.start()-3],words[m.start()-2],words[m.start()-1])
            tot_sentence=tot_sentence+1
        elif(words[m.start()+1]==")"):
            if(m.start()+2<len(words)):
                if(words[m.start()+2]==" "):
             #       print(words[m.start()-3],words[m.start()-2],words[m.start()-1])
                    tot_sentence=tot_sentence+1
            else:
              #  print(words[m.start()-3],words[m.start()-2],words[m.start()-1])
                tot_sentence=tot_sentence+1
print("no of sentences : ",tot_sentence+1)

#finding number of paragraphs
paragraphs = word.split("\n\n")
print("no of paragraphs: ",len(paragraphs))


