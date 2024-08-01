from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "sender")
    information = models.CharField(max_length= 165)
    date = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f"Post{self.id} posted by {self.user} on {self.date.strftime('%d %b %Y %H %S')}"



class Follow(models.Model):
    user_follower= models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user_following")
    user=  models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user_followed")


    def __str__(self):
        return f"{self.user} is being followed by {self.user_follower}"
    

class Like(models.Model):
    user= models.ForeignKey(User, on_delete=models.CASCADE, related_name= "liked_post")
    post= models.ForeignKey(Post, on_delete=models.CASCADE, related_name= "liked_post")

    def __str__(self):
        return f"{self.user} liked {self.post}"

    
