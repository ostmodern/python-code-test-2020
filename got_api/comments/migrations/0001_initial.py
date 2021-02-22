# Generated by Django 3.1.6 on 2021-02-17 23:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seasons', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment_text', models.TextField(max_length=250)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='seasons.episode')),
            ],
        ),
    ]
