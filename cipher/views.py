from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import MySQLdb
import base64
import datetime
from django.core.files.storage import FileSystemStorage
import subprocess
import os
from django.core.files.storage import FileSystemStorage

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db=MySQLdb.connect("localhost","root","","cipherwu")
c=db.cursor()
MASTER_KEY="Some-long-base-key-to-use-as-encryption-key"

def login(request):  
    request.session['emailid']=""
    error=""
    if(request.POST):
        emailid=request.POST.get("uname")
        request.session['emailid']=emailid
        pw=request.POST.get("pw")
        c.execute("select count('"+emailid+"') from registration where email='"+emailid+"'and password='"+pw+"'")
        data=c.fetchone()
        c.execute("select status from registration where email='"+emailid+"'and password='"+pw+"'")
        data1=c.fetchone()
        
        if((emailid=='admin@gmail.com') and (pw=='admin')):
                return HttpResponseRedirect("/admin_home/")
        elif(data[0]==0):
            error="INCORRECT USERNAME OR PASSWORD"
        else:
            if(data[0]==1 and data1[0]=="approved"):
                return HttpResponseRedirect("/user_home/")
            
            elif(data1[0]=="rejected"):
                error="Sorry!You are rejected by admin"
    return render(request,"login.html",{"error":error})    

def registration(request):
    error=""
    msg=""
    if(request.POST):
        name=request.POST.get("name")
        address=request.POST.get("address")
        dob=request.POST.get("dob")
        gender=request.POST.get("gender")
        mobile=request.POST.get("mobile")
        email=request.POST.get("email")
        pw=request.POST.get("pw")
        cpw=request.POST.get("cpw")
        answer=request.POST.get("answer")
        if(request.FILES.get('img12')):
                myfile=request.FILES['img12']
                fs=FileSystemStorage()
                filename=fs.save(myfile.name,myfile)
                fileurl=fs.url(filename)
        else:
                fileurl="/static/media/p1.png"
        if(pw==cpw):            
            c.execute("select count('"+email+"') from registration where email='"+email+"'")
            data=c.fetchone()
            c.execute("select count('"+mobile+"') from registration where mobile='"+mobile+"'")
            mob=c.fetchone()
            if data[0]==0:
                if mob[0]==0:
                    c.execute("insert into registration(name,address,dob,gender,mobile,email,image,password,answer) values('"+name+"','"+address+"','"+dob+"','"+gender+"','"+str(mobile)+"','"+email+"','"+fileurl+"','"+pw+"','"+answer+"')")
                    db.commit()    
                    msg="Wait for Admin approval!!"
                else:
                    msg="Existing mobile number"
            else:
                error="USERNAME ALREADY TAKEN!!"
        else:
            error="Password and confirm password must match!!"
    return render(request,"registration.html",{"error":error,"msg":msg})




