from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse

from pyxform.xform2json import create_survey_element_from_xml

from hashlib import md5
import unicodedata


class XForm(models.Model):

    """
    database representation of an XForm

    The data is stored in XML format and converted to the other supported
    formats when it is needed
    """

    # Users can only see their forms, auth is done by core so store the
    # username as a field on the model
    username = models.CharField(
        max_length=100
    )

    title = models.CharField(
        editable=False,
        default=u'',
        max_length=64
    )

    xml_data = models.TextField()

    description = models.TextField(
        default=u'',
        null=True
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    @property
    def hash(self):
        return u'%s' % md5(self.xml_data.encode('utf8')).hexdigest()

    @property
    def id_string(self):
        return str(self.pk)

    @property
    def url(self):
        return reverse(
            "download_xform",
            kwargs={
                "username": self.username,
                "pk": self.pk
            }
        )

    @property
    def is_crowd_form(self):
        # TODO make this a model member
        return False

    @property
    def json_data(self):
        survey = create_survey_element_from_xml(
            self.xml_data.encode('ascii', 'ignore')
        )
        return survey.to_json()
