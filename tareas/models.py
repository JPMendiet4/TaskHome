import smtplib
from email.mime.text import MIMEText
from django.db import models
from django.conf import settings


class User(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=180, blank=True, null=True)
    email = models.EmailField(max_length=150, blank=True, null=True)
    phone_number = models.CharField(max_length=12, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Homework(models.Model):
    title = models.CharField(max_length=150, blank=True, null=True)
    description = models.TextField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    time = models.TimeField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Guardar la tarea
        super(Homework, self).save(*args, **kwargs)

        # Enviar correo electrónico al usuario
        try:
            # Establecemos conexion con el servidor smtp de gmail
            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            mailServer.starttls()
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            # Construimos el mensaje simple
            email_to = self.user.email
            mensaje = MIMEText(f"""Hola {self.user.name},
            Se ha creado una nueva tarea: {self.title}""")
            mensaje['From'] = settings.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = "Nueva tarea creada"

            # Envio del mensaje
            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())

            print(f'Correo enviado correctamente a {self.user.email}')
        except Exception as e:
            print(f'Error al enviar correo electrónico: {e}')