def message(request):
    frm=""
    msg=""
    data=""
    if 'Encrypt' in request.POST:
            subprocess.call(os.path.join(BASE_DIR,r'wusalgm\WindowsFormsApplication1\WindowsFormsApplication1\bin\Debug\WindowsFormsApplication1.exe'))
    if request.session['emailid']:
        unam=request.session['emailid']
        c.execute("select * from registration where email='"+unam+"'")
        data1=c.fetchall()
        s="" 
        msg=""
        if('sub1' in request.POST):

            # pasting file system

            send=request.POST.get("send")
            subject=request.POST.get("Subject")
            content=request.POST.get("content")
            
            date=datetime.date.today()
            status="sent"
            unam=request.session['emailid']
            cc=encryp(content)
            for i in cc:
                s=s+i
            c.execute("select email from registration where email='"+send+"'")
            em=c.fetchone()
            if(em is None):
                msg="Enter valid emailid"
            else:
                if request.FILES.get("picture"):
                    myfile=request.FILES.get("picture")
                    fs=FileSystemStorage()
                    filename=fs.save(myfile.name , myfile)              
                    uploaded_file_url = fs.url(filename)
                    picture=uploaded_file_url
                    c.execute("insert into message (msgfrom,date,sendto,subject,content,status,image) values ('"+ unam +"','"+str(date)+"','"+ send +"','"+ subject +"','"+s+"','"+status+"','"+ picture +"')")
                    db.commit()            
                else:
                    msg="image error"

                return HttpResponseRedirect("/inbox/")
        if('draft' in request.POST):
            send=request.POST.get("send")
            subject=request.POST.get("Subject")
            content=request.POST.get("content")
            date=datetime.date.today()
            status="draft"         
            if request.FILES.get("picture"):
                    myfile=request.FILES.get("picture")
                    fs=FileSystemStorage()
                    filename=fs.save(myfile.name , myfile)              
                    uploaded_file_url = fs.url(filename)
                    picture=uploaded_file_url
                    c.execute("insert into message (msgfrom,date,sendto,subject,content,status,image) values ('"+ unam +"','"+str(date)+"','"+ send +"','"+ subject +"','"+content+"','"+status+"','"+ picture +"')")
                    db.commit()
            return HttpResponseRedirect("/inbox/")
        det=[]
        st="sent"
        unam=request.session['emailid']   
        c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+st+"' order by mid desc limit 2) as r order by mid")
        count=c.fetchall()
        for i in count:             
            c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
            count1=c.fetchone()
            det.append(count1) 
        c.execute("select feedback from feedback order by id desc limit 3")
        feed=c.fetchall()   
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"message.html",{"s":s,"data1":data1,"msg":msg,"det":det,"feed":feed})

def delete(request):
    if request.session['emailid']:
        id=request.GET.get("id")
        c.execute("delete from message where mid='"+id+"'")
        db.commit()
    else:
        return HttpResponseRedirect("/login/")
    return HttpResponseRedirect("/inbox/")


def inbox(request):
    frm=""
    sub=""
    if request.session['emailid']:
        unam=request.session['emailid']
        st="sent"
        c.execute("select * from registration where email='"+unam+"'")
        data1=c.fetchall()
        c.execute("select * from message where sendto='"+ unam +"' and status='"+st+"' order by date desc")
        data=c.fetchall()
        for d in data:
                frm=d[2]
                sub=d[4]
        cc=""
        for d in data:
            cc=decryp(d[5]) 
        request.session['frm']=frm
        request.session['sub']=sub
        det=[]
        s="sent"
        unam=request.session['emailid']   
        c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+s+"' order by mid desc limit 2) as r order by mid")
        count=c.fetchall()
        for i in count:             
            c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
            count1=c.fetchone()
            det.append(count1) 
        c.execute("select feedback from feedback order by id desc limit 3")
        feed=c.fetchall()
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"inbox.html",{"data1":data1,"data":data,"cc":cc,"det":det,"feed":feed})

