from django.shortcuts import render,redirect
from .models import Flight,Hotel,SaveFlight,SaveHotel
from django.db.models import Q
import json
from django.http import JsonResponse
from .utils import get_plot,get_plot1,get_plot2
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='initial:register')
def hotels_list(request):
    u = request.session['uname']
    city = request.POST.get('city')
    if city == 'some':
        return redirect('module1:home')
    f = Hotel.objects.filter(Q(city=city)).distinct()
    print(f)
    li = []
    for i in f:
        details = {
            'check': range(i.check),
            'unchecked': range(i.unchecked),
            'city': i.city,
            'name': i.name,
            'location': i.location,
            'description': i.description,
            'img': i.img,
            'price':i.price,
            'id': i.id
        }
        li.append(details)
    hotels=[]
    price=[]
    rating=[]
    for i in range(len(li)):
        hotels.append(li[i]['name'])
        price.append(li[i]['price'])
        rating.append(li[i]['check'])

    barchart=get_plot1(hotels,price)
    hist=get_plot2(rating)
    return render(request, 'module2/hotels.html', {'test': li, 'u': u,'barchart':barchart,'hist':hist})




@login_required(login_url='initial:register')
def list1(request):
    if 'uname' in request.session:
        u = request.session['uname']
        context = {'u': u}
        source = request.GET.get('source')
        destination = request.GET.get('destination')
        if source == destination or source == 'source' or destination == 'source':
            return redirect('module1:home')
        temp = Flight.objects.order_by().values('source').distinct()
        print(temp)
        cities=[]
        for i in range(len(temp)):
            cities.append(temp[i]['source'])



        # cities=['Hyderabad','Bengaluru','Kolkata','Mumbai','New Delhi']

        arr = [[0 for x in range(len(cities))] for y in range(len(cities))]
        k1,k2=0,0
        minval=100000
        for c1 in range(len(cities)):
            for c2 in range(len(cities)):
                if cities[c1]!=cities[c2]:
                    x=Flight.objects.filter(Q(source=cities[c1]) & Q(destination=cities[c2])).distinct()
                    # print(x)
                    for i in x:
                        details = {
                            'price': i.price
                        }
                        minval=min(minval,details['price'])
                        # print(details['price'])
                    # print(k1, k2)
                    arr[c1][c2]=minval
                    minval=100000
        # print(arr)

        for i in range(len(cities)):
            if cities[i]==source:
                si=i
            if cities[i]==destination:
                di=i

        farr = [[0 for x in range(2)] for y in range(len(cities)-2)]
        indices=[]
        indices.append(si)
        indices.append(di)
        a,b=0,0
        arr1=[]
        arr2=[]
        for i in range(len(arr)):
            for j in range(len(arr[0])):
                if i == si and j != di and i != j:
                    arr1.append(arr[i][j])
                    # print(i,j)
                if i==di and j != si and i != j:
                    # print(i,j)
                    arr2.append(arr[i][j])


        # print((arr))
        # print(arr1)
        # print(arr2)

        steps=[]
        stepprice=[]
        dupcities=cities.copy()
        dupcities.remove(source)
        dupcities.remove(destination)
        for i,j in zip(range(len(arr1)),dupcities):
            steps.append(j)
            stepprice.append(arr1[i]+arr2[i])

        # print(steps)
        # print(stepprice)

        val=zip(steps,stepprice)


        eachmin=100000
        avgprice=[]
        for each in cities:
            if source!=each:
                c1=Flight.objects.filter(Q(source=source) & Q(destination=each)).distinct()
                # print(c1[0])
                total=0
                count=0
                li = []
                for i in c1:
                    details = {
                        'source':i.source,
                        'destination':i.destination,
                        'flight_name':i.flight_name,
                        'flight_id':i.flight_id,
                        'duration':i.duration,
                        'departure':i.departure,
                        'arrival':i.arrival,
                        'via':i.via,
                        'price':i.price
                    }
                    li.append(details)
                print(li)
                for c in range(len(li)):
                    total+=li[c]['price']

                    # print(li[c]['price'])
                total=total//len(li)
                avgprice.append(total)
        cities.remove(source)
        cl=[]
        for each in cities:
            cl.append(source+"-"+each)
        chart=get_plot(cl,avgprice)

        viacity=""
        ind=stepprice.index(min(stepprice))
        viacity=steps[ind]
        print(min(stepprice),eachmin)
        if request.method == 'GET':
            f = Flight.objects.filter(Q(source=source) & Q(destination=destination)).distinct()


            li1 = []
            for i in f:
                details = {
                    'source': i.source,
                    'destination': i.destination,
                    'flight_name': i.flight_name,
                    'flight_id': i.flight_id,
                    'duration': i.duration,
                    'departure': i.departure,
                    'arrival': i.arrival,
                    'via': i.via,
                    'price': i.price
                }
                li1.append(details)
            for c in range(len(li1)):
                eachmin = min(eachmin, li1[c]['price'])
            print(min(stepprice),eachmin)
            if min(stepprice)<eachmin:
                return render(request, 'module2/index.html', {'test': f,'u':u,'chart':chart,'val':val,'eachmin':eachmin,'optimisedmin':min(stepprice),'is':True,'s':source,'d':destination,'viacity':viacity})
            else:
                return render(request, 'module2/index.html',{'test': f, 'u': u, 'chart': chart, 'val': val,'is':False})

    else:
        print("you cant")
        return redirect('initial:login')


def dologout(request):
    try:
        logout(request)
        del request.session['uname']
        return redirect('initial:register')
    except KeyError:
        pass
    return redirect('initial:register')


