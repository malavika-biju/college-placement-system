from django.db import models

class tbl_district(models.Model):
    district_id = models.AutoField(primary_key=True)
    district_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.district_name
    
class tbl_batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    batch_year = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.batch_year
    
class tbl_department(models.Model):
    department_id = models.AutoField(primary_key=True)
    department_name = models.CharField(max_length=100)

    def __str__(self):
        return self.department_name
    
class tbl_classtype(models.Model):
    classtype_id = models.AutoField(primary_key=True)
    classtype_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.classtype_name
    
class tbl_location(models.Model):
    location_id = models.AutoField(primary_key=True)
    location_name = models.CharField(max_length=50)
    district_id = models.ForeignKey(tbl_district, on_delete=models.CASCADE)

    def __str__(self):
        return self.location_name
    
class tbl_course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=100)
    department_id = models.ForeignKey(tbl_department, on_delete=models.CASCADE)

    def __str__(self):
        return self.course_name
    
class tbl_trainingclass(models.Model):
    trainingclass_id = models.AutoField(primary_key=True)
    trainingclass_name = models.CharField(max_length=100)
    start_time = models.TimeField()
    date = models.DateField()
    course_id = models.ForeignKey(tbl_course, on_delete=models.CASCADE)
    classtype_id = models.ForeignKey(tbl_classtype, on_delete=models.CASCADE)
    batch_id = models.ForeignKey(tbl_batch, on_delete=models.CASCADE)
    description = models.TextField()

    def __str__(self):
        return self.trainingclass_name





    


