from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template.context_processors import csrf
from django.template import RequestContext, loader

from django.db import connections
from django import forms
import json
from StringIO import StringIO





#static constant
STATIC_CHOICES_LIST_DATA = {
        
        'companyCertifications' :(
                                  ('1','Woman-Owned Business Enterprise(WBE)'),
                                  ('2','Historically Underutilized Business(HUB)'),
                                  ('3','Disadvantaged Business Enterprise(DBE)'),
                                  ('4','Native American Owned (NAO)'),
                                ),
        'cabinetSetting' : [
            ('1','Open List - All users can add new cabinets'),
            ('2','Close List - Closed List - Only Lender Executive users can add new cabinets'),
            ('3','Single Cabinet - All loan files listed under a single cabinet')
        ],
        'srfSetting' : [
            ('1','New Single Form'),
            ('2','Transaction/Collateral Tabs')
        ]
            
    }


STATE_CHOICES = (
   ('1','AL'),
   ('2','AK'),
   ('3','AZ'),
   ('4','AR'),
   ('5','CA'),
   ('6','CO'),
   ('7','CT'),
   ('8','DE'),
   ('9','FL'),
   ('10','GA'),
   ('11','HI'),
   ('12','ID'),
   ('13','IL'),
   ('14','IN'),
   ('15','IA'),
   ('16','KS'),
   ('17','KY'),
   ('18','LA'),
   ('19','ME'),
   ('20','MD'),
   ('21','MA'),
   ('22','MI'),
   ('23','MN'),
   ('24','MS'),
   ('25','MO'),
   ('26','MT'),
   ('27','NE'),
   ('28','NV'),
   ('29','NH'),
   ('30','NJ'),
   ('31','NM'),
   ('32','NY'),
   ('33','NC'),
   ('34','ND'),
   ('35','OH'),
   ('36','OK'),
   ('37','OR'),
   ('38','PA'),
   ('39','RI'),
   ('40','SC'),
   ('41','SD'),
   ('42','TN'),
   ('43','TX'),
   ('44','UT'),
   ('45','VT'),
   ('46','VA'),
   ('47','WA'),
   ('48','WV'),
   ('49','WI'),
   ('50','WY'),

)

COUNTRY_CHOICES = (
   ('1','United States'),
   ('2','Canada'),
   
)















# Create your views here.


def getCurrentUser(userName):
    
    cursor = connections['CentralAuthenticationService'].cursor()
    
    cursor.execute("select a.AccountID, a.userName, o.Name as officeName, c.Name as companyName from accounts a, offices o, companies c where a.Offices_OfficeID = o.OfficeID and o.Companies_CompanyID = c.CompanyID and a.UserName ='%s'" % userName)

    row = cursor.fetchone()
    
    return row


def getUmbrellaedCompanyIDList(CompanyID):
    
    cursor = connections['CentralAuthenticationService'].cursor()
    
    cursor.execute("select cf.Companies_CompanyID from preferredcompanylists pcl, companyfunctions cf where pcl.UmbrellaCompanyID = %s and pcl.CompanyFunctions_CompanyFunctionID = cf.CompanyFunctionID" % CompanyID)

    row = cursor.fetchall()
    
    return row

def getSetupPackageFees(companyID):
    cursor = connections['CentralAuthenticationService'].cursor()
    cursor.execute("select sp.Name, spf.Cost,spf.Comments,spf.DateEntered,a.FirstName,a.LastName, spf.DateSentToABS ,spf.OrderID from Accounts a, SetupPackageFees spf, SetupPackages sp where a.AccountID = spf.CreatorAID AND spf.SetupPackages_SetupPackageID = sp.SetupPackageID AND spf.OwnerCompanyID = %s" % companyID)
    
    row = cursor.fetchall()
    
    return row

