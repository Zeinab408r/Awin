from django.db import models
from FirstApi.models import (BaseModel,BaseEnum)


class AwinProductLinkStateEnum(BaseEnum):
    ACTIVE = 'ACTIVE'
    ON_HOLD = 'ON_HOLD'
    DELETED = 'DELETED'


class AwinProductLink(BaseModel):
    title = models.CharField(max_length=255)
    link_address = models.CharField(max_length=2000)
    state = models.CharField(max_length=255, choices=AwinProductLinkStateEnum.choices())