def inbox1(request):
    if 'Decrypt' in request.POST:
            subprocess.call(os.path.join(BASE_DIR,r'wusalgm\WindowsFormsApplication1\WindowsFormsApplication1\bin\Debug\WindowsFormsApplication1.exe'))

    if 'download' in request.POST:
        id=request.GET.get('id')
        try:
            c.execute("select image from message where mid='"+ str(id) +"'")
            image=c.fetchone()
            image=image[0]
            dd=image
            
            # import webbrowser
                     
            # return HttpResponse("<img src='"+ r'/cipher/static/media/'+image +"' alt='image'/>")
            # a_website=dd
            # webbrowser.open_new_tab(a_website)
            request.session['dd']=dd
            
            return HttpResponseRedirect('/download/')
            
            
        except:            
            return HttpResponseRedirect('/inbox/')        


      
    if request.session['emailid']:
        s=""
        unam=request.session['emailid']
        c.execute("select * from registration where email='"+unam+"'")
        data1=c.fetchall()
        id=request.GET.get("id")
        st="sent"               
        msgfrm=request.session['frm']
        sub=request.session['sub']
        if(request.POST):
            to=request.POST.get("from")
            subject=request.POST.get("subject")
            msg=request.POST.get("msg")
            sdate=datetime.date.today()
            cc=encryp(msg)
            for i in cc:
                s=s+i
            if request.FILES.get("picture"):
                    myfile=request.FILES.get("picture")
                    fs=FileSystemStorage()
                    filename=fs.save(myfile.name , myfile)              
                    uploaded_file_url = fs.url(filename)
                    picture=uploaded_file_url
                    c.execute("insert into message (msgfrom,date,sendto,subject,content,status,image) values ('"+ unam +"','"+str(sdate)+"','"+ to +"','"+ subject +"','"+s+"','"+st+"','"+ picture +"')")
                    db.commit() 
            # subprocess.call(os.path.join(BASE_DIR,r'wusalgm\WindowsFormsApplication1\WindowsFormsApplication1\bin\Debug\WindowsFormsApplication1.exe'))
            return HttpResponseRedirect("/inbox/")
        det=[]
        st="sent"
        unam=request.session['emailid']   
        c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+st+"' order by mid desc limit 2) as r order by mid")
        count=c.fetchall()
        for i in count:             
            c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
            count1=c.fetchone()
            det.append(count1) 
        c.execute("select feedback from feedback order by id desc limit 3")
        feed=c.fetchall()
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"inbox1.html",{"data1":data1,"msgfrm":msgfrm,"sub":sub,"det":det,"feed":feed})

def draft(request):
    snd=""
    sub=""
    msg=""
    if request.session['emailid']:
        s="draft"
        unam=request.session['emailid']    
        c.execute("select * from message where status='"+s+"' and msgfrom='"+unam+"'")
        data1=c.fetchall()
        for d in data1:
                snd=d[3]
                sub=d[4]
                msg=d[5]
        unam=request.session['emailid']    
        c.execute("select * from registration where email='"+unam+"'")
        data=c.fetchall()
        request.session['snd']=snd
        request.session['sub']=sub
        request.session['msg']=msg 
        det=[]
        st="sent"
        unam=request.session['emailid']   
        c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+st+"' order by mid desc limit 2) as r order by mid")
        count=c.fetchall()
        for i in count:             
            c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
            count1=c.fetchone()
            det.append(count1) 
        c.execute("select feedback from feedback order by id desc limit 3")
        feed=c.fetchall()   
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"draft.html",{"data":data,"data1":data1,"det":det,"feed":feed})

def draft1(request):
    snd=""
    if request.session['emailid']:
        s=" "
        msg=" "
        id=request.GET.get("id")
        st="sent"
        snd=request.session['snd']
        sub=request.session['sub']
        cc=request.session['msg']
        unam=request.session['emailid']   
        c.execute("select * from registration where email='"+unam+"'")
        data=c.fetchall() 
        if(request.POST):
            to=request.POST.get("to")
            subject=request.POST.get("subject")
            msg=request.POST.get("msg")
            sdate=datetime.date.today()
            cc=encryp(msg)
            if request.FILES.get("picture"):
                    myfile=request.FILES.get("picture")
                    fs=FileSystemStorage()
                    filename=fs.save(myfile.name , myfile)              
                    uploaded_file_url = fs.url(filename)
                    picture=uploaded_file_url
                    
                    for i in cc:
                        s=s+i
                    c.execute("select email from registration where email='"+to+"'")
                    em=c.fetchone()
                    if(em is None):
                        msg="Enter valid emailid"
                    else:
                        c.execute("insert into message (msgfrom,date,sendto,subject,content,status,image) values ('"+ unam +"','"+str(sdate)+"','"+ to +"','"+ subject +"','"+s+"','"+st+"','"+ picture +"')")
                        db.commit() 
                        # subprocess.call(os.path.join(BASE_DIR,r'wusalgm\WindowsFormsApplication1\WindowsFormsApplication1\bin\Debug\WindowsFormsApplication1.exe'))
                        c.execute("delete from message where mid='"+ id+"'")
                        db.commit()
                        return HttpResponseRedirect("/inbox/")
        det=[]
        st="sent"
        unam=request.session['emailid']   
        c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+st+"' order by mid desc limit 2) as r order by mid")
        count=c.fetchall()
        for i in count:             
            c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
            count1=c.fetchone()
            det.append(count1) 
        c.execute("select feedback from feedback order by id desc limit 3")
        feed=c.fetchall()   
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"draft1.html",{"data":data,"snd":snd,"sub":sub,"s":s,"msg":msg,"det":det,"feed":feed})

