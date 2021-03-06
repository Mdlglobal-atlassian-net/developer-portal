# Generated by Django 2.2.12 on 2020-05-12 16:07

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0024_add_3_2_ratio_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='speakers',
            field=wagtail.core.fields.StreamField([('speaker', wagtail.core.blocks.PageChooserBlock(page_type=['people.Person'])), ('external_speaker', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock(label='Name')), ('job_title', wagtail.core.blocks.CharBlock()), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='16:9 aspect-ratio image', label='16:9 image')), ('image_3_2', wagtail.images.blocks.ImageChooserBlock(help_text='3:2 aspect-ratio image - optional but recommended', required=False)), ('url', wagtail.core.blocks.URLBlock(label='URL', required=False))]))], blank=True, help_text='Optional list of speakers for this event', null=True),
        ),
        migrations.AlterField(
            model_name='events',
            name='featured',
            field=wagtail.core.fields.StreamField([('event', wagtail.core.blocks.PageChooserBlock(page_type=['events.Event', 'externalcontent.ExternalEvent'])), ('external_page', wagtail.core.blocks.StructBlock([('url', wagtail.core.blocks.URLBlock()), ('title', wagtail.core.blocks.CharBlock()), ('description', wagtail.core.blocks.TextBlock(required=False)), ('image', wagtail.images.blocks.ImageChooserBlock(help_text='16:9 aspect-ratio image', label='16:9 image')), ('image_3_2', wagtail.images.blocks.ImageChooserBlock(help_text='3:2 aspect-ratio image - optiopnal but recommended', label='3:2 image', required=False))]))], blank=True, help_text='Optional space to show featured events. Note that these are rendered two-up, so please set 0 or 2', null=True),
        ),
    ]
