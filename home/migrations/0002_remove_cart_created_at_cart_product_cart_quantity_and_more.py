# Generated by Django 5.2.4 on 2025-07-21 00:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cart",
            name="created_at",
        ),
        migrations.AddField(
            model_name="cart",
            name="product",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="home.product",
            ),
        ),
        migrations.AddField(
            model_name="cart",
            name="quantity",
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name="cart",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
