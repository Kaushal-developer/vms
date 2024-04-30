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

Kindly import the Postman collection "VMS.postman_collection.json" to get all the API endpoints.
 
