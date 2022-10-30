from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)


    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(
        Author, related_name="posts", on_delete=models.CASCADE
    )
    publish_date = models.DateTimeField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    content = models.TextField()
    post = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Comment by {}'.format(self.name)
