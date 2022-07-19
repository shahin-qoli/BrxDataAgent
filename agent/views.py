import json
from threading import Thread
from datetime import datetime
import pymssql as pymssql
import xlwt as xlwt
from django.db.models import Count
from django.forms import ChoiceField
from django.http import HttpResponse
from django.shortcuts import render
import requests
from agent.models import Ocrd, Vwcustomerclub, NewCustomer, Oslp, OcrdOslp, VwagentActiveCustomerPerVisitor, Ordr, \
    Vwvisitorsku, Rules, VwAgentSKUCustomerClub, VwAgentPurchaseFrequencyCClub, TransLogs, Vendor, PersonVis, \
    PersonVen, vwLeadOfVisitor, vwActiveCountPerVisitor, vwAllCustomerOfVisitor, TransLogsJason
from .forms import *
from .tasks import clubUserAchivementCreateSingle
connectB1 = pymssql.connect("192.168.10.37", "BIAgent", "ABCdef123", "b1")
conncetReport = pymssql.connect("192.168.10.37", "BIAgent", "ABCdef123", "Reporting")
# connectB1 = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER="192.168.10.37";DATABASE="B1-Burux";UID="BIAgent";PWD="ABCdef123"')
apiUrlGetRuleByKey = 'https://gamificatoin-club.burux.ir/default/Rule/PAT_GetByKey'
apiUrlUserAchivementCreate = 'https://gamificatoin-club.burux.ir/default/UserAchievement/PAT_CreateList'
apiUrlSearch = 'https://gamificatoin-club.burux.ir/default/UserAchievement/PAT_Search'

apiUrlUserAchivementCreateSingle = 'https://gamificatoin-club.burux.ir/default/UserAchievement/PAT_Create'
def initOslp(request):
    if request.method == 'GET':
        cursor = connectB1.cursor()
        sql = "SELECT slpcode,slpname from oslp"
        cursor.execute(sql)
        for bp in cursor:
            if not Oslp.objects.filter(slpcode=bp[0]).exists():
                Oslp.objects.create(slpcode=bp[0], slpname=bp[1])
            else:
                pass
        message = "OSLP inited"
        return render(request, "agent/ok.html", {"message": message})
    else:
        pass


def initOcrd(request):
    if request.method == 'GET':
        cursor = connectB1.cursor()
        sql = "SELECT CardCode,CardName,CreateDate from ocrd"
        cursor.execute(sql)
        Ocrd.objects.all().delete()
        for bp in cursor:
            if not Ocrd.objects.filter(bpcode=bp[0]).exists():
                Ocrd.objects.create(bpcode=bp[0], bpname=bp[1], bpcreatedate=bp[2])
            else:
                pass
        message = "OCRD inited"
        return render(request, "agent/ok.html", {"message": message})

    else:
        pass


def initOrdr(request):
    if request.method == 'GET':
        cursor = connectB1.cursor()
        sql = "SELECT cardcode,slpcode,docdate from ORDR"
        cursor.execute(sql)
        Ordr.objects.all().delete()
        for bp in cursor:
            ocrdid = Ocrd.objects.filter(bpcode=bp[0]).values('id')
            oslpid = Oslp.objects.filter(slpcode=bp[1]).values('id')
            Ordr.objects.create(ocrd_id=ocrdid, oslp_id=oslpid, bpcode=bp[0], slpcode=bp[1], docdate=bp[2])
        message = "ORDR inited"
        return render(request, "agent/ok.html", {"message": message})


def initOcrdOslp(request):
    if request.method == 'GET':
        cursor = conncetReport.cursor()
        OcrdOslp.objects.all().delete()
        sql = "SELECT * from Burux.findSLPforBP"
        cursor.execute(sql)
        for bp in cursor:
            ocrdid = Ocrd.objects.filter(bpcode=bp[0]).values('id')
            oslpid = Oslp.objects.filter(slpcode=bp[1]).values('id')
            OcrdOslp.objects.create(ocrd_id=ocrdid, bpcode=bp[0], oslp_id=oslpid, slpcode=bp[1])
        message = "OcrdOslp inited"
        return render(request, "agent/ok.html", {"message": message})


