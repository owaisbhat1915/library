from enum import unique
from itertools import count
import json
from typing import List
from urllib import response
from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from pymongo import MongoClient
import jwt
from django.core.mail import send_mail
import math, random
from datetime import date
import requests
# Create your views here.
from django.shortcuts import redirect
def generateOTP() :
     digits = "0123456789"
     OTP = ""
     for i in range(4) :
         OTP += digits[math.floor(random.random() * 10)]
     return OTP




# myclient = pymongo.MongoClient("mongodb://localhost:27017/Library")
myclient = MongoClient('you mongo db server link')

# user 

mydb = myclient["UserInfo"]
mycol = mydb["user"]
mycol.create_index('email', unique = True)

# books 
Bookdb=myclient['Book_Db']
Books=Bookdb['book']
Books.create_index('Book_name', unique = True)

# feedback
FeedbackDb=myclient['Feedback_Db']
feedback=FeedbackDb['feedback']


async def login(request):
    return render(request,'login.html')
async def register(request):
    return render(request,'register.html')
async def home(request):
    try:
        if(request.method=='POST'):
            email=request.POST.get('email')
            password=request.POST.get('password')
            data = mycol.find_one({'email':email})
            if(data['password']==password):
                encoded_jwt = jwt.encode({"email": email}, "LibraryAMO", algorithm="HS256")
                if(data['role']=='User'):
                    response=render(request,'home.html')
                    response.set_cookie('Email', encoded_jwt) 
                    return  response
                else:
                    response=render(request,'Admin.html')
                    response.set_cookie('Email', encoded_jwt)
                    return response
            
            else:
                return  render(request,'error.html')
        if(request.method=='GET'):
            try:
                encoded_jwt=request.COOKIES['Email'] 
                decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
                data = mycol.find_one({'email':decoded['email']})
                if(data['email']==decoded['email']):
                    if(data['role']=='User'):
                        return render(request,'home.html')
                    else:
                        return render(request,'Admin.html')

                else:
                    return  render(request,'error.html') #not login
            except:
                return  render(request,'error.html')
    except:
        return  render(request,'error.html') 

         

    
async def newUser(request):
    if(request.method=='POST'):

        name=request.POST.get('userName')
        email=request.POST.get('email')
        role=request.POST.get('role')
        password=request.POST.get('password1')
        Cpassword=request.POST.get('password2')
        if(password==Cpassword):
            mydict = { "name": name, "email":email ,"password":password,"role":role,'issue_Books':[],'history':[]}
            encoded_jwt = jwt.encode(mydict, "LibraryAMO", algorithm="HS256")

            response=render(request,'otp.html')

            response.set_cookie('Detail', encoded_jwt)

            o=generateOTP()

            Otp_en = jwt.encode({"Otp":o}, "LibraryAMO", algorithm="HS256")

            response.set_cookie('OTPv', Otp_en)

            # send_mail('OTP request',o,'narotta2003@gmail.com',[email], fail_silently=False, html_message="your otp is "+o)

            send_mail( 'OTP request', "your otp is "+o,'narotta2003@gmail.com', [email] )
            return  response
        else:
            return  render(request,'error.html')
    else:
        return  render(request,'error.html')

# async def Admin(request):
#     return render(request,'Admin.html')
async def Otp(request):
    try:
        return render(request,'otp.html')
    except:
        return  render(request,'error.html') 
async def OtpVari(request):
    try:        
        Otp1=request.POST.get('Otp')
        otp2=encoded_Otp=request.COOKIES['OTPv'] 
        decoded_otp=jwt.decode(encoded_Otp, "LibraryAMO", algorithms=["HS256"])
        detail=encoded_Otp=request.COOKIES['Detail'] 
        decoded_detail=jwt.decode(detail, "LibraryAMO", algorithms=["HS256"])
        if(Otp1==decoded_otp['Otp']):
            x=mycol.insert_one(decoded_detail)
            response=render(request,'login.html')
            response.delete_cookie('OTPv')
            response.delete_cookie('Detail')
            return response
        else:
            return  render(request,'error.html')
    except:
        return  render(request,'error.html')

async def error(request):
    return  render(request,'error.html')
