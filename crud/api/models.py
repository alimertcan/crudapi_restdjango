from django.db import models
# Create your models here.
class Passenger(models.Model):
    name = models.CharField(max_length=60)
    email = models.CharField(max_length=150)
    status = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    # def __str__(self):
    #     return str(self.pk)


class Trip(models.Model):
    total_distance = models.IntegerField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    passenger = models.ManyToManyField(Passenger)
    def __str__(self):
        return 'id:{} - TotalDistance:{} '.format(self.pk, self.total_distance)