def initPerson(request):
    if request.method == 'GET':
        cursor = conncetReport.cursor()
        PersonVis.objects.all().delete()
        PersonVen.objects.all().delete()
        sql = "SELECT id,cardcode, slpcode, userid from [visit-app].[global].person"
        cursor.execute(sql)
        for bp in cursor:
            PersonVis.objects.create(id=bp[0], bpcode=bp[1], slpcode=bp[2], userid=bp[3])
            PersonVen.objects.create(id=bp[0], bpcode=bp[1], slpcode=bp[2], userid=bp[3])
        message = "Person ven and vis inited"
        return render(request, "agent/ok.html", {"message": message})
    else:
        pass


def initVendor(request):
    if request.method == 'GET':
        cursor = conncetReport.cursor()
        Vendor.objects.all().delete()
        sql = "SELECT id,name, defaultvisitor from [visit-app].[market].vendor where id <> 0"
        cursor.execute(sql)
        for bp in cursor:
            Person = PersonVen.objects.get(id=bp[0])
            try:
                defaultvisitor = PersonVis.objects.get(id=bp[2])
            except:
                defaultvisitor = PersonVis.objects.get(id=4)
            Vendor.objects.create(person=Person, bpname=bp[1], defaultvisitor=defaultvisitor)
        message = "Vendor inited"
        return render(request, "agent/ok.html", {"message": message})
    else:
        pass


def initVwAgentPurchaseFrequencyCClub(request):
    if request.method == 'GET':
        cursor = conncetReport.cursor()
        OcrdOslp.objects.all().delete()
        sql = "SELECT CardCode,QuarterNum, [Year], Totalprice, CountInvoice,CountInvoice7MtoUp, CountInvoiceBetween4to7M from Burux.VwAgentPurchaseFrequencyCClub where [Year] = 1401 and QuarterNum = 1"
        cursor.execute(sql)
        for bp in cursor:
            ocrd = Ocrd.objects.filter(bpcode=bp[0]).values('id')
            VwAgentPurchaseFrequencyCClub.objects.create(bpcode=bp[0], quarternum=bp[1], year=bp[2], totalprice=bp[3],
                                                         countinvoice=bp[4], countinvoice7Mtoup=bp[5],
                                                         countinvoicebetween4to7M=bp[6], ocrd_id=ocrd)
        message = "VwAgentPurchaseFrequencyCClub inited"
        return render(request, "agent/ok.html", {"message": message})
    else:
        pass


def initVwAgentSKUCustomerClub(request):
    if request.method == 'GET':
        cursor = conncetReport.cursor()
        OcrdOslp.objects.all().delete()
        sql = "SELECT CardCode,QuarterNum, [jYear], Totalprice, CountOfSKU,CountOfSKU500K from Burux.VwAgentSKUCustomerClub where [jYear] = 1401 and QuarterNum = 1"
        cursor.execute(sql)
        for bp in cursor:
            ocrd = Ocrd.objects.filter(bpcode=bp[0]).values('id')
            VwAgentSKUCustomerClub.objects.create(bpcode=bp[0], quarternum=bp[1], year=bp[2], totalprice=bp[3],
                                                  countofsku=bp[4], countofsku500k=bp[5], ocrd_id=ocrd)
        message = "VwAgentSKUCustomerClub inited"
        return render(request, "agent/ok.html", {"message": message})
    else:
        pass


"""def initVwcustomerclub(request):
    if request.method == 'GET':
        Vwcustomerclub.objects.all().delete()
        cursor = conncetReport.cursor()
        sql = "SELECT CardCode,Quartern,year,numberofinvoices,countofsku,countofsku500k,totalprice from dbo.Vwcustomerclub"
        cursor.execute(sql)
        for bp in cursor:
            ocrd = Ocrd.objects.filter(bpcode=bp[0]).values('id')
            Vwcustomerclub.objects.create(bpcode=bp[0], quarter=bp[1], year=bp[2], numberofinovices=bp[3],
                                          countsku=bp[4], countskuup500kT=bp[5], totalprice=bp[6], ocrd_id=ocrd)
    else:
        pass
"""

"""def initVwagentActiveCustomerPerVisitor(request):
    if request.method == 'GET':
        VwagentActiveCustomerPerVisitor.objects.all().delete()
        cursor = conncetReport.cursor()
        sql = "SELECT slpcode,PartOfYear,countActivecustomer from burux.VwagentActiveCustomerPerVisitor where quarterN = 8"
        cursor.execute(sql)
        for bp in cursor:
            oslp = Oslp.objects.filter(slpcode=bp[0]).values('id')
            VwagentActiveCustomerPerVisitor.objects.create(slpcode=bp[0], quartern=bp[1], activecustomer=bp[2],
                                                           oslp_id=oslp)
    else:
        pass
"""


