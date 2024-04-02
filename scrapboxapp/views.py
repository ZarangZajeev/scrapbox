from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import View,CreateView,FormView,DetailView,TemplateView,UpdateView,ListView
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from django.contrib import messages

from scrapboxapp.decorators import login_required
from scrapboxapp.forms import RegistrationForm,LoginForm,UserProfileForm,ScrapForm,CategoryForm,BidsForm,ProductSearchForm
from scrapboxapp.models import UserProfile,Scrap,Wishlist,Bids
# Create your views here.

dec=[login_required,never_cache]

class LandingView(TemplateView):
    template_name="landing.html"
    
class SignUpView(CreateView):
    template_name="register.html"
    form_class=RegistrationForm

    def get_success_url(self):
        return reverse("signin")

class SigninView(FormView):
    template_name="login.html"
    form_class=LoginForm

    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            user_obj=authenticate(request,username=uname,password=pwd)
            if user_obj:
                login(request,user_obj)
                print("Login successfully")
                return redirect("index")
        print("Failed to login")
        messages.error(request,"Password or username incorrect")
        return render(request,"login.html",{"form":form})
    
@method_decorator(dec,name="dispatch")
class SignoutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")
    
@method_decorator(dec,name="dispatch")
class IndexView(ListView):
    def get(self,request,*args,**kwargs):
        qs=Scrap.objects.all().exclude(user=request.user)
        wish=Wishlist.objects.get(user=request.user)
        return render(request,"index.html",{"data":qs,"wishlist":wish})

@method_decorator(dec,name="dispatch")
class CategoryAddView(CreateView):
    template_name='category.html'
    form_class=CategoryForm
    def get_success_url(self):
        return reverse("index")

@method_decorator(dec,name="dispatch")
class ScrapAddView(View):
    def get(self,request,*args,**kwargs):
        form=ScrapForm
        return render(request,"scrap_add.html",{'form':form})
    def post(self,request,*args,**kwargs):
        form=ScrapForm(request.POST,files=request.FILES)
        if form.is_valid():
            form.instance.user=request.user
            form.save()
            messages.success(request,"Product added successfully")
            return redirect("index")
        else:
            return render(request,"scrap_add.html",{'form':form})

@method_decorator(dec,name="dispatch")
class ScrapDelateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        Scrap.objects.get(id=id).delete()
        messages.error(request,"Product deleted successfully")
        return redirect("index")

@method_decorator(dec,name="dispatch")
class ProfileUpdateView(UpdateView):
    template_name="profile_edit.html"
    form_class=UserProfileForm
    model=UserProfile

    def get_success_url(self):
        return reverse("index")
    
@method_decorator(dec,name="dispatch")
class ProfileDetailView(DetailView):
    template_name="profile.html"
    model=UserProfile
    context_object_name="data"

@method_decorator(dec,name="dispatch")
class ScrapDetailView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        form=BidsForm()
        qs=Scrap.objects.get(id=id)
        return render(request,"scrap_detail.html",{"data":qs,"form":form})

    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        form=BidsForm(request.POST)
        if form.is_valid():
            form.instance.user_id= request.user.id
            form.instance.scrap_id=id
            form.save()
            messages.success(request,"Bid added")
            return redirect("index")

@method_decorator(dec,name="dispatch")
class ScrapUpdateView(UpdateView):
    template_name="scrap_update.html"
    form_class=ScrapForm
    model=Scrap

    def get_success_url(self):
        return reverse("index")
    
@method_decorator(dec,name="dispatch")
class WishlistAddView(View):
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        scrap_obj=Scrap.objects.get(id=id)
        print(scrap_obj)
        action=request.POST.get("action")

        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        if action == "add":
            wishlist.scrap.add(scrap_obj)
            messages.success(request,"Product added to wishlist")
        elif action == "remove":
            wishlist.scrap.remove(scrap_obj)
            print("removed")
            messages.success(request,"Product Removed from wishlist")
        elif action == "remove_from_wish":
            wishlist.scrap.remove(scrap_obj)
            return redirect("wishlistview")
        return redirect("index")
    
@method_decorator(dec,name="dispatch")
class WishlistView(View):
    def get(self,request,*args,**kwargs):
        qs=Wishlist.objects.get(user_id=request.user.id)
        wishitems=Scrap.objects.exclude(user=request.user)
        return render(request,"wishlist.html",{"data":qs,"items":wishitems})
    
@method_decorator(dec,name="dispatch")
class BidRequestView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Bids.objects.all().filter(user=request.user)
        return render(request,"bid_request.html",{"data":qs})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        qs=Bids.objects.get(id=id)
        action=request.POST.get("action")
        if action=="remove":
            Bids.scrap.remove(qs)
        return redirect("all-bids")
    
@method_decorator(dec,name="dispatch")
class AllBidsView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        data=Scrap.objects.get(id=id)
        qs=Bids.objects.filter(scrap_id=id)
        return render(request,"bids.html",{"data":qs,"scrap":data})
    def post(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        action=request.POST.get("action")
        if action=="accept":
            Bids.objects.filter(id=id).update(status="Accept")
        elif action=="reject":
            Bids.objects.filter(id=id).update(status="Reject")
        return redirect("index")
    
@method_decorator(dec,name="dispatch")
def product_search(request):
    if request.method == "GET":
        form = ProductSearchForm(request.GET)
        if form.is_valid():
            product = form.cleaned_data.get('product')
            desc=form.cleaned_data.get('description')
            products=Scrap.objects.all()
            print(product, desc)

            if product:
                products = Scrap.objects.filter(name__icontains=product)

            if desc:
                products = Scrap.objects.filter(description__icontains=desc)
            print(products)

            if products:
                return render(request, "index.html", {"products": products})
            else:
                error_message = "No products available for this provided name"
                return render(request, "index.html", {"form": form, "error_message": error_message})
        else:
            error_message = "Invalid search criteria"
            return render(request, "index.html", {"form": form, "error_message": error_message})
    else:
        form = ProductSearchForm()
        return render(request, "index.html", {"form": form})
