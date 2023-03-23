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
        name = name.strip().title()  # Convierte la primera letra de cada palabra a mayúscula
        if not all(word.isalpha() for word in name.split()):
            raise serializers.ValidationError('El nombre solo puede contener letras')
        return name

    def validate_last_name(self, last_name):
        if last_name == '':
            raise serializers.ValidationError(
                'El apellido no puede estar vacio')
        last_name = last_name.strip().title()  # Convierte la primera letra de cada palabra a mayúscula
        if not all(word.isalpha() for word in last_name.split()):
            raise serializers.ValidationError('El apellido solo puede contener letras')
        return last_name


             
    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('Tiene que indicar un correo.')
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

        name = validated_data.get('name', '').capitalize()
        last_name = validated_data.get('last_name', '').capitalize()
        user = User.objects.create(
            name=name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            active=True
        )
        return user

    def update(self, instance, validated_data):
        self.validate_active(instance.active)
        validated_data = self.validate(validated_data)

        if validated_data.get('name'):
            validated_data['name'] = ' '.join(word.capitalize() for word in validated_data['name'].split())

        if validated_data.get('last_name'):
            validated_data['last_name'] = ' '.join(word.capitalize() for word in validated_data['last_name'].split())

        instance.__dict__.update(validated_data)
        instance.save()

        return instance


    def partial_update(self, instance, validated_data):
        # Actualización parcial del objeto
        # Recorre los campos que se quieren actualizar y los actualiza
        for field, value in validated_data.items():
            if field == 'name':
                instance.name = value.capitalize()
            elif field == 'last_name':
                instance.last_name = value.capitalize()
            elif field == 'email':
                instance.email = value
            elif field == 'phone_number':
                instance.phone_number = value
            elif field == 'active':
                self.validate_active(value)
                instance.active = value
        instance.save()
        return instance
    
    def delete(self, instance):
        if instance.active == False:
            raise serializers.ValidationError(
                'No existe este usuario en la base de datos')
        else:
            instance.active = False
            instance.save()
            return {'message': 'Usuario eliminado correctamente'}



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
    
    
    def update(self, instance, validated_data):
        self.validate_active(instance.active)
        validated_data = self.validate(validated_data)

        if validated_data.get('title'):
            validated_data['title'] = ' '.join(word.capitalize() for word in validated_data['title'].split())

        instance.__dict__.update(validated_data)
        instance.save()

        return instance


    def partial_update(self, instance, validated_data):
        for field, value in validated_data.items():
            if field == 'title':
                instance.name = value.capitalize()
            elif field == 'time':
                instance.last_name = value.capitalize()
            elif field == 'active':
                instance.email = value
            elif field == 'user':
                instance.phone_number = value
        instance.save()
        return instance

    
    
    def delete(self, instance):
        if instance.active == False:
            raise serializers.ValidationError(
                'No existe esta tarea en la base de datos')
        else:
            instance.active = False
            instance.save()
            return {'message': 'Tarea eliminada correctamente'}