def iniVwvisitorsku(request):
    if request.method == 'GET':
        Vwvisitorsku.objects.all().delete()
        cursor = conncetReport.cursor()

        sql = "SELECT slpcode,JMonthN,jyear,countuniquesku,countuniquecustomer FROM [dbo].[vwVisitorSKU]"
        cursor.execute(sql)
        for bp in cursor:
            oslp = Oslp.objects.filter(slpcode=bp[0]).values('id')
            Vwvisitorsku.objects.create(slpcode=bp[0], oslp_id=oslp, jmonthn=bp[1], jyear=bp[2], countuniquesku=bp[3],
                                        countuniquecustomer=bp[4])
    else:
        pass


def initvwActiveCountPerVisitor(request):
    if request.method == 'GET':
        vwActiveCountPerVisitor.objects.all().delete()
        cursor = conncetReport.cursor()
        sql = "SELECT visitorUserId,SlpCode, activecount FROM [dbo].[vwActiveCusPerVisitorMeeting]"
        cursor.execute(sql)
        for bp in cursor:
            # oslp = Oslp.objects.filter(slpcode=bp[0]).values('id')
            vwActiveCountPerVisitor.objects.create(slpcode=bp[1], slpuserid=bp[0], activecount=bp[2])
    else:
        pass


def initvwAllCustomerOfVisitor(request):
    if request.method == 'GET':
        vwAllCustomerOfVisitor.objects.all().delete()
        cursor = conncetReport.cursor()
        sql = "SELECT UserId,SlpCode, customercount FROM [dbo].[vwAllCustomerOfVisitor] where slpcode is not null"
        cursor.execute(sql)
        for bp in cursor:
            # oslp = Oslp.objects.filter(slpcode=bp[0]).values('id')
            vwAllCustomerOfVisitor.objects.create(slpcode=bp[1], slpuserid=bp[0], customercount=bp[2])
    else:
        pass


def initVwLeadOfVisitor(request):
    if request.method == 'GET':
        vwLeadOfVisitor.objects.all().delete()
        cursor = conncetReport.cursor()
        sql = "SELECT customerCardcode,visitorUserId,SlpCode FROM [dbo].[vwLeadOfVisitor]"
        cursor.execute(sql)
        for bp in cursor:
            # oslp = Oslp.objects.filter(slpcode=bp[0]).values('id')
            vwLeadOfVisitor.objects.create(slpcode=bp[2], slpuserid=bp[1], bpcode=bp[0])
    else:
        pass


def initNewCustomer(request):
    if request.method == 'GET':
        q1 = Ocrd.objects.all()
        NewCustomer.objects.all().delete()
        for a1 in q1:
            if not NewCustomer.objects.filter(bpcode=a1.bpcode).exists():
                NewCustomer.objects.create(bpcode=a1.bpcode, bpcreatedate=a1.bpcreatedate, bpused=True, slpcodeused=0,
                                           ocrd_id=a1.id)
            else:
                pass
    else:
        pass


def handleNewCustomer(request):
    if request.method == "GET":
        q1 = NewCustomer.objects.filter(bpcreatedate__gte='2022-01-01')
        for bp in q1:
            bp.bpused = False
            bp.bpuseddate = ''
            bp.save()
    else:
        pass


def testclubUserAchivementCreate(request):
    rulekey = "Rule2-CC"
    parameterkey = "score"
    userid = "test"
    clubUserAchivementCreate(rulekey, parameterkey, userid)


"""
def clubUserAchivementCreateScore(rulekey, userid, countscore):
    bodyscore = {"Ruleid": rulekey, "ParameterKey": "score", "Count": countscore,
                 "UserId": userid,
                 "DateTime": datetime.now(), "CustomParameter": []}
    res = requests.post(apiUrlUserAchivementCreate, bodyscore)
"""


def logicTry(request):
    if request.POST['rulekey'] == 'Rule1-CC':
        return (logicCustomerSKUCount(request))
    elif request.POST['rulekey'] == 'Rule2-CC':
        return (logicCustomerVolumePurchase(request))
    elif request.POST['rulekey'] == 'Rule3-CC':
        return (logicCustomerFrequencyPurchase(request))
    elif request.POST['rulekey'] == 'Rule1-VC':
        return (logicVisitorLeads(request))
    elif request.POST['rulekey'] == 'Rule2-VC':
        return (logicVisitorActiveCustomer(request))

