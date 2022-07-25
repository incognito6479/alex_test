from mainapp.models import User, Quota, Resources
from rest_framework import serializers


class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'is_superuser']


class QuotaModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quota
        fields = ['user', 'limit']


class ResourcesModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resources
        fields = ['user', 'title', 'content', 'created_at', 'slug']

    def create(self, validated_data):
        check_quota = Quota.objects.filter(user=self.context['user'])
        if check_quota:
            resources_count = Resources.objects.filter(user=self.context['user']).count()
            check_quota = check_quota.first().limit
            if resources_count == check_quota or resources_count > check_quota:
                raise serializers.ValidationError("You can not add anymore, You have reached the quota")
        obj = Resources.objects.create(**validated_data)
        if not self.context['user'].is_superuser:
            obj.user = self.context['user']
        obj.save()
        return obj