@login_required(login_url='initial:register')
def hotel_booking(request,id):
    f = Hotel.objects.filter(id=id)
    request.session['id'] = id
    li = []
    for i in f:
            details = {
                'check': range(i.check),
                'unchecked': range(i.unchecked),
                'city': i.city,
                'name': i.name,
                'location': i.location,
                'description': i.description,
                'img': i.img,
                'price':i.price,
                'id': i.id
            }
            li.append(details)

    return render(request, 'module2/hotel_booking.html',{'f':li})

        
@login_required(login_url='initial:register')
def calculate(request):
    u = request.POST.get('num')
    id = request.session['id']
    print(u)
    print("kal")
    request.session['inputno'] = u
    return redirect('module2:hotel_confirm',id)


@login_required(login_url='initial:register')
def hotel_confirm(request,id):
    f = Hotel.objects.filter(id=id)
    print("confirm")
    request.session['id'] = id
    inputno = request.session['inputno']
    li = []
    for i in f:
            details = {
                'check': range(i.check),
                'unchecked': range(i.unchecked),
                'city': i.city,
                'name': i.name,
                'location': i.location,
                'description': i.description,
                'img': i.img,
                'price':i.price,
                'id': i.id
            }
            li.append(details)
    o = li[0]['price']
    a = int('0' + request.session['inputno'])
    request.session['totalprice'] = a*o
    return render(request, 'module2/hotel_confirm.html',{'f':li,'to': a*o,'inpu':inputno})


@login_required(login_url='initial:register')
def payment(request):
    a = request.session['totalprice']
    b = request.session['inputno']
    id = request.session['id']
    f = Hotel.objects.filter(id=id)
    request.session['id'] = id
    li = []
    for i in f:
            details = {
                'check': range(i.check),
                'unchecked': range(i.unchecked),
                'city': i.city,
                'name': i.name,
                'location': i.location,
                'description': i.description,
                'img': i.img,
                'price':i.price,
                'id': i.id
            }
            li.append(details)
    return render(request,'module2/payment.html',{'a':a,'fo':li,'b':b})



@login_required(login_url='initial:register')
def flight_structure(request,id):
    request.session['flight_id'] = id
    f = Flight.objects.filter(flight_id=id)
    li = []
    for i in f:
            details = {
                'source':i.source,
                'destination':i.destination,
                'flight_name':i.flight_name,
                'flight_id':i.flight_id,
                'duration':i.duration,
                'departure':i.departure,
                'arrival':i.arrival,
                'via':i.via,
                'price':i.price
            }
            li.append(details)
    price1 = li[0]['price']
    return render(request,'module2/main1.html',{'a':request.session['flight_id'],'fo':li,'jj':price1})


@login_required(login_url='initial:register')
def paymentforflight(request):
    uy = request.POST['seats']
    id = request.session['flight_id']
    f = Flight.objects.filter(flight_id=id)
    li = []
    for i in f:
            details = {
                'source':i.source,
                'destination':i.destination,
                'flight_name':i.flight_name,
                'flight_id':i.flight_id,
                'duration':i.duration,
                'departure':i.departure,
                'arrival':i.arrival,
                'via':i.via,
                'price':i.price
            }
            li.append(details)
    a = int('0' + uy)
    total2 = li[0]['price']*a
    return render(request,'module2/paymentforflights.html',{'fo':li,'to':total2,'uy':uy})


def savepayment(request,id,seats,total):
    if request.method == 'POST':
        f = Flight.objects.filter(flight_id=id)
        li = []
        for i in f:
            details = {
                'source': i.source,
                'destination': i.destination,
                'flight_name': i.flight_name,
                'flight_id': i.flight_id,
                'duration': i.duration,
                'departure': i.departure,
                'arrival': i.arrival,
                'via': i.via,
                'price': i.price
            }
            li.append(details)
        flight = SaveFlight()
        flight.cardno = request.POST['cardno']
        flight.uname = request.session['uname']
        flight.source = li[0]['source']
        flight.destination = li[0]['destination']
        flight.flight_name = li[0]['flight_name']
        flight.flight_id = li[0]['flight_id']
        flight.duration = li[0]['duration']
        flight.departure = li[0]['departure']
        flight.arrival = li[0]['arrival']
        flight.via = li[0]['via']
        flight.price = li[0]['price']
        flight.seats = seats
        flight.totalprice = total
        print(request.POST.get('cvv'))
        if request.POST.get('cardno') == '' or request.POST.get('fullname') == '' or request.POST.get('cvv') == '' or request.POST.get('date') == '':
            print('not gone to payment')
            return render(request, 'module2/paymenterror.html')
        else:
            flight.save()
            return render(request, 'module2/thankyou.html')
    return render(request, 'module2/paymenterror.html')


def savehotel(request,id,rooms,total):
    if request.method == 'POST':
        f = Hotel.objects.filter(id=id)
        li = []
        for i in f:
            details = {
                'city': i.city,
                'name': i.name,
                'img': i.img,
                'price': i.price,
                'id': i.id
            }
            li.append(details)
        g = SaveHotel()
        g.cardno = request.POST['cardno']
        g.uname = request.session['uname']
        g.rooms = rooms
        g.totalprice = total
        g.city = li[0]['city']
        g.name = li[0]['name']
        g.img = li[0]['img']
        g.price = li[0]['price']
        if request.POST.get('cardno') == '' or request.POST.get('fullname') == '' or request.POST.get('cvv') == '' or request.POST.get('date') == '':
            print('not gone to payment')
            return render(request, 'module2/paymenterror.html')
        else:
            g.save()
            return render(request, 'module2/thankyou.html')
    return render(request, 'module2/paymenterror.html')

