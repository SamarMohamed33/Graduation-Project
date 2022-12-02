
from turtle import position
from typing import Counter
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from .models import Topic, Document
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
import xlsxwriter
# Create your views here.


def nlp(request):
    documents=Document.objects.all()
    document_df = pd.DataFrame(documents.values())
    document_df['abstract'].dropna(inplace=True)
    document_df['abstract'] = document_df['abstract'].astype(str)
    document_abstracts = document_df['abstract'].tolist()
    topics_ids = document_df['topic_id'].tolist()
    documents_ids = document_df['document_id'].tolist()
    
    tokens_dict = {}
    Counter = 1
    for item in document_abstracts:
        tokens_dict[Counter] = nltk.word_tokenize(item)
        Counter = Counter+1
    
    positions_dict = {}
    for x, y in tokens_dict.items():
        positions_dict[x] = []
        for item in range(len(y)):
            positions_dict[x].append(item)

    tokens = []
    for x, y in tokens_dict.items():
        tokens.append(y)

    positions = []
    for x, y in positions_dict.items():
        positions.append(y)

    stop_wrods = set(stopwords.words('english'))
    tokens2 = []
    positions2 = []
    panc = re.compile(r'[.?!,:;%#@$=_~"+*\(){}|0-9]')
    for x in tokens:
        newlist = []
        newpos = []
        for i in range(len(x)):
            word = panc.sub("", x[i])
            word = word.replace("/", " ")
            word = word.replace("'", "")
            word = word.replace("-", "")
            if len(word) > 2:
                word2 = word.lower()
                if word2 not in stop_wrods:
                    newlist.append(word2)
                    newpos.append(i)
        positions2.append(newpos)
        tokens2.append(newlist)
    
    tokens3 = []
    positions3 = []
    for x in tokens2:
        newlist1 = []
        newpos1 = []
        index = tokens2.index(x)
        listt = positions2[index]
        for i in range(len(x)):
            if ' ' in x[i]:
                data = x[i].split()
                data_len=len(data)-1
                count = i
                pos = listt[count]
                for d in data:
                    newlist1.append(d)
                    newpos1.append(pos)
                    count = count+1
                    pos = pos+1
                cc = i+1
                while cc < len(listt):
                    listt[cc] = listt[cc]+data_len
                    cc = cc+1
            else:
                newlist1.append(x[i])
                newpos1.append(listt[i])
        tokens3.append(newlist1)
        positions3.append(newpos1)
    

    tokens4 = []
    positions4 = []
    frequency = []
    for x, y in zip(tokens3, positions3):
        tokens5 = []
        positions5 = []
        for i, j in zip(x, y):
            poss = []
            if i not in tokens5:
                tokens5.append(i)
                poss.append(j)
                positions5.append(poss)
            else:
                index = tokens5.index(i)
                pp = positions5[index]
                pp.append(j)
        tokens4.append(tokens5)
        positions4.append(positions5)
        frequency1 = []
        for i in range(0, len(tokens5)):
            frequency1.append(x.count(tokens5[i]))
        frequency.append(frequency1)
   
    pos_str=[]
    for i in positions4:
            pos_str1=[]
            for j in i:
                strr = ""
                for x in range(len(j)):
                    strr=' '.join([str(item) for item in j])
                pos_str1.append(strr)
            pos_str.append(pos_str1)       
   
    ps = PorterStemmer()
    tokens6 = []
    for t in tokens4:
        tokens7 = []
        for i in t:
            tokens7.append(ps.stem(i))
        tokens6.append(tokens7)
    

    to = []
    po = []
    f = []
    doc_ids = []
    top_ids = []
    for i, j, k,p,d in zip(tokens6, pos_str, frequency,topics_ids,documents_ids):
        topicid=p
        document_id=d
        for l, m, n in zip(i, j, k):
                to.append(l)
                po.append(m)
                f.append(n)
                top_ids.append(topicid)
                doc_ids.append(document_id)

    
    thisdict={"tokens":to,"positions":po,"frequency":f,"doc_id":doc_ids,"topic_id":top_ids}
    df=pd.DataFrame(thisdict)
    df1=pd.DataFrame(df[0:1000000])
    df2=pd.DataFrame(df[1000000:2000000])    
    
    writer = pd.ExcelWriter('documents_abstract2.xlsx', engine='xlsxwriter')
    df1.to_excel(writer, sheet_name='Sheet1')
    df2.to_excel(writer, sheet_name='Sheet2')
    
    
    writer.save()
        
    return HttpResponse("hello")
