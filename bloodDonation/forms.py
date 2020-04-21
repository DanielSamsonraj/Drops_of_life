from django.db import froms
class donardetails(forms.Form):
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    bloodGroup=models.CharField(max_length=2)
    gender=models.CharField(max_length=1)
    contactNo=models.CharField(max_length=10)
    state=models.CharField(max_length=30)