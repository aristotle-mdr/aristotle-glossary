# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aristotle_mdr', '0002_auto_20150409_0656'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlossaryAdditionalDefinition',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('definition', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GlossaryItem',
            fields=[
                ('_concept_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='aristotle_mdr._concept')),
                ('short_name', models.CharField(max_length=100, blank=True)),
                ('version', models.CharField(max_length=20, blank=True)),
                ('synonyms', models.CharField(max_length=200, blank=True)),
                ('references', ckeditor.fields.RichTextField(blank=True)),
                ('origin_URI', models.URLField(help_text='If imported, the original location of the item', blank=True)),
                ('comments', ckeditor.fields.RichTextField(help_text='Descriptive comments about the metadata item.', blank=True)),
                ('submitting_organisation', models.CharField(max_length=256, blank=True)),
                ('responsible_organisation', models.CharField(max_length=256, blank=True)),
                ('index', models.ManyToManyField(related_name='related_glossary_items', null=True, to='aristotle_mdr._concept', blank=True)),
                ('superseded_by', models.ForeignKey(related_name='supersedes', blank=True, to='aristotle_glossary.GlossaryItem', null=True)),
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
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='glossaryadditionaldefinition',
            name='registrationAuthority',
            field=models.ForeignKey(to='aristotle_mdr.RegistrationAuthority'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='glossaryadditionaldefinition',
            unique_together=set([('glossaryItem', 'registrationAuthority')]),
        ),
    ]
