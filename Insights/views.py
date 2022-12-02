import json
from multiprocessing.sharedctypes import Value
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from joblib import PrintTime
from numpy import empty
from regex import P
from .models import Field, FieldHasKeyphrase, FieldKeyPhrase, FieldKeyphraseByYear, Year, Author, FieldHasAuthors
import pandas as pd
# Create your views here.


def insights_authors(request):
    ####Getting Fields####
    fields = Field.objects.all()
    fields_dataframe = pd.DataFrame(fields.values())
    json_records = fields_dataframe.reset_index().to_json(orient='records')
    fields_data = []
    fields_data = json.loads(json_records)
    ####Assigning Authors Info####
    citation_count_string = ""
    scholarly_output_string = ""
    authors_names = ""
    """####Default Value####
    fields_list = fields_dataframe['field_name'].tolist()
    field_option = fields_list[0]
    field_authors_ids = FieldHasAuthors.objects.filter(field_name=field_option)
    field_authors_ids_df = pd.DataFrame(field_authors_ids.values())
    authors_ids = field_authors_ids_df['author_id'].tolist()
    field_authors_info_df = pd.DataFrame()
    for author_id in authors_ids:
            field_authors_info = Author.objects.filter(pk=author_id)
            field_authors_info_minidf = pd.DataFrame(field_authors_info.values())
            field_authors_info_df = pd.concat([field_authors_info_df,field_authors_info_minidf])
    sorted_field_authors_info_df = field_authors_info_df.sort_values(['citation_count'],ascending=False)
    top_5_authors = sorted_field_authors_info_df.head(5)
    for index, row in top_5_authors.iterrows():
        citation_count_string = citation_count_string + str(row['citation_count']) + "*"
        scholarly_output_string = scholarly_output_string + str(row['scholarly_output']) + "*"
        authors_names = authors_names + str(row['auhtor_name']) + "*" """
    ####Getting Authors Info####
    ####my dictionary####
    mydictionary = {
        'fields': fields_data,
        'citation_count': citation_count_string,
        'scholarly_output': scholarly_output_string,
        'author_names': authors_names
    }
    if request.method == 'POST':
        field_option = request.POST.get('field_option')
        field_authors_ids = FieldHasAuthors.objects.filter(
            field_name=field_option)
        field_authors_ids_df = pd.DataFrame(field_authors_ids.values())
        authors_ids = field_authors_ids_df['author_id'].tolist()
        field_authors_info_df = pd.DataFrame()
        for author_id in authors_ids:
            field_authors_info = Author.objects.filter(pk=author_id)
            field_authors_info_minidf = pd.DataFrame(
                field_authors_info.values())
            field_authors_info_df = pd.concat(
                [field_authors_info_df, field_authors_info_minidf])
        sorted_field_authors_info_df = field_authors_info_df.sort_values(
            ['citation_count'], ascending=False)
        top_5_authors = sorted_field_authors_info_df.head(5)
        top_5_Name = top_5_authors["auhtor_name"].tolist()
        for index, row in top_5_authors.iterrows():
            citation_count_string = citation_count_string + \
                str(row['citation_count']) + "*"
            scholarly_output_string = scholarly_output_string + \
                str(row['scholarly_output']) + "*"
            authors_names = authors_names + str(row['auhtor_name']) + "*"
        ####my dictionary####
        mydictionary = {
            'fields': fields_data,
            'citation_count': citation_count_string,
            'scholarly_output': scholarly_output_string,
            'author_names': authors_names,
            'name': top_5_Name
        }

    return render(request, 'insights/insights_author.html', context=mydictionary)


def insights_authors_table(request):
    ####Getting Fields####
    fields = Field.objects.all()
    fields_dataframe = pd.DataFrame(fields.values())
    json_records = fields_dataframe.reset_index().to_json(orient='records')
    fields_data = []
    fields_data = json.loads(json_records)
    authors_data = []
    ####Default Value####
    fields_list = fields_dataframe['field_name'].tolist()
    field_option = fields_list[0]
    field_authors_ids = FieldHasAuthors.objects.filter(field_name=field_option)
    field_authors_ids_df = pd.DataFrame(field_authors_ids.values())
    authors_ids = field_authors_ids_df['author_id'].tolist()
    field_authors_info_df = pd.DataFrame()
    for author_id in authors_ids:
        field_authors_info = Author.objects.filter(pk=author_id)
        field_authors_info_minidf = pd.DataFrame(field_authors_info.values())
        field_authors_info_df = pd.concat(
            [field_authors_info_df, field_authors_info_minidf])
    sorted_field_authors_info_df = field_authors_info_df.sort_values(
        ['citation_count'], ascending=False)
    json_records = sorted_field_authors_info_df.reset_index().to_json(orient='records')
    authors_data = json.loads(json_records)
    ####Getting Authors Info####
    if request.method == 'POST':
        field_option = request.POST.get('field_option')
        field_authors_ids = FieldHasAuthors.objects.filter(
            field_name=field_option)
        field_authors_ids_df = pd.DataFrame(field_authors_ids.values())
        authors_ids = field_authors_ids_df['author_id'].tolist()
        field_authors_info_df = pd.DataFrame()
        for author_id in authors_ids:
            field_authors_info = Author.objects.filter(pk=author_id)
            field_authors_info_minidf = pd.DataFrame(
                field_authors_info.values())
            field_authors_info_df = pd.concat(
                [field_authors_info_df, field_authors_info_minidf])
        sorted_field_authors_info_df = field_authors_info_df.sort_values(
            ['citation_count'], ascending=False)
        json_records = sorted_field_authors_info_df.reset_index().to_json(orient='records')
        authors_data = json.loads(json_records)
    ####my dictionary####
    mydictionary = {
        'fields': fields_data,
        'authors': authors_data,
    }
    return render(request, 'insights/insights_author_table.html', context=mydictionary)


