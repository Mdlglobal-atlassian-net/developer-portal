# Generated by Django 2.2.4 on 2019-08-13 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("externalcontent", "0018_auto_20190807_1244")]

    operations = [
        migrations.AlterField(
            model_name="externalcontent",
            name="description",
            field=models.TextField(blank=True, default="", max_length=400),
        )
    ]
