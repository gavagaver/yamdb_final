from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title

from .validators import username_validation

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    '''Сериалайзер регистрации'''
    email = serializers.EmailField(required=True,
                                   max_length=settings.MAX_LENGHT_EMAIL)
    username = serializers.CharField(required=True,
                                     max_length=settings.MAX_LENGHT_USERNAME,
                                     validators=[username_validation])


class TokenSerializer(serializers.Serializer):
    '''Сериалайзер токена'''
    confirmation_code = serializers.CharField(required=True)
    username = serializers.CharField(required=True,
                                     max_length=settings.MAX_LENGHT_USERNAME)


class UserSerializer(serializers.ModelSerializer):
    ''' Сериалайзер пользователя'''
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserRestrictSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateSerializer(TitleSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        many=True,
        queryset=Genre.objects.all(),
    )
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name', read_only=True)
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        user = self.context['request'].user
        title = self.context['view'].kwargs['title_id']
        if Review.objects.filter(author=user, title=title).exists():
            raise serializers.ValidationError(
                'Вы уже оставили отзыв!'
            )
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True)

    class Meta:
        fields = ('id', 'author', 'pub_date', 'text')
        model = Comment
