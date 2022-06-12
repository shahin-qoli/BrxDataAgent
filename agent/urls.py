from django.contrib import admin
from django.urls import path
from . import views


app_name = 'agent'
urlpatterns = [
    ###neccessary INITISLIZE
    path('init/oslp', views.initOslp, name='initoslp'),
    path('init/ocrd', views.initOcrd, name='initocrd'),
    path('init/ordr', views.initOrdr, name='initordr'),
    path('init/vwAgentpurchasefrequencycclub', views.initVwAgentPurchaseFrequencyCClub, name='initvwAgentpurchasefrequencycclub'),
    path('init/VwAgentSKUCustomerClub', views.initVwAgentSKUCustomerClub, name='initVwAgentSKUCustomerClub'),

    path('init/ocrdoslp', views.initOcrdOslp, name='initocrdoslp'),
    path('init/vwvisitorsku', views.iniVwvisitorsku, name='iniVwvisitorsku'),
    path('init/newcustomer', views.initNewCustomer, name='initnewcustomer'),
    ### logics
    path('logic/try', views.logicTry, name='logicTry'),
    path('logic/try/visitoractivecustomer', views.pageRuleVC2, name='logicTryActiveCustomer'),
    path('logic/try/visitorcuscoverage', views.pageRuleVC3, name='logicTryVisitorCusCoverage'),
    path('logic/try/customerskucount', views.pageRuleCC1, name='logicTryCustomerSKUCount'),
    path('logic/try/customervolumepurchase', views.pageRuleCC2, name='logicTryCustomerVolumePurchase'),
    path('logic/try/customerfrequencypurchase', views.pageRuleCC3, name='logicTryCustomerFrequencyPurchase'),


    ### no need for now
#    path('init/VwagentActiveCustomerPerVisitor', views.initVwagentActiveCustomerPerVisitor,
#         name='VwagentActiveCustomerPerVisitor'),
    path('handle/newcustomer', views.handleNewCustomer, name='handlenewcustomer'),
#    path('logic/try/<str:rulekey>/', views.logicTry, name='logicTry'),
#    path('logic/VisitorAvticeCus', views.logicVisitorAvticeCus, name='logicVisitorAvticeCus'),
#    path('logic/VisitorNewCus', views.logicVisitorNewCus, name='logicVisitorNewCus'),
#    path('logic/VisitorInvSkuCount', views.logicVisitorInvSkuCount, name='logicVisitorInvSkuCount'),
#    path('club/getruleparams', views.clubGetRuleParams, name='clubGetRuleParams'),
    path('', views.pageIndex, name='agentindex'),
    path('report/', views.testclubUserAchivementCreate, name='test'),

   ]