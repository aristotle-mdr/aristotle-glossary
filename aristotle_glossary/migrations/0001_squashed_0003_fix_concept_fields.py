# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [(b'aristotle_glossary', '0001_initial'), (b'aristotle_glossary', '0002_auto_20160425_0143'), (b'aristotle_glossary', '0003_fix_concept_fields')]

    dependencies = [
        ('aristotle_mdr', '0020_add_uuids'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlossaryAdditionalDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('definition', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='GlossaryItem',
            fields=[
                ('_concept_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='aristotle_mdr._concept')),
                ('index', models.ManyToManyField(related_name='related_glossary_items', null=True, to='aristotle_mdr._concept', blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('aristotle_mdr._concept',),
        ),
        migrations.AddField(
            model_name='glossaryadditionaldefinition',
            name='glossaryItem',
            field=models.ForeignKey(related_name='alternate_definitions', to='aristotle_glossary.GlossaryItem'),
        ),
        migrations.AddField(
            model_name='glossaryadditionaldefinition',
            name='registrationAuthority',
            field=models.ForeignKey(to='aristotle_mdr.RegistrationAuthority'),
        ),
        migrations.AlterUniqueTogether(
            name='glossaryadditionaldefinition',
            unique_together=set([('glossaryItem', 'registrationAuthority')]),
        ),
    ]
