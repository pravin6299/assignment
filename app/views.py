from rest_framework.response import Response
from .models import Post, User
from .serializers import PostSerializer, UserRegistrationSerializer, RetrieveSerializer, GetPostSerializer
from rest_framework import status
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .pagination import SetPagination
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from .permissions import IsSuperUser, IsPostOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistration(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

class UserLoginView(generics.CreateAPIView):
    def create(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.filter(username=username).first()
        if user is None:
            raise AuthenticationFailed("User Name Does Not Exist")

        if not user.check_password(password):
            raise AuthenticationFailed("Password Invalid!")
        data = {
            'id':user.id,
            'username':user.username,
            'password':user.password,
            'token': get_tokens_for_user(user)
        }
        return Response(data)
    
class GetAllPOst(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = GetPostSerializer
    pagination_class = SetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['title', 'author__username']
    search_fields = ['title', 'body']

class CreatePostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class= SetPagination
    permission_classes = [IsAuthenticated]

    def create(self, request):
        print("user",request.user)
        print("data",request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user) 
        return Response({"message":"Post Created."},status=status.HTTP_201_CREATED)       

class RetrievePost(generics.RetrieveAPIView):
    serializer_class = RetrieveSerializer
    permission_classes = [IsAuthenticated|IsPostOwnerOrReadOnly|IsSuperUser]
    pagination_class = SetPagination

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

class UpdateAPIView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # pagination_class= SetPagination
    permission_classes = [IsAuthenticated|IsSuperUser]
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)