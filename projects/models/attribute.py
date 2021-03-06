import re

from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

identifier_re = re.compile(r'^[\w]+\Z')

validate_identifier = RegexValidator(
    identifier_re,
    _("Enter a valid 'identifier' consisting of Unicode letters, numbers or underscores."),
    'invalid'
)


class Attribute(models.Model):
    TYPE_INT = 'int'
    TYPE_STRING = 'string'
    TYPE_BOOLEAN = 'boolean'
    TYPE_DATE = 'date'
    TYPE_CHOICES = (
        (TYPE_INT, _('int')),
        (TYPE_STRING, _('string')),
        (TYPE_BOOLEAN, _('boolean')),
        (TYPE_DATE, _('date')),
    )

    name = models.CharField(max_length=255, verbose_name=_('name'))
    value_type = models.CharField(max_length=64, verbose_name=_('value type'), choices=TYPE_CHOICES)
    identifier = models.CharField(
        max_length=50, verbose_name=_('identifier'), db_index=True, unique=True, validators=[validate_identifier]
    )

    class Meta:
        verbose_name = _('attribute')
        verbose_name_plural = _('attributes')

    def __str__(self):
        return '{} ({})'.format(self.name, self.value_type)


class AttributeValueChoice(models.Model):
    attribute = models.ForeignKey(
        Attribute, verbose_name=_('attribute'), related_name='value_choices', on_delete=models.CASCADE
    )
    value = models.CharField(max_length=255, verbose_name=_('value'))
    identifier = models.CharField(
        max_length=50, verbose_name=_('identifier'), db_index=True, validators=[validate_identifier]
    )

    class Meta:
        verbose_name = _('attribute value choice')
        verbose_name_plural = _('attribute value choices')
        unique_together = ('attribute', 'identifier')

    def __str__(self):
        return self.value