def getUmbrellaedCompany(CompanyID):
    cursor = connections['CentralAuthenticationService'].cursor()
    
    cursor.execute("select c1.Name, c2.Name, f.Name, a.FirstName, a.LastName from Accounts a,PreferredCompanyProjectManagers pcpm, Companies c1, PreferredCompanyLists pcl, CompanyFunctions cf, `Functions` f, Companies c2 where a.AccountID = pcpm.Accounts_AccountID AND pcpm.PreferredCompanyLists_PreferredCompanyListID = pcl.PreferredCompanyListID AND c1.CompanyID = pcl.UmbrellaCompanyID AND pcl.CompanyFunctions_CompanyFunctionID = cf.CompanyFunctionID AND cf.Functions_FunctionID = f.FunctionID AND cf.Companies_CompanyID = c2.CompanyID AND c1.CompanyID = %s" % CompanyID)

    row = cursor.fetchall()
    
    return row

def getChildrenCompanyIDList(CompanyID):
    
    cursor = connections['CentralAuthenticationService'].cursor()
    
    cursor.execute("select c.CompanyID from companies c where c.HoldingCompanyID = '%s'" % (CompanyID))
    
    row = cursor.fetchall()
    
    return row

def getUniqueServiceCategory(companyID):
    cursor = connections['Collateral360'].cursor()
    cursor.execute("select distinct csc.CollateralServiceCategoryID, csc.Name from CompanyReportTypes crt, CollateralServiceCategories csc where crt.CollateralServiceCategories_CollateralServiceCategories = csc.CollateralServiceCategoryID AND crt.OwnerCompanyID = %s" % (companyID))
    row = cursor.fetchall()
    return row

def getCompanyReportType(companyID):
    cursor = connections['Collateral360'].cursor()
    cursor.execute("select CompanyReportTypeID, Value, DisplayName,TemplateNeeded, ShowInProcurement,VendorNeeded,CollateralServiceCategories_CollateralServiceCategories from CompanyReportTypes where OwnerCompanyID = %s" % (companyID))
    row = cursor.fetchall()
    return row


def getCompanies(companyID):
    
    cursor = connections['CentralAuthenticationService'].cursor()
    
    cursor.execute("select Lft from Companies where companyID = %s" % companyID)
    Lft = cursor.fetchone()[0]
    cursor.execute("select Rgt from Companies where companyID = %s" % companyID)
    Rgt = cursor.fetchone()[0]
    try:
        cursor.execute("select CompanyID, Name from Companies where Lft >= %s AND Rgt <= %s" % (Lft,Rgt))
        row = cursor.fetchall()
    except :
        cursor.execute("select CompanyID, Name from Companies where CompanyID = %s" % companyID)

    return row

def getOffices(companyID):
    cursor = connections['CentralAuthenticationService'].cursor()
    cursor.execute("select o.OfficeID, o.Name from offices o where o.Companies_CompanyID = %s " % companyID)
    
    row = cursor.fetchall()
    
    return row



def getAccounts(officeID):

    cursor = connections['CentralAuthenticationService'].cursor()
    cursor.execute("select a.AccountID, a.FirstName, a.LastName  from Accounts a where a.Offices_OfficeID = %s " % officeID)
    
    row = cursor.fetchall()
    
    return row


def getSingleAccount(accountID):
    cursor = connections[connections['CentralAuthenticationService'].cursor()]
    cursor.execute("select a.")

def getSessionUser(request):
    name = request.session['first_name']+" "+request.session['last_name']
    
    current_user = {
        
        'userName' : name,
        'officeName' : request.session['office_name'],
        'companyName' : request.session['company_name'],
        'is_holding_company':request.session['is_holding_company']
        
    }
    return current_user

def getSingleCompany(companyID):
    cursor = connections['CentralAuthenticationService'].cursor()
    cursor.execute("select c.Name,c.CompanyType,c.Website, c.Credo,c.Certifications, c.HeadquarterOfficeID from companies c where c.CompanyID = %s" % (companyID))
    
    row = cursor.fetchone()
    
    return row

def getSingleOffice(officeID):
    cursor = connections['CentralAuthenticationService'].cursor()
    cursor.execute("select o.Name,o.AddressLine1,o.AddressLine2,o.City, o.State, o.Zip, o.Country, o.PhoneNumber, o.Fax, o.BillingContactAccountID from offices o where o.officeID = %s" % officeID)

    row = cursor.fetchone()
    
    return row


