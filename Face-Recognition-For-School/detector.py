import cv2,os
import numpy as np
from PIL import Image 
import sqlite3
import time
from colorama import init
from termcolor import colored

init()

path = os.path.dirname(os.path.abspath(__file__))

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read(path+r'\trainer\trainer.yml')


faceCascade = cv2.CascadeClassifier(path+r'\Classifiers\face.xml')

conn = sqlite3.connect("FaceBase.db")

def InitDataBase():
    cmd = "SELECT * FROM People"
    cursor = conn.execute(cmd)
    
    for row in cursor:
        conn.execute("UPDATE People SET Appear= 0 WHERE ID="+str(row[0]))
        
    conn.commit()
        
def getProfile(id):
    cmd = "SELECT * FROM People WHERE ID="+str(id)
    cursor = conn.execute(cmd)
    profile = None
    
    for row in cursor:
        profile=row
        
    return profile

def Update():
    cmd = "SELECT * FROM People"
    cursor = conn.execute(cmd)
    
    appear = 0
    
    for row in cursor:
        if (row[3] == 1):
            appear += 1
        else:
            print(colored("Absent Student: "+str(row[1]) + ' point: '+str(row[2]),'red'))
    
    print(colored("Available: " + str(appear),'blue'))

    cursor = conn.execute(cmd)

    for row in cursor:
        if (row[3] == 1):
            print(colored("Student "+str(row[1])+" entered at "+row[4]+' point: '+str(row[2]),'green'))
        

InitDataBase()

cam = cv2.VideoCapture(0)

font = cv2.FONT_HERSHEY_SIMPLEX

while not(cv2.waitKey(1) & 0xFF == ord('q')):
    ret, im =cam.read()
    
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(gray, 1.2,5)
 
    
    for(x,y,w,h) in faces:
        nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
        #print (nbr_predicted)
        cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
        
        profile = getProfile(nbr_predicted)
        
        
        if (profile != None):
            cv2.putText(im,str(profile[1]), (x,y+h+30),font, 1.1, (0,255,0))
            cv2.putText(im,str(profile[3]), (x,y+h+60),font, 1.1, (0,255,0))
            
            if (profile[3] == 0):
                if (time.strftime("%H:%M:%S",time.localtime()) > "07:00:00"):
                    conn.execute('UPDATE People SET POINT='+str(profile[2]-1)+' WHERE ID='+str(nbr_predicted))
                    conn.commit()
                
                cmd = "UPDATE People SET Appear= 1 WHERE ID="+str(nbr_predicted)
                conn.execute(cmd)
                
                cmd = 'UPDATE People SET Time="' + str(time.strftime("%H:%M:%S",time.localtime()))+'" WHERE ID='+str(nbr_predicted)
                
                    
                conn.execute(cmd)
                
                os.system("cls")
                Update()
        
        cv2.imshow('im',im)



cmd = "SELECT * FROM People"
cursor = conn.execute(cmd)

for row in cursor:
    if (row[3] == 0):
        conn.execute('UPDATE People SET POINT='+str(row[2]-2)+' WHERE ID='+str(row[0]))

os.system('cls')
Update()

cam.release()
cv2.destroyAllWindows()
conn.commit()
conn.close()