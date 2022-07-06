
from pyexpat import model
from django.contrib.auth.password_validation import validate_password
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.models import UserInfo
from .models import (
    ExperimentMany, 
    NoteMany, 
    PhotoMany, 
    Research,
    PHenology,
    Photo,
    Production,
    ProductTypes,
    Experiment,
    AllData,
    Note,
    Plants,
    Protect,
    ProductionMany,
    Countries,
    Months
)

class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Months
        fields = "__all__"

class PlantsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plants
        fields = ['id','name']


class ProductTypesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypes
        fields = ['id','product']

class ProductTypeManySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypes
        fields = ['product']


class CountriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countries
        fields = ['id','name_ru']

class MonthRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, month):
        return str(month)

    def to_internal_value(self, data):
        return Months.objects.get(id=data)

class ProductRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, product):
        return str(product)

    def to_internal_value(self, data):
        return ProductTypes.objects.get(id=data)


class UserInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['full_name'] 

class PlantsResponceSerializer(ModelSerializer):
    class Meta:
        model = Plants
        fields=['name']


class ProductionManyResponceSerializers(serializers.ModelSerializer):
    product = PlantsResponceSerializer()
    type_product = ProductTypesSerializer()
    class Meta:
        model = ProductionMany
        fields = ['product','product_hs_code','type_product']

class ProductionGetManySerializers(serializers.ModelSerializer):
    # product = PlantsResponceSerializer()
    # type_product = ProductTypeManySerializer()
    class Meta:
        model = ProductionMany
        fields = ['product','product_hs_code','type_product']

class CountryRelatedField(serializers.RelatedField):
    def display_value(self, instance):
        return instance

    def to_representation(self, name_ru):
        return str(name_ru)

    def to_internal_value(self, data):
        return Countries.objects.get(id=data)

class PhotoManySerializers(serializers.ModelSerializer):
    class Meta:
        model = PhotoMany
        fields = ['photo']


class NoteManySerializers(serializers.ModelSerializer):
    class Meta:
        model = NoteMany
        fields = ['note']


class ExperimentManySerializers(serializers.ModelSerializer):
    class Meta:
        model = ExperimentMany
        fields = ['experiment']


class ResearchGetSerializer(ModelSerializer):
    # created_by = UserInfoSerializers()
    # updated_by = UserInfoSerializers()
    class Meta:
        model = Research
        fields=['id','quarantine_type','name_latin','name_uzb','type','description','status','country','confirmation_status','created_by','updated_by']
        extra_kwargs = {
            'quarantine_type': {'required': True},
            'name_latin': {'required': True},
            'name_uzb': {'required': True},
            'type': {'required': True},
            'description': {'required': True},
            'country': {'required': True},
            'status': {'required': False},
            'confirmation_status': {'required': False}
            # 'created_by': {'required': False},
            # 'updated_by': {'required': False}
        }
    def update(self, instance, validated_data):
        instance.quarantine_type = validated_data.get('quarantine_type', instance.quarantine_type)
        instance.name_latin = validated_data.get('name_latin', instance.name_latin)
        instance.name_uzb = validated_data.get('name_uzb', instance.name_uzb)
        instance.type = validated_data.get('type', instance.type)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.confirmation_status = validated_data.get('confirmation_status', instance.confirmation_status)
        if validated_data.get('country') is not None:
            instance.country.clear()
            for country in validated_data.get('country'):
                instance.country.add(country)

        instance.save()
        return instance

class ResearchResponceSerializer(ModelSerializer):
    #country = CountryRelatedField(read_only=True,many=True)
    country = CountriesSerializer(read_only=True,many=True)
    created_by = UserInfoSerializers()
    updated_by = UserInfoSerializers()
    class Meta:
        model = Research
        fields="__all__"
        
# class PHenologyResponceSerializer(ModelSerializer):
#     created_by = UserInfoSerializers()
#     updated_by = UserInfoSerializers()
#     month_eggs = MonthRelatedField(queryset=Months.objects.all(), many=True, required=False)
#     month_larva = MonthRelatedField(queryset=Months.objects.all(), many=True, required=False)
#     month_fungus = MonthRelatedField(queryset=Months.objects.all(), many=True, required=False)
#     month_mature = MonthRelatedField(queryset=Months.objects.all(), many=True, required=False)
#     month_m = MonthRelatedField(queryset=Months.objects.all(), many=True, required=False)
#     class Meta:
#         model = PHenology
#         fields="__all__"
       
        # exclude = ['created_by','updated_by']

class PHenologyResponceSerializer(ModelSerializer):
    created_by = UserInfoSerializers()
    updated_by = UserInfoSerializers()
    month_eggs = MonthSerializer(many=True, required=False)
    month_larva = MonthSerializer(many=True, required=False)
    month_fungus = MonthSerializer(many=True, required=False)
    month_mature = MonthSerializer(many=True, required=False)
    month_m = MonthSerializer(many=True, required=False)
    class Meta:
        model = PHenology
        fields="__all__"
       


