from django.contrib import admin
from django.urls import path
from . import views


app_name = 'agent'
urlpatterns = [
    path('init/oslp', views.initOslp, name='initoslp'),
    path('init/ocrd', views.initOcrd, name='initocrd'),
    path('init/ordr', views.initOrdr, name='initordr'),
    path('init/vwAgentpurchasefrequencycclub', views.initVwAgentPurchaseFrequencyCClub, name='initvwAgentpurchasefrequencycclub'),
    path('init/vwcustomerclub', views.initVwcustomerclub, name='initvwcustomerclub'),
    path('init/vwvisitorsku', views.iniVwvisitorsku, name='iniVwvisitorsku'),
    path('init/newcustomer', views.initNewCustomer, name='initnewcustomer'),
    path('init/VwagentActiveCustomerPerVisitor', views.initVwagentActiveCustomerPerVisitor, name='VwagentActiveCustomerPerVisitor'),
    path('init/ocrdoslp', views.initOcrdOslp, name='initocrdoslp'),
    path('handle/newcustomer', views.handleNewCustomer, name='handlenewcustomer'),
#    path('logic/try/<str:rulekey>/', views.logicTry, name='logicTry'),
    path('logic/try/visitoractivecustomer', views.pageRuleVC2, name='logicTryActiveCustomer'),
    path('logic/try/visitorcuscoverage', views.pageRuleVC3, name='logicTryVisitorCusCoverage'),
    path('logic/VisitorAvticeCus', views.logicVisitorAvticeCus, name='logicVisitorAvticeCus'),
#    path('logic/VisitorNewCus', views.logicVisitorNewCus, name='logicVisitorNewCus'),
    path('logic/VisitorInvSkuCount', views.logicVisitorInvSkuCount, name='logicVisitorInvSkuCount'),
#    path('club/getruleparams', views.clubGetRuleParams, name='clubGetRuleParams'),
    path('', views.pageIndex, name='agentindex'),

   ]