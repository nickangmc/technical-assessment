# Generated by Django 4.0.8 on 2022-10-29 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0002_alter_category_name_alter_item_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='date_created',
            new_name='created_dt',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='date_updated',
            new_name='last_updated_dt',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='date_created',
            new_name='created_dt',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='date_updated',
            new_name='last_updated_dt',
        ),
    ]