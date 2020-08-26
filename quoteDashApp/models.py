from django.db import models
import re, bcrypt


class UserManager(models.Manager):
    def loginValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        validationErrors = {}
        usersEmail = User.objects.filter(email = postData["email"])       
        if len(postData["email"]) == 0:
            validationErrors["emailreq"] = "User email address required."     
        elif len(usersEmail) == 0:
            validationErrors["emailnotfound"] = "Email not found. Please register first."
            print(validationErrors)
        else:
            userToCheck = usersEmail[0]     
            if bcrypt.checkpw(postData["password"].encode(), usersEmail[0].password.encode()):
                print("password matches")
            else:
                validationErrors["passwordmatch"] = "Password Incorrect"            
        return validationErrors


    def userValidator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        validationErrors = {}
        if len(postData ["fname"]) == 0:
            validationErrors["fnamereq"] = "First Name required."
        if len(postData ["lname"]) == 0:
            validationErrors["lnamereq"] = "Last Name required."
        if len(postData["email"]) == 0:
            validationErrors["emailreq"] = "Valid email address required."
        elif not EMAIL_REGEX.match(postData['email']):
            validationErrors["invalidEmail"] = "Not a valid email address.  Try again."
        else:
            repeatEmail = User.objects.filter(email = postData["email"])
            if len(repeatEmail)>0:
                validationErrors["emailTaken"] = "This email address is already registered."
        # if len(postData["password"]) < 5:
        #     validationErrors["PWreq"] = "Password Required more than 5 characters."
        # if postData["password"] != postData ["confirmPW"]:
        #     validationErrors["confirmError"] = "Passwords do not match."
        return validationErrors


class QuoteManager(models.Manager):
    def quoteValidator(self, postData):
        validationErrors = {}
        if len(postData ["author"]) < 3:
            validationErrors["quote"] = "Please enter a Author name more than 3 characters"
        if len(postData["content"]) < 10:
            validationErrors["content"] = "Please enter more than 10 characters"
        return validationErrors

class User(models.Model):
        # id - is implicit when creating models   
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()      
    def __str__(self):
        return f"UserObject--{self.firstName} {self.lastName}, {self.email}\n"

class Quote(models.Model):
    # id - is implicit when creating models
    author = models.CharField(max_length=45)
    content = models.TextField()
    user_id = models.ForeignKey(
        User, related_name="quote", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()  
    def __str__(self):
        return f"QuoteObject-{self.author}{self.content}\n"