class PHenologyGetSerializer(ModelSerializer):
    # created_by = UserInfoSerializers()
    # updated_by = UserInfoSerializers()
    month_eggs = MonthRelatedField(queryset=Months.objects.all(), many=True, required=False)
    month_larva = MonthRelatedField(queryset=Months.objects.all(), many=True, required=False)
    month_fungus = MonthRelatedField(queryset=Months.objects.all(), many=True, required=False)
    month_mature = MonthRelatedField(queryset=Months.objects.all(), many=True, required=False)
    month_m = MonthRelatedField(queryset=Months.objects.all(), many=True, required=False)
    class Meta:
        model = PHenology
        fields="__all__"
        extra_kwargs = {
            'created_by': {'required': False},
            'updated_by': {'required': False}
        }
        # exclude = ['created_by','updated_by']
    def update(self, instance, validated_data):
        instance.pheno_status = validated_data.get('pheno_status', instance.pheno_status)
        """Fenologiyasi"""
        instance.eggs = validated_data.get('eggs', instance.eggs)
        instance.day_eggs = validated_data.get('day_eggs', instance.day_eggs)
        """Lichinka"""
        instance.larva = validated_data.get('larva', instance.larva)
        instance.day_larva = validated_data.get('day_larva', instance.day_larva)
        """G'umbak"""
        instance.fungus = validated_data.get('fungus', instance.fungus)
        instance.day_fungus = validated_data.get('day_fungus', instance.day_fungus)
        """Yetuk Zot"""
        instance.mature = validated_data.get('mature', instance.mature)
        instance.day_mature = validated_data.get('day_mature', instance.day_mature)
        """Ko'payishi"""
        instance.manipulation = validated_data.get('manipulation', instance.manipulation)
        instance.day_m = validated_data.get('day_m', instance.day_m)
        instance.prediction = validated_data.get('prediction', instance.prediction)
        instance.confirmation_status = validated_data.get('confirmation_status', instance.confirmation_status)
        if validated_data.get('month_eggs') is not None or len(validated_data.get('month_eggs')) != 0 :
            instance.month_eggs.clear()
            for eggs in validated_data.get('month_eggs'):
                instance.month_eggs.add(eggs)
        if validated_data.get('month_larva') is not None or len(validated_data.get('month_larva')) != 0:
            instance.month_larva.clear()
            for larva in validated_data.get('month_larva'):
                instance.month_larva.add(larva)
        if validated_data.get('month_fungus') is not None or len(validated_data.get('month_fungus')) != 0:
            instance.month_fungus.clear()
            for fungus in validated_data.get('month_fungus'):
                instance.month_fungus.add(fungus)
        if validated_data.get('month_mature') is not None or len(validated_data.get('month_mature')) != 0:
            instance.month_mature.clear()
            for mature in validated_data.get('month_mature'):
                instance.month_mature.add(mature)
        if validated_data.get('month_m') is not None or len(validated_data.get('month_m')) != 0:
            instance.month_m.clear()
            for month_m in validated_data.get('month_m'):
                instance.month_m.add(month_m)

        instance.save()
        return instance


class PhotoSerializer(ModelSerializer):
    created_by = UserInfoSerializers()
    updated_by = UserInfoSerializers()
    photo = PhotoManySerializers(many=True, required=False,)
    class Meta:
        model = Photo
        fields=["id", "photo",'name','photo_status','confirmation_status','all_data','created_by','updated_by']
        extra_kwargs = {
            'photo_status': {'required': False},
            'confirmation_status': {'required': False},
            'photo': {'required': False},
            'created_by': {'required': False},
            'updated_by': {'required': False}
        }

class ProductionGetSerializer(ModelSerializer):
    product = ProductionGetManySerializers(many=True, required=False)
    class Meta:
        model = Production
        fields="__all__"
        extra_kwargs = {
            'product_status': {'required': False},
            'product': {'required': False},
            'confirmation_status': {'required': False},
            'created_by': {'required': False},
            'updated_by': {'required': False}
        }
    def update(self, instance, validated_data):
        instance.product_status = validated_data.get('product_status', instance.product_status)
        # if validated_data.get('product') is not None:
        #     instance.product.clear()
        #     for producta in validated_data.get('product'):
        #         plant = Plants.objects.get(id = producta.get('product'))
        #         plant_type = ProductTypes.objects.get(id = producta.get('type_product'))
        #         product_data = ProductionMany.objects.create(product = plant,product_hs_code = product.get('product_hs_code'),type_product =plant_type)
        #         instance.product.add(product_data)
        instance.save()
        return instance

