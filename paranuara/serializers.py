from rest_framework import serializers

from paranuara.models import Person, Company, Food


class PersonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ('id', 'name')


class PersonContactDetailSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField(source='get_age')

    class Meta:
        model = Person
        fields = ('id', 'name', 'age', 'address', 'phone')


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('id', 'name')


class CompanyDetailSerializer(serializers.ModelSerializer):
    employees = PersonContactDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ('id', 'name', 'employees')


class PersonFoodDetailSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField(source='get_age')
    username = serializers.ReadOnlyField(source='name')
    fruits = serializers.SerializerMethodField()
    vegetables = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ('username', 'age', 'fruits', 'vegetables')

    def get_fruits(self, obj):
        return self.get_favorite_foods(obj, Food.TYPE_FRUIT)

    def get_vegetables(self, obj):
        return self.get_favorite_foods(obj, Food.TYPE_VEGETABLE)

    def get_favorite_foods(self, obj, food_type):
        foods = []
        for food in obj.favorite_foods.filter(type=food_type):
            foods.append(food.name)
        return foods
