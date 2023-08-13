from rest_framework import serializers
from .models import User,Product


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']
        extra_kwargs = {
            'id': {'read_only': True},
        }
        
class ProductSerializer(serializers.ModelSerializer):
		user=UserSerializer(read_only=True)
		class Meta:
			model = Product
			fields = ['id','user', 'url', 'title', 'price', 'description', 'reviews_count', 'ratings_count', 'ratings', 'media_count']
			extra_kwargs = {
				'id': {'read_only': True},
			}