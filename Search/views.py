from __future__ import print_function
from ast import Return
from audioop import reverse
import json
import token
from turtle import pos, position
from unittest import result
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from joblib import PrintTime
from matplotlib.style import context
from numpy import True_, append
from regex import P
from .models import Field, FieldHasAuthors, Topic, Document, TopicHasKeyphrase, TopicKeyphrase, Author, DocumentTitleTokens, FieldHasKeyphrase, FieldKeyPhrase, FieldKeyphraseByYear, Year, DocAbstractTokens,TopicTokens,AuthUser,UserHistory,UserDocument
import pandas as pd
from IPython.display import HTML
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

def search(request):
    field_names = []
    array_names = ""

    if request.method == 'POST':
        search_input = request.POST.get('search_input')
        search_input = search_input.lower()
        field = Field.objects.all()
        df = pd.DataFrame(field.values())
        field_names = df['field_name'].tolist()
        for x in field_names:
            array_names += x+"*"
        request.session['input'] = search_input
        return redirect('search_results')

    mydict = {
        'array_names': array_names,
    }
    return render(request, 'search.html', context=mydict)

def search_results(request,):
    search_input = request.session.get('input')
    final_results = []
    data = []
    field = Field.objects.all()
    df = pd.DataFrame(field.values())
    field_names = df['field_name'].tolist()
    for j in field_names:
        Partial_Ratio = fuzz.partial_ratio(j.lower(), search_input.lower())
        if Partial_Ratio == 100:
            final_results.append(j)

    keyphrases = FieldKeyPhrase.objects.all()
    keyphrases_df = pd.DataFrame(keyphrases.values())
   
    field_keyphrase2 = []
    field_keyphrase_id2 = []
    
    for index,row in keyphrases_df.iterrows():
        keyphrase=row['name']
        Partial_Ratio = fuzz.partial_ratio(keyphrase.lower(), search_input.lower())
        if Partial_Ratio == 100:
            field_keyphrase2.append(keyphrase)
            field_keyphrase_id2.append(row['id'])

    dict = {}
    for x in field_keyphrase_id2:
        f_key = get_object_or_404(FieldHasKeyphrase, f_keyphrase_id=x)

        ff = str(f_key.field_name_id)
        if ff in dict.keys():
            dict[ff].append(x)
        else:
            dict[ff] = []
            dict[ff].append(x)
        
    new_dict = {}
    for x, y in dict.items():
        new_dict[x] = []
        list_of_ids = dict[x]
        for i in list_of_ids:
            obj = FieldKeyphraseByYear.objects.filter(pk=i)
            dff = pd.DataFrame(obj.values())
            obj_scholarly = dff['scholarly_output'].tolist()
            obj_scholarly = [i for i in obj_scholarly if i != 0]
        
            growth = (
                (obj_scholarly[-1]-obj_scholarly[0])/obj_scholarly[0])*100
            new_dict[x].append(growth)
    
    new_dict2 = {}
    for x, y in new_dict.items():
        list_of_growth = new_dict[x]
        total = sum(list_of_growth)
        new_dict2[x] = total

    sorted_dict = {}
    sorted_keys = sorted(new_dict2, key=new_dict2.get, reverse=True)

    for w in sorted_keys:
        sorted_dict[w] = new_dict2[w]

    for x, y in sorted_dict.items():
        if x not in final_results:
            final_results.append(x)
    if len(final_results)<1:
        return render(request,'no_results.html')
    final_results_df=pd.DataFrame()
    for t in final_results:
        field_topic = Topic.objects.filter(field_name=t)
        field_topic_df = pd.DataFrame(field_topic.values())
        citation = sum(field_topic_df['citation_count'].tolist())
        views = sum(field_topic_df['views_count'].tolist())
        scholarly = sum(field_topic_df['scholarly_output'].tolist())
        temp_df=pd.DataFrame({'field_name':[t],'citation_count':[citation],'views_count':[views],'scholarly_output':[scholarly]})
        final_results_df=pd.concat([final_results_df,temp_df])
    
    json_records = final_results_df.reset_index().to_json(orient='records')
    data = json.loads(json_records)

    return render(request, 'search_results.html', {'data': data})

def search_field_info(request, field_name):
    user_=get_object_or_404(AuthUser,pk=request.user)
       
    history=UserHistory.objects.create( 
    history_name=field_name,
    username=user_,
    url=request.build_absolute_uri()
    )

    field_topics = Topic.objects.filter(field_name=field_name)
    field_topics_df = pd.DataFrame(field_topics.values())
    
    years = []
    scholarly_output = []
    topic_names = field_topics_df['name'].tolist()
    topic_ids = field_topics_df['topic_id'].tolist()
    counts = []
    for t in topic_ids:
        document = Document.objects.filter(topic=t)
        document_df = pd.DataFrame(document.values())

        df4 = document_df['year'].value_counts().reset_index(name='number')
        df = df4.sort_values(by='index')
        print(df)

        list = df['index'].tolist()
        list2 = df['number'].tolist()
        counts.append(len(list2))
        years.append(list)
        scholarly_output.append(list2)

    growth = []
    for item in scholarly_output:
        list3 = item
        growthh = ((list3[-1]-list3[0])/list3[0])*100
        growth.append(growthh)

    dict2 = {'topic_ids': topic_ids, 'topic_name': topic_names, 'years': years,
             'scholarly_output': scholarly_output, 'growth': growth, 'counts': counts}
    dict_df2 = pd.DataFrame(dict2)
    dff = dict_df2.sort_values(by="growth", ascending=False)
    df_filtered = dff[dff['counts'] > 7]
    ids = df_filtered['topic_ids'].tolist()
    namess = df_filtered['topic_name'].tolist()
    yearss = df_filtered['years'].tolist()
    scholarlyoutputs = df_filtered['scholarly_output'].tolist()
    growths = df_filtered['growth'].tolist()

    new_year = []
    for item in yearss:
        array_years = ""
        for t in item:
            array_years += str(t)+"*"
        new_year.append(array_years)

    new_scholarly = []
    for item in scholarlyoutputs:
        array_scholarly = ""
        for s in item:
            array_scholarly += str(s)+"*"
        new_scholarly.append(array_scholarly)

    dict3 = {'ids': ids, 'topic_name': namess, 'years': new_year,
             'scholarly_output': new_scholarly, 'growth': growths}
    dict3_df = pd.DataFrame(dict3)
    dict4_df = dict3_df.head(10)
    
    names = dict4_df['topic_name'].tolist()
    if request.method == 'POST':
        op = request.POST.get('p_option')
        select_color = dict4_df.loc[dict4_df['topic_name'] == op]
        y = str(select_color['years'])
        print(y)
        print(select_color)
    vi1 = request.GET.get('p_option')
    print(vi1)

    json_records = dict4_df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)
    mydict = {
        'data': data,
        'field_name': field_name,
        'names': names
    }
    return render(request, 'search_field_info.html', context=mydict)

