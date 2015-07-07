

from django.db import models


class Accountaccesslog(models.Model):
    accountaccesslogid = models.BigIntegerField(db_column='AccountAccessLogID', primary_key=True)  # Field name made lowercase.
    accesstimestamp = models.DateTimeField(db_column='AccessTimeStamp', blank=True, null=True)  # Field name made lowercase.
    browser = models.CharField(db_column='Browser', max_length=45, blank=True, null=True)  # Field name made lowercase.
    ip = models.CharField(db_column='IP', max_length=45, blank=True, null=True)  # Field name made lowercase.
    accounts_accountid = models.ForeignKey('Accounts', db_column='Accounts_AccountID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accountaccesslog'


class Accountapplications(models.Model):
    isdeactivated = models.IntegerField(db_column='IsDeactivated')  # Field name made lowercase.
    accounts_accountid = models.ForeignKey('Accounts', db_column='Accounts_AccountID')  # Field name made lowercase.
    applications_applicationid = models.ForeignKey('Applications', db_column='Applications_ApplicationID')  # Field name made lowercase.
    accountapplicationid = models.BigIntegerField(db_column='AccountApplicationID', primary_key=True,blank= True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accountapplications'


class Accounts(models.Model):
    accountid = models.BigIntegerField(db_column='AccountID', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=45, blank=True, null=True)  # Field name made lowercase.
    hintquestion = models.CharField(db_column='HintQuestion', max_length=90, blank=True, null=True)  # Field name made lowercase.
    hintanswer = models.CharField(db_column='HintAnswer', max_length=90, blank=True, null=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    middleinitial = models.CharField(db_column='MiddleInitial', max_length=45, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=45, blank=True, null=True)  # Field name made lowercase.
    qualifications = models.CharField(db_column='Qualifications', max_length=45, blank=True, null=True)  # Field name made lowercase.
    imagesigniture = models.CharField(db_column='ImageSigniture', max_length=45, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=45, blank=True, null=True)  # Field name made lowercase.
    cellphone = models.CharField(db_column='CellPhone', max_length=13, blank=True, null=True)  # Field name made lowercase.
    directphone = models.CharField(db_column='DirectPhone', max_length=13, blank=True, null=True)  # Field name made lowercase.
    extension = models.IntegerField(db_column='Extension', blank=True, null=True)  # Field name made lowercase.
    lastlogindate = models.DateField(db_column='LastLoginDate', blank=True, null=True)  # Field name made lowercase.
    createdbyaccountid = models.BigIntegerField(db_column='CreatedByAccountID')  # Field name made lowercase.
    offices_officeid = models.ForeignKey('Offices', db_column='Offices_OfficeID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'accounts'


class Applications(models.Model):
    applicationid = models.BigIntegerField(db_column='ApplicationID', primary_key=True)  # Field name made lowercase.
    applicationname = models.CharField(db_column='ApplicationName', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'applications'



class Companies(models.Model):
    companyid = models.BigIntegerField(db_column='CompanyID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    website = models.CharField(db_column='Website', max_length=45, blank=True, null=True)  # Field name made lowercase.
    logo = models.CharField(db_column='Logo', max_length=45, blank=True, null=True)  # Field name made lowercase.
    credo = models.CharField(db_column='Credo', max_length=45, blank=True, null=True)  # Field name made lowercase.
    usespda = models.IntegerField(db_column='UsesPDA', blank=True, null=True)  # Field name made lowercase.
    certifications = models.TextField(db_column='Certifications', blank=True, null=True)  # Field name made lowercase.
    companytype = models.CharField(db_column='CompanyType', max_length=45, blank=True, null=True)  # Field name made lowercase.
    isholdingcompany = models.IntegerField(db_column='IsHoldingCompany', blank=True, null=True)  # Field name made lowercase.
    holdingcompanyid = models.ForeignKey('self', db_column='HoldingCompanyID', blank=True, null=True)  # Field name made lowercase.
    headquarterofficeid = models.BigIntegerField(db_column='HeadquarterOfficeID')  # Field name made lowercase.
    entities_entityid = models.ForeignKey('Entities', db_column='Entities_EntityID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'companies'


class Companyapplications(models.Model):
    applications_applicationid = models.ForeignKey(Applications, db_column='Applications_ApplicationID')  # Field name made lowercase.
    companies_companyid = models.ForeignKey(Companies, db_column='Companies_CompanyID')  # Field name made lowercase.
    isdeactivated = models.IntegerField(db_column='IsDeactivated', blank=True, null=True)  # Field name made lowercase.
    companyapplicationid = models.BigIntegerField(db_column='CompanyApplicationID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'companyapplications'
        


class Companyclientcontacts(models.Model):
    companyclientcontactid = models.BigIntegerField(db_column='CompanyClientContactID', primary_key=True)  # Field name made lowercase.
    contact = models.TextField(db_column='Contact', blank=True, null=True)  # Field name made lowercase.
    addedbyaccountid = models.BigIntegerField(db_column='AddedByAccountID', blank=True, null=True)  # Field name made lowercase.
    addedtimestamp = models.DateTimeField(db_column='AddedTimestamp', blank=True, null=True)  # Field name made lowercase.
    companies_companyid = models.ForeignKey(Companies, db_column='Companies_CompanyID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'companyclientcontacts'


class Companyfunctions(models.Model):
    functions_functionid = models.ForeignKey('Functions', db_column='Functions_FunctionID')  # Field name made lowercase.
    companies_companyid = models.ForeignKey(Companies, db_column='Companies_CompanyID')  # Field name made lowercase.
    companyfunctionid = models.BigIntegerField(db_column='CompanyFunctionID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'companyfunctions'


class Companyteams(models.Model):
    companyteamid = models.BigIntegerField(db_column='CompanyTeamID', primary_key=True)  # Field name made lowercase.
    teamname = models.CharField(db_column='TeamName', max_length=45, blank=True, null=True)  # Field name made lowercase.
    creatoraccountid = models.CharField(db_column='CreatorAccountID', max_length=45, blank=True, null=True)  # Field name made lowercase.
    companies_companyid = models.ForeignKey(Companies, db_column='Companies_CompanyID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'companyteams'


class Companyteamusers(models.Model):
    companyteamuserid = models.BigIntegerField(db_column='CompanyTeamUserID', primary_key=True)  # Field name made lowercase.
    companyteams_companyteamid = models.ForeignKey(Companyteams, db_column='CompanyTeams_CompanyTeamID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'companyteamusers'







class Entities(models.Model):
    entityid = models.BigIntegerField(db_column='EntityID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'entities'


class Functions(models.Model):
    functionid = models.IntegerField(db_column='FunctionID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'functions'


class Offices(models.Model):
    officeid = models.BigIntegerField(db_column='OfficeID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=45, blank=True, null=True)  # Field name made lowercase.
    addressline1 = models.CharField(db_column='AddressLine1', max_length=45, blank=True, null=True)  # Field name made lowercase.
    addressline2 = models.CharField(db_column='AddressLine2', max_length=45, blank=True, null=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=45, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=2, blank=True, null=True)  # Field name made lowercase.
    zip = models.IntegerField(db_column='Zip', blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='Country', max_length=45, blank=True, null=True)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=13, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='Fax', max_length=13, blank=True, null=True)  # Field name made lowercase.
    latitude = models.DecimalField(db_column='Latitude', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    longitude = models.DecimalField(db_column='Longitude', max_digits=10, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    isdeactivated = models.IntegerField(db_column='IsDeactivated', blank=True, null=True)  # Field name made lowercase.
    companies_companyid = models.ForeignKey(Companies, db_column='Companies_CompanyID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'offices'


class Preferredcompanylists(models.Model):
    preferredcompanylistid = models.IntegerField(db_column='PreferredCompanyListID', primary_key=True)  # Field name made lowercase.
    companyfunctions_companyfunctionid = models.ForeignKey(Companyfunctions, db_column='CompanyFunctions_CompanyFunctionID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'preferredcompanylists'


class Preferredcompanyprojectmanagers(models.Model):
    isprimary = models.IntegerField(db_column='IsPrimary')  # Field name made lowercase.
    preferredcompanylists_preferredcompanylistid = models.ForeignKey(Preferredcompanylists, db_column='PreferredCompanyLists_PreferredCompanyListID')  # Field name made lowercase.
    accounts_accountid = models.ForeignKey(Accounts, db_column='Accounts_AccountID')  # Field name made lowercase.
    preferredcompanyprojectmanagerid = models.CharField(db_column='PreferredCompanyProjectManagerID', primary_key=True, max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'preferredcompanyprojectmanagers'
