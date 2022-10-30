from graphene_django import DjangoObjectType;
import graphene
from my_app.models import Post as PostModel
from my_app.models import Author as AuthorModel
from my_app.models import Comment as CommentModel

class Comment(DjangoObjectType):
    class Meta:
        model = CommentModel
        fields = ['id', 'name', 'email', 'content', 'created', 'post']

class Post(DjangoObjectType):
    class Meta:
        model = PostModel
        fields = ['id', 'title', 'description', 'author', 'publish_date', 'comments']
    def resolve_comments(self, info):
        return CommentModel.objects.filter(post=self)

class Author(DjangoObjectType):
    class Meta:
        model = AuthorModel
        fields = ['id', 'name', 'posts']
    def resolve_posts(self, info):
        return PostModel.objects.filter(author=self)

    @classmethod

    def get_node(cls, info, id):
        return AuthorModel.objects.get(id=id)

class AuthorInput(graphene.InputObjectType):
    author_id = graphene.ID()

class CreateAuthor(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    author = graphene.Field(Author)

    @classmethod
    def mutate(cls, root, info, **user_data):
        author_instance = AuthorModel(
            name=user_data.get('name')
        )
        author_instance.save()
        return CreateAuthor(author=author_instance)

class CreatePost(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()
        publish_date = graphene.DateTime()
        author_id = graphene.ID()

    post = graphene.Field(Post)

    @classmethod
    def mutate(cls, root, info, **user_data):
        post_instance = PostModel(
            title=user_data.get('title'),
            description=user_data.get('description'),
            publish_date=user_data.get('publish_date'),
            author_id=user_data.get('author_id')
        )
        post_instance.save()
        return CreatePost(post=post_instance)

class CreateComment(graphene.Mutation):
    class Arguments:
        name = graphene.String()
        email = graphene.String()
        content = graphene.String()
        created = graphene.DateTime()
        post_id = graphene.ID()

    comment = graphene.Field(Comment)

    @classmethod
    def mutate(cls, root, info, **user_data):
        comment_instance = CommentModel(
            name=user_data.get('name'),
            email=user_data.get('email'),
            content=user_data.get('content'),
            created=user_data.get('created'),
            post_id=user_data.get('post_id')
        )
        comment_instance.save()
        return CreateComment(comment=comment_instance)

class DeleteComment(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
    comment = graphene.Field(Comment)

    @staticmethod
    def mutate(root, info, **user_data):
        comment_instance = CommentModel.objects.get(pk=user_data.get('id'))
        comment_instance.delete()

        return DeleteComment(ok=True)

class UpdatePost(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        description = graphene.String()

    post = graphene.Field(Post)

    @staticmethod
    def mutate(root, info, **user_data):
        post_instance = PostModel.objects.get(pk=user_data.get('id'))

        if post_instance:
            post_instance.title = user_data.get('title')
            post_instance.description = user_data.get('description')
            post_instance.save()

            return UpdatePost(post=post_instance)
        return UpdatePost(post=post_instance)


class Mutation(graphene.ObjectType):
    """
    This class contains the fields of models that are supposed to be
    mutated.
    """
    create_post = CreatePost.Field()
    create_author = CreateAuthor.Field()
    update_post = UpdatePost.Field()
    create_comment = CreateComment.Field()
    delete_comment = DeleteComment.Field()


class Query(graphene.ObjectType):
    authors = graphene.List(Author)
    posts = graphene.List(Post)
    comments = graphene.List(Comment)
    post = graphene.Field(Post, post_id=graphene.Int())

    def resolve_authors(self, info):
        return AuthorModel.objects.all()

    def resolve_posts(self, info):
        return PostModel.objects.all()

    def resolve_comments(self, info):
        return CommentModel.objects.all()

    def resolve_post(self, info, post_id):
        return PostModel.objects.get(pk=post_id)

schema = graphene.Schema(query=Query, mutation=Mutation)