async def insertBook(request):
    if(request.method=='GET'):
        try:
            encoded_jwt=request.COOKIES['Email'] 
            decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
            data = mycol.find_one({'email':decoded['email']})
            if(data['email']==decoded['email']):
                if(data['role']=='Admin'):
                    return render(request,'insertBook.html')
                else:
                    return  render(request,'error.html') 
            else:
                return  render(request,'error.html') #not login
        except:
            return  render(request,'error.html') 
    else:
        return  render(request,'error.html') 
async def searchBook(request):
    if(request.method=='GET'):
        try:
            encoded_jwt=request.COOKIES['Email'] 
            decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
            data = mycol.find_one({'email':decoded['email']})
            if(data['email']==decoded['email']):
                if(data['role']=='Admin' ):
                    x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/insertBook','Insert book'],['/history','History'],['/FeedbackList','Feedback list'],['/LogOut','Log out']]}
                    return render(request,'searchBook.html',x)
                elif(data['role']=='User'):
                    x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/history','History'],['/LogOut','Log out']]}
                    return render(request,'searchBook.html',x)
                else:
                    return  render(request,'error.html') 
            else:
                return  render(request,'error.html') #not login
        except:
            return  render(request,'error.html') 
    else:
        return  render(request,'error.html') 

async def insert(request):
    try:
        data=json.load(request)
        Book_name=data['Book_name']
        Author_name = data['Author_name']
        Type = data['Type']
        Description =data['Description']
        try:
            Books.insert_one({'Book_name':Book_name,'Author_name':Author_name,'Type':Type,'Description':Description,'curr':0,'total':1})
            return JsonResponse({'status':True})
        except:
            for x in Books.find({'Book_name':Book_name,'Author_name':Author_name}):
                print(x)
                Books.update_one({'Book_name':Book_name,'Author_name':Author_name},{ "$set": { "total": x['total']+1 } })
            return JsonResponse({'status':True})
    except:
        return JsonResponse({'status':False})
async def profile(request):
    try:
        encoded_jwt=request.COOKIES['Email'] 
        decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
        data = mycol.find_one({'email':decoded['email']})
        if(data['email']==decoded['email']):
            if(data['role']=='Admin' ):
                x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/insertBook','Insert book'],['/history','History'],['/FeedbackList','Feedback list'],['/LogOut','Log out']],'name':data['name'],'email':data['email'],'role':data['role']}
                return render(request,'profile.html',x)
            elif(data['role']=='User'):
                x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/history','History'],['/LogOut','Log out']],'name':data['name'],'email':data['email'],'role':data['role']}
                return render(request,'profile.html',x)
            else:
                return  render(request,'error.html') 
        else:
            return  render(request,'error.html')
    except:
        return  render(request,'error.html')
async def search(request):
    try:
        data=json.load(request)
        result=[]
        # print(data)
        for x in Books.find(data,{'_id':0,'Book_name':1,'Author_name':1,'Type':1,'Description':1,'curr':1,'total':1}):
            if(x['total']>x['curr']):
                result.append(x)
        return JsonResponse({'status':True,'Books_data':result})
    except:
        return JsonResponse({'status':False})


async def issueBook(request):
    try:
        data=json.load(request)
        for x in Books.find(data,{'_id':0,'Book_name':1,'Author_name':1,'Type':1,'Description':1,'curr':1,'total':1}):
            if(x['total']>x['curr']):
                encoded_jwt=request.COOKIES['Email'] 
                decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
                data1 = mycol.find_one({'email':decoded['email']})
                if(data1['email']==decoded['email']):
                    List=data1['issue_Books']
                    if(data in List):
                        return JsonResponse({'status':False})
                    today = date.today()
                    d2 = today.strftime("%B %d, %Y")
                    issue_data=data1['issue_Books']
                    issue_data.append(data)
                    history_data={'Date':d2,'Book_name':data['Book_name'],'Author_name':data['Author_name'],'Status':'Issue'}
                    history_val=data1['history']
                    history_val.append(history_data)
                    mycol.update_one({'email':data1['email']},{"$set": { 'issue_Books':issue_data,'history':history_val}})
                    Books.update_one(data,{ "$set": { "curr": x['curr']+1}})
        return JsonResponse({'status':True})
    except:
        return JsonResponse({'status':False})
