from django.conf import settings
from django.db import models
from .objectid import ObjectID
from .objectid import  create_objectid as _create_objectid 


DCID = getattr(settings, 'DCID', 0)


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
    
    def save(self, *args, **kwargs):
        update_fields = kwargs.get('update_fields', None)
        if update_fields and not 'cdcid' in update_fields:
            kwargs['update_fields'].append('cdcid')
        self.cdcid = DCID        
        super().save(*args, **kwargs)