"""def logicVisitorCusCoverage(request):
    rulekey = request.POST['rulekey']
    basegem = request.POST['gem']
    basescore = request.POST['score']
    visq = Vwvisitorsku.objects.filter(jmonthn=12)
    datalist = []
    for vis in visq:
        allcus = len(OcrdOslp.objects.filter(oslp_id=vis.oslp_id))
        if not allcus == 0:
            percent = (vis.countuniquecustomer / allcus) * 100
        else:
            pass

        countgem = int(percent) * int(basegem)
        countscore = int(percent) * int(basescore)
        if request.POST.__contains__('club'):
            clubUserAchivementCreateGem(rulekey, vis.slpcode, countgem)
            clubUserAchivementCreateScore(rulekey, vis.slpcode, countscore)
        elif request.POST.__contains__('excel'):
            data = (rulekey, vis.slpcode, countgem, countscore)
            datalist.append(data)

    if request.POST.__contains__('excel'):
        return (exportUserAchivement(request, datalist))


   
def renderRuleFormWoutDate(request):
    if request.method == "GET":
        form = ruleWoDate()
        return render(request, 'agent/index-2.html', {'form': form})

"""

"""
def logicVisitorAvticeCus(request):
    rulekey = 'Rule2-VC'
    visq = VwagentActiveCustomerPerVisitor.objects.all()
    basegem = request.POST['gem']
    basescore = request.POST['score']
    datalist = []
    for vis in visq:
        # gemcount = vis.quartern * basegem
        # scorecount = vis.quartern * basescore
        if request.POST.__contains__('club'):
            for i in range(vis.activecustomer):
                clubUserAchivementCreate(rulekey, basegem, vis.slpcode)
                clubUserAchivementCreate(rulekey, basescore, vis.slpcode)
        elif request.POST.__contains__('excel'):
            data = (rulekey, vis.slpcode, basegem, basescore)
            datalist.append(data)

    if request.POST.__contains__('excel'):
        return (exportUserAchivement(request, datalist))



def logicVisitorNewCus(request):
    rulekey = request.POST['rulekey']
    basegem = int(request.POST['gem'])
    basescore = int(request.POST['score'])
    cusq = NewCustomer.objects.filter(bpused=False)
    datalist = []
    for cus in cusq:
        if Ordr.objects.filter(bpcode=cus.bpcode).exists() and OcrdOslp.objects.filter(bpcode=cus.bpcode).values(
                'slpcode') == Ordr.objects.filter(bpcode=cus.bpcode).values('slpcode'):
            bp =NewCustomer.objects.filter(bpcode=Ordr.objects.filter(bpcode=cus.bpcode).values('bpcode'))

            if request.POST.__contains__('club'):
                clubUserAchivementCreateGem(rulekey, Ordr.objects.filter(bpcode=cus.bpcode).values('slpcode'), basegem)
                clubUserAchivementCreateScore(rulekey, Ordr.objects.filter(bpcode=cus.bpcode).values('slpcode'),
                                              basescore)
            elif request.POST.__contains__('excel'):
                data = (rulekey, Ordr.objects.filter(bpcode=cus.bpcode).values('slpcode'), basegem, basescore)
                datalist.append(data)

    if request.POST.__contains__('excel'):
        return (exportUserAchivement(request, datalist))

"""
# Done for new structure
# Rule2-VC
def logicVisitorActiveCustomer(request):
    rulekey = 'Rule2-VC'
    basescore = request.POST['score']
    basegem = request.POST['gem']
    datalist = []
    create_list = []
    vq = vwActiveCountPerVisitor.objects.all()
    ruleid = get_rule_id(rulekey)
    for v in vq:
        if request.POST.__contains__('club'):
            CustomParameter = []
            for i in range(v.activecount):
               Datetime = datetime.now()
               d = f"1401/03/31"
               score_single_create = {"Ruleid": ruleid, "ParameterKey": basescore,
                                       "UserId": v.slpuserid,
                                       "DateTime": d, "CustomParameter": CustomParameter}
               gem_single_create = {"Ruleid": ruleid, "ParameterKey": basegem,
                                     "UserId": v.slpuserid,
                                     "DateTime": d, "CustomParameter": CustomParameter}
               create_list.append(score_single_create)
               create_list.append(gem_single_create)

            # clubUserAchivementCreate(rulekey, basescore, bp.bpcode)

        elif request.POST.__contains__('excel'):
             data = (rulekey, v.slpuserid, basescore,basegem )
             datalist.append(data)

    if request.POST.__contains__('excel'):
        return exportUserAchivement(request, datalist)
    elif request.POST.__contains__('club'):
        clubUserAchivementCreate.delay(create_list)


