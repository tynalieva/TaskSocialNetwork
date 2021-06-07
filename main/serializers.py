from rest_framework import serializers
from django.contrib.auth.models import User

from main.models import Post, Category, PostImage

from rest_framework_simplejwt.tokens import RefreshToken
#
#
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(min_length=6, write_only=True, required=True)
#     password2 = serializers.CharField(min_length=6, write_only=True, required=True)
#     # first_name = serializers.CharField(required=True)
#     # last_name = serializers.CharField(required=True)
#
#     class Meta:
#         model = User
#         fields = ('username', 'password', 'email', 'first_name', 'last_name', 'password2')
#
#     def validate_first_name(self, value):
#         if not value.istitle():
#             raise serializers.ValidationError("Name with start with uppercase")
#         return value
#
#     def validate(self, attrs):
#         password2 = attrs.pop('password2')
#         if attrs['password'] != password2:
#             raise serializers.ValidationError('Password did not match!')
#         return attrs
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             first_name=validated_data['first_name'],
#             last_name=validated_data['last_name'],
#         )
#         user.set_password(validated_data["password"])
#         user.save()
#         return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'token')

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.save()
            return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'parent')

    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     if instance.children.exists():
    #         representation['children'] = CategorySerializer(instance=instance.children.all(), many=True).data
    #
    #     return representation


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        exclude = ('id', )


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)
    images = PostImageSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body', 'owner', 'comments', 'category', 'preview','images')

    # def create(self, validated_data):
    #     print(validated_data)
    #     request = self.context.get('request')
    #     # print("File", request.FILES)
    #     images_data = request.FILES
    #     created_post = Post.objects.create(**validated_data)
    #     print(created_post)
    #     # for images_data in images_data.getlist('images'):
    #     #     PostImage.objects.create(
    #     #         post=created_post, image=images_data
    #     #     )
    #     images_obj = [PostImage(post=created_post, image=image)
    #                   for image in images_data.getlist('images')]
    #     PostImage.objects.bulk_create(images_obj)
    #     return created_post
    #
    # def validate(self, attrs):
    #     print(attrs)
    #     return super().validate(attrs)