async def returnBook(request):
    try:
        encoded_jwt=request.COOKIES['Email'] 
        decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
        data = mycol.find_one({'email':decoded['email']})
        if(data['email']==decoded['email']):
                if(data['role']=='Admin' ):
                    x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/insertBook','Insert book'],['/history','History'],['/FeedbackList','Feedback list'],['/LogOut','Log out']]}
                    return render(request,'returnBook.html',x)
                elif(data['role']=='User'):
                    x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/history','History'],['/LogOut','Log out']]}
                    return render(request,'returnBook.html',x)
                else:
                    return  render(request,'error.html') 
        else:
            return  render(request,'error.html')
    except:
        return  render(request,'error.html')
    
async def ReturnBook_list(request):
    try:
        encoded_jwt=request.COOKIES['Email'] 
        decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
        data = mycol.find_one({'email':decoded['email']})
        if(data['email']==decoded['email']):
            List=data['issue_Books']
            if(len(List)!=0):
                return  JsonResponse({'status':True,'list':data['issue_Books']})
            else:
                return JsonResponse({'status':False})
        else:
            return JsonResponse({'status':False})
    except:
        return JsonResponse({'status':False})

async def return_issue_book(request):
    try:
        data=json.load(request)
        encoded_jwt=request.COOKIES['Email'] 
        decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
        data1 = mycol.find_one({'email':decoded['email']})
        if(data1['email']==decoded['email']):
            List=data1['issue_Books']
            List.remove(data)
            today = date.today()
            d2 = today.strftime("%B %d, %Y")
            history_data={'Date':d2,'Book_name':data['Book_name'],'Author_name':data['Author_name'],'Status':'Return'}
            history_val=data1['history']
            history_val.append(history_data)
            mycol.update_one({'email':data1['email']},{"$set": { 'issue_Books':List,'history':history_val}})
            x=Books.find_one(data)
            Books.update_one(data,{ "$set": { "curr": x['curr']-1}})
            return JsonResponse({'status':True})
    except:
        return JsonResponse({'status':False})
async def history(request):
    try:
        encoded_jwt=request.COOKIES['Email'] 
        decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
        data = mycol.find_one({'email':decoded['email']})
        if(data['email']==decoded['email']):
                if(data['role']=='Admin' ):
                    x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/insertBook','Insert book'],['/history','History'],['/FeedbackList','Feedback list'],['/LogOut','Log out']]}
                    return render(request,'history.html',x)
                elif(data['role']=='User'):
                    x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/history','History'],['/LogOut','Log out']]}
                    return render(request,'history.html',x)
                else:
                    return  render(request,'error.html') 
        else:
            return  render(request,'error.html')
    except:
        return  render(request,'error.html')

async def BookHistory_list(request):
    try:
        encoded_jwt=request.COOKIES['Email'] 
        decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
        data = mycol.find_one({'email':decoded['email']})
        if(data['email']==decoded['email']):
            List=data['history']
            
            if(len(List)!=0):
                return  JsonResponse({'status':True,'list':data['history']})
            else:
                return JsonResponse({'status':False})
        else:
            return JsonResponse({'status':False})
    except:
        return JsonResponse({'status':False})


async def LogOut(request):
    response= redirect('/')
    response.delete_cookie('Email')
    return response

async def FeedSubmit(request):
    try:
        data=json.load(request)
        feedback.insert_one(data)
        return JsonResponse({'status':True})
    except:
        return JsonResponse({'status':False})

async def FeedbackList(request):
    if(request.method=='GET'):
        try:
            encoded_jwt=request.COOKIES['Email'] 
            decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
            data = mycol.find_one({'email':decoded['email']})
            if(data['email']==decoded['email']):
                if(data['role']=='Admin'):
                    return render(request,'FeedbackList.html')
                else:
                    return  render(request,'error.html') 
            else:
                return  render(request,'error.html') #not login
        except:
            return  render(request,'error.html') 
    else:
        return  render(request,'error.html') 


async def Feedback_list(request):
    try:
        encoded_jwt=request.COOKIES['Email'] 
        decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
        data = mycol.find_one({'email':decoded['email']})
        if(data['email']==decoded['email']):
            List=[]
            for x in feedback.find({},{'_id': 0, 'Email': 0,  'Phone': 0}):
                List.append(x)
            if(len(List)!=0):
                return  JsonResponse({'status':True,'list':List})
            else:
                return JsonResponse({'status':False})
        else:
            return JsonResponse({'status':False})
    except:
        return JsonResponse({'status':False})

