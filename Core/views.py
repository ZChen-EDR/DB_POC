from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
import json

from django.db import connections
def getCurrentUserInfo(request):
    name = request.session['first_name']+" "+request.session['last_name']
    current_user = {
        
        'userName' : name,
        'officeName' : request.session['office_name'],
        'companyName' : request.session['company_name'],
        'is_holding_company':request.session['is_holding_company']

    }
    return current_user

def getCurrentFormTemplate(companyID,formTypeID):
    cursor = connections['Collateral360'].cursor()
    cursor.execute("select CollateralDataFormTemplate from CollateralDataFormTemplates where OwnerCompanyID =%s and CollateralDataFormTypes_CollateralDataFormTypeID = %s and IsCurrent = %s" % (companyID,formTypeID,1))
    
    row = cursor.fetchone()
    return row
    

    
def getCabinet(companyID):
    cursor = connections['Collateral360'].cursor()
    cursor.execute("select CabinetID, Name from Cabinets where OwnerCompanyID = %s" % companyID)
    row = cursor.fetchall()
    return row

def getCompanyReportType(companyID):
    cursor=connections['Collateral360'].cursor()
    cursor.execute("select crt.CompanyReportTypeID, crt.Value, crt.DisplayName, csc.Name from CompanyReportTypes crt, CollateralServiceCategories csc where crt.CollateralServiceCategories_CollateralServiceCategories = csc.CollateralServiceCategoryID and crt.OwnerCompanyID = %s AND crt.showInProcurement = 1 order by csc.Name desc" % (companyID) )
    row = cursor.fetchall()
    return row

def getUniqueReportCategory(companyID):
    cursor=connections['Collateral360'].cursor()
    cursor.execute("select distinct csc.Name from CompanyReportTypes crt, CollateralServiceCategories csc where crt.CollateralServiceCategories_CollateralServiceCategories = csc.CollateralServiceCategoryID and (crt.OwnerCompanyID = %s or crt.OwnerCompanyID = %s) AND crt.showInProcurement = 1 order by csc.Name desc" % (companyID,0) )
    row = cursor.fetchall()
    return row

# Create your views here.
def index(request):
    
    current_user = getCurrentUserInfo(request)
    
    tabs = [
        {
            'Name':'Open',
            'Class':'Active',
            'Columns': ['Cabinet','Loan No','Borrower','Address','State']
        },
        {'Name':'Close'},
        {'Name':'Upcomming Due Dates'},
        {'Name':'Open Bids'},
        {'Name':'Awarded Bids'},
        {'Name':'Accepted Bids'},
        {'Name':'Draf Service Requests'}
    ]
    
    #print a
    context = {
        'currentUserInfo':current_user,
        'tabs':tabs
    }
    template = 'Core/lenderPortal.html'
    return render(request,template,context)



def cabinet(request):
    current_user = getCurrentUserInfo(request)
    
    companyID  = request.session['company_id']
    
    cabinet_raw = getCabinet(companyID)
    
    cabinet_list = []
    
    for cabinet in cabinet_raw:
        current_cabinet = {
            
            'cabinet_id':cabinet[0],
            'cabinet_name':cabinet[1]
            
        }
        cabinet_list.append(current_cabinet)
    
    
    context = {
        'currentUserInfo':current_user,
        'cabinet_list' : cabinet_list
    }
    template = "Core/cabinet_selection.html"

    return render(request,template,context)


def srf(request,cabinetID):
    current_user = getCurrentUserInfo(request)
    
    
    
    template_json = getCurrentFormTemplate(request.session['company_id'],1)[0]
    
    template_dict = json.loads(template_json)
    
    companyReportTypeList = getCompanyReportType(request.session['company_id'])
    
    category_list = getUniqueReportCategory(request.session['company_id'])
    
    fields_array=[]
    field_item={}
    for category in category_list:
        field_item['fieldIdentity'] = category[0]
        field_item['fieldDisplay'] = category[0]
        field_item['fieldType'] = 'multiple'
        field_item['required'] = False
        field_item['field_category'] = 'Service'
        field_item['list'] = []
        for companyReportType in companyReportTypeList:
            current_service_option = {}
            if companyReportType[3] == category[0]:
                current_service_option['fieldIdentity'] = companyReportType[1]
                current_service_option['fieldDisplay'] = companyReportType[2]
                
                field_item['list'].append(current_service_option)
            
        fields_array.append(field_item)
        field_item ={}
    
    
    
    for item in template_dict['Collateral']:
        if item['Table']['tableIdentity'] == "select_services":
            item['Fields'] = fields_array
            
    
    
    collateral_list = []
    transaction_list = []
    invoice_list =[]
    #service_list=[]
    
    for key,value in template_dict.viewitems():
        for item in value:
           if item['Table']['tableIdentity']=="select_services":
               continue
           else:
               for field in item['Fields']:
                if field['field_category']=='Collateral':
                    collateral_list.append(field['fieldIdentity'])
                elif field['field_category']=='loan':
                    transaction_list.append(field['fieldIdentity'])
                elif field['field_category']=='Invoice':
                    invoice_list.append(field['fieldIdentity'])
                   
    #print  collateral_list
    #print  transaction_list
    #print  invoice_list             
    
    
    
    
    context = {
        'currentUserInfo':current_user,
        'column_set':template_dict
    }
        
    
    
    
    if request.POST:
        data_point = request.POST
        transaction_data ={}
        collateral_data={}
        invoice_data={}
        
        
        for transaction in transaction_list:
            transaction_data[transaction] = data_point.get(transaction,"0")
            
        
        for collateral in collateral_list:
            collateral_data[collateral] = data_point.get(collateral,"0")
            
        for invoice in invoice_list:
            invoice_data[invoice] = data_point.get(invoice,"0")
            
        
        transaction_json = json.dumps(transaction_data)
        collateral_json = json.dumps(collateral_data)
        
        print transaction_json
        print collateral_json
        print invoice_data
        
        
        
        #for column in column_set:
        #    data_set[column] = data_point.get(column,"0")
        
        #username = data_point.get("username","0")
        #collateralname = data_point.get("collateralname","0")
        
        #print data_point.get("borrowers_name","0")
        
    template = "Core/srf.html"
    
    return render(request,template,context)
