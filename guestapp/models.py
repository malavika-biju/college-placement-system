from django.db import models

class tbl_login(models.Model):
    login_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=50)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.username
    
class tbl_company(models.Model):
    company_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=50)
    location_id = models.ForeignKey('adminapp.tbl_location', on_delete=models.CASCADE)
    company_logo = models.ImageField()
    contact_number = models.BigIntegerField()
    contact_email = models.CharField(max_length=50)

    id_proof = models.ImageField()
    login_id = models.ForeignKey(tbl_login, on_delete=models.CASCADE)
    reg_date = models.DateField(auto_now_add=True)
 

class tbl_student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=50)
    resume = models.FileField()
    course_id = models.ForeignKey('adminapp.tbl_course', on_delete=models.CASCADE)
    login_id = models.ForeignKey(tbl_login, on_delete=models.CASCADE)
    id_proof = models.ImageField()
    mark = models.FloatField()
    percentage = models.FloatField()
    photo = models.ImageField()
    reg_id = models.DateField(auto_now_add=True)
    email = models.CharField(max_length=50)
    batch_id = models.ForeignKey('adminapp.tbl_batch', on_delete=models.CASCADE)
    gender = models.CharField(max_length=10)
    contact_number = models.BigIntegerField()