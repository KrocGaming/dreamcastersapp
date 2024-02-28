from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
from .filters import *
from .forms import *
from django.utils.decorators import method_decorator
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.contrib import messages
from datetime import timedelta

def error_404(request, exception):
    return render(request, '404.html')

def index(request):
    return render(request, 'index/index.html')

def loginpage(request):
    if request.user.is_authenticated:
        return redirect('dashboardpage')

    form = LoginForm(request.POST or None)
    msg = None

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboardpage')
            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating the form'
    return render(request, "accounts/auth-signin.html", {"form": form, "msg": msg})


def logoutuser(request):
    logout(request)
    return redirect('loginpage')

@login_required
def dashboardpage(request):
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    yesterday_start = today_start - timedelta(days=1)
    this_month_start = today_start.replace(day=1)
    this_year_start = today_start.replace(month=1, day=1)

    all_today = CustomerEnqiuery.objects.filter(
        created_on__gte=today_start,
        created_on__lt=today_start + timedelta(days=1),
    ).order_by('-created_on')

    all_today_accepted = CustomerEnqiuery.objects.filter(
        created_on__gte=today_start,
        created_on__lt=today_start + timedelta(days=1),
        accepted="Accepted"
    ).order_by('-created_on')

    all_yesterday = CustomerEnqiuery.objects.filter(
        created_on__gte=yesterday_start,
        created_on__lt=today_start,
    ).order_by('-created_on')

    all_yesterday_accepted = CustomerEnqiuery.objects.filter(
        created_on__gte=yesterday_start,
        created_on__lt=today_start,
        accepted="Accepted"
    ).order_by('-created_on')

    all_this_month = CustomerEnqiuery.objects.filter(
        created_on__gte=this_month_start,
        created_on__lt=today_start + timedelta(days=1),
    ).order_by('-created_on')

    all_this_month_accepted = CustomerEnqiuery.objects.filter(
        created_on__gte=this_month_start,
        created_on__lt=today_start + timedelta(days=1),
        accepted="Accepted"
    ).order_by('-created_on')

    all_this_year = CustomerEnqiuery.objects.filter(
        created_on__gte=this_year_start,
        created_on__lt=today_start + timedelta(days=1),
    ).order_by('-created_on')

    all_this_year_accepted = CustomerEnqiuery.objects.filter(
        created_on__gte=this_year_start,
        created_on__lt=today_start + timedelta(days=1),
         accepted="Accepted"
    ).order_by('-created_on')


    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # today_start = timezone.now().date()

    all = CustomerEnqiuery.objects.filter(
        created_on__gte=today_start,
        status__isnull=True
    ).order_by('-created_on')

    context = {
        'all': all,
        'count_today': all_today.count(),
        'count_today_accepted': all_today_accepted.count(),
        'count_yesterday': all_yesterday.count(),
        'count_yesterday_accepted': all_yesterday_accepted.count(),
        'count_this_month': all_this_month.count(),
        'count_this_month_accepted': all_this_month_accepted.count(),
        'count_this_year': all_this_year.count(),
        'count_this_year_accepted': all_this_year_accepted.count(),
    }
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def alllist(request):
    all = CustomerEnqiuery.objects.all().order_by('-created_on')
    context = {
        'all':all
    }
    return render(request, 'all/alllist.html',context)


class CustomerEnqInline():
    form_class = CustomerEnquireForm
    model = CustomerEnqiuery
    template_name = "all/addenq.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('alllist')


class CustomerEnqCreate(CustomerEnqInline, CreateView):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ctx = super(CustomerEnqCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                
            }
        else:
            return {
               
            }

   
class CustomerEnqUpdate(CustomerEnqInline, UpdateView):
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(CustomerEnqUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            
        }
    


@login_required
def CustomerEnqView(request,pk):
    all = get_object_or_404(CustomerEnqiuery,id=pk)
    print(all)
    context = {
        'all':all
    }
    return render(request, 'all/viewenq.html',context)

@login_required
def CustomerEnqStatPro(request, pk):
    customer_enquiry = get_object_or_404(CustomerEnqiuery, id=pk)

    if customer_enquiry.accepted == "Accepted":
        # Display a message indicating that it's already accepted
        messages.warning(request, 'This enquiry is already accepted.')
    else:
        # Proceed with the update
        userid = get_object_or_404(User, id=request.user.id)
        customer_enquiry.accepted = "Accepted"
        statusid = get_object_or_404(Status, id=1)
        customer_enquiry.status = statusid
        customer_enquiry.user = userid
        customer_enquiry.save()
        messages.success(request, 'Enquiry accepted successfully.')

    return redirect('alllist')




@login_required
def processinglist(request):
    all = CustomerEnqiuery.objects.filter(status__id=1).order_by('-created_on')
    context = {
        'all':all
    }
    return render(request, 'processing/processinglist.html',context)

 
@login_required
def view_customerenqprocess(request,pk):
    all = get_object_or_404(CustomerEnqiuery,id=pk)
    print(all)
    context = {
        'all':all
    }
    return render(request, 'processing/viewprocessenq.html',context)

@login_required
def changefollowup_customerenq(request, pk):
    customer_enquiry = get_object_or_404(CustomerEnqiuery, id=pk)
    statusid = get_object_or_404(Status, id=2)
    customer_enquiry.status = statusid
    customer_enquiry.save()
    return redirect('processing-list')



