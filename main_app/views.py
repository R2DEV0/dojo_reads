from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Book, Author, Review
import bcrypt




def index(request):
    return render(request, 'login.html')


def new_user(request):
    errors = User.objects.new_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        name= request.POST['name']
        user_name= request.POST['user_name']
        email= request.POST['email']
        password= request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        new_user = User.objects.create(name=name, user_name=user_name, email=email, password=pw_hash)
        request.session['user_id'] = new_user.id

        return redirect(f'/all_books/{new_user.id}')



def login(request):
    
    errors = User.objects.return_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    login_user_list = User.objects.filter(email=request.POST['email'])  
    logged_in_user = login_user_list[0]
    request.session['user_id'] = logged_in_user.id
    return redirect(f'/all_books/{logged_in_user.id}')



def all_books(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/') 
    
    last_three = Review.objects.all().order_by('-id')[:3]
    context = {
        'user' : User.objects.get(id=request.session['user_id']),
        'details' : Review.objects.all(),
        'books' : Book.objects.all(),
        'last_three' : last_three

    }
    return render(request, 'all_books.html', context)



def add_book(request):
    if 'user_id' not in request.session:
        return redirect('/')

    author = Author.objects.all()
    context={
        'user' : User.objects.get(id=request.session['user_id']),
        'author' : author
    }
    
    return render(request, 'add_book.html', context)



def process_new(request):

    errors = User.objects.book_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add_book')

    title = request.POST['title']
    review = request.POST['review']
    rating = request.POST['rating']
    user_id = request.session['user_id']
    
    if request.POST['new_auth'] == '':
        author = request.POST['author']
        author= Author.objects.get(id=author)
        this_book = Book.objects.create(title=title, author=author)
    else:
        added_auth = request.POST['new_auth']
        new_auth = Author.objects.create(name=added_auth)
        this_book = Book.objects.create(title=title, author=new_auth)

    this_book_id = this_book.id
    review= Review.objects.create(comment=review, rating=rating, user=User.objects.get(id=user_id), book=this_book)

    return redirect(f'/one_book/{this_book_id}')



def one_book(request, this_book_id):
    if 'user_id' not in request.session:
        return redirect('/') 

    user = User.objects.get(id=request.session['user_id'])

    book = Book.objects.get(id=this_book_id)
    author = book.author.name
    review = book.books.all()

    context = {
        'book' : book,
        'author' : author,
        'review' : review,
        'user' : user,
    }
    return render(request, 'one_book.html', context)



def add_review(request):
    user = User.objects.get(id=request.session['user_id'])
    comment = request.POST['comment']
    rating = request.POST['rating']
    book_id = request.POST['book_id']

    book_updated = Book.objects.get(id=book_id)
    Review.objects.create(comment=comment, rating=rating, user=user, book=book_updated)

    return redirect(f'/one_book/{book_id}')



def user_page(request, user_id):
    if 'user_id' not in request.session:
        return redirect('/')

    user = User.objects.get(id=user_id)
    review_count = user.users.all()
    print(review_count)
    
    count = 0
    for x in review_count:
        if [x]:
            count = count + 1
    
    context={
        'user' : user,
        'books' :user.users.all(),
        'count' : count
    }

    return render(request, 'user_page.html', context)



def logout(request):
    request.session.flush()
    return redirect('/')