from .objectid import ObjectID, create_objectid
try:
    from .models import ObjectidModel
except:
    pass


__version__='1.0.7'

VERSION = __version__