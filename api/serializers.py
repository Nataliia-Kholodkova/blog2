from rest_framework import serializers


from news.models import Post, Comment, Tag, Category
from users.models import User
from django.db.models import Q

# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


category_choices = [(values['title'].lower(), values['title']) for values in
                    Category.objects.all().order_by('title').values('title')]
tag_choices = [(value['tag'], value['tag']) for value in Tag.objects.all().order_by('tag').values('tag')]
category_choices_multiple = [('category', values['title']) for values in
                             Category.objects.all().order_by('title').values('title')]
def create_comment_serializer(user, post_id, parent_id=None):
    class CommentCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = ('id', "text")
        def __init__(self, *args, **kwargs):
            self.post_id = post_id
            self.parent_object = None
            if parent_id:
                parent_queryset = Comment.objects.filter(id=parent_id)
                if parent_queryset.exists() and parent_queryset.count() == 1:
                    self.parent_object = parent_queryset.first()
                else:
                    raise serializers.ValidationError('Invalid comment id to reply on')
            return super().__init__(*args, **kwargs)

        def validate(self, attrs):
            self.post_object = None

            post_queryset = Post.objects.filter(id=self.post_id)
            print(post_queryset)
            if post_queryset.exists() and post_queryset.count() == 1:
                self.post_object = post_queryset.first()
            else:
                raise serializers.ValidationError('Invalid post id')
            return attrs

        def create(self, validated_data):

            text = validated_data.get("text")
            main_user = user
            parent_obj = self.parent_object
            post_obj = self.post_object
            comment = Comment.objects.create(
                text=text, user=main_user,
                parent=parent_obj, post=post_obj
            )
            comment.save()
            return comment
    return CommentCreateSerializer



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'firstname', 'lastname', 'username'
        )


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'username', 'email', 'firstname', 'lastname', 'password1', 'password2',
        )

    def validate_password1(self, value):
        data = self.get_initial()
        password1 = data.get('password1', None)
        password2 = data.get('password2', None)
        if (not password1 or not password2) or password1 != password2:
            raise serializers.ValidationError('Passwords must match.')
        return value

    def create(self, validated_data):
        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        return self.Meta.model.objects.create_user(**data)


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    token = serializers.CharField(allow_blank=True, read_only=True)


    class Meta:
        model = User
        fields = (
            'email', 'password', 'token'
        )

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        user = User.objects.filter(email=email).distinct()
        if user.exists() and user.count() == 1:
            user = user.first()
        else:
            raise serializers.ValidationError('Invalid email')
        if user:
            if not user.check_password(password):
                raise serializers.ValidationError('Invalid password')
        data['token'] = 'SOME TOKEN'
        return data



class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = serializers.SerializerMethodField()
    class Meta:
        model = Comment
        fields = ('id', 'post', 'user', "text", 'replies')

    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.replies.all(), many=True).data
        return []




class CommentChildSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('user', "text", 'id')


class PostDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    user = UserSerializer()
    tags = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()


    class Meta:
        model = Post
        fields = ('user', "title", "description", "text", "keywords", "category", "tags",
                  'created', 'comments', "is_approved", 'id')

    def get_comments(self, obj):
        comments = obj.comments.all()
        comments = comments.filter(parent=None)
        return CommentSerializer(comments, many=True).data

    def get_category(self, obj):
        return obj.category.title

    def get_tags(self, obj):
        tags = obj.tags.all().values('tag')
        return tags

class PostSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ("user", "title", "description", "text", "keywords", "category", "tags")

    def get_category(self, obj):
        return obj.category.title

    def get_tags(self, obj):
        tags = obj.tags.all().values('tag')
        return tags

    def get_user(self, obj):
        return obj.user.id


# class LoginSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super().get_token(user)
#         user_data = UserSerializer(user).data
#         for key, value in user_data.items():
#             if key != 'id':
#                 token[key] = value
#         return token