def get_rule_id(rule_key):
    bodygetrule = {'Key': rule_key}
    Headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    resruleid = requests.post(apiUrlGetRuleByKey, json=bodygetrule, headers=Headers, auth=(
        "shahin", "b61994a253844e75a8fea629f2df30932a6976b5c60445eeb7b59a7f3733b24b"))
    response = resruleid.json()
    ruleid = response["Value"]["Id"]
    return ruleid

# Done for new structure
# Rule1-VC
def logicVisitorLeads(request):
    rulekey = 'Rule1-VC'
    basescore = request.POST['score']
    basegem = request.POST['gem']
    datalist = []
    create_list = []
    vq = vwLeadOfVisitor.objects.all()
    ruleid = get_rule_id(rulekey)
    for v in vq:
        if request.POST.__contains__('club'):
            CustomParameter = []

            Datetime = datetime.now()
            d = f"1401/03/31"

            score_single_create = {"Ruleid": ruleid, "ParameterKey": basescore,
                                       "UserId": v.slpuserid,
                                       "DateTime": d, "CustomParameter": CustomParameter}
            gem_single_create = {"Ruleid": ruleid, "ParameterKey": basegem,
                                     "UserId": v.slpuserid,
                                     "DateTime": d, "CustomParameter": CustomParameter}
            create_list.append(score_single_create)
            create_list.append(gem_single_create)

            # clubUserAchivementCreate(rulekey, basescore, bp.bpcode)

        elif request.POST.__contains__('excel'):
            data = (rulekey, v.slpuserid, basescore,basegem)
            datalist.append(data)

    if request.POST.__contains__('excel'):
        return (exportUserAchivement(request, datalist))
    elif request.POST.__contains__('club'):
        clubUserAchivementCreate.delay(create_list)


# Done for new structure
# Rule2.CC
def logicCustomerVolumePurchase(request):
    rulekey = 'Rule2-CC'
    ruleid = get_rule_id(rulekey)
    basescore = request.POST['score']
    datalist = []
    create_list = []
    bpq = VwAgentPurchaseFrequencyCClub.objects.all()
    for bp in bpq:
        totalprice = 0 if bp.totalprice == None else bp.totalprice
        quanof1MT = int(totalprice / 10000000)
        for i in range(quanof1MT):
            if request.POST.__contains__('club'):
                CustomParameter = []
                Datetime = datetime.now()
                d = f"1401/03/31"
                single_create = {"Ruleid": ruleid, "ParameterKey": basescore,
                                 "UserId": bp.bpcode,
                                 "DateTime": d, "CustomParameter": CustomParameter}
                create_list.append(single_create)
                # clubUserAchivementCreate(rulekey, basescore, bp.bpcode)

            elif request.POST.__contains__('excel'):
                data = (rulekey, bp.bpcode, basescore)
                datalist.append(data)

    if request.POST.__contains__('excel'):
        return (exportUserAchivement(request, datalist))
    elif request.POST.__contains__('club'):
        clubUserAchivementCreate.delay(create_list)


