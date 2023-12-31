from smtplib import SMTP
import os
from socket import *
import time
import base64
from stat import *
import re



string=""
def list_files(startpath,string):
    if (os.path.isdir(startpath))==False:
        print(os.path.isfile(startpath))
        string = "Invalid Variable"
        return string
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        ind = '' * 4 * (level)
        string = string+"\n"+ind+os.path.basename(root)
        subind = '' * 4 * (level + 1)
        for f in files:
            string=string+"\n"+subind+ f
    return string

def rename(src,dest):
    os.rename(src,dest)

def download(path):
    fp = open(path, 'r')
    str1 = fp.read()
    return str1

def upload(txt):
    ll = txt.split('>')
    fp = open(path0 + ll[0], 'w')
    fp.write(ll[1])


serverPort = 3001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("127.0.0.1", serverPort))
serverSocket.listen(1)
print("Ready to receive orders!")
print("=======================================")
print("Button function description")
count = 0
while True:
    connectionSocket, addr = serverSocket.accept()
    while True:
        base64_bytes = connectionSocket.recv(1024)
        message_bytes = base64.b64decode(base64_bytes)
        sentence = message_bytes.decode('ascii')

        path0 = "C:\\jupyter\\Conf\\"  # paths to the server and client directories are stored
        path1 = "C:\\jupyter\\Conf\\Menu\\"
        path2 = "C:\\jupyter\\Orders\\Order\\"
        path3 = "C:\\jupyter\\Orders\\"
        print(sentence)                            #printing the decoded sentence
        if (sentence[0] == '0'):
            strr = "\nPlease enter correct option!"
            connectionSocket.send(strr.encode())
        elif (sentence[0] == '1'):
            strr = list_files(path1 + sentence[1:], string)  # to list all files
            strr = "\nMenu" + strr
            connectionSocket.send(strr.encode())
        elif (sentence[0] == '2'):
            count += 1
            os.mkdir(path2 + sentence[1:])  # to create new dir
            strr = list_files(path2, string)
            upload("Bill.txt>" + strr + "\n" + str(count) + " items x 100 = " + str(count * 100))
            strr = "\nOrder Placed! \n\nYour Order is :" + strr +"\n\n Please proceed to payment"
            total =0
            total = str(count*100)
            connectionSocket.send(strr.encode())
        elif (sentence[0] == '3'):
            strr = download(path0 + "Bill.txt")
            strr="\nBill \n"+strr
            connectionSocket.send(strr.encode())

        elif (sentence[0]=='4'):
            upload(sentence[1:]) #to upload money file
            strr="\npayment has been payed Successfully \n\n Please check you Order Details "
            connectionSocket.send(strr.encode())
        elif(sentence[0]=='5'):
            count-=1
            os.rmdir(path2+sentence[1:]) #to delete a file
            strr=list_files(path2,string)
            upload("Bill.txt>"+strr+"\n"+str(count)+" items x 100 = "+str(count*100))
            strr="Order Deleted! \nYour Order is :"+strr +"\n\npayment has been retransactioned"+ "\nplease check bill & proceed payment"
            connectionSocket.send(strr.encode())
        elif(sentence[0]=='6'): 
            temp=sentence.split('>') 
            #print(temp)
            #print(path2)
            #print(path2+temp[0][1:])
            #print(path2+temp[1])
            rename(path2+temp[0][1:],path2+temp[1]) #to rename a file 
            strr=list_files(path2,string) 
            upload("Bill.txt>"+strr+"\n"+str(count)+" items x 100 = "+str(count*100)) 
            strr="\nOrder Edited! \n\nYour Order is :"+strr 
            connectionSocket.send(strr.encode())       
        elif(sentence[0]=='7'):
            strr=""
            s=list_files(path2,string) #to print details of all files
            ls=s.split('\n')
            for i in ls:
                if i:
                    st=os.stat(path2+i)
                    strr+=i+"\t"+str(time.asctime(time.localtime(st[ST_MTIME])))+"\n"
            strr="\nOrder Details! \n\nName\tDate&Time\n"+strr
            connectionSocket.send(strr.encode())

        elif(sentence[0]=='8'):
            executable = os.access(path3+"Bill.txt", os.W_OK) #to check if bill is writable
            if(executable==True):
                strr="\t\nCan edit.\nOrder not placed yet."+"\n"
            else:
                strr="\t\nCannot edit order placed."+"\n"
            strr="\nOrder Status! \n\n"+strr
            connectionSocket.send(strr.encode())

        elif (sentence[0] == '9'):
            os.chmod(path3 + "Bill.txt", S_IREAD)  # to make bill read-only
            strr = "\nYour Order is Confirmed."
            details = list_files(path2, string)
            regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
            if (re.search(regex, sentence[1:])):  # to check for valid mail-id to send
                server = SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.ehlo()
                gmail_user = 'icandyshop8@gmail.com'
                gmail_app_password = 'oxxfpxpdflgpgmwa'
                server.login(gmail_user,gmail_app_password)
                sent_from = gmail_user
                to = sentence[1:]
                subject = 'Choco Rush - Order Placed'
                body = "Dear Customer! Your order has been placed. Thankyou for shopping.\nDetails: \n Item you have ordered is :" + details
                email_text = """\ 
                            From: %s 
                            To:   %s 
                            Subject: %s 
                            %s
                            """ % (sent_from,to, subject, body)
                server.sendmail(sent_from, to, email_text)
                print('Email sent!')
                server.quit()
                strr += "\nPlease check your mail for details"
                connectionSocket.send(strr.encode())
            else:
                strr += "\nBut Invalid mail id. So mail is not sent"
                print('Email is not valid')
                connectionSocket.send(strr.encode())

               

        elif (sentence[0] == '.'):
            strr = "\n\nOrder dispatched! \nWill be delivered soon!\nTHANK YOU!"
            connectionSocket.send(strr.encode())
            for i in list_files(path2, string).split('\n'):
                if i:
                    os.rmdir(path2 + i)
            
serverSocket.close()


