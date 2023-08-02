from django.db import models
from django.utils.timezone import now


# Create your models here.
TIPOLOGIA_CHOICES = [
    ("SUv", "SUV"),
    ("Wagon", "Wagon"),
]

class CarMake(models.Model):
    Name = models.CharField(null=False,max_length=2000, default="name", )
    Description = models.CharField(null=False, max_length=2000, default="description")
    def __str__(self):
            return "Name: " + self.Name + "," + \
                "Description: " + self.Description


class CarModel(models.Model):
    car_id = models.IntegerField(default=1, primary_key=True)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    Name = models.CharField(null=False, max_length=2000,default="name", )
    Dealerid = models.IntegerField(default=0)
    Type = models.CharField(null=False,max_length=2000, choices=TIPOLOGIA_CHOICES)
    Year = models.DateField(default=now)

    def __str__(self):

        return (
            "Name: "
            + self.Name
            + ", "
            + "Description: "
            + str(self.Dealerid)  # Convert Dealerid to string
            + ", "
            + "Type: "
            + self.Type
        )


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
import json
class DealerReview:

    def __init__(self, dealership, name, purchase, review):
        # Required attributes
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        # Optional attributes
        self.purchase_date = ""
        self.purchase_make = ""
        self.purchase_model = ""
        self.purchase_year = ""
        self.sentiment = ""
        self.id = ""

    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)
