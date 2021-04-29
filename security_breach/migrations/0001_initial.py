# Generated by Django 3.1.6 on 2021-04-29 11:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

is_testing = "pytest" in sys.argv


class Migration(migrations.Migration):

    initial = True

    dependencies = (
        [
            ("core", "0001_initial"),
            migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ]
        if is_testing
        else []
    )

    operations = (
        [
            migrations.CreateModel(
                name="EnvVarsExposed",
                fields=[
                    (
                        "id",
                        models.AutoField(
                            auto_created=True,
                            primary_key=True,
                            serialize=False,
                            verbose_name="ID",
                        ),
                    ),
                    ("is_repo_private", models.BooleanField(blank=True, null=True)),
                    (
                        "severity_from_log_analysis",
                        models.CharField(blank=True, max_length=50, null=True),
                    ),
                    ("exists_on_codecov", models.BooleanField(blank=True, null=True)),
                    (
                        "known_clone_by_attacker",
                        models.BooleanField(blank=True, null=True),
                    ),
                    ("exposed_env_vars", models.TextField(blank=True, null=True)),
                    (
                        "sensitive_exposed_in_git_origin",
                        models.TextField(blank=True, null=True),
                    ),
                    (
                        "owner",
                        models.ForeignKey(
                            blank=True,
                            null=True,
                            on_delete=django.db.models.deletion.DO_NOTHING,
                            to=settings.AUTH_USER_MODEL,
                        ),
                    ),
                    (
                        "repo",
                        models.ForeignKey(
                            blank=True,
                            null=True,
                            on_delete=django.db.models.deletion.DO_NOTHING,
                            to="core.repository",
                        ),
                    ),
                ],
                options={
                    "db_table": "env_vars_exposed",
                    "unique_together": {("repo", "owner")},
                },
            ),
        ]
        if is_testing
        else []
    )
