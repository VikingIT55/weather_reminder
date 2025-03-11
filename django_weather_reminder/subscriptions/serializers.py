from rest_framework import serializers

from subscriptions.models import City, PeriodEnum, Subscription


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    period = serializers.ChoiceField(choices=[(e.value, e.name) for e in PeriodEnum])
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def validate_period(self, value):
        try:
            return PeriodEnum(int(value))
        except ValueError:
            raise serializers.ValidationError("Invalid period value.")

    def validate(self, attrs):
        if attrs.get('delivery_method') == 'webhook' and not attrs.get('webhook_url'):
            raise serializers.ValidationError({
                'webhook_url': 'Webhook URL is required when delivery method is webhook.'
            })
        return attrs
