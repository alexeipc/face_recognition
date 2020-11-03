import cv2
import os
import sqlite3

path = os.path.dirname(os.path.abspath(__file__))
cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier(path+r'\Classifiers\face.xml')

i=0
offset=50

def Update(Id, Name):
    conn = sqlite3.connect("FaceBase.db")
    cmd = "SELECT * FROM People WHERE ID="+str(Id)
    cursor = conn.execute(cmd)
    isExist = 0
    for row in cursor:
        isExist = 1
    if (isExist == 1):
        cmd = "UPDATE People SET NAME="+str(Name)+" WHERE ID="+str(Id)
    else : cmd = "INSERT INTO People(ID,Name) Values("+str(Id)+","+str(Name)+")"
    
    conn.execute(cmd)
    conn.commit()
    conn.close()
        

id=input('enter your id: ')
name=input('enter your name: ')
Update(id,'"'+name+'"')

s = "#"

while True:
    ret, im =cam.read()
    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces=detector.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    
    for(x,y,w,h) in faces:
        i=i+1
        cv2.imwrite("dataSet/face-"+str(id) +'.'+ str(i) + ".jpg", gray[y-offset:y+h+offset,x-offset:x+w+offset])
        
        os.system("cls")
        if (i%5 == 0): s += "#"
        print (str(s) + ":"+str(i) + '%')
        
        
        cv2.rectangle(im,(x-50,y-50),(x+w+50,y+h+50),(225,0,0),2)
        cv2.imshow('im',im[y-offset:y+h+offset,x-offset:x+w+offset])
        
        cv2.waitKey(100)
    if i>=100:
        cam.release()
        cv2.destroyAllWindows()
        break

