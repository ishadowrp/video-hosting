from rest_framework import serializers
from .models import Media, MediaRating
from rest_framework.validators import UniqueTogetherValidator


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ('id', 'title', 'description', 'media', 'author', 'date_posted', 'views_count', 'current_rating')
        extra_kwargs = {'description': {'required': False}}
        lookup_field = 'title'


class MediaRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaRating
        fields = ('id', 'media', 'author', 'rating')
        lookup_field = 'rating'
        validators = [
                    UniqueTogetherValidator(
                        queryset=MediaRating.objects.all(),
                        fields=['media', 'author'],
                        message='You have already set a rating for this media!'
                    )
                ]
