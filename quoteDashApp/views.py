from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import User, Quote

# Create your views here.
############################################
#               Register/Login
############################################
def index(request):
    return render(request, "loginPage.html")

def registerUser(request):
    # print(request.POST)
    validationErrors = User.objects.userValidator(request.POST)
    if len(validationErrors)>0:
        for key, value in validationErrors.items():
            messages.error(request,value)
            print(request.POST)
            print(validationErrors)
        return redirect ("/")
    else:
        #encrypt PW thennn create user        
        securePW = bcrypt.hashpw(request.POST["password"].encode(),bcrypt.gensalt()).decode()
        newUser = User.objects.create(firstName = request.POST["fname"], lastName = request.POST["lname"], email = request.POST["email"], password = securePW)
        request.session["loggedInID"] = newUser.id
    return render (request, "quoteHomepage.html")

def login(request):
    # print(validationErrors)    
    validationErrors = User.objects.loginValidator(request.POST)
    if len(validationErrors)>0:
        for value in validationErrors.values():
            messages.error(request,value) 
            print(validationErrors)       
        return redirect ("/")
    else:
        usersEmail = User.objects.filter(email = request.POST["email"]) 
        request.session["loggedInID"] = usersEmail[0].id
        return redirect("/home")

def home(request):
    if "loggedInID" not in request.session:
        messages.error(request, "You must log in first.")
        return redirect("/")
    context = {
        "loggedinuser" : User.objects.get(id = request.session["loggedInID"]),
        "authorQuote" : Quote.objects.all(),
        "userInfo" : User.objects.all()
    }
    print(request.session["loggedInID"])
    return render(request, "quoteHomepage.html", context) 

def logout(request):
    request.session.clear()
    return redirect("/")

############################################
#               quoteHomepage
############################################
def userQuotes(request):
    validationErrors = Quote.objects.quoteValidator(request.POST)
    if len(validationErrors)>0:
        for key, value in validationErrors.items():
            messages.error(request,value)
        return redirect ("/home")
    Quote.objects.create(author= request.POST['author'], content= request.POST['content'], user_id= User.objects.get(id= request.session['loggedInID']))
    print(request.POST)
    return redirect("/home")

def deleteQuote(request, quotesID):   
    b = Quote.objects.get(id=quotesID)
    b.delete()
    return redirect("/home") 

def addAuthorQuote(request):
    Quote.objects.create(
        author = request.POST['author'],
        content = request.POST['content'],
    )
    print(request.POST)
    return redirect('/home')
    
def editUserAcct(request, userID):
    context = {
        "loggedinuser" : User.objects.get(id=userID)
    }
    return render(request, "editUserAcct.html", context)

def updateUser(request, userID):
    print(request.POST)
    user = User.objects.get(id = request.session["loggedInID"])
    validationErrors = User.objects.userValidator(request.POST)  
    print('*'*25)
    if len(validationErrors) > 0:
        for key, value in validationErrors.items():
            messages.error(request, value)
            print(validationErrors)
        return redirect(f"/editUserAcct/{user.id}")
    else:
        user.firstName = request.POST['fname']
        user.lastName = request.POST['lname']
        user.email = request.POST['email']
        user.save()
    return redirect("/home")


def loggedUserQuotes(request, userID):
    context = {
        "loggedinuser" : User.objects.get(id = request.session["loggedInID"]),
        "specificuser" : User.objects.get(id=userID)
    }
    return render(request, "loggedUserQuotes.html", context)


# {% for items in allUserQuotes %}
# {% endfor %}

