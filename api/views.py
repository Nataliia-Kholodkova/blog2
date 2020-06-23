from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

from news.models import Post, Comment
from users.models import User
from .permissions import IsOwner
from .serializers import (
    PostSerializer, CommentSerializer, PostDetailSerializer, create_comment_serializer,
    UserCreateSerializer, UserLoginSerializer
)

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

class UserLoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)




# class PostListView(APIView):
#     def get(self, request):
#         post = Post.objects.filter(is_approved=True, is_editing_approved=True)
#         serializer = PostSerializer(post, many=True)
#         return Response(serializer.data)

class PostListView(ListAPIView):
    queryset = Post.objects.all()
    # queryset = Post.objects.filter(is_approved=True, is_editing_approved=True)
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny]


class PostDetailView(RetrieveAPIView):
    queryset = Post.objects.filter()
    serializer_class = PostDetailSerializer


class PostCreateView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class PostUpdateView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwner, IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostDeletelView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwner, IsAuthenticated]

class CommentDetailView(RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

class CommentPostView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        comments = Comment.objects.filter(post__pk=pk, parent__isnull=True)
        if comments:
            serialiser = CommentSerializer(Comment.objects.filter(post__pk=pk, parent__isnull=True), many=True)
            return Response(serialiser.data, status=HTTP_200_OK)
        return Response("Error. No such post", status=HTTP_400_BAD_REQUEST)



class CommentCreateView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        post_id = self.request.GET.get('post_id', None)
        parent_id = self.request.GET.get('parent_id', None)
        return create_comment_serializer(user=self.request.user, post_id=post_id, parent_id=parent_id)


class CommentUpdateView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner, IsAuthenticated]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CommentDeletelView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsOwner, IsAuthenticated]



    # {"user": {"email": "dan@ukr.net", "password": "aqswdefr"}, "text": "TEST API", "post":10}
