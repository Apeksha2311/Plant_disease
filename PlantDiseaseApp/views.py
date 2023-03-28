from django.shortcuts import render,redirect

from django.views import View

from .forms import RegisterForm , LoginForm , ImageForm

from django.contrib.auth import authenticate,login,logout

from .models import CategoryModel,ImageModel

from django.contrib import messages


# Create your views here.

def signout_view(request):
    logout(request)
    messages.success(request , 'Successfully LogOut..')

    return redirect('home')


class home_view(View):
    
    def get(self , request):

        if request.user.is_authenticated:
            return redirect('gallery')

        forms = LoginForm()
        context = {'forms':forms}
        return render(request , 'home.html' , context)

    def post(self , request):

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username = username , password = password)

        if user is not None:
            login(request , user)
            messages.success(request , 'Successfully LogIn..')


            return redirect('gallery')

        return redirect('home')


class register_view(View):
    def get(self , request):

        if request.user.is_authenticated:
            return redirect('gallery')

        forms = RegisterForm()
        context = {'forms':forms}

        return render(request , 'register.html' , context)

    def post(self , request):

        forms = RegisterForm(request.POST)
        if forms.is_valid():
            forms.save()

            return redirect('home')

        context = {'forms':forms}
        return render(request , 'register.html' , context)

class gallery_view(View):
    def get(self , request):
        category = CategoryModel.objects.all()
        Images = ImageModel.objects.all()

        context = {'category':category , 'Images':Images}
        return render(request , 'gallery.html',context)

    def post(self , request):
        return render(request , 'gallery.html')
        # return redirect('gallery')

class Cat_view(View):
    def get(self , request ,id):
        Images = ImageModel.objects.filter(cat = id)
        category = CategoryModel.objects.all()

        context = {'category':category , 'Images':Images}
        return render(request , 'gallery.html',context)



class myupload_view(View) :
    def get(self ,request):
        Images =ImageModel.objects.filter(uploaded_by = request.user)
        context = {'Images':Images}
        return render(request , 'myupload.html',context)   



class addimage_view(View):
    def get(self , request):
        forms = ImageForm()
        context = {'forms':forms}
        if not request.user.is_authenticated:
            return redirect('home')

        
        return render(request , 'addimage.html',context)

    def post(self , request):
        img = request.FILES['image']
        print(type(img))
         #convert the file to bytes
        # finaleimg = img.read()
        # print(type(finaleimg))
        forms = ImageForm(request.POST , request.FILES)

        top1 = '1. Species: %s, Status: %s, Probability: %.4f'%('Tomato','late blight',0.7)
        top2 = '2. Species: %s, Status: %s, Probability: %.4f'%('apple','healthy',0.1)
        top3 = '3. Species: %s, Status: %s, Probability: %.4f'%('chikoo','healthy',00.5)

        predictions = [ { 'pred':top1 }, { 'pred':top2 }, { 'pred':top3 } ]
        print(predictions)

        if forms.is_valid():
            task = forms.save(commit=False)
            task.uploaded_by = request.user
            task.save()
            messages.success(request , 'Image is Added Successfully..')
            return redirect('gallery')
        if not request.user.is_authenticated:
            return redirect('home')
        return render(request , 'addimage.html')
            

#    create view for single view img 
def view_image(request,image_id):
    image = ImageModel.objects.get(id=image_id)
    context = {'image': image}
    return render(request, 'image.html', context)           