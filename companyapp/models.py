from django.db import models

# Create your models here.
class tbl_jobpost(models.Model):
    jobpost_id = models.AutoField(primary_key=True)
    requirement = models.TextField()
    cutoff_mark = models.FloatField()
    post_date = models.DateField(auto_now_add=True)
    application_end_date = models.DateField()
    position = models.CharField(max_length=100)
    photo = models.ImageField()
    company_id = models.ForeignKey('guestapp.tbl_company', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='open')