# Done for new structure
# Rule3.CC
def logicCustomerFrequencyPurchase(request):
    rulekey = 'Rule3-CC'
    ruleid = get_rule_id(rulekey)
    basescoreup7m = request.POST['scoreup7m']
    basescoreup4to7m = request.POST['scoreup4to7m']
    datalist = []
    create_list = []
    bpq = VwAgentPurchaseFrequencyCClub.objects.all()
    for bp in bpq:

        countinvoice7Mtoup = 0 if bp.countinvoice7Mtoup == None else bp.countinvoice7Mtoup
        countinvoicebetween4to7M = 0 if bp.countinvoicebetween4to7M == None else bp.countinvoicebetween4to7M

        for i in range(countinvoice7Mtoup):
            if request.POST.__contains__('club'):
                CustomParameter = []
                Datetime = datetime.now()
                d = f"1401/03/31"
                single_create = {"Ruleid": ruleid, "ParameterKey": basescoreup7m,
                                 "UserId": bp.bpcode,
                                 "DateTime": d, "CustomParameter": CustomParameter}
                create_list.append(single_create)
                # clubUserAchivementCreate(rulekey, basescoreup7m, bp.bpcode)
            elif request.POST.__contains__('excel'):
                data = (rulekey, bp.bpcode, basescoreup7m)
                datalist.append(data)
        for i in range(countinvoicebetween4to7M):
            if request.POST.__contains__('club'):
                CustomParameter = []
                Datetime = datetime.now()
                d = f"1401/03/31"
                single_create = {"Ruleid": ruleid, "ParameterKey": basescoreup4to7m,
                                 "UserId": bp.bpcode,
                                 "DateTime": d, "CustomParameter": CustomParameter}
                create_list.append(single_create)
                # clubUserAchivementCreate(rulekey, basescoreup4to7m, bp.bpcode)
            elif request.POST.__contains__('excel'):
                data = (rulekey, bp.bpcode, basescoreup4to7m)
                datalist.append(data)

    if request.POST.__contains__('excel'):
        return (exportUserAchivement(request, datalist))
    elif request.POST.__contains__('club'):
        clubUserAchivementCreate.delay(create_list)

#Redesigend
# Done for new structure
# Rule1.CC quan of inv line
def logicCustomerSKUCount(request):
    rulekey = 'Rule1-CC'
    ruleid = get_rule_id(rulekey)
    CustomParameter = []
    Datetime = datetime.now()
    d = f"1401/03/31"
    basescore = request.POST['score']
    datalist = []
    create_list = []
    bpq = VwAgentSKUCustomerClub.objects.all()
    for bp in bpq:
        countofsku500k = 0 if bp.countofsku500k == None else bp.countofsku500k
        try:
            UserId = PersonVen.objects.get(bpcode=bp.bpcode).userid
        except:
            UserId = PersonVen.objects.get(bpcode='c50000').userid
        for i in range(countofsku500k):
            if request.POST.__contains__('club'):

                single_create = {"Ruleid": ruleid, "ParameterKey": basescore,
                                 "UserId": bp.bpcode,
                                 "DateTime": d, "CustomParameter": CustomParameter}
                #create_list.append(single_create)
                t = Thread(target=clubUserAchivementCreateSingle(single_create))
                t.start()
                #clubUserAchivementCreateSingle.delay(single_create)
            elif request.POST.__contains__('excel'):
                data = (rulekey, bp.bpcode, basescore)
                datalist.append(data)


    if request.POST.__contains__('excel'):
        return (exportUserAchivement(request, datalist))
    else:
        message = "{} is done".format(rulekey)
        return render(request, "agent/ok.html", {"message": message})
    #elif request.POST.__contains__('club'):
    #    clubUserAchivementCreate.delay(create_list)

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
                        auth=("shahin", "b61994a253844e75a8fea629f2df30932a6976b5c60445eeb7b59a7f3733b24b"))
    responsecreat = res.json()
    status = responsecreat['Succeeded']
    sysloggerJson(datetime.now(), body, status)


"""def clubUserAchivementCreate(create_list):
    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # CustomParameter = []
    # bodygetrule = {'Key': rulekey }
    # Headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # resruleid = requests.post(apiUrlGetRuleByKey,json= bodygetrule,headers= Headers,auth=("shahin", "d26da96e2f0d41c2bf75616d38cb24f1429045c950c24acdbb4e0dc59c112721"))
    # response = resruleid.json()
    # ruleid = response["Value"]["Id"]
    # Datetime = datetime.now()
    # d = f"{Datetime}"
    bodygem = {"List": create_list}
    body = json.dumps(bodygem)
    res = requests.post(apiUrlUserAchivementCreate, json=bodygem, headers=newHeaders,
                        auth=("shahin", "b61994a253844e75a8fea629f2df30932a6976b5c60445eeb7b59a7f3733b24b"))
    responsecreat = res.json()
    status = responsecreat['Succeeded']
    sysloggerJson(datetime.now(), body, status)
"""


"""def logicVisitorInvSkuCount(request):
    rulekey = request.POST['rulekey']
    basegem = int(request.POST['gem'])
    basescore = int(request.POST['score'])
    visq = Vwvisitorsku.objects.all()
    datalist = []
    for vis in visq:
        gemcount = vis.countuniquesku * basegem
        scorecount = vis.countuniquesku * basescore
        if request.POST.__contains__('club'):
            clubUserAchivementCreate(rulekey, vis.slpcode, gemcount)

        #           clubUserAchivementCreateScore(rulekey, vis.slpcode, scorecount)
        elif request.POST.__contains__('excel'):
            data = (rulekey, vis.slpcode, gemcount, scorecount)
            datalist.append(data)
    if request.POST.__contains__('excel'):
        return (exportUserAchivement(request, datalist))
"""

