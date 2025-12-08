from django.db.models.signals import post_save
from django.dispatch import receiver
from fcm_django.models import FCMDevice
from firebase_admin.messaging import Message, Notification
from .models import expensa, contrato
import datetime

# Helper simple para meses en español (para evitar problemas de configuración de servidor)
MESES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
    7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
}

@receiver(post_save, sender=expensa)
def enviar_notificacion_expensa(sender, instance, created, **kwargs):
    if created:
        try:
            # 1. Buscar contrato activo y propietario
            contrato_activo = instance.unidad.contratos_unidad.filter(estado='A').first()

            if not contrato_activo or not contrato_activo.propietario.user:
                return

            propietario = contrato_activo.propietario
            usuario_dueno = propietario.user
            
            # 2. Preparar datos para el mensaje personalizado
            nombre_persona = propietario.nombre.split()[0] # Tomamos solo el primer nombre
            nombre_unidad = str(instance.unidad) # Asumiendo que el __str__ de unidad dice algo como "A-101"
            
            # Obtener el nombre del mes actual o de la fecha de emisión
            mes_actual = MESES[instance.fecha_emision.month]
            
            # --- CREACIÓN DEL MENSAJE PERSONALIZADO ---
            titulo_msg = f"Expensa de {mes_actual} 📅"
            cuerpo_msg = f"Hola {nombre_persona}, se ha generado la cuota de tu unidad {nombre_unidad} por {instance.monto} {instance.currency}."

            # 3. Buscar dispositivos
            dispositivos = FCMDevice.objects.filter(user=usuario_dueno)

            if dispositivos.exists():
                dispositivos.send_message(
                    Message(
                        notification=Notification(
                            title=titulo_msg,
                            body=cuerpo_msg
                        ),
                        data={
                            "tipo": "nueva_expensa",
                            "expensa_id": str(instance.id),
                            "click_action": "FLUTTER_NOTIFICATION_CLICK"
                        }
                    )
                )
                print(f"✅ Notificación enviada a {nombre_persona} ({usuario_dueno.username})")

        except Exception as e:
            print(f"Error en notificación: {e}")