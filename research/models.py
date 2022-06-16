
from users.models import UserInfo
from django.db import models
from django.utils.translation import gettext_lazy as _




# from .managers import UserManager


class MonthChoice(models.IntegerChoices):
    January = 1, 'January'
    February = 2, 'February'
    March = 3, 'March'
    April = 4, 'April'
    May = 5, 'May'
    June = 6, 'June'
    July = 7, 'July'
    August = 8, 'August'
    September = 9, 'September'
    October = 10, 'October'
    November = 11, 'November'
    December = 12, 'December'


MONTHS = (
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
)

TYPE_CHOICES = (
    ('1', 'Yes'),
    ('2', 'No')
)


class UserRoles(models.IntegerChoices):
    Managers = 1, 'Managers'
    WORKER = 2, 'WORKER'



class BaseModel(models.Model):
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_time = models.DateTimeField(auto_now_add=False, auto_now=True)
    created_by = models.ForeignKey(UserInfo, related_name='created_%(model_name)s', null=True, on_delete=models.SET_NULL)
    updated_by = models.ForeignKey(UserInfo, related_name='updated_%(model_name)s', null=True, on_delete=models.SET_NULL)

    class Meta:
        abstract = True
        ordering = ('id',)
        get_latest_by = 'created_time'


class Countries(models.Model):
    name_ru = models.CharField(max_length=100, verbose_name='country')

    class Meta:
        verbose_name_plural = 'Countries'
        db_table = 'country'

    def __str__(self):
        return self.name_ru


class ProductTypes(models.Model):
    product = models.CharField(max_length=100, verbose_name='product type')

    class Meta:
        verbose_name_plural = 'Product Types'
        db_table = 'product type'


class Months(models.Model):
    month = models.CharField(max_length=100, verbose_name='months', blank=True)

    class Meta:
        verbose_name_plural = 'Months'
        db_table = 'month'

    def __str__(self):
        return self.month


class Research(BaseModel):
    """ Zararli organizm """
    quarantine_type = models.CharField(choices=TYPE_CHOICES, blank=True, max_length=10)
    name_latin = models.CharField(max_length=25, blank=True, null=True,unique=True,verbose_name='Латинское названи')
    name_uzb = models.CharField(max_length=25, blank=True, null=True)
    type = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    country = models.ManyToManyField(Countries, blank=True, verbose_name='Countries+')
    status = models.BooleanField(default=False)
    confirmation_status = models.BooleanField(default=False)


    class Meta:
        verbose_name = _('Research')
        verbose_name_plural = _('Research')
        default_permissions = ()


class PHenology(BaseModel):
    # phenology = models.ForeignKey('AllData', on_delete=models.CASCADE, null=True, 
    #                                 related_name='phenology', related_query_name='phenology')
    pheno_status = models.BooleanField(default=False, blank=False)
    """Fenologiyasi"""
    eggs = models.TextField(null=True)
    month_eggs = models.ManyToManyField(Months, blank=True, verbose_name='Month of eggs+')
    day_eggs = models.TextField(max_length=100, blank=True, null=True)
  
    """Lichinka"""
    larva = models.TextField(blank=True, null=True)
    month_larva = models.ManyToManyField(Months, blank=True, related_name='Month of larva+')
    day_larva = models.TextField(max_length=100, blank=True, null=True)
 
    """G'umbak"""
    fungus = models.TextField(blank=True, null=True)
    month_fungus = models.ManyToManyField(Months, blank=True, related_name='Month of fungus+')
    day_fungus = models.TextField(max_length=100, blank=True, null=True)

    """Yetuk Zot"""
    mature = models.TextField(blank=True, null=True)
    month_mature = models.ManyToManyField(Months, blank=True, related_name='Month of mature+')
    day_mature = models.TextField(max_length=100, blank=True, null=True)

    """Ko'payishi"""
    manipulation = models.TextField(blank=True, null=True)
    month_m = models.ManyToManyField(Months, blank=True, related_name='Month of manipulation+')
    day_m = models.TextField(max_length=100, blank=True, null=True)
    prediction = models.TextField(blank=True, null=True)
    confirmation_status = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Phenology detail')
        verbose_name_plural = _('Phenology details')
        db_table = 'PHenology'