@login_required
def followuplist(request):
    all = CustomerEnqiuery.objects.filter(status__id=2).order_by('-created_on')
    context = {
        'all':all
    }
    return render(request, 'followup/followuplist.html',context)

 
@login_required
def view_customerenqfollow(request,pk):
    all = get_object_or_404(CustomerEnqiuery,id=pk)
    print(all)
    context = {
        'all':all
    }
    return render(request, 'followup/viewfollowupenq.html',context)

@login_required
def changeconfirmed_customerenq(request, pk):
    customer_enquiry = get_object_or_404(CustomerEnqiuery, id=pk)
    statusid = get_object_or_404(Status, id=3)
    customer_enquiry.status = statusid
    customer_enquiry.save()
    return redirect('followup-list')

@login_required
def changerejected_customerenq(request, pk):
    customer_enquiry = get_object_or_404(CustomerEnqiuery, id=pk)
    statusid = get_object_or_404(Status, id=5)
    customer_enquiry.status = statusid
    customer_enquiry.save()
    return redirect('followup-list')


@login_required
def confirmedlist(request):
    all = CustomerEnqiuery.objects.filter(status__id=3).order_by('-created_on')
    context = {
        'all':all
    }
    return render(request, 'confirmed/confirmlist.html',context)

 
@login_required
def view_customerenqconfirm(request,pk):
    all = get_object_or_404(CustomerEnqiuery,id=pk)
    print(all)
    context = {
        'all':all
    }
    return render(request, 'confirmed/viewconfirmupenq.html',context)

@login_required
def changetravelled_customerenq(request, pk):
    customer_enquiry = get_object_or_404(CustomerEnqiuery, id=pk)
    statusid = get_object_or_404(Status, id=4)
    customer_enquiry.status = statusid
    customer_enquiry.save()
    return redirect('confirmed-list')




@login_required
def rejectedlist(request):
    all = CustomerEnqiuery.objects.filter(status__id=4).order_by('-created_on')
    context = {
        'all':all
    }
    return render(request, 'rejected/rejectedlist.html',context)


@login_required
def traveledlist(request):
    all = CustomerEnqiuery.objects.filter(status__id=5).order_by('-created_on')
    context = {
        'all':all
    }
    return render(request, 'travelled/travelledlist.html',context)

@login_required
def customerdetailslist(request):
    all1 = CustomerDetails.objects.all().order_by('-created_on')
    myFilter = Passenger_details_filter(request.GET, queryset=all1)
    all = myFilter.qs
    context = {
        'all':all,
        'myFilter':myFilter,
        
    }
    return render(request, 'customer details/customerlist.html',context)

 



        

class ProductInline():
    form_class = CustomerDetailsForm
    model = CustomerDetails
    template_name = "customer details/customerform.html"

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))

        self.object = form.save()

        # for every formset, attempt to find a specific formset save function
        # otherwise, just save.
        for name, formset in named_formsets.items():
            formset_save_func = getattr(
                self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()
        return redirect('customerdetails-list')

    def formset_variants_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        variants = formset.save(
            commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for variant in variants:
            variant.customerdetailsid = self.object
            variant.save()

    def formset_images_valid(self, formset):
        """
        Hook for custom formset saving.. useful if you have multiple formsets
        """
        images = formset.save(
            commit=False)  # self.save_formset(formset, contact)
        # add this, if you have can_delete=True parameter set in inlineformset_factory func
        for obj in formset.deleted_objects:
            obj.delete()
        for image in images:
            image.customerdetailsid = self.object
            image.save()


class ProductCreate(ProductInline, CreateView):
    
    @method_decorator(login_required)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    

    def form_valid(self, form):
        
        customerenqid = self.kwargs.get('pk')
        
       
        customer_enq = get_object_or_404(CustomerEnqiuery, id=customerenqid)
        
      
        form.instance.customerenqid = customer_enq
        
        # Rest of your form validation logic...
        
        return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        ctx = super(ProductCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {
                'variants': PassengerDetailsFormSet(prefix='variants'),
                'images': PassengerdocFormSet(prefix='images'),
            }
        else:
            return {
                'variants': PassengerDetailsFormSet(self.request.POST or None, self.request.FILES or None, prefix='variants'),
                'images': PassengerdocFormSet(self.request.POST or None, self.request.FILES or None, prefix='images'),
            }


class ProductUpdate(ProductInline, UpdateView):
    @method_decorator(login_required)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def get_context_data(self, **kwargs):
        ctx = super(ProductUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'variants': PassengerDetailsFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='variants'),
            'images': PassengerdocFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='images'),
        }



@login_required
def delete_image(request, pk):
    try:
        image = PassengerDoc.objects.get(id=pk)
    except PassengerDoc.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
        )
        return redirect('update_product', pk=image.customerdetailsid.id)

    image.delete()
    messages.success(
        request, 'Image deleted successfully'
    )
    return redirect('update_product', pk=image.customerdetailsid.id)

@login_required
def delete_variant(request, pk):
    try:
        variant = Passenger.objects.get(id=pk)
    except Passenger.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
        )
        return redirect('update_product', pk=variant.customerdetailsid.id)

    variant.delete()
    messages.success(
        request, 'Variant deleted successfully'
    )
    return redirect('update_product', pk=variant.customerdetailsid.id)

@login_required
def deleteproduct(request, id):
    lease = get_object_or_404(CustomerDetails, pk=id)
    lease.delete()
    return redirect('customerdetails-list')