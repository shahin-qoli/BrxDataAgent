import json
from datetime import datetime
import pymssql as pymssql
import xlwt as xlwt
from django.db.models import Count
from django.forms import ChoiceField
from django.http import HttpResponse
from django.shortcuts import render
import requests
from agent.models import Ocrd, Vwcustomerclub, NewCustomer, Oslp, OcrdOslp, VwagentActiveCustomerPerVisitor, Ordr, \
    Vwvisitorsku, Rules,VwAgentSKUCustomerClub,VwAgentPurchaseFrequencyCClub, TransLogs
from .forms import *

connectB1 = pymssql.connect("192.168.10.37", "BIAgent", "ABCdef123", "BURUX")
conncetReport = pymssql.connect("192.168.10.37", "BIAgent", "ABCdef123", "Reporting")
#connectB1 = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER="192.168.10.37";DATABASE="B1-Burux";UID="BIAgent";PWD="ABCdef123"')
apiUrlGetRuleByKey = 'https://gamificatoin-club.burux.ir/default/Rule/PAT_GetByKey'
apiUrlUserAchivementCreate = 'https://gamificatoin-club.burux.ir/default/UserAchievement/PAT_Create'
apiUrlSearch = 'https://gamificatoin-club.burux.ir/default/UserAchievement/PAT_Search'

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
        return render(request,"agent/ok.html", {"message" : message})
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
        return render(request,"agent/ok.html", {"message" : message})

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
        return render(request,"agent/ok.html", {"message" : message})

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
        return render(request,"agent/ok.html", {"message" : message})

def initVwAgentPurchaseFrequencyCClub(request):
    if request.method == 'GET':
        cursor = conncetReport.cursor()
        OcrdOslp.objects.all().delete()
        sql = "SELECT CardCode,QuarterNum, [Year], Totalprice, CountInvoice,CountInvoice7MtoUp, CountInvoiceBetween4to7M from Burux.VwAgentPurchaseFrequencyCClub where [Year] = 1400 and QuarterNum = 4"
        cursor.execute(sql)
        for bp in cursor:
            ocrd = Ocrd.objects.filter(bpcode=bp[0]).values('id')
            VwAgentPurchaseFrequencyCClub.objects.create(bpcode=bp[0], quarternum=bp[1], year=bp[2], totalprice=bp[3],
                                          countinvoice=bp[4], countinvoice7Mtoup=bp[5], countinvoicebetween4to7M=bp[6], ocrd_id=ocrd)
        message = "VwAgentPurchaseFrequencyCClub inited"
        return render(request, "agent/ok.html", {"message": message})
    else:
        pass


def initVwAgentSKUCustomerClub(request):
    if request.method == 'GET':
        cursor = conncetReport.cursor()
        OcrdOslp.objects.all().delete()
        sql = "SELECT CardCode,QuarterNum, [jYear], Totalprice, CountOfSKU,CountOfSKU500K from Burux.VwAgentSKUCustomerClub where [jYear] = 1400 and QuarterNum = 4"
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
    clubUserAchivementCreate(rulekey, parameterkey, userid )

def clubUserAchivementCreate(rulekey, parameterkey, userid):
    newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    CustomParameter = []
    bodygetrule = {'Key': rulekey }
    Headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    resruleid = requests.post(apiUrlGetRuleByKey,json= bodygetrule,headers= Headers,auth=("shahin", "d26da96e2f0d41c2bf75616d38cb24f1429045c950c24acdbb4e0dc59c112721"))
    response = resruleid.json()
    ruleid = response["Value"]["Id"]
    Datetime = datetime.now()
    d = f"{Datetime}"
    bodygem = {"Ruleid": ruleid, "ParameterKey": parameterkey,
               "UserId": userid,
               "DateTime": d, "CustomParameter": CustomParameter}
    #body = json.dumps(bodygem)
    res = requests.post(apiUrlUserAchivementCreate,json= bodygem,headers= newHeaders,auth=("shahin", "d26da96e2f0d41c2bf75616d38cb24f1429045c950c24acdbb4e0dc59c112721"))
    responsecreat = res.json()
    status = responsecreat['Succeeded']
    syslogger(datetime.now(), ruleid, parameterkey, userid, CustomParameter,status )



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


def logicVisitorAvticeCus(request):
    rulekey = 'Rule2-VC'
    visq = VwagentActiveCustomerPerVisitor.objects.all()
    basegem = request.POST['gem']
    basescore = request.POST['score']
    datalist = []
    for vis in visq:
       # gemcount = vis.quartern * basegem
        #scorecount = vis.quartern * basescore
        if request.POST.__contains__('club'):
            for i in range(vis.activecustomer):
              clubUserAchivementCreate(rulekey, basegem, vis.slpcode)
              clubUserAchivementCreate(rulekey, basescore, vis.slpcode)
        elif request.POST.__contains__('excel'):
            data = (rulekey, vis.slpcode, basegem, basescore)
            datalist.append(data)

    if request.POST.__contains__('excel'):
        return (exportUserAchivement(request, datalist))