def field_summary(request, field_name):
    # summary
    field_topics = Topic.objects.filter(field_name=field_name)
    field_topics_df = pd.DataFrame(field_topics.values())

    c_c = field_topics_df['citation_count'].tolist()
    v_c = field_topics_df['views_count'].tolist()
    s_o = field_topics_df['scholarly_output'].tolist()

    # sum of each list

    cc_sum = sum(c_c)
    vc_sum = sum(v_c)
    so_sum = sum(s_o)

    # keyphrases
    keyphrases_ids = FieldHasKeyphrase.objects.filter(field_name=field_name)
    keyphrases_ids_df = pd.DataFrame(keyphrases_ids.values())
    key_ids = keyphrases_ids_df['f_keyphrase_id'].tolist()
    keyphrases_names = []
    for i in key_ids:
        name = get_object_or_404(FieldKeyPhrase, pk=i)
        keyphrases_names.append(str(name.name))
    print(keyphrases_names)
    so_list = []
    year_list = []
    for i in key_ids:
        key_info = FieldKeyphraseByYear.objects.filter(f_keyphrase=i)
        df = pd.DataFrame(key_info.values())
        df_year = df['year_id'].tolist()
        y_list = []
        for y in df_year:
            yy = get_object_or_404(Year, id=y)
            y_list.append(yy.year)

        df_so = df['scholarly_output'].tolist()
        so_list.append(df_so)
        year_list.append(y_list)

    dictt = {'name': keyphrases_names, 'year': year_list, 'so_list': so_list}

    dictt_df = pd.DataFrame(dictt)
    print(dictt_df)

    name = keyphrases_names[0]
    select_so = so_list[0]
    selet_year = year_list[0]
    select_so_sstr = ""
    for s in select_so:
        select_so_sstr += str(s)+"*"
    select_year_sstr = ""
    for s in selet_year:
        select_year_sstr += str(s)+"*"
    if request.method == 'POST':
        op = request.POST.get('p_option')
        select_key = keyphrases_names.index(op)
        select_so = so_list[select_key]
        selet_year = year_list[select_key]
        select_so_sstr = ""
        for s in select_so:
            select_so_sstr += str(s)+"*"
        select_year_sstr = ""
        for s in selet_year:
            select_year_sstr += str(s)+"*"

      
        mydict = {
            'field_name': field_name,
            'names': keyphrases_names,
            'cc_sum': cc_sum,
            'vc_sum': vc_sum,
            'so_sum': so_sum,
            'name': op,
            'scholarly_output': select_so_sstr,
            'year': select_year_sstr

        }
        return render(request, 'field_summary.html', context=mydict)

    mydict = {
        'field_name': field_name,
        'names': keyphrases_names,
        'cc_sum': cc_sum,
        'vc_sum': vc_sum,
        'so_sum': so_sum,
        'name': name,
        'scholarly_output': select_so_sstr,
        'year': select_year_sstr

    }
    return render(request, 'field_summary.html', context=mydict)

def search_for_topic(request):
    if request.method == 'POST':
        search_input = request.POST.get('search_input')
        search_input = search_input.lower()
        tokens = nltk.word_tokenize(search_input)
        positions = []
        for i in range(len(tokens)):
            positions.append(i)
        
        stop_wrods = set(stopwords.words('english'))
        panc = re.compile(r'[.?!,:;%#@$=_~"+*\(){}|0-9]')
        tokens2 = []
        positions2 = []
        for x in range(len(tokens)):
            word = panc.sub("", tokens[x])
            word = word.replace("/", " ")
            word = word.replace("'", "")
            word = word.replace("-", "")
            if len(word) > 2:
                word2 = word.lower()
                if word2 not in stop_wrods:
                    tokens2.append(word2)
                    positions2.append(positions[x])
                
        tokens3 = []
        positions3 = []
        for x in range(len(tokens2)):
            index = x
            if ' ' in tokens2[x]:
                data = tokens2[x].split()
                data_len = len(data)-1
                count = index
                pos = positions2[count]
                for d in data:
                    tokens3.append(d)
                    positions3.append(pos)
                    count = count+1
                    pos = pos+1
                cc = index+1
                while cc < len(positions2):
                    positions2[cc] = positions2[cc]+data_len
                    cc = cc+1
            else:
                tokens3.append(tokens2[x])
                positions3.append(positions2[index])
      
        tokens4 = []
        positions4 = []
        frequency = []
        for x, y in zip(tokens3, positions3):
            poss = []
            if x not in tokens4:
                tokens4.append(x)
                poss.append(y)
                positions4.append(poss)
            else:
                index = tokens4.index(x)
                pp = positions4[index]
                pp.append(y)
        for i in range(0, len(tokens4)):
            frequency.append(tokens3.count(tokens4[i]))

        ps = PorterStemmer()
        tokens5 = []
        for t in tokens4:
            tokens5.append(ps.stem(t))
        request.session['input'] = tokens5
        request.session['input2']=search_input
        return redirect('search_topic_results')
    return render(request, 'search_for_topic.html')

