from django.shortcuts import get_object_or_404
from rest_framework import views
from rest_framework import permissions
from .serializers import (
    AllDataSerializer,
    ExperimentSerializer,
    NoteSerializer, 
    PHenologySerializer,
    PhotoSerializer, 
    ProductionSerializer, 
    ProtectSerializer, 
    ResearchGetSerializer,
    UserPasswordChangeSerializer,
    UserSerializer,
    ResearchResponceSerializer
)
from users.models import UserInfo
from .models import (
    AllData, 
    Note, 
    Photo, 
    PhotoMany,
    Plants,
    ProductTypes,
    ProductionMany, 
    Research,
    Production,
    PHenology,
    Protect,
    Experiment,
    NoteMany,
    ExperimentMany
)
from rest_framework.response import Response
from rest_framework import status
import json

class UserPasswordChangeAPIView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request):
        self.object = self.get_object()
        serializer = UserPasswordChangeSerializer(data=request.data)
        user_info_serializer = UserSerializer(request.user)
        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response(
                    {
                        "old_password": ["Wrong password."]
                    },
                    status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(user_info_serializer.data, status=status.HTTP_200_OK)


class AllDataAPIView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]
    def get(self,request):
        all_data = AllData.objects.all()
        note = AllDataSerializer(all_data,many=True).data

        return Response(note,status = status.HTTP_200_OK)
    
    def post(self,request):
        print(request.data)
        all_data ={}
        all_data['all_research']=json.loads(request.data.get('all_research'))
        all_data['all_product']=json.loads(request.data.get('all_product'))
        all_data['all_phenology']=json.loads(request.data.get('all_phenology'))
        all_data['all_protect']=json.loads(request.data.get('all_protect'))
        print(all_data)
        serializer = AllDataSerializer(data=all_data)
        # # print("SER", serializer.data)
        if serializer.is_valid():
        #     print("OK", serializer.validated_data)
            all_research=serializer.data.get('all_research')
            all_product=serializer.data.get('all_product')
            all_phenology=serializer.data.get('all_phenology')
            all_protect = serializer.data.get('all_protect')
            # all_note =serializer.data.get('all_note')
            # all_photo =serializer.data.get('all_photo')
            # all_experiment =serializer.data.get('all_experiment')

            # Research create
            countrys = all_research.pop('country')
            researchz = Research.objects.create(**all_research)
            researchz.created_by = request.user
            for i in countrys:
                researchz.country.add(i)
            researchz.save()
            # Production create
            products = all_product.pop('product')
            productadd = Production.objects.create(**all_product)
            productadd.created_by = request.user
            for product in products:
                plant = Plants.objects.get(id = product.get('product'))
                plant_type = ProductTypes.objects.get(id = product.get('type_product'))
                product_data = ProductionMany.objects.create(product = plant,product_hs_code = product.get('product_hs_code'),type_product =plant_type)
                productadd.product.add(product_data)
            # PHenology create
            
            month_eggss = all_phenology.pop('month_eggs')
            month_larvaa = all_phenology.pop('month_larva')
            month_funguss = all_phenology.pop('month_fungus')
            month_maturee = all_phenology.pop('month_mature')
            month_mm = all_phenology.pop('month_m')
            phenologya = PHenology.objects.create(**all_phenology)
            phenologya.created_by = request.user
            for i in month_larvaa:
                phenologya.month_larva.add(i)
            for i in month_eggss:
                phenologya.month_eggs.add(i)
            for i in month_funguss:
                phenologya.month_fungus.add(i)
            for i in month_maturee:
                phenologya.month_mature.add(i)
            for i in month_mm:
                phenologya.month_m.add(i)
            phenologya.save()
            
            
            #Protect create
            protect = Protect.objects.create(**all_protect)
            protect.created_by = request.user 
            protect.agro_vedio = request.FILES.get('agro_vedio')
            protect.bio_vedio = request.FILES.get('bio_vedio')
            protect.chemistry_vedio = request.FILES.get('chemistry_vedio')
            all_datas = AllData.objects.create(all_research = researchz,all_product = productadd,all_phenology = phenologya,all_protect= protect)
            
            # Create Photo
            photos = Photo.objects.create(all_data=all_datas,created_by= request.user )
            images = request.FILES.getlist('photo')
            for image in images:
                photo_many= PhotoMany.objects.create(photo=image)
                photos.photo.add(photo_many)

            # Create Note
            note_data = Note.objects.create(noteo=all_datas,created_by= request.user) 
            notes = request.FILES.getlist('note')
            for note in notes:
                note_many= NoteMany.objects.create(note=note)
                note_data.note.add(note_many)

            # Experiment create
            experiment_data = Experiment.objects.create(experiments=all_datas, created_by= request.user)
            experiments = request.FILES.getlist('experiment')
            for experiment in experiments:
                experiment_many= ExperimentMany.objects.create(experiment=experiment)
                experiment_data.experiment.add(experiment_many)       

            return Response(AllDataSerializer(all_datas).data,status=status.HTTP_200_OK)
        else:
            return Response({"error": serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        return Response(all_data,status=status.HTTP_200_OK)
            
class ResearchAPIView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        research_data = get_object_or_404(Research.objects.all(), pk=pk)
        return Response(ResearchResponceSerializer(research_data).data,status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        research_data = get_object_or_404(Research.objects.all(), pk=pk)
        data = request.data
        serializer = ResearchGetSerializer(instance=research_data, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            print(request.user)
            research_save = serializer.save()
            research_save.updated_by = request.user
        return Response(ResearchResponceSerializer(research_save).data,status = status.HTTP_201_CREATED)

class ProductionAPIView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        product_data = get_object_or_404(Production.objects.all(), pk=pk)
        return Response(ProductionSerializer(product_data).data,status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        product_data = get_object_or_404(Production.objects.all(), pk=pk)
        data = request.data
        print(request.user)
        serializer = ProductionSerializer(instance=product_data, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            product_save = serializer.save()
            product_save.updated_by = request.user
            if request.data.get('product') is not None:
                product_save.product.clear()
                for product in request.data.get('product'):
                    plant = Plants.objects.get(id = product.get('product'))
                    plant_type = ProductTypes.objects.get(id = product.get('type_product'))
                    product_data = ProductionMany.objects.create(product = plant,product_hs_code = product.get('product_hs_code'),type_product =plant_type)
                    product_save.product.add(product_data)
        return Response(ProductionSerializer(product_save).data,status = status.HTTP_201_CREATED)

class ProtectAPIView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        protect_data = get_object_or_404(Protect.objects.all(), pk=pk)
        return Response(ProtectSerializer(protect_data).data,status=status.HTTP_200_OK)
        
    def put(self, request, pk):
        protect_data = get_object_or_404(Protect.objects.all(), pk=pk)
        data = request.data
        print(bool(request.FILES.get('agro_vedio')))
        serializer = ProtectSerializer(instance=protect_data, data=data, partial=True)
        if serializer.is_valid():
            print(type(request.FILES.get('bio_vedio')))
            protect_save = serializer.save()
            protect_save.updated_by=request.user
            if bool(request.FILES.get('agro_vedio')):   
                protect_save.agro_vedio = request.FILES.get('agro_vedio')
            if bool(request.FILES.get('bio_vedio')):
                protect_save.bio_vedio = request.FILES.get('bio_vedio')
            if bool(request.FILES.get('chemistry_vedio')):
                protect_save.chemistry_vedio = request.FILES.get('chemistry_vedio')
            protect_save.save()
            return Response(ProtectSerializer(protect_save).data,status = status.HTTP_201_CREATED)
        else:
            return Response({"error":serializer.errors},status = status.HTTP_400_BAD_REQUEST)
class PHenologyAPIView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        research_data = get_object_or_404(PHenology.objects.all(), pk=pk)
        return Response(PHenologySerializer(research_data).data,status=status.HTTP_200_OK)
        
    def put(self, request, pk):
        phenology_data = get_object_or_404(PHenology.objects.all(), pk=pk)
        data = request.data
        serializer = PHenologySerializer(instance=phenology_data, data=data, partial=True)
        if serializer.is_valid():
            phenology_save = serializer.save()
            phenology_save.updated_by=request.user
            return Response(PHenologySerializer(phenology_save).data,status = status.HTTP_201_CREATED)
        else:
            return Response({"errors":serializer.errors},status = status.HTTP_400_BAD_REQUEST)

class PhotoUpdateAPIView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        photo_data = get_object_or_404(Photo.objects.all(), pk=pk)
        return Response(PhotoSerializer(photo_data).data,status=status.HTTP_200_OK)
        
    def put(self, request, pk):
       
        photo_data = get_object_or_404(Photo.objects.all(), pk=pk)
        data = request.data
        photos = request.FILES.getlist('photo')
        serializer = PhotoSerializer(instance=photo_data, data=data, partial=True)
        if serializer.is_valid():
            photo_save = serializer.save(name = "image")
            photo_save.updated_by=request.user
            if bool(photos):
                photo_save.photo.clear()
                for photo in photos:
                    image = PhotoMany.objects.create(photo = photo)
                    photo_save.photo.add(image)
            photo_save.save()
            return Response(PhotoSerializer(photo_save).data,status = status.HTTP_201_CREATED)
        else:
            return Response({"errot":serializer.errors.data},status = status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
class NoteUpdateAPIView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        note_data = get_object_or_404(Note.objects.all(), pk=pk)
        return Response(NoteSerializer(note_data).data,status=status.HTTP_200_OK)
        
    def put(self, request, pk):
       
        note_data = get_object_or_404(Note.objects.all(), pk=pk)
        data = request.data
        notes = request.FILES.getlist('note')
        serializer = NoteSerializer(instance=note_data, data=data, partial=True)
        if serializer.is_valid():
            note_save = serializer.save(name="note",updated_by=request.user)
            if bool(notes):
                note_save.note.clear()
                for note in notes:
                    note_da = NoteMany.objects.create(note = note)
                    note_save.note.add(note_da)
            note_save.save()
            return Response(NoteSerializer(note_save).data,status = status.HTTP_201_CREATED)
        else:
            return Response({"errot":serializer.errors.data},status = status.HTTP_400_BAD_REQUEST)
 
class ExperimentUpdateAPIView(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):
        experiment_data = get_object_or_404(Experiment.objects.all(), pk=pk)
        return Response(ExperimentSerializer(experiment_data).data,status=status.HTTP_200_OK)
        
    def put(self, request, pk):
       
        experiment_data = get_object_or_404(Experiment.objects.all(), pk=pk)
        data = request.data
        experiments = request.FILES.getlist('experiment')
        print(bool(experiments))
        serializer = ExperimentSerializer(instance=experiment_data, data=data, partial=True)
        if serializer.is_valid():
            experiment_save = serializer.save(name="experiment",)
            experiment_save.updated_by=request.user
            if bool(experiments):
                experiment_save.experiment.clear()
                for experiment in experiments:
                    experiment_da = ExperimentMany.objects.create(experiment = experiment)
                    experiment_save.experiment.add(experiment_da)
            experiment_save.save()
            return Response(ExperimentSerializer(experiment_save).data,status = status.HTTP_201_CREATED)
        else:
            return Response({"errot":serializer.errors.data},status = status.HTTP_400_BAD_REQUEST)    

class WokrekResult(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        context=[]
        s=1
        users = UserInfo.objects.all()
        for user in users:
            if user.user_role == 1:
                continue
            counts={}
            counts['user'] = user.full_name
            counts['Зарарлирганизм']=Research.objects.filter(created_by=user).count()
            counts['Маҳсулот']= Production.objects.filter(created_by=user).count()
            counts['Фенология']= PHenology.objects.filter(created_by=user).count()
            counts['Қаршикураш']= Protect.objects.filter(created_by=user).count()
            counts['Фото']= Photo.objects.filter(created_by=user).count()
            counts['Қўлёзмалар']=Note.objects.filter(created_by=user).count()
            counts['Тажрибалар'] = Experiment.objects.filter(created_by=user).count()
            counts['Сумма'] = counts['Зарарлирганизм'] + counts['Маҳсулот'] + counts['Қаршикураш']\
                                + counts['Фото'] + counts['Фенология'] + counts['Қўлёзмалар'] + counts['Тажрибалар']
            context.append(counts)
            s+=1
        return Response(context)


class Quarantine(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        context={}
        karantin_true={}
        karantin_false={}
        karantin_all={}
        quarantine_type_true = Research.objects.filter(quarantine_type = '1')
        karantin_true['Karantinsoni'] = quarantine_type_true.count()
        karantin_true['Вирус'] = quarantine_type_true.filter(type='Вирус').count()
        karantin_true['Касаллик'] = quarantine_type_true.filter(type='Касаллик').count()
        karantin_true['Заракунанда'] = quarantine_type_true.filter(type='Заракунанда').count()
        karantin_true['Бегонаўт'] = quarantine_type_true.filter(type='Бегона ўт').count()
        karantin_true['Бактерия'] = quarantine_type_true.filter(type='Бактерия').count()
        context['Karantin']=karantin_true
        quarantine_type_false= Research.objects.filter(quarantine_type = '2')
        karantin_false['Karantinsoni'] = quarantine_type_false.count()
        karantin_false['Вирус'] = quarantine_type_false.filter(type='Вирус').count()
        karantin_false['Касаллик'] = quarantine_type_false.filter(type='Касаллик').count()
        karantin_false['Заракунанда'] = quarantine_type_false.filter(type='Заракунанда').count()
        karantin_false['Бегонаўт'] = quarantine_type_false.filter(type='Бегона ўт').count()
        karantin_false['Бактерия'] = quarantine_type_false.filter(type='Бактерия').count()
        context['Karantinemas']=karantin_false
        karantin_all['Organizm']= karantin_true['Karantinsoni']+karantin_false['Karantinsoni']
        karantin_all['Вирус'] = karantin_true['Вирус']+karantin_false['Вирус']
        karantin_all['Касаллик'] = karantin_true['Касаллик'] + karantin_false['Касаллик']
        karantin_all['Заракунанда'] = karantin_true['Заракунанда']+karantin_false['Заракунанда']
        karantin_all['Бегона'] =karantin_true['Бегонаўт'] + karantin_false['Бегонаўт']
        karantin_all['Бактерия'] = karantin_true['Бактерия'] + karantin_false['Бактерия']
        context['UmumiyKarantin'] = karantin_all
 
        print(quarantine_type_true.count())
        return Response(context)