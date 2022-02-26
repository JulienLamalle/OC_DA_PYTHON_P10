# Project 10 (Julien Lamalle)

### This project was done in python <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="30" height="30"/> with django and django rest framework



To clone this folder, execute the following command: 

```
git clone git@github.com:JulienLamalle/OC_DA_PYTHON_P10.git
```

From your terminal you can enter the file as follows: 

```
cd OC_DA_PYTHON_P10
```

Now your have to create a virtual environment for this project using this command:

```
python -m venv env
```

Then you have to activate your environment:

```
source env/bin/activate
```

You now need to install all the libraries necessary for this program to work properly, for this you can run the following command: 

```
pip install -r requirements.txt
```

You are now in the application folder with your environment launched, so you can access the django application using the following command: 

```
cd src
```

To start the server locally, make sure you are in the src folder and run the following command: 

```
python manage.py runserver
```

Now you can go to the following url in your browser to create your account and find your jwt token to request this API using postman for example:

```
http://localhost:8000/signup/
```

To access to the API endpoints documentation and models schema you can go to the following url after you have started the server:

```
http://localhost:8000/documentation/
```

### ENJOY 🎉 ! 


