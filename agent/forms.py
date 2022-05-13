from django import forms
import json
import requests

def clubGetRuleParams(rulekey, type):
    apiUrlGetRuleByKey = 'https://gamificatoin-club.burux.ir/default/Rule/PAT_GetByKey'
    headers = {"Authorization" : "Basic c2hhaGluOmQyNmRhOTZlMmYwZDQxYzJiZjc1NjE2ZDM4Y2IyNGYxNDI5MDQ1Yzk1MGMyNGFjZGJiNGUwZGM1OWMxMTI3MjE="}
    body = {'Key': rulekey }
    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    jsonData = json.dumps(body)
    res = requests.post(apiUrlGetRuleByKey,json= body,headers= newHeaders,auth=("shahin", "d26da96e2f0d41c2bf75616d38cb24f1429045c950c24acdbb4e0dc59c112721"))
    response = res.json()
    params = response["Value"]["RuleParameters"]
    score_list = []
    gem_list = []
    for param in params:
        if param['Key'].startswith('sc') == True:
           tuplescore = (param['Key'], param['Value'])
           score_list.append(tuplescore)
        elif param['Key'].startswith('ge') == True:
            tuplegem = (param['Key'], param['Value'])
            gem_list.append(tuplegem)
    if type == 'gem':
       return gem_list
    elif type == 'score':
       return score_list


class ruleActiceCusForm(forms.Form):
    rulekey = 'Rule2.VC'
    gemChoices = clubGetRuleParams(rulekey,'gem')
    scoreChoices = clubGetRuleParams(rulekey,'score')
  #  rulekey = forms.ChoiceField(label='rulekey', choices=rulekeychoices)
    gem = forms.ChoiceField(label='gem',choices= gemChoices)
    score = forms.ChoiceField(label='score', choices= scoreChoices)
    excel = forms.BooleanField(label='excel',required=False)
    club = forms.BooleanField(label='club',required=False)

