import json
from venv import create
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import login as auth_login
import pandas as pd
from .forms import signupform
from .models import Field , AuthUser,UserField,UserHistory,Document,UserDocument
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# Create your views here.
def signup(request):
    form=signupform()
    if request.method=='POST':
        form=signupform(request.POST)
        if form.is_valid():
            User=form.save()
            auth_login(request,User)
            return redirect('choose_fields')
        
    return render(request,'signup.html',{'form':form})

#def choose_fields(request):
 #   fields = Field.objects.all()
  #  return render(request, 'fields.html', {'fields': fields}) 

@login_required
def choose_fields(request):
    ff=Field.objects.all()
    if request.method=='POST':
        fields=request.POST.getlist('fields')
        user_=get_object_or_404(AuthUser,pk=request.user)
        for field in fields:
            fieldd=get_object_or_404(Field,pk=field)
            User_Field=UserField.objects.create( 
            field_name=fieldd,
            username=user_
        )

        return redirect('home')   
    return render(request, 'fields.html',{'fields':ff})

def account(request):
    user_=get_object_or_404(AuthUser,pk=request.user)
    ###### user history #######
    history=UserHistory.objects.filter(username=user_)   
    df=pd.DataFrame(history.values())
    histories=df['history_name'].tolist()
    for i in range(len(histories)):
        if i==len(histories)-1:
            break
        if histories[i]==histories[i+1]:
            df.drop([i+1], axis=0, inplace=True)
        
    
    json_records = df.reset_index().to_json(orient='records')
    data = []
    data = json.loads(json_records) 

    ##### user favorites #######
    favorites=UserDocument.objects.filter(username=user_)   
    favorites_df=pd.DataFrame(favorites.values())
    document_names=[]
    for index,row in favorites_df.iterrows():
        doc_id=row['document_id']
        doc_name=get_object_or_404(Document,pk=doc_id)
        document_names.append(doc_name.name)
    favorites_df["name"]=document_names
  
    json_records = favorites_df.reset_index().to_json(orient='records')
    data_fav = []
    data_fav = json.loads(json_records) 
    return render(request,'account/my_account.html',{'data':data,'data_fav':data_fav})    