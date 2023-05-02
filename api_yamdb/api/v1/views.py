from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg
from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework import viewsets, mixins, filters
from reviews.models import Title, Category, Genre, Review
from .serializers import (RegisterSerializer, TokenSerializer, UserSerializer,
                          TitleCreateSerializer, TitleSerializer,
                          CategorySerializer, GenreSerializer,
                          ReviewSerializer, CommentSerializer,
                          UserRestrictSerializer)
from .permissions import (IsAdminOrReadOnly, IsAdmin,
                          IsModeratorAdminAuthorOrReadOnly)
from .filters import CategoriesFilter, GenresFilter, TitlesFilter
from users.models import User


class MixinSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


@api_view(['POST'])
def register(request):
    ''' Регистрация нового пользователя
    Получить код подтверждения на переданный
    email. Права доступа'''
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    email = serializer.validated_data.get('email')
    user = User.objects.filter(email=email).first()
    if user and user.username != username:
        return Response({'Error': 'не существует username'},
                        status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.filter(username=username).first()
    if user and user.email != email:
        return Response({'Error': 'не существует email'},
                        status=status.HTTP_400_BAD_REQUEST)
    user, created = User.objects.get_or_create(username=username, email=email)
    send_mail(subject='тема',
              message=f'Confirmation code: {user.confirmation_code}',
              from_email=settings.DEFAULT_FROM_EMAIL,
              recipient_list=[user.email],
              fail_silently=False
              )
    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def get_token(request):
    ''' Получение JWT-токена
    Получение JWT-токена в обмен
    на username и confirmation code.
    Права доступа: Доступно без токена.'''
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data.get('username')
    confirmation_code = serializer.validated_data.get('confirmation_code')
    user = get_object_or_404(User, username=username)
    if confirmation_code != user.confirmation_code:
        return Response({
            'Отсутствует обязательное поле или оно некорректно'},
            status=status.HTTP_400_BAD_REQUEST)
    return Response(
        {'token': f'Bearer {RefreshToken.for_user(user).access_token}'},
        status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'head', 'patch', 'delete',
                         'options')

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=(IsAuthenticated,))
    def me(self, request):
        serializer = UserRestrictSerializer(
            self.request.user,
            request.data,
            partial=True)
        serializer.is_valid(raise_exception=True)
        if request.method == 'PATCH':
            serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(MixinSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    filterset_class = CategoriesFilter
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class GenreViewSet(MixinSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'slug')
    filterset_class = GenresFilter
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().annotate(rating=Avg('reviews__score'))
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitlesFilter
    search_fields = ('name', 'year')

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TitleCreateSerializer
        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsModeratorAdminAuthorOrReadOnly,)

    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get('title_id'))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(title=self.get_title(), author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsModeratorAdminAuthorOrReadOnly,)

    def get_review(self):
        return get_object_or_404(Review,
                                 id=self.kwargs.get('review_id', 'title_id'))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(
            review=self.get_review(), author=self.request.user
        )