def search_topic_results(request):
    search_input = request.session.get('input')
    if len(search_input)==0:
        return render(request,'no_results.html')
    ################### search in topics names ###################
    dict_topics = {}
    for x in search_input:
        topics = TopicTokens.objects.filter(tokens=x)
        topics_df = pd.DataFrame(topics.values())
        if len(topics_df)!=0:
            dict_topics[x] = topics_df
    result_of_topics = []        
    if len(search_input)==len(dict_topics):
        first = list(dict_topics)
        first_key = first[0]
        min_value = len(dict_topics[first_key])
        min_df = pd.DataFrame(dict_topics[first_key])
        for x, y in dict_topics.items():
            if min_value > len(y):
                min_value = len(y)
                first_key = x
                min_df = dict_topics[x]    
        topic_list = min_df['topic_id'].tolist()  
        del dict_topics[first_key]  
        if len(dict_topics)<1:
            result_of_topics=topic_list
        else:
            counter = 0
            for x, y in dict_topics.items():
                df = y
                topic_list2 = df['topic_id'].tolist()
                if counter is not 0:
                    topic_list = result_of_topics
                    result_of_topics = []
                a, b = len(topic_list), len(topic_list2)
                i, j = 0, 0
                while i < a and j < b:
                    if topic_list[i] == topic_list2[j]:
                        result_of_topics.append(topic_list[i])
                        i += 1
                        j += 1
                    elif topic_list[i] < topic_list2[j]:
                        i += 1
                    else:
                        j += 1
                counter = counter+1  
    ################# document titles#####################
    dict = {}
    for x in search_input:
        documents = DocumentTitleTokens.objects.filter(token=x)
        documents_df = pd.DataFrame(documents.values())
        if len(documents_df)!=0:
           dict[x] = documents_df
    
    topics_Doctitles=[]   
    if len(dict)==len(search_input):
        first = list(dict)
        first_key = first[0]
        min_value = len(dict[first_key])
        min_df = pd.DataFrame(dict[first_key])

        for x, y in dict.items():
            if min_value > len(y):
                min_value = len(y)
                first_key = x
                min_df = dict[x]
        del dict[first_key]
        doc_list = min_df['doc_id'].tolist()
        result = []  
        if len(dict) < 1:
            result = doc_list   
        else:
            result=intersection(dict,doc_list)    
        titles=get_topics(result)
        topics_Doctitles=titles['topics']
        
     ######## get documents based on document abstract ###########################
    dict_abstract = {}
    for x in search_input:
        documents = DocAbstractTokens.objects.filter(token=x)
        documents_df = pd.DataFrame(documents.values())
        if len(documents_df)!=0:
            dict_abstract[x] = documents_df
    topics_DocAbs=[]

    if len(search_input)==len(dict_abstract):
        first_abstract = list(dict_abstract)
        first_key_abstract = first_abstract[0]
        min_value_abstract = len(dict_abstract[first_key_abstract])
        min_df_abstract = pd.DataFrame(dict_abstract[first_key_abstract])
        
        for x, y in dict_abstract.items():
            if min_value_abstract > len(y):
                min_value_abstract = len(y)
                first_key_abstract = x
                min_df_abstract = dict_abstract[x]

        dict_abstract1 = {}
        dict_abstract1.update(dict_abstract)

        del dict_abstract[first_key_abstract]
        
        # min dataframe
        doc_list = min_df_abstract['doc_id'].tolist()
        result2=[]
        if len(dict_abstract)<1:
            result2=doc_list
        else:
            result_of_DocAbs=intersection(dict_abstract,doc_list)
            result2=get_postions(dict_abstract1,result_of_DocAbs)
        dict_DocAbs=get_topics(result2)
        topics_DocAbs=dict_DocAbs['topics']
       
    priority=[]
    for r1 in result_of_topics:
        if r1 in topics_Doctitles and r1 in topics_DocAbs:
            priority.append(r1)  
    for r1 in result_of_topics:
        if r1 not in priority:
            priority.append(r1)
    for r2 in topics_Doctitles:        
        if r2 not in priority:
            priority.append(r2)
    for a in topics_DocAbs:         
        if a not in priority:  
            priority.append(a)
                    
    if len(priority)==0:
        return render(request,'no_results.html')            
    
    final_df=get_topics_names(priority)
    json_records = final_df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records) 
    if request.method=='POST':
        menu_choice=request.POST.get('menu_choice')
        sorted_df=sort_fun_topic(menu_choice,final_df)
        page = request.GET.get('page',1)
        json_records = sorted_df.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_records) 
        mydict = {
        'mydata': paginator_fun(page,data)
        }    
        return render(request, 'search_topic_results.html',context=mydict)

    page = request.GET.get('page',1)
    mydict = {
        'mydata': paginator_fun(page,data),
    }    
      
    return render(request, 'search_topic_results.html',context=mydict)

def sort_fun_topic(sort_type,df):
    if sort_type == "citation count(highest)" :
        df = df.sort_values("citation_count",ascending=False)
    if sort_type == "citation count(lowest)" :
        df = df.sort_values("citation_count")
    if sort_type == "Views Count(highest)" :
        df = df.sort_values("views_count",ascending=False)
    if sort_type == "Views Count(lowest)" :
        df = df.sort_values("views_count")  
    if sort_type == "Scholarly Output(highest)" :
        df = df.sort_values("scholarly_output",ascending=False)
    if sort_type == "Scholarly Output(lowest)" :
        df = df.sort_values("scholarly_output")      
    if sort_type == "Topic Name(A-Z)" :
        df = df.sort_values("name") 
    if sort_type == "Topic Name(Z-A)" :
        df = df.sort_values("name",ascending=False) 
    if sort_type == "Relevance" :
        df=df

    return df    

def get_topics_names(ids):
    names_df=pd.DataFrame()
    for i in range(len(ids)):
        topic = Topic.objects.filter(pk=ids[i])
        df2 = pd.DataFrame(topic.values())
        if i !=0:
            l=df2['name'].tolist()
            l_=l[0]
            name_list=names_df['name'].tolist()
            if l_ not in name_list:
                names_df=pd.concat([names_df,df2])
        else:
            names_df=pd.concat([names_df,df2])
        
    return  names_df

def get_topics(result):
    list1=[]
    for l in result:
        doc=Document.objects.filter(pk=l)
        doc_df=pd.DataFrame(doc.values())
        top=int(doc_df['topic_id'])
        topic=get_object_or_404(Topic,pk=top)
        list1.append(topic.topic_id)
    
    freq = {}
    for items in list1:
        freq[items] = list1.count(items)
    sort_orders = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    topics=[]
    for i in sort_orders:
        topics.append(i[0])
    dict={'topics':topics}
    return dict

def intersection(dict,doc_list):
    result = []
    counter = 0
    for x, y in dict.items():
        df = y
        doc_list2 = df['doc_id'].tolist()
        if counter is not 0:
            doc_list = result
            result = []
        a, b = len(doc_list), len(doc_list2)
        i, j = 0, 0
        while i < a and j < b:
            if doc_list[i] == doc_list2[j]:
                result.append(doc_list[i])
                i += 1
                j += 1
            elif doc_list[i] < doc_list2[j]:
                i += 1
            else:
                j += 1

        counter = counter+1


    return result

