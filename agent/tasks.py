from datetime import datetime

from celery.decorators import task
from celery import Celery
from celery.utils.log import get_task_logger
from time import sleep
import json
import requests
from agent.models import TransLogs, TransLogsJason

apiUrlUserAchivementCreateSingle = 'https://gamificatoin-club.burux.ir/default/UserAchievement/PAT_Create'
apiUrlUserAchivementCreate = 'https://gamificatoin-club.burux.ir/default/UserAchievement/PAT_CreateList'
logger = get_task_logger(__name__)
@task(name='clubUserAchivementCreate')
def clubUserAchivementCreate(create_list):
    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    bodygem = {"List": create_list}
    body = json.dumps(bodygem)
    res = requests.post(apiUrlUserAchivementCreate, json=bodygem, headers=newHeaders,
                        auth=("shahin", "b61994a253844e75a8fea629f2df30932a6976b5c60445eeb7b59a7f3733b24b"))
    responsecreat = res.json()
    status = responsecreat['Succeeded']
    sysloggerJson(datetime.now(), body, status)


@task(name='clubUserAchivementCreateSingle')
def clubUserAchivementCreateSingle(single_create):
    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # CustomParameter = []
    # bodygetrule = {'Key': rulekey }
    # Headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # resruleid = requests.post(apiUrlGetRuleByKey,json= bodygetrule,headers= Headers,auth=("shahin", "d26da96e2f0d41c2bf75616d38cb24f1429045c950c24acdbb4e0dc59c112721"))
    # response = resruleid.json()
    # ruleid = response["Value"]["Id"]
    # Datetime = datetime.now()
    # d = f"{Datetime}"
    bodygem = single_create
    print("ok")
    body = json.dumps(bodygem)
    res = requests.post(apiUrlUserAchivementCreateSingle, json=bodygem, headers=newHeaders,
                        auth=("shahin", "b61994a253844e75a8fea629f2df30932a6976b5c60445eeb7b59a7f3733b24b"), verify=False)
    responsecreat = res.json()
    status = responsecreat['Succeeded']
    sysloggerJson(datetime.now(), body, status)


def sysloggerJson(requestdate, request_body, status):
    TransLogsJason.objects.create(requestdate=requestdate, request_body=request_body, status=status)