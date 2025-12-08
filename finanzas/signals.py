from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice
from .models import expensa, contrato

# Esta función se ejecuta CADA VEZ que se guarda una expensa
@receiver(post_save, sender=expensa)
def enviar_notificacion_expensa(sender, instance, created, **kwargs):
    # 'created' es True si es una expensa nueva. False si solo se editó.
    if created:
        print(f"--- Nueva expensa creada para la unidad {instance.unidad.id} ---")
        
        try:
            # 1. Buscamos el contrato ACTIVO de esa unidad para saber quién es el dueño actual
            # Usamos el related_name 'contratos_unidad' que definiste
            contrato_activo = instance.unidad.contratos_unidad.filter(
                estado='A'
            ).first()

            if not contrato_activo:
                print("No hay contrato activo para esta unidad. No se envía notificación.")
                return

            # 2. Obtenemos el propietario y su usuario de sistema
            propietario = contrato_activo.propietario
            usuario_dueno = propietario.user

            if not usuario_dueno:
                print(f"El propietario {propietario} no tiene un usuario de sistema asignado.")
                return

            # 3. Buscamos los dispositivos (celulares) registrados de ese usuario
            # FCMDevice es la tabla que crea la librería fcm_django
            dispositivos = FCMDevice.objects.filter(user=usuario_dueno)

            if dispositivos.exists():
                # 4. Enviamos la notificación
                dispositivos.send_message(
                    title="Nueva Expensa Generada",
                    body=f"Se ha generado una expensa de {instance.monto} {instance.currency} para tu unidad.",
                    data={
                        "tipo": "nueva_expensa",
                        "expensa_id": str(instance.id),
                        "monto": str(instance.monto)
                    } 
                    # 'data' es información oculta útil para que Flutter sepa a qué pantalla ir al tocar
                )
                print(f"Notificación enviada a {usuario_dueno.username}")
            else:
                print(f"El usuario {usuario_dueno.username} no tiene dispositivos registrados.")

        except Exception as e:
            print(f"Error enviando notificación: {e}")