def get_postions(dict_abstract1,result2):
    dict_position = {}
    for x, y in dict_abstract1.items():
        dff1 = pd.DataFrame()
        for z in result2:
            dff = y.loc[y['doc_id'] == z]
            if len(dff) > 1:
                str_pos = ""
                pos = dff['position'].tolist()
                for i in pos:
                    str_pos = str_pos+i+" "
                freq = dff['frequency'].tolist()
                frequency = sum(freq)
                doc = dff['doc_id'].tolist()
                doc_id = doc[0]
                top = dff['topic_id'].tolist()
                topic_id = top[0]
                id = 1
                dff = pd.DataFrame({'id': [id], 'token': [x], 'position': [str_pos], 'frequency': [
                                   frequency], 'doc_id': [doc_id], 'topic_id': [topic_id]})

            dff1 = pd.concat([dff1, dff])

        dict_position[x] = dff1
       
    tookens = []
    poss = []
    frequencyy = []
    document_ids = []

    for x, y in dict_position.items():
        tookens_list = y['token'].tolist()
        tookens.append(tookens_list[0])
        poss_list = y['position'].tolist()
        poss.append(poss_list)
        frequencyy_list = y['frequency'].tolist()
        frequencyy.append(frequencyy_list)
        document_ids_list = y['doc_id'].tolist()
        document_ids.append(document_ids_list)

    abstract_results = []
    for d in range(len(document_ids[0])):
        counter = 0
        for t, p in zip(tookens, poss):

            ind = (poss.index(p))+1
            if ind >= len(poss):
                break
            p2 = poss[ind]
            list1 = p[d].split()
            list2 = p2[d].split()

            a, b = len(list1), len(list2)
            i, j = 0, 0
            found = 0
            while i < a and j < b:
                c1 = int(list1[i])
                c2 = int(list2[j])
                if c1 < c2:
                    difference = c2-c1
                    if difference <= 5:
                        i += 1
                        j += 1
                        found = found+1
                    else:
                        break
                else:
                    j += 1
            if found != 0:
                counter = counter+1

        if counter == (len(tookens)-1):
            abstract_results.append(document_ids[0][d])
    return abstract_results        

def search_for_document(request):
    if request.method == 'POST':      
        search_input = request.POST.get('search_input')
        search_input = search_input.lower()
        tokens = nltk.word_tokenize(search_input)
        positions = []
        for i in range(len(tokens)):
            positions.append(i)
      
        stop_wrods = set(stopwords.words('english'))
        panc = re.compile(r'[.?!,:;%#@$=_~"+*\(){}|0-9]')
        tokens2 = []
        positions2 = []
        for x in range(len(tokens)):
            word = panc.sub("", tokens[x])
            word = word.replace("/", " ")
            word = word.replace("'", "")
            word = word.replace("-", "")
            if len(word) > 2:
                word2 = word.lower()
                if word2 not in stop_wrods:
                    tokens2.append(word2)
                    positions2.append(positions[x])
        tokens3 = []
        positions3 = []
        for x in range(len(tokens2)):
            index = x
            if ' ' in tokens2[x]:
                data = tokens2[x].split()
                data_len = len(data)-1
                count = index
                pos = positions2[count]
                for d in data:
                    tokens3.append(d)
                    positions3.append(pos)
                    count = count+1
                    pos = pos+1
                cc = index+1
                while cc < len(positions2):
                    positions2[cc] = positions2[cc]+data_len
                    cc = cc+1
            else:
                tokens3.append(tokens2[x])
                positions3.append(positions2[index])
       
        tokens4 = []
        positions4 = []
        frequency = []
        for x, y in zip(tokens3, positions3):
            poss = []
            if x not in tokens4:
                tokens4.append(x)
                poss.append(y)
                positions4.append(poss)
            else:
                index = tokens4.index(x)
                pp = positions4[index]
                pp.append(y)
        for i in range(0, len(tokens4)):
            frequency.append(tokens3.count(tokens4[i]))

        ps = PorterStemmer()
        tokens5 = []
        for t in tokens4:
            tokens5.append(ps.stem(t))

        request.session['input'] = tokens5
        request.session['input2'] = search_input
        return redirect('search_document_results')

    return render(request, 'search_for_document.html')

def search_document_results(request):
    search_input = request.session.get('input')
    if len(search_input)==0:
        return render(request,'no_results.html')
    search_input_string = request.session.get('input2')
    keywords_dict=search_in_keywords(search_input_string) 
    author_keywords=keywords_dict['author_list']
    indexed_keywords=keywords_dict['indexed_list']
    
    ######## get documents based on document title ###########################
    dict = {}
    for x in search_input:
        documents = DocumentTitleTokens.objects.filter(token=x)
        documents_df = pd.DataFrame(documents.values())
        if len(documents_df)!=0:
            dict[x] = documents_df
    result = []        
    if len(search_input)==len(dict):    
        ###### min dataframe #######
        first = list(dict)
        first_key = first[0]
        min_value = len(dict[first_key])
        min_df = dict[first_key]

        for x, y in dict.items():
            if min_value > len(y):
                min_value = len(y)
                first_key = x
                min_df = dict[x]

        del dict[first_key]
        doc_list = min_df['doc_id'].tolist()
        
        if len(dict) < 1:
            result = doc_list
        else:
            result=intersection(dict,doc_list) 

    ######## get documents based on document abstract ###########################
    dict_abstract = {}
    for x in search_input:
        documents = DocAbstractTokens.objects.filter(token=x)
        documents_df = pd.DataFrame(documents.values())
        if len(documents_df)!=0:
            dict_abstract[x] = documents_df
    result2 = []        
    if len(search_input)==len(dict_abstract):

        first_abstract = list(dict_abstract)
        first_key_abstract = first_abstract[0]
        min_value_abstract = len(dict_abstract[first_key_abstract])
        min_df_abstract = pd.DataFrame(dict_abstract[first_key_abstract])

        for x, y in dict_abstract.items():
            if min_value_abstract > len(y):
                min_value_abstract = len(y)
                first_key_abstract = x
                min_df_abstract = dict_abstract[x]

        dict_abstract1 = {}
        dict_abstract1.update(dict_abstract)

        del dict_abstract[first_key_abstract]
        # min dataframe
        doc_list = min_df_abstract['doc_id'].tolist()
        

        if len(dict_abstract)<1:
            result2=doc_list
        else:
            rslt=intersection(dict_abstract,doc_list) 
            result2=get_position_doc(dict_abstract1,rslt)
    ##############select documents based on abstract#################
    
    priority=[]
    for r1 in result:
        if r1 in result2:
            priority.append(r1)  
    for r1 in result:
        if r1 not in priority:
            priority.append(r1)
    for r2 in result2:        
        if r2 not in priority:
            priority.append(r2)
    """for a in author_keywords:         
        if a not in priority:  
            priority.append(a) 
    for x in indexed_keywords:        
        if x not in priority:  
            priority.append(x) """

    if len(priority)==0:
        return render(request,'no_results.html')             

    docc_df = pd.DataFrame()
    for r in priority:
        docc = Document.objects.filter(document_id=r)
        df2 = pd.DataFrame(docc.values())
        idd=int(df2['topic_id'])
        topic=get_object_or_404(Topic,topic_id=idd)
        df2['topic_id']=topic.name   
        docc_df = pd.concat([docc_df, df2], ignore_index=True, axis=0)
    
    json_records = docc_df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)
    page = request.GET.get('page',1)
    documents=paginator_fun(page,data)
    
    if request.method == 'POST':
        if 'refine' in request.POST:
            list_of_options = request.POST.getlist('option')
            list_of_p_options = request.POST.getlist('p_option')
            final_df=refine(list_of_options,list_of_p_options,docc_df)
            json_records = final_df.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            page = request.GET.get('page',1)
            print(list_of_options)
            print(list_of_p_options)
            print(final_df)
            mydict = {
                'documents':paginator_fun(page,data)
            }
            return render (request,'search_document_results.html',context=mydict)
        if 'sort' in request.POST:
            menu_choice =  request.POST.get('menu_choice')
            docc_df=sort_fun(menu_choice,docc_df)
            json_records = docc_df.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            page = request.GET.get('page',1)
            mydict = {
                'documents':paginator_fun(page,data)
            }    
            return render (request,'search_document_results.html',context=mydict)
    mydict = {
        'documents':documents
    }    
    return render(request, 'search_document_results.html', context=mydict)


