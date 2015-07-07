from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

from django.db import connections

# Create your views here.

from .forms import NameForm
from .models import Accounts, Accountapplications,Applications, Companies, Companyapplications, Offices 


def authenticate_query(name,app):
    
    cursor = connections['CentralAuthenticationService'].cursor()
    
    
    cursor.execute("select c.CompanyID from accounts a, offices o, companies c where a.Offices_OfficeID = o.OfficeID and o.Companies_CompanyID = c.CompanyID and a.UserName = '%s'" % name)
    
    companyID = int(cursor.fetchone()[0])
    
    
    cursor.execute("select ap.IsDeactivated from companies c, companyapplications ap, applications app where c.CompanyID = ap.Companies_CompanyID and ap.Applications_ApplicationID = app.ApplicationID and app.ApplicationName = '%s' and c.CompanyID = %d" % (app,companyID))
    
    activeCompany = cursor.fetchone()
    
    if activeCompany:
        cursor.execute("select aa.IsDeactivated from centralauthenticationservice_db_poc.accounts a, centralauthenticationservice_db_poc.accountapplications aa, centralauthenticationservice_db_poc.applications app where a.UserName = '%s' AND a.AccountID = aa.Accounts_AccountID AND app.ApplicationID = aa.Applications_ApplicationID AND app.ApplicationName ='%s'" % (name,app))
        active = cursor.fetchone()
        if active[0]==0:
            activeAccount = True
        else:
            activeAccount = False
    
        return activeAccount
    
    else:
        
        return False



def get_relevent_information(user_name):
    cursor = connections['CentralAuthenticationService'].cursor()
    cursor.execute("select ca.AccountID,ca.FirstName,ca.LastName, co.OfficeID, co.Name, cc.CompanyID, cc.Name, cc.IsHoldingCompany from centralauthenticationservice_db_poc.accounts ca,centralauthenticationservice_db_poc.offices co,centralauthenticationservice_db_poc.companies cc where ca.Offices_OfficeID = co.OfficeID AND co.Companies_CompanyID = cc.CompanyID AND ca.UserName ='%s' " % (user_name))
    #print user_name
    row = cursor.fetchone()
    return row




def index(request):
    
    
    
    if request.method =='POST':
        form = NameForm(request.POST)
        if form.is_valid():
            
            name = form.cleaned_data['user_name']
           
            valid = authenticate_query(name,'Collateral360')
            if valid:
                user_info = get_relevent_information(name)
                #print user_info
                request.session['user_id'] = user_info[0]
                request.session['first_name'] = user_info[1]
                request.session['last_name'] = user_info[2]
                request.session['office_id'] = user_info[3]
                request.session['office_name'] = user_info[4]
                request.session['company_id'] = user_info[5]
                request.session['company_name'] = user_info[6]
                request.session['is_holding_company'] = user_info[7]
                
                
                
                return HttpResponseRedirect('/Core')
    context = {}    
    return render(request,'Authentication/sign_in3.html',context)











        
