import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DEBUG", "1") == "1"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
INSTALLED_APPS = ["hospital","django.contrib.admin","django.contrib.auth","django.contrib.contenttypes",
  "django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles"]
MIDDLEWARE = ["django.middleware.security.SecurityMiddleware","django.contrib.sessions.middleware.SessionMiddleware",
  "django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware",
  "django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","hospital.middleware.LanguageMiddleware",
  "django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF = "config.urls"
TEMPLATES = [{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[],"APP_DIRS":True,
  "OPTIONS":{"context_processors":["django.template.context_processors.request","django.contrib.auth.context_processors.auth",
  "django.contrib.messages.context_processors.messages"]}}]
WSGI_APPLICATION = "config.wsgi.application"
if os.environ.get("DB_NAME"):  # PostgreSQL for production
    DATABASES = {"default":{"ENGINE":"django.db.backends.postgresql","NAME":os.environ["DB_NAME"],
      "USER":os.environ.get("DB_USER",""),"PASSWORD":os.environ.get("DB_PASSWORD",""),
      "HOST":os.environ.get("DB_HOST","localhost"),"PORT":os.environ.get("DB_PORT","5432")}}
else:
    DATABASES = {"default":{"ENGINE":"django.db.backends.sqlite3","NAME":BASE_DIR/"db.sqlite3"}}
AUTH_PASSWORD_VALIDATORS = [{"NAME":"django.contrib.auth.password_validation."+n} for n in
  ["UserAttributeSimilarityValidator","MinimumLengthValidator","CommonPasswordValidator","NumericPasswordValidator"]]
TIME_ZONE = "Africa/Mogadishu"; USE_TZ = True; USE_I18N = True
MEDIA_URL = "media/"; MEDIA_ROOT = BASE_DIR/"media"
STATIC_URL = "static/"; STATIC_ROOT = BASE_DIR/"staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_URL = "login"; LOGIN_REDIRECT_URL = "portal"; LOGOUT_REDIRECT_URL = "home"
if not DEBUG:
    SESSION_COOKIE_SECURE = CSRF_COOKIE_SECURE = SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000