def get_position_doc(dict_abstract1,result2):
    dict_position = {}
    for x, y in dict_abstract1.items():
        dff1 = pd.DataFrame()
        for z in result2:
            dff = y.loc[y['doc_id'] == z]
            if len(dff) > 1:
                str_pos = ""
                pos = dff['position'].tolist()
                for i in pos:
                    str_pos = str_pos+i+" "
                freq = dff['frequency'].tolist()
                frequency = sum(freq)
                doc = dff['doc_id'].tolist()
                doc_id = doc[0]
                top = dff['topic_id'].tolist()
                topic_id = top[0]
                id = 1
                dff = pd.DataFrame({'id': [id], 'token': [x], 'position': [str_pos], 'frequency': [
                                   frequency], 'doc_id': [doc_id], 'topic_id': [topic_id]})
            dff1 = pd.concat([dff1, dff])
        dict_position[x] = dff1
     
    tookens = []
    poss = []
    frequencyy = []
    document_ids = []

    for x, y in dict_position.items():
        tookens_list = y['token'].tolist()
        tookens.append(tookens_list[0])
        poss_list = y['position'].tolist()
        poss.append(poss_list)
        frequencyy_list = y['frequency'].tolist()
        frequencyy.append(frequencyy_list)
        document_ids_list = y['doc_id'].tolist()
        document_ids.append(document_ids_list)

    abstract_results = []
    abstract_results_ff = []
    for d in range(len(document_ids[0])):
        counter = 0
        for t, p in zip(tookens, poss):
            ind = (poss.index(p))+1
            if ind >= len(poss):
                break
            p2 = poss[ind]
            list1 = p[d].split()
            list2 = p2[d].split()
            a, b = len(list1), len(list2)
            i, j = 0, 0
            found = 0
            while i < a and j < b:
                c1 = int(list1[i])
                c2 = int(list2[j])
                if c1 < c2:
                    difference = c2-c1
                    if difference <= 5:
                        i += 1
                        j += 1
                        found = found+1
                    else:
                        break
                else:
                    j += 1
            if found != 0:
                counter = counter+1

        if counter == (len(tookens)-1):
            ff = []
            for f in frequencyy:
                ff.append(f[d])
            min_ff = min(ff)
            abstract_results_ff.append(min_ff)
            abstract_results.append(document_ids[0][d])

    ############   sort  #################
    sorted_abstract = [x for _, x in sorted(zip(abstract_results_ff, abstract_results))]

    return sorted_abstract

def paginator_fun(page,data):
    paginator = Paginator(data,60)
    try:
        my_data = paginator.page(page)
    except PageNotAnInteger:
        my_data = paginator.page(1)
    except EmptyPage:
        my_data = paginator.page(paginator.num_pages)
    return my_data

def refine(list_of_years,list_of_document_types,df):
    print("refine")
    if len(list_of_years) > 0 and len(list_of_document_types) > 0:
        finall = pd.DataFrame()
        for item in range(len(list_of_years)):
            list_of_years[item] = int(list_of_years[item])
            pd22 = df.loc[df['year'] == list_of_years[item]]
            finall = pd.concat([finall, pd22])
        new_finall = pd.DataFrame()
        for item in range(len(list_of_document_types)):
            pd_doc = finall.loc[finall['document_type']
                                == list_of_document_types[item]]
            new_finall = pd.concat([new_finall, pd_doc])

        
        return new_finall
    elif len(list_of_years) > 0 and len(list_of_document_types) == 0:
        finall = pd.DataFrame()
        for item in range(len(list_of_years)):
            list_of_years[item] = int(list_of_years[item])
            pd22 = df.loc[df['year'] == list_of_years[item]]
            finall = pd.concat([finall, pd22])

        return finall

    elif len(list_of_document_types) > 0 and len(list_of_years) == 0:
        finall = pd.DataFrame()
        for item in range(len(list_of_document_types)):
            pd22 = df.loc[df['document_type'] == list_of_document_types[item]]
            finall = pd.concat([finall, pd22])
        return finall

def sort_fun(sort_type,df):
    if sort_type == "Date(newest)" :
        df = df.sort_values("year",ascending=False)
    if sort_type == "Date(oldest)" :
        df = df.sort_values("year")
    if sort_type == "Cited by(highest)" :
        df = df.sort_values("cited_by",ascending=False)
    if sort_type == "Cited by(lowest)" :
        df = df.sort_values("cited_by")  
    if sort_type == "Topic Name(A-Z)" :
        df = df.sort_values("topic_id") 
    if sort_type == "Topic Name(Z-A)" :
        df = df.sort_values("topic_id",ascending=False)     
        
    return df    

def search_in_keywords(search_input):
    documents=Document.objects.all()
    documents_df=pd.DataFrame(documents.values())
    indexed_list=[]
    author_list=[]
    for index,row in documents_df.iterrows():
        indexed=str(row['indexed_keywords'])
        author=str(row['author_keywords'])
        Partial_Ratio_author = fuzz.partial_ratio(author.lower(), search_input.lower())
        Partial_Ratio_indexed = fuzz.partial_ratio(indexed.lower(), search_input.lower())
        if Partial_Ratio_author==100:
            author_list.append(row['document_id'])
        elif Partial_Ratio_indexed==100:
            indexed_list.append(row['document_id'])
    dict={'indexed_list':indexed_list,'author_list':author_list}      
    return  dict
    
def search_for_author(request):
    return render(request, 'search_for_author.html')

