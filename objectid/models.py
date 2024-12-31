from django.conf import settings
from django.db import models
from .objectid import ObjectID
from .objectid import  create_objectid as _create_objectid 


class ObjectidModel(models.Model):
    '''objectid ID model
    '''
    class Meta:
        abstract = True
        
    id = models.CharField(
        'id',
        max_length=24,
        primary_key=True,
        default=_create_objectid
    )

    def get_id_datetime(self):
        oid = ObjectID(self.id)
        return oid.timestamp
 