class ProductionResponceSerializer(ModelSerializer):
    created_by = UserInfoSerializers()
    updated_by = UserInfoSerializers()
    product = ProductionGetManySerializers(many=True)
    class Meta:
        model = Production
        fields="__all__"

class ProductionResponceSerializer2(ModelSerializer):
    created_by = UserInfoSerializers()
    updated_by = UserInfoSerializers()
    product = ProductionManyResponceSerializers(many=True)
    class Meta:
        model = Production
        fields="__all__"
       


class ProductTypesSerializer(ModelSerializer):
    class Meta:
        model = ProductTypes
        fields="__all__"


class ExperimentSerializer(ModelSerializer):
    created_by = UserInfoSerializers()
    updated_by = UserInfoSerializers()
    experiment = ExperimentManySerializers(many=True, required=False)
    class Meta:
        model = Experiment
        fields="__all__"
        extra_kwargs = {
            'created_by': {'required': False},
            'updated_by': {'required': False}
        }

        # exclude = ['created_by','updated_by']


class NoteSerializer(ModelSerializer):
    created_by = UserInfoSerializers()
    updated_by = UserInfoSerializers()
    note = NoteManySerializers(many=True, required=False)
    class Meta:
        model = Note
        fields="__all__"
        extra_kwargs = {
            'created_by': {'required': False},
            'updated_by': {'required': False}
        }

        # exclude = ['created_by','updated_by']
    def update(self, instance, validated_data):
        instance.note_status = validated_data.get('note_status', instance.note_status)
        instance.confirmation_status = validated_data.get('confirmation_status', instance.confirmation_status)
        instance.save()
        return instance

class PlantsSerializer(ModelSerializer):
    class Meta:
        model = Plants
        fields=['id','name']
        extra_kwargs = {
            'name': {'required': True}
        }

class ProtectGetSerializer(ModelSerializer):
    class Meta:
        model = Protect
        fields="__all__"
        extra_kwargs = {
            'created_by': {'required': False},
            'updated_by': {'required': False}
        }
    def update(self, instance, validated_data):
        instance.protect_status = validated_data.get('protect_status', instance.protect_status)
        instance.agro_protect = validated_data.get('agro_protect', instance.agro_protect)
        instance.bio_protect = validated_data.get('bio_protect', instance.bio_protect)
        instance.chemistry_protect = validated_data.get('chemistry_protect', instance.chemistry_protect)
        instance.confirmation_status = validated_data.get('confirmation_status', instance.confirmation_status)

        instance.save()
        return instance

class ProtectResponceSerializer(ModelSerializer):
    created_by = UserInfoSerializers()
    updated_by = UserInfoSerializers()
    class Meta:
        model = Protect
        fields="__all__"



class AllDataGetSerializer(ModelSerializer):
    all_research = ResearchGetSerializer()
    all_product = ProductionGetSerializer()
    all_phenology = PHenologyGetSerializer()
    all_protect = ProtectGetSerializer()
    photos = PhotoSerializer(source='photes', many=True, read_only=True)
    notes_out = NoteSerializer(source='notes', many=True, read_only=True)
    experiments_out = ExperimentSerializer(source='experiments', many=True, read_only=True)
    
    class Meta:
        model = AllData
        fields="__all__"
        extra_kwargs = {
            'photes': {'required': False},
            'product': {'required': False},
            'notes': {'required': False},
            'experiments': {'required': False}
        }

class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInfo
        fields = ['id', 'username',]


class AllDataResponceSerializer(ModelSerializer):
    all_research = ResearchResponceSerializer()
    all_product = ProductionResponceSerializer()
    all_phenology = PHenologyResponceSerializer()
    all_protect = ProtectResponceSerializer()
    photos = PhotoSerializer(source='photes', many=True, read_only=True)
    notes_out = NoteSerializer(source='notes', many=True, read_only=True)
    experiments_out = ExperimentSerializer(source='experiments', many=True, read_only=True)
    class Meta:
        model = AllData
        fields="__all__"

class AllDataResponceSerializer2(ModelSerializer):
    all_research = ResearchResponceSerializer()
    all_product = ProductionResponceSerializer2()
    all_phenology = PHenologyResponceSerializer()
    all_protect = ProtectResponceSerializer()
    photos = PhotoSerializer(source='photes', many=True, read_only=True)
    notes_out = NoteSerializer(source='notes', many=True, read_only=True)
    experiments_out = ExperimentSerializer(source='experiments', many=True, read_only=True)
    class Meta:
        model = AllData
        fields="__all__"
class ChackManagerSerializer(serializers.Serializer):
    confirmation_status=serializers.BooleanField()
    def update(self, instance, validated_data):
        instance.confirmation_status = validated_data.get('confirmation_status', instance.confirmation_status)