def sent(request):
    if request.session['emailid']:
        s="sent"
        unam=request.session['emailid']    
        c.execute("select * from message where status='"+s+"' and msgfrom='"+unam+"'")
        data1=c.fetchall()
        unam=request.session['emailid']    
        c.execute("select * from registration where email='"+unam+"'")
        data=c.fetchall()
        det=[]
        st="sent"
        unam=request.session['emailid']   
        c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+st+"' order by mid desc limit 2) as r order by mid")
        count=c.fetchall()
        for i in count:             
            c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
            count1=c.fetchone()
            det.append(count1) 
        c.execute("select feedback from feedback order by id desc limit 3")
        feed=c.fetchall()   
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"sent.html",{"data":data,"data1":data1,"det":det,"feed":feed})

#def sent1(request):
   # if request.session['emailid']:
    #    id=request.GET.get("id")  
     #   c.execute("select date,sendto,subject from message where mid='"+id+"'")
      #  data1=c.fetchall()
       # unam=request.session['emailid']    
        #c.execute("select * from registration where email='"+unam+"'")
       # data=c.fetchall()
    #else:
     #   return HttpResponseRedirect("/login/")
    #return render(request,"sent1.html",{"data":data,"data1":data1})

def feedback(request):
    msg=""
    if request.session['emailid']:
        unam=request.session['emailid']    
        c.execute("select * from registration where email='"+unam+"'")
        data=c.fetchall()
        if(request.POST):
            msgfrom=request.session['emailid']
            msgto="admin"
            subject=request.POST.get("subject")
            feedback=request.POST.get("feedback")
            date=datetime.date.today()
            c.execute("insert into feedback (sendfrom,sendto,date,subject,feedback) values ('"+ msgfrom +"','"+ msgto +"','"+str(date)+"','"+ str(subject) +"','"+str(feedback)+"')")
            db.commit()
            msg="Feedback entered successfully"
        det=[]
        st="sent"
        unam=request.session['emailid']   
        c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+st+"' order by mid desc limit 2) as r order by mid")
        count=c.fetchall()
        for i in count:             
            c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
            count1=c.fetchone()
            det.append(count1) 
        c.execute("select feedback from feedback order by id desc limit 3")
        feed=c.fetchall()   
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"feedback.html",{"data":data,"msg":msg,"det":det,"feed":feed})

def changeimage(request):
    if request.session['emailid']:
        unam=request.session['emailid']    
        c.execute("select * from registration where email='"+unam+"'")
        data=c.fetchall()
        for d in data:
            uid=d[0]
        if(request.POST):
            if(request.FILES['img']):
                myfile=request.FILES['img']
                fs=FileSystemStorage()
                filename=fs.save(myfile.name,myfile)
                fileurl=fs.url(filename)
            c.execute("update registration set image='"+fileurl+"' where uid='"+str(uid)+"'")
            db.commit()  
            return HttpResponseRedirect("/profile/")        
        det=[]
        st="sent"
        unam=request.session['emailid']   
        c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+st+"' order by mid desc limit 2) as r order by mid")
        count=c.fetchall()
        for i in count:             
            c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
            count1=c.fetchone()
            det.append(count1) 
        c.execute("select feedback from feedback order by id desc limit 3")
        feed=c.fetchall()      
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"changeimage.html",{"data":data,"det":det,"feed":feed})