async def AboutUs(request):
    try:
        encoded_jwt=request.COOKIES['Email'] 
        decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
        data = mycol.find_one({'email':decoded['email']})
        if(data['email']==decoded['email']):
            if(data['role']=='Admin' ):
                x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/insertBook','Insert book'],['/history','History'],['/FeedbackList','Feedback list'],['/LogOut','Log out']],'name':data['name'],'email':data['email'],'role':data['role']}
                return render(request,'AboutUs.html',x)
            elif(data['role']=='User'):
                x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/history','History'],['/LogOut','Log out']],'name':data['name'],'email':data['email'],'role':data['role']}
                return render(request,'AboutUs.html',x)
            else:
                return  render(request,'error.html') 
        else:
            return  render(request,'error.html')
    except:
        return  render(request,'error.html')
async def Ebooks(request):
    try:
        encoded_jwt=request.COOKIES['Email'] 
        decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
        data = mycol.find_one({'email':decoded['email']})
        if(data['email']==decoded['email']):
            if(data['role']=='Admin' ):
                x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/insertBook','Insert book'],['/history','History'],['/FeedbackList','Feedback list'],['/LogOut','Log out']]}
                return render(request,'Ebooks.html',x)
            elif(data['role']=='User'):
                x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/history','History'],['/LogOut','Log out']]}
                return render(request,'Ebooks.html',x)
            else:
                return  render(request,'error.html') 
        else:
            return  render(request,'error.html')
    except:
        return  render(request,'error.html')




async def EbooksBookName(request):
    try:
        query = request.GET.get('data')
        encoded_jwt=request.COOKIES['Email'] 
        decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
        data = mycol.find_one({'email':decoded['email']})
        if(data['email']==decoded['email']):
            bookData = Books.find_one({'Book_name':query})
            if(data['role']=='Admin' ):
                x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/insertBook','Insert book'],['/history','History'],['/FeedbackList','Feedback list'],['/LogOut','Log out']],'name':query,'Description':bookData['Description'],'Author_name':bookData['Author_name']}
                return render(request,'book.html',x)
            elif(data['role']=='User'):
                x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/history','History'],['/LogOut','Log out']],'name':query,'Description':bookData['Description'],'Author_name':bookData['Author_name']}
                return render(request,'book.html',x)
            else:
                return  render(request,'error.html') 
        else:
            return  render(request,'error.html')
    except:
        return  render(request,'error.html')


     

async def Ebook_list(request):
    try:
        List=set()
        for x in Books.find({},{'_id':0,'Book_name':0,'Author_name':0,'Description':0,'curr':0,'total':0}):
            List.add(str(x['Type']))
        if(len(List)!=0):
            # print(type(List))
            list2=dict()
            for i in List:
                list2.update({str(i):[]})
            for x in Books.find({},{'_id':0,'curr':0,'total':0}):
                temp=list2[x['Type']]
                temp.append(x['Book_name'])
                list2[x['Type']]=temp
            # print(list2)
            return  JsonResponse({'status':True,'list':list2})
        else:
            return JsonResponse({'status':False})
    except:
        return JsonResponse({'status':False})

async def news(request):
    try:
        encoded_jwt=request.COOKIES['Email'] 
        decoded=jwt.decode(encoded_jwt, "LibraryAMO", algorithms=["HS256"])
        data = mycol.find_one({'email':decoded['email']})
        if(data['email']==decoded['email']):
            if(data['role']=='Admin' ):
                x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/insertBook','Insert book'],['/history','History'],['/FeedbackList','Feedback list'],['/LogOut','Log out']]}
                return render(request,'news.html',x)
            elif(data['role']=='User'):
                x={'para':[['/profile','Profile'],['/returnBook','Return book'],['/searchBook','Search book'],['/history','History'],['/LogOut','Log out']]}
                return render(request,'news.html',x)
            else:
                return  render(request,'error.html') 
        else:
            return  render(request,'error.html')
    except:
        return  render(request,'error.html')


async def newsList(request):
    try:
        response = requests.get("https://newsapi.org/v2/top-headlines?country=in&apiKey=yourapikey",auth=('user', 'pass')).json()
        return  JsonResponse(response)
    except:
        return JsonResponse({'status':False})
