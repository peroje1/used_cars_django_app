from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count,Avg
from .models import Car
from .forms import CarForm
import plotly.express as px
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404

def dashboard_view(request):
    # Cars per brand
    brand_data = Car.objects.values('brand').annotate(total=Count('id')).order_by('-total')
    fig_bar = px.bar(
        x=[b['brand'] for b in brand_data],
        y=[b['total'] for b in brand_data],
        labels={'x': 'Brand', 'y': 'Car Count'},
        title='Cars per Brand'
    )

    # Pie chart
    fig_pie = px.pie(
        names=[b['brand'] for b in brand_data],
        values=[b['total'] for b in brand_data],
        title='Cars per brand'
    )

    # Average price per brand
    avg_price_data = Car.objects.values('brand').annotate(avg_price=Avg('price')).order_by('-avg_price')
    fig_avg = px.bar(
        x=[b['brand'] for b in avg_price_data],
        y=[b['avg_price'] for b in avg_price_data],
        labels={'x': 'Brand', 'y': 'Avg Price'},
        title='Average price per brand'
    )

    # Cars per year
    year_data = Car.objects.values('year').annotate(total=Count('id')).order_by('year')
    fig_year = px.line(
        x=[y['year'] for y in year_data],
        y=[y['total'] for y in year_data],
        labels={'x': 'Year', 'y': 'Car Count'},
        title='Cars per year'
    )

    context = {
        'chart_pie': fig_pie.to_html(full_html=False),
        'chart_avg': fig_avg.to_html(full_html=False),
        'chart_year': fig_year.to_html(full_html=False),
    }
    return render(request, 'listings/dashboard.html', context)

def car_list(request):
    cars = Car.objects.all().order_by('-created_at')

    # Filters (keep existing code for filters)
    brand = request.GET.get('brand')
    min_year = request.GET.get('min_year')
    max_year = request.GET.get('max_year')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if brand and brand != 'All':
        cars = cars.filter(brand=brand)
    if min_year:
        cars = cars.filter(year__gte=min_year)
    if max_year:
        cars = cars.filter(year__lte=max_year)
    if min_price:
        cars = cars.filter(price__gte=min_price)
    if max_price:
        cars = cars.filter(price__lte=max_price)

    brands = Car.objects.values_list('brand', flat=True).distinct()

    total_results = cars.count()

    paginator = Paginator(cars, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'cars': page_obj,
        'brands': brands,
        'filters': {
            'brand': brand or 'All',
            'min_year': min_year or '',
            'max_year': max_year or '',
            'min_price': min_price or '',
            'max_price': max_price or '',
        },
        'page_obj': page_obj,
        'total_results': total_results
    }
    return render(request, 'listings/car_list.html', context)


def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    return render(request, 'listings/car_detail.html', {'car': car})

@login_required
def add_car(request):
    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES)
        if form.is_valid():
            car = form.save(commit=False)
            car.owner = request.user
            car.save()
            return redirect('car_list')
    else:
        form = CarForm()
    return render(request, 'listings/car_form.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def edit_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if car.owner != request.user:
        return HttpResponseForbidden("You are not allowed to edit this listing.")

    if request.method == 'POST':
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = CarForm(instance=car)

    return render(request, 'listings/car_form.html', {'form': form, 'edit_mode': True})


@login_required
def delete_car(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    if car.owner != request.user:
        return HttpResponseForbidden("You are not allowed to delete this listing.")

    if request.method == 'POST':
        car.delete()
        return redirect('car_list')

    return render(request, 'listings/confirm_delete.html', {'car': car})