def getRoles(app,companyID):
    if app == 'PARCEL':
        cursor = connections['PARCEL_DB_POC'].cursor()
        
        
    elif app == 'Collateral':
        cursor = connections['Collateral360'].cursor()
        cursor.execute("select RoleID,RoleName from CollateralRoles where OwnerCompanyID = 0 or OwnerCompanyID = %s" % companyID)

    row = cursor.fetchall()
    
    return row

def getSingleAccount(accountID):
    cursor = connections['CentralAuthenticationService'].cursor()
    cursor.execute("select UserName,Email,RoleID,EmployeeNumber,CellPhone,Title,FirstName,LastName,MiddleInitial,EmailClosing,Qualifications,ImageSigniture from Accounts where AccountID = %s" % accountID)
    row = cursor.fetchone()
    role_id = row[2]
    cursor_2 = connections['Collateral360'].cursor()
    cursor_2.execute("select Name from CollateralRoles where RoleID = %s" % role_id)
    role_name = cursor_2.fetchone()[0]
    
    row_group = {
        
        'row' : row,
        'role_name':role_name
        
    }
    
    
    return row_group


#view starts here
#company list view

def index(request):
    
    #current_user = request.session['user_name']
    #currentUserInfo = getCurrentUser(current_user)
    
    #print currentUserInfo[1]
    
    
    
    #currentUserInfo = {'userName':request.session,'officeName':currentUserInfo[2], 'companyName':currentUserInfo[3]}
    
    
    #get current info
    currentUserInfo = getSessionUser(request)
    current_company_id = request.session['company_id']
    
    #grab umbrellaed company id list
    
    #is_holding_company = request.session['is_holding_company']
    
    #companyList = getUmbrellaedCompanyIDList(current_company_id)
    #print companyList
    #companyList_where = str(companyList[0][0])
    
    #for index in range(1,len(companyList)):
         
    #     companyList_where = companyList_where+","+str(companyList[index][0])
    
    #companyList_where = companyList_where+','+str(request.session['company_id'])
    
         
    companyList = getCompanies(current_company_id)
    
    
    
    companyListStandard = []
    
    
    for index in range(len(companyList)):
        companyID = str(companyList[index][0])
        companyName = str(companyList[index][1])
        companyDict = {'companyID':companyID,'companyName':companyName}
        
        companyListStandard.append(companyDict)
    
    
    context = RequestContext(request,{
           'currentUserInfo':currentUserInfo,
           'companyListStandard' : companyListStandard
        })
    template = 'AccountMgmt/CompanyList.html'
    
    return render(request,template,context)
    
    
def office_list_view(request, companyID):
    
    #currentUserInfo = getCurrentUser("JC")
    
    #print currentUserInfo[0]
    
    #currentUserInfo = {'userName':currentUserInfo[0],'officeName':currentUserInfo[1], 'companyName':currentUserInfo[2]}
    
    
    currentUserInfo = getSessionUser(request)
    
    
    office_list = getOffices(companyID)
    
    office_list_standard = []
    for index in range(len(office_list)):
        officeID = str(office_list[index][0])
        officeName = str(office_list[index][1])
        office_tuple = {'officeID':officeID,'officeName':officeName}
        office_list_standard.append(office_tuple)
    
    
    
    context = RequestContext(request,{
        
         'currentUserInfo' : currentUserInfo,
         'office_list_standard' : office_list_standard
        
        })
    
    template = 'AccountMgmt/OfficeList.html'
    
    return render(request,template,context)



def account_view(request,companyID,officeID):
    
    #currentUserInfo = getCurrentUser("JC")
    
    #print currentUserInfo[0]
    
    #currentUserInfo = {'userName':currentUserInfo[0],'officeName':currentUserInfo[1], 'companyName':currentUserInfo[2]}
    
    currentUserInfo = getSessionUser(request)
    
    
    
    user_list = getAccounts(officeID)
    
    print user_list
    
    print user_list
    
    user_list_standard = []
    
    for index in range(len(user_list)):
        accountID = str(user_list[index][0])
        firstname = str(user_list[index][1])
        lastname = str(user_list[index][2])
        name = firstname+" "+lastname
        account_tuple = {'accountID':accountID, 'name' : name }
        user_list_standard.append(account_tuple)
        
    context = RequestContext(request,{
        'currentUserInfo':currentUserInfo,
        'user_list_standard':user_list_standard
    })
    template = 'AccountMgmt/AccountList.html'
    return render(request,template,context)




