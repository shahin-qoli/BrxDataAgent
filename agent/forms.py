from django import forms
import json
import requests

type_choices = ["gem", "score"]


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
    rulekey = 'Rule2-VC'
    gemChoices = clubGetRuleParams(rulekey,'gem')
    scoreChoices = clubGetRuleParams(rulekey,'score')
  #  rulekey = forms.ChoiceField(label='rulekey', choices=rulekeychoices)
    gem = forms.ChoiceField(label='gem',choices= gemChoices)
    score = forms.ChoiceField(label='score', choices= scoreChoices)
    excel = forms.BooleanField(label='excel',required=False)
    club = forms.BooleanField(label='club',required=False)
    rulekey = forms.CharField(label='rulekey')


class ruleVisitorCoverageForm(forms.Form):
    rulekey = 'Rule3-VC'
    gemChoices = clubGetRuleParams(rulekey,'gem')
    scoreChoices = clubGetRuleParams(rulekey,'score')
  #  rulekey = forms.ChoiceField(label='rulekey', choices=rulekeychoices)
   # gemb10 = forms.ChoiceField(label='gemb10',choices= gemChoices)
    scoreb10 = forms.ChoiceField(label='scoreb10', choices= scoreChoices)
    gemb1020 = forms.ChoiceField(label='gemb1020',choices= gemChoices)
    scoreb1020 = forms.ChoiceField(label='scoreb1020', choices= scoreChoices)
    gemb2040 = forms.ChoiceField(label='gemb2040',choices= gemChoices)
    scoreb2040 = forms.ChoiceField(label='scoreb2040', choices= scoreChoices)
    gemu40 = forms.ChoiceField(label='gemu40',choices= gemChoices)
    scoreu40 = forms.ChoiceField(label='scoreu40', choices= scoreChoices)
    excel = forms.BooleanField(label='excel',required=False)
    club = forms.BooleanField(label='club',required=False)

#'Rule1.CC'
class ruleCustomerSKUCount(forms.Form):
    rulekey = 'Rule1-CC'
    scoreChoices = clubGetRuleParams(rulekey,'score')
  #  rulekey = forms.ChoiceField(label='rulekey', choices=rulekeychoices)
   # gemb10 = forms.ChoiceField(label='gemb10',choices= gemChoices)
    score = forms.ChoiceField(label='score', choices= scoreChoices)
    excel = forms.BooleanField(label='excel',required=False)
    club = forms.BooleanField(label='club',required=False)
    rulekey = forms.CharField(label='rulekey')

#'Rule2.CC'
class ruleCustomerVolumePurchase(forms.Form):
    rulekey = 'Rule2-CC'
    scoreChoices = clubGetRuleParams(rulekey,'score')
  #  rulekey = forms.ChoiceField(label='rulekey', choices=rulekeychoices)
   # gemb10 = forms.ChoiceField(label='gemb10',choices= gemChoices)
    score = forms.ChoiceField(label='score', choices= scoreChoices)
    excel = forms.BooleanField(label='excel',required=False)
    club = forms.BooleanField(label='club',required=False)
    rulekey = forms.CharField(label='rulekey')

#'Rule3.CC'
class ruleCustomerFrequencyPurchase(forms.Form):
    rulekey = 'Rule3-CC'
    scoreChoices = clubGetRuleParams(rulekey,'score')
  #  rulekey = forms.ChoiceField(label='rulekey', choices=rulekeychoices)
   # gemb10 = forms.ChoiceField(label='gemb10',choices= gemChoices)
    rulekey = forms.CharField(label='rulekey',show_hidden_initial= False)
    scoreup7m = forms.ChoiceField(label='scoreup7m', choices= scoreChoices)
    scoreup4to7m = forms.ChoiceField(label='scoreup4to7m', choices= scoreChoices)
    excel = forms.BooleanField(label='excel',required=False)
    club = forms.BooleanField(label='club',required=False)


class reportFromClub(forms.Form):
    type = forms.ChoiceField(label='scoreOrGem', choices= type_choices)
    rule_id = forms.IntegerField()
    user_id = forms.CharField(max_length= 200)
    start_date = forms.DateField( )
    end_date = forms.DateField( )
    current_date = forms.DateField()


