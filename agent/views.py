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
    Vwvisitorsku, Rules
from .forms import ruleActiceCusForm, ruleVisitorCoverageForm

connectB1 = pymssql.connect("192.168.10.37", "BIAgent", "ABCdef123", "B1-Burux")
conncetReport = pymssql.connect("192.168.10.37", "BIAgent", "ABCdef123", "Reports")
# connectB1 = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER="192.168.10.37";DATABASE="B1-Burux";UID="BIAgent";PWD="ABCdef123"')
apiUrlGetRuleByKey = 'https://gamificatoin-club.burux.ir/default/Rule/PAT_GetByKey'
apiUrlUserAchivementCreate = 'localhost:7000/v1/UserAchivement/PAT_Create'


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


def initVwAgentPurchaseFrequencyCClub(request):
    if request.method == 'GET':
        cursor = conncetReport.cursor()
        OcrdOslp.objects.all().delete()
        sql = "SELECT CardCode,QuarterNum, [Year], Totalprice, CountInvoice,CountInvoice7MtoUp, CountInvoiceBetween5to7M from Burux.VwAgentPurchaseFrequencyCClub where [Year] = 1400 and QuarterNum = 4"
        cursor.execute(sql)
        for bp in cursor:
            ocrd = Ocrd.objects.filter(bpcode=bp[0]).values('id')
            Vwcustomerclub.objects.create(bpcode=bp[0], quarternum=bp[1], year=bp[2], totalprice=bp[3],
                                          countinvoice=bp[4], countinvoice7Mtoup=bp[5], countinvoicebetween5to7=bp[6], ocrd_id=ocrd)
    else:
        pass



def initVwcustomerclub(request):
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


def initVwagentActiveCustomerPerVisitor(request):
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


def clubUserAchivementCreate(rulekey, parameterkey, userid):
    bodygem = {"Ruleid": rulekey, "ParameterKey": parameterkey,
               "UserId": userid,
               "DateTime": datetime.now(), "CustomParameter": []}

    res = requests.post(apiUrlUserAchivementCreate, bodygem)


def clubUserAchivementCreateScore(rulekey, userid, countscore):
    bodyscore = {"Ruleid": rulekey, "ParameterKey": "score", "Count": countscore,
                 "UserId": userid,
                 "DateTime": datetime.now(), "CustomParameter": []}
    res = requests.post(apiUrlUserAchivementCreate, bodyscore)


def logicTry(request, rulekey):
    if request.method == 'GET':
        if rulekey == "Rule1-VC":
            pass
    #       return render(request, 'agent/index-2.html', {'form': form,'message':"salam"})
    elif request.method == 'POST':
        if request.POST['rulekey'] == 'VisitorCustomerCoverage':
            return (logicVisitorCusCoverage(request))
        elif request.POST['rulekey'] == 'VisitorAvticeCustomer':
            return (logicVisitorAvticeCus(request))
        #      elif request.POST['rulekey'] == 'VisitorNewCustomer':
        #           return(logicVisitorNewCus(request))
        elif request.POST['rulekey'] == 'VisitorInvoiceSkuCount':
            return (logicVisitorInvSkuCount(request))


def logicVisitorCusCoverage(request):
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


"""   
def renderRuleFormWoutDate(request):
    if request.method == "GET":
        form = ruleWoDate()
        return render(request, 'agent/index-2.html', {'form': form})

"""


def logicVisitorAvticeCus(request):
    rulekey = 'Rule2.VC'
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
            clubUserAchivementCreateGem(rulekey, vis.slpcode, gemcount)
            clubUserAchivementCreateScore(rulekey, vis.slpcode, scorecount)
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
    rulekey = 'Rule2.VC'
    form = ruleActiceCusForm
    if request.method == 'GET':
        return render(request, 'agent/index-2.html', {'form': form})
    elif request.method == 'POST':
       return(logicVisitorAvticeCus(request))

def pageRuleVC3(request):
    rulekey = 'Rule3.VC'
    form = ruleVisitorCoverageForm
    if request.method == 'GET':
        return render(request, 'agent/index-2.html', {'form': form})
    elif request.method == 'POST':
       return(logicVisitorCusCoverage(request))

