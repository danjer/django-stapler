
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'y130-j9oz4r5aoamn_n=+s-*7n)*3^s$jmf4(qw6ik28()g^(n'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mem_db"
    }
}
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "stapler.tests.test_app.apps.TestAppConfig",
]
