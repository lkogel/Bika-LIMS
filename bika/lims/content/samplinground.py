"""
    Sampling Round
"""

import sys

from Products.Archetypes.public import *

from AccessControl import ClassSecurityInfo
from plone.app.folder.folder import ATFolder
from Products.Archetypes.references import HoldingReference
from Products.CMFCore import permissions
from zope.interface import implements

from bika.lims import bikaMessageFactory as _
from bika.lims.browser.fields import DurationField
from bika.lims.browser.widgets import DurationWidget
from bika.lims.browser.widgets import ReferenceWidget as BikaReferenceWidget
from bika.lims.config import PROJECTNAME
from bika.lims.content.bikaschema import BikaFolderSchema
from bika.lims.idserver import renameAfterCreation
from bika.lims.interfaces import ISamplingRound
from bika.lims.utils import getUsers


Template = ReferenceField(
    'Template',
    allowed_types=('SRTemplate',),
    referenceClass=HoldingReference,
    relationship='SamplingRoundSRTemplate',
    mode='rw',
    read_permission=permissions.View,
    write_permission=permissions.ModifyPortalContent,
    widget=BikaReferenceWidget(
        label=_('Template'),
        size=20,
        catalog_name='bika_setup_catalog',
        showOn=True,
    ),
)

SamplingFrequency = DurationField(
    'SamplingFrequency',
    vocabulary_display_path_bound=sys.maxint,
    widget=DurationWidget(
        label=_('Sampling Frequency'),
        description=_('Indicate the amount of time between recurring '
            'field trips'),
    ),
)

Sampler = StringField(
    'Sampler',
    vocabulary='getSamplers',
    vocabulary_display_path_bound=sys.maxint,
    widget=SelectionWidget(
        label=_('Default Sampler'),
        description=_('Select the default Sampler to be assigned'),
    ),
)

Department = ReferenceField(
    'Department',
    allowed_types=('Department',),
    referenceClass=HoldingReference,
    relationship='SRTemplateDepartment',
    vocabulary_display_path_bound=sys.maxint,
    widget=BikaReferenceWidget(
        label=_('Department'),
        description=_('Select the lab Department responsible'),
        catalog_name='bika_setup_catalog',
        showOn=True,
    )
)

Instructions = TextField(
    'Instructions',
    searchable=True,
    default_content_type='text/plain',
    allowed_content_types=('text/plain'),
    default_output_type="text/plain",
    widget=TextAreaWidget(
        label=_('Sampling Instructions'),
        append_only=True,
    ),
)


schema = BikaFolderSchema.copy() + Schema((
    Template,
    SamplingFrequency,
    Sampler,
    Department,
    Instructions,
))


class SamplingRound(ATFolder):
    implements(ISamplingRound)
    security = ClassSecurityInfo()
    displayContentsTab = False
    schema = schema

    _at_rename_after_creation = True

    def _renameAfterCreation(self, check_auto_id=False):
        renameAfterCreation(self)

    def isOpen(self):
        """ Returns true if the SamplingRound is in 'open' state
        """
        return True

    def getSamplers(self):
        users = getUsers(self, ['Sampler', 'LabManager', 'Manager'])
        return users


registerType(SamplingRound, PROJECTNAME)