def insights_keyphrases(request):
    ####Getting Fields####
    fields = Field.objects.all()
    fields_dataframe = pd.DataFrame(fields.values())
    json_records = fields_dataframe.reset_index().to_json(orient='records')
    fields_data = []
    fields_data = json.loads(json_records)
    ####Initializing Data####
    keyphrases_df = pd.DataFrame()
    keyphrases_data = []
    ####Getting Keyphrases####
    if request.method == 'POST':
        field_option = request.POST.get('field_option')
        field_keyphrase_ids = FieldHasKeyphrase.objects.filter(
            field_name=field_option)
        field_keyphrase_ids_df = pd.DataFrame(field_keyphrase_ids.values())
        field_keyphrase_ids_list = field_keyphrase_ids_df['f_keyphrase_id'].tolist(
        )
        keyphrases_df = pd.DataFrame()
        years_scholarly_output_df = pd.DataFrame()
        years_df = pd.DataFrame()
        for f in field_keyphrase_ids_list:
            keyphrase = FieldKeyPhrase.objects.filter(pk=f)
            keyphrases_minidf = pd.DataFrame(keyphrase.values())
            keyphrases_df = pd.concat([keyphrases_df, keyphrases_minidf])
            years_scholarly_output = FieldKeyphraseByYear.objects.filter(pk=f)
            years_scholarly_output_minidf = pd.DataFrame(
                years_scholarly_output.values())
            years_scholarly_output_df = pd.concat(
                [years_scholarly_output_df, years_scholarly_output_minidf])
        ids = keyphrases_df['id'].tolist()
        names_list = keyphrases_df['name'].tolist()
        for index, row in years_scholarly_output_df.iterrows():
            year_id = row['year_id']
            year = Year.objects.filter(pk=year_id)
            years_minidf = pd.DataFrame(year.values())
            years_df = pd.concat([years_df, years_minidf])
        scholarly_output_list = years_scholarly_output_df['scholarly_output'].tolist(
        )
        year_list = years_df['year'].tolist()
        final_dict = {
            'scholarly_output': scholarly_output_list,
            'year': year_list
        }
        final_dataframe = pd.DataFrame(final_dict)
        sorted_final_dataframe = final_dataframe.sort_values(['year'])
        grouped = sorted_final_dataframe.groupby(sorted_final_dataframe.year)
        df_new1 = grouped.get_group(2011)
        df_new2 = grouped.get_group(2012)
        df_new3 = grouped.get_group(2013)
        df_new4 = grouped.get_group(2014)
        df_new5 = grouped.get_group(2015)
        df_new6 = grouped.get_group(2016)
        df_new7 = grouped.get_group(2017)
        df_new8 = grouped.get_group(2018)
        df_new9 = grouped.get_group(2019)
        df_new10 = grouped.get_group(2020)
        df_newlist = df_new1['scholarly_output'].tolist()
        df_newlist1 = df_new2['scholarly_output'].tolist()
        df_newlist2 = df_new3['scholarly_output'].tolist()
        df_newlist3 = df_new4['scholarly_output'].tolist()
        df_newlist4 = df_new5['scholarly_output'].tolist()
        df_newlist5 = df_new6['scholarly_output'].tolist()
        df_newlist6 = df_new7['scholarly_output'].tolist()
        df_newlist7 = df_new8['scholarly_output'].tolist()
        df_newlist8 = df_new9['scholarly_output'].tolist()
        df_newlist9 = df_new10['scholarly_output'].tolist()
        final_dictionary = {
            'id': ids,
            'keyphrase': names_list,
            '2011': df_newlist,
            '2012': df_newlist1,
            '2013': df_newlist2,
            '2014': df_newlist3,
            '2015': df_newlist4,
            '2016': df_newlist5,
            '2017': df_newlist6,
            '2018': df_newlist7,
            '2019': df_newlist8,
            '2020': df_newlist9
        }
        finally_dataframe = pd.DataFrame(final_dictionary)
        json_records = finally_dataframe.reset_index().to_json(orient='records')
        keyphrases_data = json.loads(json_records)

    ####my dictionary####
    mydictionary = {
        'fields': fields_data,
        'keyphrases': keyphrases_data,


    }
    return render(request, 'insights/insights_keyphrases.html', context=mydictionary)


def insights_keyphrases_chart(request, id):
    keyphrase_name = get_object_or_404(FieldKeyPhrase, pk=id)
    key_name = keyphrase_name.name
    graph_data = FieldKeyphraseByYear.objects.filter(pk=id)
    graph_dataframe = pd.DataFrame(graph_data.values())
    scholarly_output = graph_dataframe['scholarly_output'].tolist()
    years = [2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020]
    scholarly_output_str = ""
    years_str = ""
    for s in scholarly_output:
        scholarly_output_str = scholarly_output_str+str(s)+"*"
    for y in years:
        years_str = years_str+str(y)+"*"

    mydict = {
        'name': key_name,
        'years': years_str,
        'scholarly_output': scholarly_output_str
    }

    return render(request, 'insights/insights_keyphrases_chart.html', context=mydict)
