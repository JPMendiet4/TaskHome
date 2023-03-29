from rest_framework import serializers
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
from django.conf import settings
import re
import datetime
from tareas.models import User, Homework


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    @staticmethod
    def validate_name(name):
        if name == '':
            raise serializers.ValidationError('El nombre no puede estar vacio')
        name = name.strip().title()
        if not all(word.isalpha() for word in name.split()):
            raise serializers.ValidationError('El nombre solo puede contener letras')
        return name

    @staticmethod
    def validate_last_name(last_name):
        if last_name == '':
            raise serializers.ValidationError(
                'El apellido no puede estar vacio')
        last_name = last_name.strip().title()
        if not all(word.isalpha() for word in last_name.split()):
            raise serializers.ValidationError('El apellido solo puede contener letras')
        return last_name

    @staticmethod
    def validate_email(value):
        if not value:
            raise serializers.ValidationError('Tiene que indicar un correo.')
        elif not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise serializers.ValidationError(
                'El correo electrónico no es válido')
        return value

    @staticmethod
    def validate_phone_number(phone_number):
        if not phone_number:
            raise serializers.ValidationError(
                'Tiene que indicar un número de telefono.')

        pattern = re.compile(
            r'^\+?\d{0,2}\s?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}$')

        if not pattern.match(phone_number):
            raise serializers.ValidationError(
                'El número de teléfono es inválido.')

        return phone_number

    @staticmethod
    def validate_active(value):
        if value is not True:
            raise serializers.ValidationError(
                "El usuario debe ser activado para poder asignarle tareas."
            )
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

    @staticmethod
    def delete(instance):
        if instance.status is False:
            raise serializers.ValidationError(
                'No existe este usuario en la base de datos')
        else:
            instance.status = False
            instance.save()
            return {'message': 'Usuario eliminado correctamente'}


class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = '__all__'

    @staticmethod
    def validate_title(title):
        if title == '':
            raise serializers.ValidationError('El nombre no puede estar vacio')
        return title

    @staticmethod
    def validate_time(value):
        if not value:
            raise serializers.ValidationError('El tiempo es requerido.')
        elif value < datetime.time(hour=6) or value > datetime.time(hour=18):
            raise serializers.ValidationError('El tiempo debe estar entre las 6:00 a.m. y las 6:00 p.m.')
        return value

    @staticmethod
    def validate_status(value):
        if not value:
            raise serializers.ValidationError('Debe establecer el estado de la tarea')
        return value

    @staticmethod
    def validate_user(user):
        if not user:
            raise serializers.ValidationError('Debe asignarle la tarea a un usuario')
        if not User.objects.filter(pk=user.pk).exists():
            raise serializers.ValidationError('El usuario ingresado no existe')
        return user

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "title": instance.title,
            "description": instance.description,
            "time": instance.time,
            "status": instance.get_status_display(),
            "user": {
                'id': instance.user.id,
                'username': (
                        str(instance.user.name).split(" ")[0] + " " + str(instance.user.last_name).split(" ")[0]
                )

            }
        }

    def create(self, validated_data):
        existing_homework = Homework.objects.filter(
            title=validated_data['title'], status__in=['C', 'P']).first()
        if existing_homework:
            existing_homework.status = validated_data.get('status', existing_homework.status)
            existing_homework.save()
            return existing_homework


        homework = super().create(validated_data)

        # enviar un correo electrónico al usuario asignado a la tarea
        user = homework.user
        subject = 'Nueva tarea asignada'
        message = f'Hola {user.name}, se te ha asignado una nueva tarea: {homework.title}'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        send_mail(subject, message, email_from, recipient_list)

        return homework

    def update(self, instance, validated_data):
        status = validated_data.get('status')
        if status and status not in ['C', 'P', 'T']:
            raise ValidationError('Invalid status')

        if validated_data.get('title'):
            validated_data['title'] = ' '.join(word.capitalize() for word in validated_data['title'].split())

        # Obtener el usuario asignado a la tarea
        user = validated_data.get('user', None)
        if user is not None:
            instance.user = user

        # Actualizar la instancia y guardarla
        instance.__dict__.update(validated_data)
        instance.save()

        # Obtener los detalles del usuario asignado a la tarea
        user = instance.user
        user_full_name = f"{user.name} {user.last_name}"
        user_email = user.email

        # Enviar el correo electrónico
        subject = f"La tarea '{instance.title}' ha sido actualizada"
        message = f"Hola {user_full_name},\nLa tarea '{instance.title}' ha sido actualizada.\nGracias,\nEl equipo de Tareas"
        from_email = 'mi_correo_ejemplo@example.com'
        recipient_list = [user_email]
        send_mail(subject, message, from_email, recipient_list)

        return instance

    @staticmethod
    def partial_update(instance, validated_data):
        status = validated_data.get('status')
        if status and status not in ['C', 'P', 'T']:
            raise ValidationError('Invalid status')

        for field, value in validated_data.items():
            if field == 'title':
                instance.name = value.capitalize()
            elif field == 'time':
                instance.last_name = value.capitalize()
            elif field == 'status':
                instance.status = value
                if value == 'C':
                    send_mail(
                        'Tarea creada',
                        f'La tarea {instance.title} ha sido creada.',
                        'from@example.com',
                        [instance.user.email],
                        fail_silently=False,
                    )
                elif value == 'T':
                    send_mail(
                        'Tarea terminada',
                        f'La tarea {instance.title} ha sido terminada.',
                        'from@example.com',
                        [instance.user.email],
                        fail_silently=False,
                    )
            elif field == 'user':
                instance.phone_number = value
        instance.save()
        return instance

    @staticmethod
    def delete(instance):
        if instance.active is False:
            raise serializers.ValidationError(
                'No existe esta tarea en la base de datos')
        else:
            instance.active = False
            instance.save()
            send_mail(
                'Tarea eliminada',
                f'La tarea {instance.title} ha sido eliminada.',
                'from@example.com',
                [instance.user.email],
                fail_silently=False,
            )
            return {'message': 'Tarea eliminada correctamente'}