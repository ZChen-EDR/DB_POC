from django import forms

roleChoices = (('1','dsfdsfds'),('2','sdfsdfdsf'))

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




 
class SingleAccountForm(forms.Form):
   def __init__(self, *args, **kwargs):
        super(SingleAccountForm, self).__init__(*args, **kwargs)
        self.fields['Default_Access_Level'].widget.attrs['readonly'] = True
        #self.fields['isEP'].widget.attrs['readonly'] = True
        #self.fields['allowSign'].widget.attrs['readonly'] = True

   username = forms.CharField(
      label = 'User Name',
      max_length = 100,
      required=True,
      widget=forms.TextInput(attrs={'placeholder':'User Name used for log in'}),
      )
   
   email = forms.EmailField(
      label = 'Email',
      initial = 'zchen1007@gmail.com'
      
   )
   #top
   Default_Access_Level = forms.CharField(max_length = 100)
   Employee_Number = forms.CharField(max_length=100,required = False)
   phone = forms.IntegerField(label='Direct or Cell phone', required = False)
   title = forms.CharField(label = 'Title', required=False)
   #isEP = forms.BooleanField(label ='Environmental Professional(as defined by AAI Rule)', required = False)
   #allowSign = forms.BooleanField(label = 'Allow Administrators to sign for me', required=False)
   firstName = forms.CharField(max_length = 100, label= 'First Name')
   middleInitial = forms.CharField(max_length = 100, label= 'Middle Initial', required = False)
   lastName = forms.CharField(max_length = 100, label = 'Last Name')
   emailClosing = forms.CharField(max_length = 100, label= 'Email Clsing',required = False)
    
   #middle
   addQualification = forms.FileField(label = 'Add Qualifications', required = False)
   addSigniture = forms.FileField(label = 'Add Signiture Image', required = False)
   
   
   #bottom
   accountNumber = forms.CharField(label='Account #', required = False)
   Password = forms.CharField(widget = forms.PasswordInput(),required = False)
   repName = forms.CharField(label = 'Rep.Name', required = False)
   repEmail = forms.EmailField(label ='Rep. Email', required = False)
   
   def clean(self):
        cleaned_data = super(SingleAccountForm, self).clean()
        raise forms.ValidationError(
            "This error was added to show the non field errors styling.")
        return cleaned_data
   

class SingleOfficeForm(forms.Form):
   def __init__(self, *args,**kwargs):
         self.billingContactList = kwargs.pop('billingContactList') 
         super(SingleOfficeForm,self).__init__(*args,**kwargs)
         self.fields['billingContact'].choices = self.billingContactList
         #self.fields['country'] = forms.ChoiceField(choices=COUNTRY_CHOICES)
         #self.fields['state'] = forms.ChoiceField(choices=STATE_CHOICES)

   

   officeName = forms.CharField(max_length = 100,label = 'Office Name')
   address1 = forms.CharField(max_length = 100,label = 'Address')
   address2 = forms.CharField(max_length = 100,label = ' ',required=False)
   country = forms.ChoiceField(label = 'Country',choices=COUNTRY_CHOICES)
   city = forms.CharField(label= 'City', max_length= 100)
   state = forms.ChoiceField(label = 'State/Province',choices = STATE_CHOICES)
   zipcode = forms.CharField(label = 'Zip/Postal Code',max_length = 50 )
   latitude = forms.CharField(label = 'Latitude', required = False)
   longitude = forms.CharField(label = 'Longitude', required = False)
   reGeocode = forms.BooleanField(label = 'Re-geocod on save', required = False)
   phone = forms.CharField(max_length= 100,label = 'Phone',required = False)
   fax = forms.CharField(max_length = 100, label = 'Fax',required = False)
   billingContact = forms.ChoiceField()
   
   
   
   def clean(self):
        cleaned_data = super(SingleOfficeForm, self).clean()
        raise forms.ValidationError(
            "This error was added to show the non field errors styling.")
        return cleaned_data

