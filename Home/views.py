from webbrowser import get
from wsgiref.simple_server import demo_app
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from Search.models import Topic
from .models import Field, AuthUser, UserField, Topic, Year, Document
import pandas as pd
# Create your views here.


def home(request):
    user_ = get_object_or_404(AuthUser, pk=request.user)
    print(user_.username)
    # user_fields=get_object_or_404(UserField,username=user_.username)
    user_fields = UserField.objects.filter(username=user_.username)
    temp = pd.DataFrame(user_fields.values())
    user_fields = temp['field_name_id'].tolist()
    print(user_fields)
    field_dict = {}
    for f in user_fields:
        temp_topics = Topic.objects.filter(field_name=f)
        temp_topics_df = pd.DataFrame(temp_topics.values())
        topics_info = pd.DataFrame()
        for index, row in temp_topics_df.iterrows():
            topic_id = row['topic_id']
            document = Document.objects.filter(topic=topic_id)
            document_df = pd.DataFrame(document.values())
            df = document_df['year'].value_counts().reset_index(name='number')
            df = df.sort_values(by='index')
            temp_df = pd.DataFrame({'topic_id': topic_id, 'Year': [
                                   df['index'].tolist()], 'scholarly_output': [df['number'].tolist()]})
            topics_info = pd.concat([topics_info, temp_df])

        field_dict[f] = topics_info
    print(field_dict)
    for x, y in field_dict.items():
        growth = []
        for index, row in y.iterrows():
            scholarly_output = row['scholarly_output']
            growth.append(
                ((scholarly_output[-1]-scholarly_output[0])/scholarly_output[0])*100)
        y["growth"] = growth

    #### sort dataframe #####
    new_dict = {}
    for x, y in field_dict.items():
        Top5 = (y.sort_values(by=['growth'], ascending=False)).head(5)
        new_dict[x] = Top5['topic_id'].tolist()

    final = {}
    for x, y in new_dict.items():
        temp = pd.DataFrame()
        for i in y:
            temp2 = pd.DataFrame((Topic.objects.filter(topic_id=i)).values())
            temp = pd.concat([temp, temp2])
        json_records = temp.reset_index().to_json(orient='records')
        data = []
        data = json.loads(json_records)
        final[x] = data

    return render(request, 'home/home.html', {'final': final})