def field_example(request, field_name):
    col_name = "Citation Count"
    field = get_object_or_404(Field, pk=field_name)
    topics = Topic.objects.filter(field_name=field_name).values()
    topics_df = pd.DataFrame(topics)
    df1 = topics_df[["name", "citation_count", "topic_id"]]
    df1 = df1.sort_values(by="citation_count", ascending=False)
    df1_top10 = df1.head(10)
    list1 = df1_top10['name'].to_list()
    list2 = df1_top10['citation_count'].to_list()

    array_names = ""
    array_citation = ""

    for name in list1:
        array_names += name+"*"
    for citation in list2:
        array_citation += str(citation)+","

    json_records = df1_top10.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)
    option_value = "Citation Count"
    mydict = {
        'field': field,
        'names_list': list1,
        'citation_list': list2,
        'array_names': array_names,
        'array_citation': array_citation,
        'data': data,
        'col_name': col_name,
        'option': option_value}

    if request.method == 'POST':
        option_value = request.POST.get('option')
        if option_value == "Citation Count":
            col_name = "Citation Count"
            mydict = {
                'field': field,
                'names_list': list1,
                'citation_list': list2,
                'array_names': array_names,
                'array_citation': array_citation,
                'data': data,
                'col_name': col_name,
                'option': option_value}
            return render(request, 'field_example.html', context=mydict)

        elif option_value == "Scholarly Output":
            col_name = "Scholarly Output"
            df1 = topics_df[["name", "scholarly_output", "topic_id"]]
            df1 = df1.sort_values(by="scholarly_output", ascending=False)
            df1_top10 = df1.head(10)
            df1_top10 = df1_top10.rename(
                columns={"scholarly_output": "citation_count"})
           
            list1 = df1_top10['name'].to_list()
            list2 = df1_top10['citation_count'].to_list()
            array_names = ""
            array_Scholarly = ""
         
            for name in list1:
                array_names += name+"*"
            for scholarly in list2:
                array_Scholarly += str(scholarly)+","

            json_records = df1_top10.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            mydict = {
                'field': field,
                'names_list': list1,
                'citation_list': list2,
                'array_names': array_names,
                'array_citation': array_Scholarly,
                'data': data,
                'col_name': col_name,
                'option': option_value}
            return render(request, 'field_example.html', context=mydict)

        elif option_value == "Views Count":
            col_name = "Views Count"
            df1 = topics_df[["name", "views_count", "topic_id"]]
            df1 = df1.sort_values(by="views_count", ascending=False)
            df1_top10 = df1.head(10)
            df1_top10 = df1_top10.rename(
                columns={"views_count": "citation_count"})
           
            list1 = df1_top10['name'].to_list()
            list2 = df1_top10['citation_count'].to_list()
            array_names = ""
            array_Scholarly = ""
            
            for name in list1:
                array_names += name+"*"
            for scholarly in list2:
                array_Scholarly += str(scholarly)+","
            json_records = df1_top10.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            mydict = {
                'field': field,
                'names_list': list1,
                'citation_list': list2,
                'array_names': array_names,
                'array_citation': array_Scholarly,
                'data': data,
                'col_name': col_name,
                'option': option_value}

            return render(request, 'field_example.html', context=mydict)
    return render(request, 'field_example.html', context=mydict)

def field_example_authors(request, field_name):
    field = get_object_or_404(Field, pk=field_name)
    Authors = FieldHasAuthors.objects.filter(field_name=field).values()
    Authors_df = pd.DataFrame(Authors)

    Authors_ids = Authors_df['author_id'].tolist()

    array_names = []
    array_citation = []
    array_scholarly = []

    for id in Authors_ids:
        value = get_object_or_404(Author, pk=id)
        array_names.append(value.auhtor_name)
        array_citation.append(value.citation_count)
        array_scholarly.append(value.scholarly_output)

    thisdict = {"names": array_names,
                "citation": array_citation, "ids": Authors_ids}
    Citation_df = pd.DataFrame(thisdict)

    Citation_df = Citation_df.sort_values(
        by="citation",
        ascending=False
    )
    Citation_df_1 = Citation_df.head(10)
    Citation_df_1 = Citation_df_1.rename(columns={"citation": "optionn"})
    names_citation=Citation_df_1['names'].tolist()
    names = ""
    for item in range(10):
        names+= names_citation[item]+"*"

    json_records = Citation_df_1.reset_index().to_json(orient='records')
    data1 = []
    data1 = json.loads(json_records)

    authors_names = ""
    for item in range(10):
        authors_names += array_names[item]+"*"

    sorted_ = []
    sorted_ = Citation_df_1['optionn'].tolist()
    Citation_string = ""
    for item in range(10):
        Citation_string += str(sorted_[item])+","
    col_name = "Citation Count"
    mydict = {
        'field': field,
        'authors_names': names,
        'cited_scho': Citation_string,
        'data1': data1,
        'col_name': col_name

    }
    if request.method == 'POST':
        option_value = request.POST.get('option')
        if option_value == "Citation Count":
            
            col_name = "Citation Count"
            mydict = {
                'field': field,
                'authors_names': names,
                'cited_scho': Citation_string,
                'data1': data1,
                'col_name': col_name
            }
            return render(request, 'field_example_authors.html', context=mydict)
        elif option_value == "Scholarly Output":
            col_name = option_value
            thisdict2 = {"names": array_names,
                         "scholarly": array_scholarly, "ids": Authors_ids}
            scholarly_df = pd.DataFrame(thisdict2)
            scholarly_df = scholarly_df.sort_values(
                by="scholarly",
                ascending=False
            )
           
            scholarly_df_1 = scholarly_df.head(10)
            scholarly_df_1 = scholarly_df_1.rename(
                columns={"scholarly": "optionn"})

            json_records = scholarly_df_1.reset_index().to_json(orient='records')
            data2 = []
            data2 = json.loads(json_records)
            Scholarly_string = ""
            for item in range(10):
                Scholarly_string += str(array_scholarly[item])+","

                mydict = {
                    'field': field,
                    'authors_names': authors_names,
                    'data1': data2,
                    'cited_scho': Scholarly_string,
                    'col_name': col_name
                }
            return render(request, 'field_example_authors.html', context=mydict)

    return render(request, 'field_example_authors.html', context=mydict)

def topic_example(request):
    topic = get_object_or_404(Topic, pk=1)
    topic_info = [topic.citation_count,
                  topic.scholarly_output, topic.views_count]
    topic_info = str(topic.citation_count)+" " + \
        str(topic.scholarly_output)+" "+str(topic.views_count)
    document = Document.objects.filter(topic=31)
    df = pd.DataFrame(document.values())
    df1 = df[["name", "cited_by", "document_id"]]
    df1.sort_values(
        by="cited_by",
        ascending=False
    )

    df2 = df1.loc[df1['cited_by'] >= 100]
    df2 = df2.head(10)
    df2.index += 1

    json_records = df2.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)

    keyphrase_ids = TopicHasKeyphrase.objects.filter(topic=1)

    key_df = pd.DataFrame(keyphrase_ids.values())
    keyphrase_ids = key_df['t_keyphrase_id'].tolist()
    # print(keyphrase_ids)
    array_names = ""
    array_relevace = ""

    for id in keyphrase_ids:
        value = get_object_or_404(TopicKeyphrase, pk=id)
        array_names += value.name+","
        array_relevace += str(value.relevance)+" "

    publisher_df = df[["publisher"]]
    df4 = publisher_df['publisher'].value_counts().reset_index(name='number')

    list1 = df4['index'].to_list()
    list2 = df4['number'].to_list()

    array_publisher = ""
    for x in range(3):
        array_publisher += list1[x]+","

    array_count = ""
    for x in range(3):
        array_count += str(list2[x])+" "

    mydict = {
        'topic': topic,
        'topic_info': topic_info,
        'document': document,
        'data': data,
        'array_names': array_names,
        'array_relevace': array_relevace,
        'array_publisher': array_publisher,
        'array_count': array_count
    }

    return render(request, 'topic_example.html', context=mydict)