def single_company_view(request,companyID):
    from .form import SingleCompanyForm
    
    currentUserInfo = getSessionUser(request)
    
    company_central = getSingleCompany(companyID)
    
    #print company_central[4]
    #io = StringIO(company_central[3])
    #a = json.load(io)
    #print a
     
    preferredcompanylist = getUmbrellaedCompany(companyID) 
    setupfeelist = getSetupPackageFees(companyID)
    companyreportTypelist = getCompanyReportType(companyID)
    companyCategorylist = getUniqueServiceCategory(companyID)
    
    companyreportTypeDict = {}
    for companyCategory in companyCategorylist:
        companyreportTypeDict[companyCategory[1]]=[]
        for companyreportType in companyreportTypelist:
            if companyreportType[6] == companyCategory[0]:
                companyreportTypeDict[companyCategory[1]].append(companyreportType)
                
    
    #print companyCategorylist
    print  companyreportTypeDict
        
    
    
    certification_list = json.loads(company_central[4])
    print certification_list
    #for index in range(0,companyCertifications.length):
   
    
    
 
    office_init_list = getOffices(companyID)
    #get office list
    companyHeadquarters = []
    companyHeadquarters
    for office in office_init_list:
        companyHeadquarters.append((str(office[0]),office[1]))
    
    #print companyHeadquarters
    choices_list_data = {
        
        'companyComponents' : (('1','Lender Standard Config'),('2','Lender Supreme Config')),
        'companyCertifications' : STATIC_CHOICES_LIST_DATA['companyCertifications'],
        'companyHeadquarters' : companyHeadquarters,
        'cabinetSetting' : STATIC_CHOICES_LIST_DATA['cabinetSetting'],
        'srfSetting' : STATIC_CHOICES_LIST_DATA['srfSetting'],
            
    }
    #print len(certification_list)
    
    certification_choice_list = []
    for index_data in range(0,len(certification_list)):
        for index_list in range(0,len(STATIC_CHOICES_LIST_DATA['companyCertifications'])):
            if certification_list[index_data] in STATIC_CHOICES_LIST_DATA['companyCertifications'][index_list]:
                certification_choice_list.append(int(STATIC_CHOICES_LIST_DATA['companyCertifications'][index_list][0]))
    
    
    #print certification_choice_list
    
    
    
    
    
    
    
       
    form_data = {
        'companyName':company_central[0],
        'companyType':company_central[1],
        'companyCertifications' :certification_choice_list,
        'webAddress':company_central[2],
        'slogan':company_central[3],
        'companyHeadQuarters' : company_central[5],
        'companyComponents':1,
        'cabinetSetting':1,
        'srfSetting':1,
        
    }
    
    print preferredcompanylist[0][1]
    
    form = SingleCompanyForm(form_data,choices_list=choices_list_data,auto_id = False)
    
    context = {
        'currentUserInfo' : currentUserInfo,
        'form':form,
        'preferredCompanyList' : preferredcompanylist,
        'setupfees' :setupfeelist,
        'companyReportList' : companyreportTypelist,
        'companyCategoryList' : companyCategorylist
        
    }
    
    template = 'AccountMgmt/SingleCompany.html'
    return render(request,template,context)

