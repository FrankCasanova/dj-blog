# Generated by Django 5.0.8 on 2024-09-04 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_comment'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Comment',
            new_name='Comment_djb',
        ),
        migrations.RenameIndex(
            model_name='comment_djb',
            new_name='blog_commen_created_ddecab_idx',
            old_name='blog_commen_created_0e6ed4_idx',
        ),
    ]
