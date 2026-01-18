from rest_framework import serializers
from urllib.parse import urlparse


class YouTubeURLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, attrs):
        value = attrs.get(self.field)
        if value:
            parsed_url = urlparse(value)
            domain = parsed_url.netloc.lower()

            # Проверяем, что домен содержит youtube.com или youtu.be
            if not ('youtube.com' in domain or 'youtu.be' in domain):
                raise serializers.ValidationError(
                    {self.field: "Допустимы только ссылки на YouTube (youtube.com или youtu.be)"}
                )


def validate_youtube_url(value):
    if value:
        parsed_url = urlparse(value)
        domain = parsed_url.netloc.lower()

        if not ('youtube.com' in domain or 'youtu.be' in domain):
            raise serializers.ValidationError(
                "Допустимы только ссылки на YouTube (youtube.com или youtu.be)"
            )
    return value

