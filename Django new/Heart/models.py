from django.db import models

# class PredResults(models.Model):

#     Patient_ID = models.IntegerField()
#     Patient_Age = models.IntegerField()
#     Patient_Gender = models.IntegerField()
#     Patient_Blood_Pressure = models.IntegerField()
#     Patient_Heartrate = models.IntegerField()
#     Heart_Disease = models.CharField(max_length=30)

#     def __str__(self):
#         return self.Heart_Disease

class PredResults(models.Model):

    Patient_ID = models.CharField(max_length=30)
    Patient_Age = models.CharField(max_length=30)
    Patient_Gender = models.CharField(max_length=30)
    Patient_Blood_Pressure = models.CharField(max_length=30)
    Patient_Heartrate = models.CharField(max_length=30)
    Heart_Disease = models.CharField(max_length=30)

    def __str__(self):
        return self.Heart_Disease