class ProductionMany(models.Model):
    product = models.ForeignKey('Plants',on_delete=models.CASCADE, blank=True, verbose_name='Plants+')
    product_hs_code = models.CharField(max_length=15, blank=True, null=True, verbose_name='KOD TN ved')
    type_product = models.ForeignKey(ProductTypes,on_delete=models.CASCADE, blank=True, related_name='Product types+')
    

    def __str__(self):
        return self.product_hs_code

class Production(BaseModel):
    product_status = models.BooleanField(default=False)
    product = models.ManyToManyField(ProductionMany, blank=True, verbose_name='Plants+')
    confirmation_status = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')
        db_table = 'Production'
    
    # def __str__(self):
    #     return self.product_hs_code

class Protect(BaseModel):
   
    protect_status = models.BooleanField(default=False)
    agro_protect = models.CharField(max_length=255, null=True, blank=True)
    agro_vedio = models.FileField(upload_to="agro_vedio/",null=True,blank=True)
    bio_protect = models.CharField(max_length=255, null=True, blank=True)
    bio_vedio = models.FileField(upload_to="bio_vedio/",null=True,blank=True)
    chemistry_protect = models.CharField(max_length=255, null=True, blank=True)
    chemistry_vedio = models.FileField(upload_to="chemistry_vedio/",null=True,blank=True)
    confirmation_status = models.BooleanField(default=False)
    class Meta:
        verbose_name = _('Protection result')
        verbose_name_plural = _('Protection results')
        db_table = 'protect'

        
class PhotoMany(models.Model):
    name = models.CharField(max_length=50,default="image")
    photo = models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d')


class NoteMany(models.Model):
    name = models.CharField(max_length=50,default="note")
    note = models.FileField(blank=True, null=True, upload_to='notes/%Y/%m/%d')

class ExperimentMany(models.Model):
    name = models.CharField(max_length=50,default="experiment")
    experiment = models.FileField(blank=True, null=True, upload_to='experiments/%Y/%m/%d')


class Photo(BaseModel):
    name = models.CharField(max_length=100, blank=True)
    photo = models.ManyToManyField(PhotoMany,blank=True,related_name="photo_new")

    all_data = models.ForeignKey('AllData', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='photes',)
    photo_status = models.BooleanField(default=False)
    confirmation_status = models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.photo.url)
   

class Note(BaseModel):
    name = models.CharField(max_length=100, blank=True)
    note = models.ManyToManyField(NoteMany,blank=True,related_name="note_new")

    noteo = models.ForeignKey('AllData', on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='notes', )
    note_status = models.BooleanField(default=False)
    confirmation_status = models.BooleanField(default=False)
 

class Experiment(BaseModel):
    name = models.CharField(max_length=100, blank=True)
    experiment = models.ManyToManyField(ExperimentMany,blank=True,related_name="experiment_new")

    experiments = models.ForeignKey('AllData', on_delete=models.CASCADE, null=True,blank=True,
                                    related_name='experiments', related_query_name='experiments')
    experiment_status = models.BooleanField(default=False)
    confirmation_status = models.BooleanField(default=False)

class Plants(models.Model):
    name = models.CharField(max_length = 300, default = '')
    type = models.CharField(max_length = 300, default = '')
    add_data = models.DateField(auto_now_add = True)

    def __str__(self):
        return self.name


class AllData(models.Model):
    all_research = models.ForeignKey(Research,verbose_name="Zararli organizm",on_delete=models.CASCADE,related_name="all_research")
    all_product = models.ForeignKey(Production,verbose_name="Maxsulot",related_name="all_product",on_delete=models.CASCADE)
    all_phenology = models.ForeignKey(PHenology,verbose_name="PHenology",related_name='all_phenology',on_delete=models.CASCADE)
    all_protect = models.ForeignKey(Protect,verbose_name='Qarshi kurash',related_name='all_protect',on_delete=models.CASCADE)
    # all_photo = models.ManyToManyField(Photo,verbose_name='Rasm',related_name='all_photo',)
    # all_note = models.ManyToManyField(Note,verbose_name="Qolyozma",related_name="all_note",)
    # all_experiment = models.ManyToManyField(Experiment,verbose_name='Tajribalar',related_name='all_experiment',)
    created_time = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_time = models.DateTimeField(auto_now_add=False, auto_now=True)

    