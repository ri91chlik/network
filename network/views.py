from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.http import JsonResponse
from .models import User, Post, Follow, Like

def delete_like(request, post_id):
    post= Post.objects.get(pk=post_id)
    user= User.objects.get(pk=request.user.id)
    like= Like.objects.filter(user=user, post=post)
    like.delete()
    return JsonResponse({"message": "deleted"})
    


def append_like(request, post_id):
    post= Post.objects.get(pk=post_id)
    user= User.objects.get(pk=request.user.id)
    current_like=Like(user=user, post=post)
    current_like.save()
    return JsonResponse({"message": "liked"})



def edit(request, post_id):
    if request.method== "POST":
        data= json.loads(request.body)
        edit_post= Post.objects.get(pk=post_id)
        edit_post.information= data["information"]
        edit_post.save()
        return JsonResponse({"message": "Jesus is the Lord", "data": data["information"]})







def index(request):
    all_posts = Post.objects.all().order_by("id").reverse()
    # paginator
    paginator= Paginator(all_posts, 10)
    page_number= request.GET.get('page')
    page_posts= paginator.get_page(page_number)

    all_liked_posts= Like.objects.all()
    individual_likes= []

    try:
        for liked_post in all_liked_posts:
            if liked_post.user.id == request.user.id:
                individual_likes.append(liked_post.post.id)
    except:
        individual_likes= []

        

    return render(request, "network/index.html", { 
        "all_posts": all_posts,
        "page_posts":page_posts,
        "individual_likes":individual_likes,
    })




def new_post(request):
    if request.method == "POST":
        information = request.POST['information']
        user = User.objects.get(pk=request.user.id)
        post= Post(information= information, user=user)
        post.save()
        return  HttpResponseRedirect(reverse(index))




def profile(request, user_id):
    user= User.objects.get(pk=user_id)
    all_posts= Post.objects.filter(user=user).order_by("id").reverse()

  
    following= Follow.objects.filter(user=user)
    followers= Follow.objects.filter(user_follower=user)


    try:
        verify_follow= followers.filter(user=User.objects.get(pk=request.user.id))
        if len(verify_follow) != 0:
            is_following = True
        else: 
            is_following = False
    except:
            is_following != True


    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    page_posts= paginator.get_page(page_number)
    return render(request, "network/profile.html", { 
                "all_posts":all_posts,
                "page_posts":page_posts,
                "username":user.username,
                "following":following,
                "followers":followers,
                "is_following":is_following,
                "user_identity":user,
                
    })        


def follow(request):
    follow1= request.POST['follow1']
    presentUser= User.objects.get(pk=request.user.id)
    follow1_info= User.objects.get(username=follow1)
    userInfo= Follow(user=presentUser, user_follower=follow1_info)
    userInfo.save()
    user_id= follow1_info.id

    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))


def unfollow(request):
    follow1= request.POST['follow1']
    presentUser= User.objects.get(pk=request.user.id)
    follow1_info= User.objects.get(username=follow1)
    userInfo= Follow.objects.get(user=presentUser, user_follower=follow1_info)
    userInfo.delete()
    user_id= follow1_info.id

    return HttpResponseRedirect(reverse(profile, kwargs={'user_id':user_id}))


def following(request):
    presentUser= User.objects.get(pk=request.user.id)
    followers= Follow.objects.filter(user=presentUser)
    all_posts= Post.objects.all().order_by('id').reverse()
    posts_of_presentUser=[]

    for post in all_posts:
        for individual in followers:
            if individual.user_follower== post.user:
                posts_of_presentUser.append(post)

    paginator = Paginator(posts_of_presentUser, 10)
    page_number = request.GET.get('page')
    page_posts= paginator.get_page(page_number)
    return render(request, "network/following.html", { 
                 "page_posts":page_posts,
    })






def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")