def exportUserAchivement(request, rows):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="UserAchivement.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('UserAchivement')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = ['RuleKey', 'UserId', 'Gem', 'Score', ]
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)
    wb.save(response)
    return response


def syslogger(requestdate, ruleid, parameterkey, userid, CustomParameter, status):
    TransLogs.objects.create(requestdate=requestdate, ruleid=ruleid, parameterkey=parameterkey, userid=userid,
                             CustomParameter=CustomParameter, status=status)


def sysloggerJson(requestdate, request_body, status):
    TransLogsJason.objects.create(requestdate=requestdate, request_body=request_body, status=status)


"""
This section is just for test, I have to write def for retriev e data from khsoravi api
"""


def pageIndex(request):
    if request.method == 'GET':
        rule_list = []
        rules = Rules.objects.all()
        # for rule in rules:
        #   rule_list.append(rule.title)
        return render(request, "agent/index.html", {"rules": rules})


def pageRuleVC2(request):
    rulekey = 'Rule2-VC'
    message = 'شما در حال محاسبه قانون مشتری فعال برای ویزیتور هستید'
    form = ruleVisitorActiveForm(initial={"rulekey": rulekey, "message": message})
    if request.method == 'GET':
        return render(request, 'agent/index-2.html', {'form': form, "message": message})


def pageRuleVC3(request):
    rulekey = 'Rule3-VC'
    form = ruleVisitorCoverageForm(initial={"rulekey": rulekey})
    if request.method == 'GET':
        return render(request, 'agent/index-2.html', {'form': form})


def pageRuleVC1(request):
    rulekey = 'Rule1-VC'
    message = 'شما در حال محاسبه قانون لید برای ویزیتور هستید'
    form = ruleVisitorLeadsForm(initial={"rulekey": rulekey, "message": message})
    if request.method == 'GET':
        return render(request, 'agent/index-2.html', {'form': form, "message": message})


def pageRuleCC1(request):
    rulekey = 'Rule1-CC'
    message = 'شما در حال محاسبه قانون خط فاکتور برای مشتری هستید'
    form = ruleCustomerSKUCount(initial={"rulekey": rulekey, "message": message})
    if request.method == 'GET':
        return render(request, 'agent/index-2.html', {'form': form, "message": message})


def pageRuleCC2(request):
    rulekey = 'Rule2-CC'
    message = 'شما در حال محاسبه قانون حجم خرید برای مشتری هستید'
    form = ruleCustomerVolumePurchase(initial={"rulekey": rulekey, "message": message})
    if request.method == 'GET':
        return render(request, 'agent/index-2.html', {'form': form, "message": message})


def pageRuleCC3(request):
    rulekey = 'Rule3-CC'
    message = 'شما در حال محاسبه قانون استمرار خرید برای مشتری هستید'
    form = ruleCustomerFrequencyPurchase(initial={"rulekey": rulekey})
    if request.method == 'GET':
        return render(request, 'agent/index-2.html', {'form': form, "message": message})


def pageReport(request):
    if request.method == 'GET':
        form = reportFromClub
        return render(request, "agent/report.html", {"form": form})
    elif request.method == 'POST':
        Type = request.POST['type']
        RuleId = request.POST['rule_id']
        UserId = request.POST['user_id']
        StartDate = request.POST['start_date']
        EndDate = request.POST['end_date']
        CurrentDate = request.POST['current_date']
        body = {'filter': {'filters': [{"Field": "Type", "Value": Type}, {"Field": "RuleId", "Value": RuleId},
                                       {"Field": "UserId", "Value": UserId},
                                       {"Field": "StartDate", "Value": StartDate},
                                       {"Field": "EndDate", "Value": EndDate},
                                       {"Field": "CurrentDate", "Value": CurrentDate}]}}
        newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post(apiUrlGetRuleByKey, json=body, headers=newHeaders,
                            auth=("shahin", "d26da96e2f0d41c2bf75616d38cb24f1429045c950c24acdbb4e0dc59c112721"))
        response = res.json()
