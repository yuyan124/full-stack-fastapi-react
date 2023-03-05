from typing import List, Optional, Union

from pydantic.networks import EmailStr
from redmail import EmailSender

from app.config import setting
from app.providers.log import logger
from app.schemas import UserCreate

e = EmailSender(
    host=setting.EMAIL_STMP_HOST,
    port=setting.EMAIL_STMP_PORT,
    username=setting.EMAIL_STMP_USERNAME,
    password=setting.EMAIL_STMP_PASSWORD,
)
e.sender = setting.EMAIL_FROM_EMAIL
e.set_template_paths(html=setting.EMAIL_TEMPLATE_DIR)


def send_email(
    receviers: Union[List[EmailStr], EmailStr],
    subject: str,
    html_template: Optional[str] = None,
) -> None:
    msg = e.send(subject=subject, receivers=receviers, html_template=html_template)
    logger.debug(msg)


def send_new_account_email(
    receviers: Union[List[EmailStr], EmailStr], 
    #user: UserCreate
) -> None:

    subject = f"Welcome to {setting.PROJECT_NAME}!"
    send_email(receviers, subject, "new_account.html")
