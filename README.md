
## Soccer App

##### Steps to launch:

- Git clone the source code to specific path

```
git clone https://github.com/mrlafranchi/soccer_api.git
```
- Install Virtual Environment (Optoinal)

- Install required packages
```
pip install -r requirements.txt
```
- Migrate the database
```
python manage.py makemigrations general
python manage.py migrate
```
- Make a super user
```
python manage.py createsuperuser
```
- Launch the site
```
python manage.py runserver
```
- Visit URL
```
http://localhost:8000
http://localhost:8000/admin
```
login with the credential for superuser you created.