def all_documents(request, id):
    topic=get_object_or_404(Topic,pk=id)

    document = Document.objects.filter(topic=id)
    df = pd.DataFrame(document.values())
    df1 = df[["name", "cited_by", "year", "document_type", "document_id"]]
    json_records = df1.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)
    page = request.GET.get('page',1)
    
    if request.method == 'POST':
        list_of_options = request.POST.getlist('option')
        list_of_p_options = request.POST.getlist('p_option')
        if len(list_of_options) > 0 and len(list_of_p_options) > 0:
            final = pd.DataFrame()
            for item in range(len(list_of_options)):
                list_of_options[item] = int(list_of_options[item])
                pd22 = df.loc[df['year'] == list_of_options[item]]
                print(pd22)
                final = pd.concat([final, pd22])
            new_final = pd.DataFrame()
            for item in range(len(list_of_p_options)):
                pd_doc = final.loc[final['document_type']
                                   == list_of_p_options[item]]
                new_final = pd.concat([new_final, pd_doc])

            df1 = new_final[["name", "cited_by",
                             "year", "document_type", "document_id"]]
            json_records = df1.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            page = request.GET.get('page',1)
            mydict = {
                'topic': topic,
                'document': document,
                'data': paginator_fun(page,data)}
            return render(request, 'all_documents.html', context=mydict)
        elif len(list_of_options) > 0 and len(list_of_p_options) == 0:
            final = pd.DataFrame()
            for item in range(len(list_of_options)):
                list_of_options[item] = int(list_of_options[item])
                pd22 = df.loc[df['year'] == list_of_options[item]]
                print(pd22)
                final = pd.concat([final, pd22])

            df1 = final[["name", "cited_by", "year",
                         "document_type", "document_id"]]
            json_records = df1.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            page = request.GET.get('page',1)
            mydict = {
                'topic': topic,
                'document': document,
                'data': paginator_fun(page,data)}
            return render(request, 'all_documents.html', context=mydict)

        elif len(list_of_p_options) > 0 and len(list_of_options) == 0:
            final = pd.DataFrame()
            for item in range(len(list_of_p_options)):
                pd22 = df.loc[df['document_type'] == list_of_p_options[item]]
                print(pd22)
                final = pd.concat([final, pd22])

            df1 = final[["name", "cited_by", "year",
                         "document_type", "document_id"]]
            json_records = df1.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            page = request.GET.get('page',1)
            mydict = {
                'topic': topic,
                'document': document,
                'data': paginator_fun(page,data)
            }
            return render(request, 'all_documents.html', context=mydict)

    mydict = {
        'topic': topic,
        'document': document,
        'data': paginator_fun(page,data)
    }
    return render(request, 'all_documents.html', context=mydict)

def all_topics(request,field_name):
    col_name = "Citation Count"
    field = get_object_or_404(Field, pk=field_name)
    topics = Topic.objects.filter(
        field_name=field_name).values()
    topics_df = pd.DataFrame(topics)
    df1 = topics_df[["name", "citation_count", "topic_id"]]
    df1 = df1.sort_values(by="citation_count", ascending=False)
    list1 = df1['name'].to_list()
    list2 = df1['citation_count'].to_list()

    array_names = ""
    array_citation = ""

    for name in list1:
        array_names += name+"*"
    for citation in list2:
        array_citation += str(citation)+","

    json_records = df1.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)
    option_value = "Citation Count"
    mydict = {
        'field': field,
        'names_list': list1,
        'citation_list': list2,
        'array_names': array_names,
        'array_citation': array_citation,
        'data': data,
        'col_name': col_name,
        'option': option_value}

    if request.method == 'POST':
        option_value = request.POST.get('option')
        if option_value == "Citation Count":
            col_name = "Citation Count"
            mydict = {
                'field': field,
                'names_list': list1,
                'citation_list': list2,
                'array_names': array_names,
                'array_citation': array_citation,
                'data': data,
                'col_name': col_name,
                'option': option_value}
            return render(request, 'all_topics.html', context=mydict)

        elif option_value == "Scholarly Output":
            col_name = "Scholarly Output"
            df1 = topics_df[["name", "scholarly_output", "topic_id"]]
            df1 = df1.sort_values(by="scholarly_output", ascending=False)
            # df1_top10=df1.head(10)
            df1 = df1.rename(columns={"scholarly_output": "citation_count"})
            print(df1)
            list1 = df1['name'].to_list()
            list2 = df1['citation_count'].to_list()
            array_names = ""
            array_Scholarly = ""
            print(list2)
            for name in list1:
                array_names += name+"*"
            for scholarly in list2:
                array_Scholarly += str(scholarly)+","

            json_records = df1.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            mydict = {
                'field': field,
                'names_list': list1,
                'citation_list': list2,
                'array_names': array_names,
                'array_citation': array_Scholarly,
                'data': data,
                'col_name': col_name,
                'option': option_value}
            return render(request, 'all_topics.html', context=mydict)

        elif option_value == "Views Count":
            col_name = "Views Count"
            df1 = topics_df[["name", "views_count", "topic_id"]]
            df1 = df1.sort_values(by="views_count", ascending=False)
            # df1_top10=df1.head(10)
            df1 = df1.rename(columns={"views_count": "citation_count"})
            print(df1)
            list1 = df1['name'].to_list()
            list2 = df1['citation_count'].to_list()
            array_names = ""
            array_Scholarly = ""
            print(list2)
            for name in list1:
                array_names += name+"*"
            for scholarly in list2:
                array_Scholarly += str(scholarly)+","
            json_records = df1.reset_index().to_json(orient='records')
            data = []
            data = json.loads(json_records)
            mydict = {
                'field': field,
                'names_list': list1,
                'citation_list': list2,
                'array_names': array_names,
                'array_citation': array_Scholarly,
                'data': data,
                'col_name': col_name,
                'option': option_value}

            return render(request, 'all_topics.html', context=mydict)
    return render(request, 'all_topics.html', context=mydict)

