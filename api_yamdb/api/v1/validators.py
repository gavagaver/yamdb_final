import re

from rest_framework import serializers


def username_validation(username):
    username_not_valid = 'me'
    if username == username_not_valid:
        raise serializers.ValidationError({'username': 'такой username нельзя'
                                          'использовать'})
    if not re.match(r'^[\w.@+-]+\Z', username):
        raise serializers.ValidationError(
            {'username': 'Letters, digits and @/./+/-/_ only.'})
