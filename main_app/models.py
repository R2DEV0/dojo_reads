from django.db import models
import re, bcrypt


class ShowManager(models.Manager):
    def new_validator(self, postData):
        user = User.objects.filter(email=postData['email'])
        errors= {}

        if (len(postData['name']) < 2):
            errors['name'] = 'Name must be at least 2 characters long.'
        
        if (len(postData['user_name']) < 2):
            errors['user_name'] = 'User name must be at least 2 characters long.'
        
        if (len(postData['password']) < 8):
            errors['password'] = 'Password must be at least 8 characters long.'
        
        if postData['confirmed_pass'] != postData['password']:
            errors['password'] = 'Password must match the confirmation.'

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):       
            errors['email'] = "Invalid email address."

        if user:
            errors['email'] = "Email already registered"
        else:
            pass

        if user:
            errors['user_name'] = "User name is already registered"
        else:
            pass

        return errors


    def return_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['email'])

        if (len(postData['email']) < 1):
            errors['email'] = "No email was entered."
        if (len(postData['password']) < 1):
            errors['password'] = "No password was entered."
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(postData['password'].encode(), logged_user.password.encode()):
                return errors
            else:
                errors['no_pass'] = 'Incorrect password'
        errors['no_email'] = 'Email is not registered'
        return errors


    def book_validator(self, postData):
        errors = {}
        if (len(postData['title']) < 2):
            errors['title'] = 'Book title must be at least 2 characters'
        if (len(postData['new_auth']) > 0) and (len(postData['new_auth']) < 2):
            errors['new_auth'] = 'Author name must be at least 2 characters'
        if (len(postData['review']) < 10):
            errors['review'] = 'Review must have at least 10 characters'
        return errors




class User(models.Model):
    name= models.CharField(max_length=255)
    user_name= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    password= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)
    objects = ShowManager()


class Author(models.Model):
    name= models.CharField(max_length=255)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)


class Book(models.Model):
    title= models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='authors', on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)


class Review(models.Model):
    comment= models.CharField(max_length=455)
    rating= models.IntegerField()
    user= models.ForeignKey(User, related_name='users', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, related_name='books', on_delete=models.CASCADE)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)