def all_authors(request, field_name):
    field = get_object_or_404(Field, pk=field_name)
    Authors = FieldHasAuthors.objects.filter(field_name=field).values()
    Authors_df = pd.DataFrame(Authors)

    Authors_ids = Authors_df['author_id'].tolist()

    array_names = []
    array_citation = []
    array_scholarly = []

    for id in Authors_ids:
        value = get_object_or_404(Author, pk=id)
        array_names.append(value.auhtor_name)
        array_citation.append(value.citation_count)
        array_scholarly.append(value.scholarly_output)

    thisdict = {"names": array_names,
                "citation": array_citation, "ids": Authors_ids}
    Citation_df = pd.DataFrame(thisdict)

    Citation_df = Citation_df.sort_values(
        by="citation",
        ascending=False
    )
    Citation_df_1 = Citation_df.head(50)
    Citation_df_1 = Citation_df_1.rename(columns={"citation": "optionn"})

    json_records = Citation_df_1.reset_index().to_json(orient='records')
    data1 = []
    data1 = json.loads(json_records)

    authors_names = ""
    for item in range(50):
        authors_names += array_names[item]+"*"

    sorted_ = []
    sorted_ = Citation_df_1['optionn'].tolist()
    Citation_string = ""
    for item in range(50):
        Citation_string += str(sorted_[item])+","
    col_name = "Citation Count"
    mydict = {
        'field': field,
        'authors_names': authors_names,
        'cited_scho': Citation_string,
        'data1': data1,
        'col_name': col_name

    }
    if request.method == 'POST':
        option_value = request.POST.get('option')
        if option_value == "Citation Count":
            col_name = "Citation Count"
            mydict = {
                'field': field,
                'authors_names': authors_names,
                'cited_scho': Citation_string,
                'data1': data1,
                'col_name': col_name
            }
            return render(request, 'all_authors.html', context=mydict)
        elif option_value == "Scholarly Output":
            col_name = option_value
            thisdict2 = {"names": array_names,
                         "scholarly": array_scholarly, "ids": Authors_ids}
            scholarly_df = pd.DataFrame(thisdict2)
            scholarly_df = scholarly_df.sort_values(
                by="scholarly",
                ascending=False
            )
            print(scholarly_df)
            scholarly_df_1 = scholarly_df.head(50)
            scholarly_df_1 = scholarly_df_1.rename(
                columns={"scholarly": "optionn"})

            json_records = scholarly_df_1.reset_index().to_json(orient='records')
            data2 = []
            data2 = json.loads(json_records)
            Scholarly_string = ""
            for item in range(50):
                Scholarly_string += str(array_scholarly[item])+","

                mydict = {
                    'field': field,
                    'authors_names': authors_names,
                    'data1': data2,
                    'cited_scho': Scholarly_string,
                    'col_name': col_name
                }
            return render(request, 'all_authors.html', context=mydict)

    return render(request, 'all_authors.html', context=mydict)

def document_info(request, id):
    user_=get_object_or_404(AuthUser,pk=request.user)
    document = get_object_or_404(Document, pk=id)
    user_=get_object_or_404(AuthUser,pk=request.user)
    if request.method=='POST':
        fav=request.POST.get('doc')
        fav_=UserDocument.objects.create( 
        document=document,
        username=user_
        )
       
    history=UserHistory.objects.create( 
    history_name=document.name,
    username=user_,
    url=request.build_absolute_uri()
    )
    document_abstract=document.abstract
    topic_id=Document.objects.get(pk=id).topic.topic_id
    topic_name=Document.objects.get(pk=id).topic.name
    topic_documents=Document.objects.filter(topic=topic_id)
    topic_documents_df=pd.DataFrame(topic_documents.values())
  
    for index,row in topic_documents_df.iterrows():
        abstract=row['abstract']
        ratio=fuzz.token_set_ratio(document_abstract.lower(),abstract.lower())
        if ratio <55:
            topic_documents_df.drop(index,axis=0,inplace=True)
    json_records = topic_documents_df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)
    return render(request, 'document_info.html', {"document": document,'data':data,'topic_name':topic_name})

def topic_info(request, id):
    topic = get_object_or_404(Topic, pk=id)
    user_=get_object_or_404(AuthUser,pk=request.user)
    history=UserHistory.objects.create( 
    history_name=topic.name,
    username=user_,
    url=request.build_absolute_uri()
    )
    topic_info = [topic.citation_count,
                  topic.scholarly_output, topic.views_count]
    topic_info = str(topic.citation_count)+" " + \
        str(topic.scholarly_output)+" "+str(topic.views_count)
    document = Document.objects.filter(topic=topic.topic_id)
    df = pd.DataFrame(document.values())
    df2 = df[["name", "cited_by", "document_id"]]
    df2.sort_values(
        by="cited_by",
        ascending=False
    )

    # df2=df1.loc[df1['cited_by']>=100]
    df2 = df2.head(10)
    df2.index += 1

    json_records = df2.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records)

    keyphrase_ids = TopicHasKeyphrase.objects.filter(topic=topic.topic_id)

    key_df = pd.DataFrame(keyphrase_ids.values())
    keyphrase_ids = key_df['t_keyphrase_id'].tolist()
    # print(keyphrase_ids)
    array_names = ""
    array_relevace = ""

    for id in keyphrase_ids:
        value = get_object_or_404(TopicKeyphrase, pk=id)
        array_names += value.name+","
        array_relevace += str(value.relevance)+" "

    publisher_df = df[["publisher"]]
    df4 = publisher_df['publisher'].value_counts().reset_index(name='number')

    list1 = df4['index'].to_list()
    list2 = df4['number'].to_list()
    print(list1)
    print(list2)

    total = 0
    for x in list2:
        total += x
    list3 = []
    counter = 0
    for x in list2:
        x = round((x/total)*100, 2)
        if x >= 1:
            counter = counter+1
            list3.append(x)
    print(counter)
    print(list3)
    array_count = ""
    array_publisher = ""
    for x in list3:
        array_count += str(x)+","

    for x in range(counter):
        array_publisher += list1[x]+","
    print(array_count)
    print(array_publisher)

    mydict = {
        'topic': topic,
        'topic_info': topic_info,
        'document': document,
        'data': data,
        'array_names': array_names,
        'array_relevace': array_relevace,
        'array_publisher': array_publisher,
        'array_count': array_count,
        'counter': counter
    }
    return render(request, 'topic_info.html', context=mydict)

def author_info(request, id):
    author = get_object_or_404(Author, pk=id)
    author_info = [author.citation_count, author.scholarly_output]
    author_info = str(author.citation_count)+" "+str(author.scholarly_output)
    docs = Document.objects.filter(authors=author.auhtor_name)
    print(docs)
    return render(request, 'author_info.html', {"author": author, "author_info": author_info})
