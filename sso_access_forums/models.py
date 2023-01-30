from django.db import models

# Create your models here.


class General(models.Model):
    """Stores info about individual users.
    """
    
    class Meta:
        """Stores metadata about the table in general.

        Refer to https://docs.djangoproject.com/en/4.1/ref/models/options/
        for details on each field.
        """
        managed = False
        default_permissions = ()
        permissions = (("basic_access", "Can access this app"),)