def viewfeedback(request):
    if request.session['emailid']:
        c.execute("select * from feedback")
        data=c.fetchall()
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"viewfeedback.html",{"data":data})

def userview(request):
    if request.session['emailid']:
        c.execute("select * from registration")
        data=c.fetchall()
        id=request.GET.get("id")
        status=request.GET.get("status")
        if(id):    
            c.execute("update registration set status='"+ status +"' where uid='"+id+"';")
            db.commit()
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"userview.html",{"data":data})

def profile(request):
    if request.session['emailid']:
        unam=request.session['emailid']    
        c.execute("select * from registration where email='"+unam+"'")
        data=c.fetchall()
        if(request.POST):
            return HttpResponseRedirect("/editprofile/")
        det=[]
        st="sent"
        unam=request.session['emailid']   
        c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+st+"' order by mid desc limit 2) as r order by mid")
        count=c.fetchall()
        for i in count:             
            c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
            count1=c.fetchone()
            det.append(count1) 
        c.execute("select feedback from feedback order by id desc limit 3")
        feed=c.fetchall()   
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"profile.html",{"data":data,"det":det,"feed":feed})

def editprofile(request):
    if request.session['emailid']:
        unam=request.session['emailid']    
        c.execute("select * from registration where email='"+unam+"'")
        data=c.fetchall()
        for d in data:
            uid=d[0]
        if(request.POST):
            name=request.POST["e1"]
            address=request.POST["e2"]
            dob=request.POST["e3"]
            mobile=request.POST["e5"]
            email=request.POST["e6"]
            password=request.POST["e7"]
            # if(request.FILES['img']):
            #     myfile=request.FILES['img']
            #     fs=FileSystemStorage()
            #     filename=fs.save(myfile.name,myfile)
            #     fileurl=fs.url(filename)
            c.execute("update registration set name='"+name+"',address='"+address+"',dob='"+dob+"',mobile='"+mobile+"',email='"+email+"',password='"+password+"' where uid='"+str(uid)+"'")
            db.commit()  
            return HttpResponseRedirect("/profile/")
        det=[]
        st="sent"
        unam=request.session['emailid']   
        c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+st+"' order by mid desc limit 2) as r order by mid")
        count=c.fetchall()
        for i in count:             
            c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
            count1=c.fetchone()
            det.append(count1) 
        c.execute("select feedback from feedback order by id desc limit 3")
        feed=c.fetchall()   
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"editprofile.html",{"data":data,"det":det,"feed":feed})
 
def index(request):
    return render(request,"index.html")  

def common_home(request):
    return render(request,"common_home.html")  

def admin_home(request): 
    if request.session['emailid']:
        c.execute("select count(uid) from registration")
        data=c.fetchone()
        date=datetime.date.today()
        time=datetime.datetime.today()
        z=str(time)
        c.execute("select count(id) from feedback")
        feed=c.fetchone()
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"admin_home.html",{"data":data[0],"date":date,"time":z[11:20],"feed":feed[0]}) 
   
def user_home(request):
    det=[]
    if request.session['emailid']:
        unam=request.session['emailid']    
        c.execute("select * from registration where email='"+unam+"'")
        data=c.fetchall()
        c.execute("select count(uid) from registration")
        dat=c.fetchone()
        s="sent"
        c.execute("select count(mid) from message where sendto='"+unam+"' and status='"+s+"'")
        data1=c.fetchone()
        date=datetime.date.today()
        time=datetime.datetime.today()
        z=str(time)
        c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+s+"' order by mid desc limit 2) as r order by mid")
        count=c.fetchall()
        for i in count:             
            c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
            count1=c.fetchone()
            det.append(count1)          
        c.execute("select feedback from feedback order by id desc limit 3")
        feed=c.fetchall()
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"user_home.html",{"data":data,"dat":dat[0],"data1":data1[0],"date":date,"time":z[11:20],"count":count,"det":det,"feed":feed}) 

