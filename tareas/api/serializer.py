from rest_framework import serializers
import re
import datetime
from tareas.models import User, Homework


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'

    def validate_name(self, name):
        if name == '':
            raise serializers.ValidationError('El nombre no puede estar vacio')
        if name.isalpha():
            return name
        
    def validate_last_name(self, last_name):
        if last_name == '':
            raise serializers.ValidationError(
                'El apellido no puede estar vacio')
        if last_name.isalpha():
            return last_name
             
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('Tiene que indicar un correo.')
        elif self.initial_data.get('name') in value:
            raise serializers.ValidationError(
                'El email no puede contener el nombre')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError(
                'El correo electrónico no es válido')
        return value

    def validate_phone_number(self, phone_number):
        if not phone_number:
            raise serializers.ValidationError(
                'Tiene que indicar un número de telefono.')

        pattern = re.compile(
            r'^\+?\d{0,2}\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$')

        if not pattern.match(phone_number):
            raise serializers.ValidationError(
                'El número de teléfono es inválido.')

        return phone_number

    def validate_active(self, value):
        if value != True:
            raise serializers.ValidationError("El usuario debe ser activado.")
        return value

    def validate(self, value):
        return value

    def create(self, validated_data):
        phone_number = validated_data.get('phone_number')
        email = validated_data.get('email')

        # Check if phone number or email already exist in other users
        if phone_number and User.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                'El número de teléfono ya está en uso.')
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                'El correo electrónico ya está en uso.')

        # Check if there is an inactive user with the same name
        existing_user = User.objects.filter(
            name=validated_data['name'], active=False).first()
        if existing_user:
            existing_user.active = True
            existing_user.save()
            return existing_user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.validate_active(instance.active)
        validated_data = self.validate(validated_data)
        if validated_data.get('name'):
            instance.name = validated_data.get('name').capitalize()
        if validated_data.get('active'):
            instance.active = validated_data.get('active')
        instance.save()
        return instance



class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'

    def validate_title(self, title):
        if title == '':
            raise serializers.ValidationError('El nombre no puede estar vacio')
        return title
        
        
    def validate_time(self, value):
        if not value:
            raise serializers.ValidationError('El tiempo es requerido.')
        elif value < datetime.time(hour=6) or value > datetime.time(hour=18):
            raise serializers.ValidationError('El tiempo debe estar entre las 6:00 a.m. y las 6:00 p.m.')
        return value

    def validate_active(self, value):
        if value != True:
            raise serializers.ValidationError("El usuario debe ser activado.")
        return value     
    
    def validate_user(self, user):
        if not user:
            raise serializers.ValidationError('Debe asignarle la tarea a un usuario')
        if not User.objects.filter(pk=user.pk).exists():
            raise serializers.ValidationError('El usuario ingresado no existe')
        return user

  
    
    def create(self, validated_data):
        existing_homework = Homework.objects.filter(
            title=validated_data['title'], active=False).first()
        if existing_homework:
            existing_homework.active = True
            existing_homework.save()
            return existing_homework

        return super().create(validated_data)
    
    
    
    def delete(self, instance):
        if instance.active == False:
            raise serializers.ValidationError(
                'No existe esta tarea en la base de datos')
        else:
            instance.active = False
            instance.save()
            return {'message': 'Tarea eliminada correctamente'}