class SingleCompanyForm(forms.Form):
    def __init__(self,*args,**kwargs):
      self.choices_list = kwargs.pop('choices_list')
      super(SingleCompanyForm,self).__init__(*args,**kwargs)
      self.fields['companyType'].widget.attrs['readonly'] = True
      self.fields['companyComponents'].choices = self.choices_list['companyComponents']
      self.fields['companyCertifications'].choices = self.choices_list['companyCertifications']
      self.fields['companyHeadQuarters'].choices = self.choices_list['companyHeadquarters']
      self.fields['cabinetSetting'].choices = self.choices_list['cabinetSetting']
      self.fields['srfSetting'].choices = self.choices_list['srfSetting']
      
      
    #basic
    companyName = forms.CharField(max_length=100,label='Company Name')
    companyType = forms.CharField(label='Company Type')
    companyComponents = forms.ChoiceField(label='Company Components')
    webAddress = forms.URLField(label='Web Access', required = False)
    slogan = forms.CharField(max_length = 100,label ='Slogan', required = False)
    companyHeadQuarters = forms.ChoiceField(label= 'Company Headquarters',required = False)
    companyCertifications = forms.MultipleChoiceField(label='Company Certifications', required = False)
    billLender = forms.BooleanField(label='Bill Lender',required = False)
    cabinetSetting = forms.ChoiceField(label='Cabinet Settings')
    srfSetting = forms.ChoiceField(label = 'Service Request Settings')
    companyLogo = forms.FileField(label='Upload the Company Logo',required = False)
    
    def clean(self):
        cleaned_data = super(SingleCompanyForm, self).clean()
        raise forms.ValidationError(
            "The cabinetSetting, companyComponents, srfSetting is still static")
        return cleaned_data
    


    


class TestForm(forms.Form):
    def __init__(self, roleChoices, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)
        self.fields['select1'] = forms.ChoiceField(choices=roleChoices)
    """
    Form with a variety of widgets to test bootstrap3 rendering.
    """
    date = forms.DateField(required=False)
    subject = forms.CharField(
        max_length=100,
        help_text='my_help_text',
        required=True,
        widget=forms.TextInput(attrs={'placeholder': 'placeholdertest'}),
    )
    password = forms.CharField(widget=forms.PasswordInput)
    message = forms.CharField(required=False, help_text='<i>my_help_text</i>')
    sender = forms.EmailField(label='Sender ? unicode')
    secret = forms.CharField(initial=42, widget=forms.HiddenInput)
    cc_myself = forms.BooleanField(
        required=False, help_text='You will get a copy in your mailbox.')
    select1 = forms.ChoiceField(choices=roleChoices)
    select2 = forms.MultipleChoiceField(
        choices=roleChoices,
        help_text='Check as many as you like.',
    )
    select3 = forms.ChoiceField(choices=roleChoices)
    select4 = forms.MultipleChoiceField(
        choices=roleChoices,
        help_text='Check as many as you like.',
    )
    category1 = forms.ChoiceField(
        choices=roleChoices, widget=forms.RadioSelect)
    category2 = forms.MultipleChoiceField(
        choices=roleChoices,
        widget=forms.CheckboxSelectMultiple,
        help_text='Check as many as you like.',
    )
    category3 = forms.ChoiceField(
        widget=forms.RadioSelect, choices=roleChoices)
    category4 = forms.MultipleChoiceField(
        choices=roleChoices,
        widget=forms.CheckboxSelectMultiple,
        help_text='Check as many as you like.',
    )
    addon = forms.CharField(
        widget=forms.TextInput(attrs={'addon_before': 'before', 'addon_after': 'after'}),
    )

    required_css_class = 'bootstrap3-req'

    def clean(self):
        cleaned_data = super(TestForm, self).clean()
        raise forms.ValidationError(
            "This error was added to show the non field errors styling.")
        return cleaned_data
      
      
class FilesForm(forms.Form):
    text1 = forms.CharField()
    file1 = forms.FileField()
    file2 = forms.FileField(required=False)
    file3 = forms.FileField(widget=forms.ClearableFileInput)
    file4 = forms.FileField(required=False, widget=forms.ClearableFileInput)