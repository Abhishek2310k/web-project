Download 'yolov3.weights' file from 'https://pjreddie.com/media/files/yolov3.weights' for the 
pre-trained object detection model and paste it in '/api'

after cloning the repository from github you need to 

 ---- >   install docker

and after installing the docker go to the Cistup folder 

 ---- >   cd Cistup

 ---- >   docker compose up


 < ---- If the docker command is showing error ---- >

after cloning go to the Cistup folder

 ---- >   cd client 

in the client folder enter the command 

 ---- >   npm i

this will install all of the dependencies and now you are ready to start the front-end part

 ---- >   npm start

Now the front end is running on port 3000

 < ---- For running the backend ---- >

go to the api folder 

 ---- >   cd ../api (if you were origionally in client folder) or cd api (if you were origionally on the Cistup folder)


now in api folder run the command

pip install -r requirements.txt

to install all of the dependencies for python

now you are ready to start the backend server enter the command

 ---- >   flask run --host 0.0.0.0

0r 

 ---- >   python3 app.py or python app.py  (depending on your python version)   



  < ---- Now both the front end backend are running and you can upload and perform object detection on the image ---- >