def single_office_view(request,companyID,officeID):
    from .form import SingleOfficeForm
    from .form import STATE_CHOICES
    
    currentUserInfo = getSessionUser(request)
    
    #form building
    billingContactList_data = []
    accounts = getAccounts(officeID)
    for index in range(0,len(accounts)):
        current_tuple = (str(index+1),accounts[index][1]+" "+accounts[index][2])
        billingContactList_data.append(current_tuple)
        
    print billingContactList_data
    
    #data collection
    office_info = getSingleOffice(officeID)
    #print office_info
    
    #o.Name,o.AddressLine1,o.AddressLine2,o.City, o.State, o.Zip, o.Country, o.PhoneNumber, o.Fax, o.BillindgContactAccountID
    
    current_state = office_info[4]
    current_country = office_info[6]
    
    for state in STATE_CHOICES:
        if current_state==state[1]:
            current_state = state[0]
            break
    
    for country in COUNTRY_CHOICES:
        if current_country ==country[1]:
            current_country = country[0]
    
    form_data = {
        
        'officeName':office_info[0],
        'address1':office_info[1],
        'address2':office_info[2],
        'state':int(current_state),
        'city':office_info[3],
        'country':int(current_country),
        'zipcode':office_info[5],
        'phone':office_info[7],
        'fax' : office_info[8],
        'billingContact':int(office_info[9]),
    }
    
    
    
    
    
    
        
    form = SingleOfficeForm(form_data,billingContactList=billingContactList_data,auto_id = False)
    
    
    context={
        'form':form,
        'currentUserInfo':currentUserInfo,
        }
    template = 'AccountMgmt/SingleOffice.html'
    return render(request,template,context)
    
    
    
    
def single_account_view(request, accountID,companyID,officeID):
    from .form import  SingleAccountForm
    from django.forms.forms import BoundField
    
    #build form
    #"select UserName,Email,RoleID,EmployeeNumber,CellPhone,Title,FirstName,LastName,MiddleInitial,EmailClosing,Qualifications,ImageSigniture from Accounts where AccountID =
    account_info = getSingleAccount(accountID)
    
    #print account_info
    
    #take the data
    currentUserInfo = getSessionUser(request)
    form_data = {
        
        'username':account_info['row'][0],
        'email':account_info['row'][1],
        'Default_Access_Level':account_info['role_name'],
        'Employee_Number' : account_info['row'][3],
        'phone' : account_info['row'][4],
        'title':account_info['row'][5],
        'isEP' : False,
        'allowSign' : False,
        'firstName' :account_info['row'][6],
        'lastName': account_info['row'][7],
        'middleInitial':account_info['row'][8],
        'emailClosing' : account_info['row'][9],
        'addQualification':account_info['row'][10],
        'addSigniture' : account_info['row'][11],
    
    }
    
    form  = SingleAccountForm(form_data)
    #non_field = form.fields['Default_Access_Level']
    
    leftFields = [
                    BoundField(form,form.fields['username'],'username'),
                    BoundField(form,form.fields['email'],'email'),
                    BoundField(form,form.fields['Default_Access_Level'],'Default_Access_Level'),
                    BoundField(form,form.fields['Employee_Number'],'Employee_Number'),
                    BoundField(form,form.fields['phone'],'phone'),
                    BoundField(form,form.fields['title'],'title'),
                    #BoundField(form,form.fields['isEP'],'isEP'),
                    #BoundField(form,form.fields['allowSign'],'allowSign'),
                ]
    
    rightFields = [
                    BoundField(form,form.fields['firstName'],'firstName'),
                    BoundField(form,form.fields['middleInitial'],'middleInitial'),
                    BoundField(form,form.fields['lastName'],'lastName'),
                    BoundField(form,form.fields['emailClosing'],'emailClosing'),
    ]
    
    middleFields = [
                    BoundField(form,form.fields['addQualification'],'addQualification'),
                    BoundField(form,form.fields['addSigniture'],'addSigniture'),
                    
    ]
    
    bottomFields = [
                    BoundField(form,form.fields['accountNumber'],'accountNumber'),
                    BoundField(form,form.fields['Password'],'Password'),
                    BoundField(form,form.fields['repName'],'repName'),
                    BoundField(form,form.fields['repEmail'],'repEmail'),
    ]
        
    
    
    
    
    context = {
    'leftFields':leftFields,
    'rightFields' : rightFields,
    'middleFields' : middleFields,
    'bottomFields' : bottomFields,
    'currentUserInfo':currentUserInfo,
    }
    template = "AccountMgmt/SingleAccount.html"
    return render(request,template,context)
  
    
    
    
    
    
