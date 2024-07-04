from celery import shared_task
import time
from users.models import User
from users.serializers import UserSerializer
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)
@shared_task
def send_bill(rental_event_data):
    user_id = rental_event_data['user']
    user = User.objects.get(pk=user_id)
    user_serializer = UserSerializer(user)
    bill = {
        'rental_event': rental_event_data,
        'bike': user_serializer.data
    }
    send_email.delay(user.email, bill)

@shared_task
def send_email(email, contents):
    logger.info("Sending...")
    time.sleep(5)
    logger.info(f"Successfully sent email to {email} with contents: {contents}")
    pass