def userbase(request):
    det=[]
    s="sent"
    unam=request.session['emailid']   
    c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+s+"' order by mid desc limit 2) as r order by mid")
    count=c.fetchall()
    for i in count:             
        c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
        count1=c.fetchone()
        det.append(count1) 
    return render(request,"userbase.html",{"det":det,"count":count}) 

def result(request):
    if request.session['emailid']:
        res=""
        unam=request.session['emailid']    
        c.execute("select * from registration where email='"+unam+"'")
        dat=c.fetchall()
        if(request.POST):
            z=request.POST.get("Search")
            s="SELECT * FROM `message` WHERE sendto like '"+z+"%' and msgfrom='"+ request.session['emailid'] +"' "
            c.execute(s)
            res=c.fetchall()
        det=[]
        st="sent"
        unam=request.session['emailid']   
        c.execute("select * from(select * from message where sendto='"+unam+"' and status='"+st+"' order by mid desc limit 2) as r order by mid")
        count=c.fetchall()
        for i in count:             
            c.execute("select name,image from registration where email='"+ str(i[2]) + "'")
            count1=c.fetchone()
            det.append(count1) 
        c.execute("select feedback from feedback order by id desc limit 3")
        feed=c.fetchall()   
    else:
        return HttpResponseRedirect("/login/")
    return render(request,"result.html",{"res":res,"dat":dat,"det":det,"feed":feed}) 


def forgot_password(request):
    data=""
    if(request.POST):
            z=request.POST["uname"]
            no=request.POST["mobile"]
            c.execute(" select count(email) from registration where email='"+z+"' and mobile='"+no+"' ")
            data=c.fetchone()
            if(data[0]>0):
               request.session['funame']=z
               return HttpResponseRedirect("/question/")
            else:
                data="Check your email or mobile"
    return render(request,"forgot_password.html",{"data":data})  

def question(request):
    msg=""
    if(request.POST):
        answer=request.POST["answer"]
        uname=request.session['funame']
        c.execute("select count(answer) from registration where email='"+uname+"' and answer='"+answer+"'")
        data=c.fetchone()
        if(data[0]>0):
            return HttpResponseRedirect("/forgotpwd/")
        else:
            msg="Enter correct answer"
    return render(request,"question.html",{"msg":msg}) 

   
def forgotpwd(request):
    msg=""
    if(request.POST):
        npass=request.POST["npass"]
        cpass=request.POST["cpass"]
        if(npass==cpass):
            c.execute("update registration set password='"+ cpass +"' where email='"+ request.session['funame'] +"'")
            db.commit()
            return HttpResponseRedirect("/login/")
        else:
            msg="Password and confirm password must match"
    return render(request,"forgotpwd.html",{"msg":msg})
    
    #ENCRYPTION AND DECRYPTION

def encryp(cc):
    e=[]
    res=[]
    encr=[]
    for d in cc:
        e.append(d)
    for z in range(0,len(e)):
        res.append(ord(e[z])+1)
    for z in range(0,len(res)):
        print(chr(res[z]),end="")
        encr.append(chr(res[z]))
    return encr     
    
def decryp(pp):
    decr=[]
    result=""
    m=[]
    for i in range(0,len(pp)):
       m.append(pp[i])
    for z in range(0,len(m)):
        decr.append(ord(m[z])-1)
    print("")
    for z in range(0,len(decr)):
        print(chr(decr[z]),end="")
        result=result+chr(decr[z])
    return result
# Create your views here.

def download(request):
    data=request.session['dd']
    
    return render(request,'download.html',{"data":data})