from django.db import models


class Flight(models.Model):
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=50)
    flight_name = models.CharField(max_length=50)
    flight_id = models.CharField(max_length=32,primary_key=True)
    duration = models.CharField(max_length=30)
    departure = models.CharField(max_length=50)
    arrival = models.CharField(max_length=50)
    via = models.CharField(max_length=32)
    price = models.IntegerField(null=True)
    def __str__(self):
        return f'{self.source},{self.destination}'


class Hotel(models.Model):
    city = models.CharField(max_length=30,null=True)
    name = models.CharField(max_length=300)
    location = models.CharField(max_length=500)
    description = models.CharField(max_length=500)
    check = models.IntegerField()
    unchecked = models.IntegerField()
    img = models.CharField(max_length=500)
    price = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.name,self.city}'



class SaveFlight(models.Model):
    cardno = models.CharField(max_length=30)
    uname = models.CharField(max_length=30)
    source = models.CharField(max_length=30)
    destination = models.CharField(max_length=50)
    flight_name = models.CharField(max_length=50)
    flight_id = models.CharField(max_length=32, primary_key=True)
    duration = models.CharField(max_length=30)
    departure = models.CharField(max_length=50)
    arrival = models.CharField(max_length=50)
    via = models.CharField(max_length=32)
    price = models.IntegerField(null=True)
    seats = models.IntegerField(null=True)
    totalprice = models.IntegerField(null=True)


class SaveHotel(models.Model):
    cardno = models.CharField(max_length=30)
    uname = models.CharField(max_length=30)
    city = models.CharField(max_length=30,null=True)
    name = models.CharField(max_length=300)
    img = models.CharField(max_length=500)
    price = models.IntegerField(null=True)
    rooms = models.IntegerField(null=True)
    totalprice = models.IntegerField(null=True)


