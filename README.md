# vms
VMS = Vendor Management System
According to the requested backend API Implementation of the Vendor management system (https://drive.google.com/file/d/1hLWc35hpLQ0EPDAZjZloomeAxgn3V7g9/view), I have included it here.  
Steps to set up the Repo.
1) git clone https://github.com/Kaushal-developer/vms.git
2) Create a Python virtual environment.
3) active virtual environment.
4) Run the command pip install -r requirements.txt ( let me know if any package dependency error)
5) If you want to use fresh DB then remove the existing db file
    1) Run the command python manage.py migrate
    2) python manage.py createsuperuser (to create a user)
    3) use this credential to generate tokens via the Generate Token API.
6) Run the command python manage.py collectstatic
7) Run the command python manage.py runserver.
8) Generate tokem via API

Kindly import the Postman collection "VMS.postman_collection.json" to get all the API endpoints.
 
Extra Description about repo.
1) In the repo lib folder contains all the common custom files like custom mixings, custom models, custom serializer.
Benefits of custom files is we can manage everything on custom file. which ease the works on individual files like views.py, models.py, serializer.py

2) I created different serializer which might have suffix like Listserialzier, Detail serialzier so benefits of this is we can customize the fields which only used by client so it imporves the load by fetching mentioned field data ( technically improves database interaction and query.)

3) Custom middleware provides extra benefits to the server in order to customize any requests.

4) I Used django-lifecycle hooks which ultimately the same thing running as signals. But it provides more ease and reliable and conditional way so we can call the function after or befor update/create on specific condition.
The performance metrics will get genreate by using this approach.

5) As everything is customized so each request response also got customized. So if you created something in vendor then the response will come like VendorName created successfully.

6) Customized paginator file in Django DRF so it will give response accordingly for the list APIs.

7) Same way we can manage filters too which helps to sort and search accorss the list of data.