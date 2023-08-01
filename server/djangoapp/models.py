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


# <HINT> Create a plain Python class `DealerReview` to hold review data