"""
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
#Rule2.CC
def logicCustomerVolumePurchase(request):
    rulekey = 'Rule2-CC'
    basescore = request.POST['score']
    datalist = []
    bpq = VwAgentPurchaseFrequencyCClub.objects.all()
    for bp in bpq:
        totalprice = 0 if bp.totalprice == None else bp.totalprice
        quanof1MT = int(totalprice/10000000)
        for i in range(quanof1MT):
          if request.POST.__contains__('club'):
              clubUserAchivementCreate(rulekey, basescore, bp.bpcode)

          elif request.POST.__contains__('excel'):
              data = (rulekey, bp.bpcode, basescore)
              datalist.append(data)

    if request.POST.__contains__('excel'):
        return (exportUserAchivement(request, datalist))

#Rule3.CC
def logicCustomerFrequencyPurchase(request):
    rulekey = 'Rule3-CC'
    basescoreup7m = request.POST['scoreup7m']
    basescoreup4to7m = request.POST['scoreup4to7m']
    datalist = []
    bpq = VwAgentPurchaseFrequencyCClub.objects.all()
    for bp in bpq:

        countinvoice7Mtoup = 0 if bp.countinvoice7Mtoup == None else bp.countinvoice7Mtoup
        countinvoicebetween5to7M = 0 if bp.countinvoicebetween5to7M == None else bp.countinvoicebetween5to7M

        for i in range(countinvoice7Mtoup):
          if request.POST.__contains__('club'):
              clubUserAchivementCreate(rulekey, basescoreup7m, bp.bpcode)
          elif request.POST.__contains__('excel'):
              data = (rulekey, bp.bpcode, basescoreup7m)
              datalist.append(data)
        for i in range(countinvoicebetween5to7M):
          if request.POST.__contains__('club'):
              clubUserAchivementCreate(rulekey, basescoreup4to7m, bp.bpcode)
          elif request.POST.__contains__('excel'):
              data = (rulekey, bp.bpcode, basescoreup4to7m)
              datalist.append(data)

    if request.POST.__contains__('excel'):
        return (exportUserAchivement(request, datalist))


#Rule1.CC quan of inv line
def logicCustomerSKUCount(request):
    rulekey = 'Rule1-CC'
    basescore = request.POST['score']
    datalist = []
    bpq = VwAgentSKUCustomerClub.objects.all()
    for bp in bpq:
        countofsku500k = 0 if bp.countofsku500k == None else bp.countofsku500k

        for i in range(countofsku500k):
          if request.POST.__contains__('club'):
              clubUserAchivementCreate(rulekey, basescore, bp.bpcode)
          elif request.POST.__contains__('excel'):
              data = (rulekey, bp.bpcode, basescore)
              datalist.append(data)

    if request.POST.__contains__('excel'):
        return (exportUserAchivement(request, datalist))


#
def logicVisitorInvSkuCount(request):
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
    TransLogs.objects.create(requestdate= requestdate, ruleid= ruleid, parameterkey= parameterkey, userid= userid, CustomParameter= CustomParameter, status= status)





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
    form = ruleActiceCusForm(initial ={"rulekey": rulekey })
    if request.method == 'GET':
        return render(request, 'agent/index-2.html', {'form': form})


def pageRuleVC3(request):
    rulekey = 'Rule3-VC'
    form = ruleVisitorCoverageForm(initial ={"rulekey": rulekey })
    if request.method == 'GET':
        return render(request, 'agent/index-2.html', {'form': form})



def pageRuleCC1(request):
    rulekey = 'Rule1-CC'
    message = 'شما در حال محاسبه قانون خط فاکتور برای مشتری هستید'
    form = ruleCustomerSKUCount(initial ={"rulekey": rulekey, "message": message })
    if request.method == 'GET':
        return render(request, 'agent/index-2.html', {'form': form, "message": message})


def pageRuleCC2(request):
    rulekey = 'Rule2-CC'
    message = 'شما در حال محاسبه قانون حجم خرید برای مشتری هستید'
    form = ruleCustomerVolumePurchase(initial ={"rulekey": rulekey, "message": message })
    if request.method == 'GET':
        return render(request, 'agent/index-2.html', {'form': form, "message": message})

def pageRuleCC3(request):
    rulekey = 'Rule3-CC'
    message = 'شما در حال محاسبه قانون استمرار خرید برای مشتری هستید'
    form = ruleCustomerFrequencyPurchase(initial ={"rulekey": rulekey })
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
        body = {'filter':{ 'filters' : [ { "Field": "Type", "Value": Type },{ "Field": "RuleId", "Value": RuleId },{ "Field": "UserId", "Value": UserId },
                                         {"Field": "StartDate", "Value": StartDate},{"Field": "EndDate", "Value": EndDate}, {"Field": "CurrentDate", "Value": CurrentDate} ]} }
        newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        res = requests.post(apiUrlGetRuleByKey, json=body, headers=newHeaders,
                            auth=("shahin", "d26da96e2f0d41c2bf75616d38cb24f1429045c950c24acdbb4e0dc59c112721"))
        response = res.json()



