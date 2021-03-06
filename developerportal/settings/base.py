"""
Django settings for developerportal project.

Generated by 'django-admin startproject' using Django 2.1.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import logging
import os
from decimal import Decimal

from django.core.management.utils import get_random_secret_key

from wagtail.embeds.oembed_providers import all_providers

from developerportal.apps.common.constants import ENVIRONMENT_PRODUCTION
from developerportal.apps.common.settings_helpers import _get_redis_url_for_cache

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.dirname(PROJECT_DIR)

ACTIVE_ENVIRONMENT = os.environ.get("ACTIVE_ENVIRONMENT", ENVIRONMENT_PRODUCTION)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())

ADMINS = [("DevPortal Admins", "dev-portal-errors@mozilla.com")]

# Application definition
INSTALLED_APPS = [
    "developerportal.apps.common",
    "developerportal.apps.articles",
    "developerportal.apps.content",
    "developerportal.apps.events",
    "developerportal.apps.externalcontent",
    "developerportal.apps.health",
    "developerportal.apps.home",
    "developerportal.apps.ingestion",
    "developerportal.apps.mozimages",
    "developerportal.apps.people",
    "developerportal.apps.taskqueue",
    "developerportal.apps.topics",
    "developerportal.apps.videos",
    "wagtail.contrib.forms",
    "wagtail.contrib.modeladmin",
    "wagtail.contrib.routable_page",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail.core",
    "storages",
    "modelcluster",
    "taggit",
    "django_countries",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django_celery_results",
    "mozilla_django_oidc",  # needs to be loaded after auth
]
# Note that "raven.contrib.django.raven_compat" is added to INSTALLED_APPS
# if Sentry is enabled -- see later in this file

MIDDLEWARE = [
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    # In case someone has their Auth0 revoked while logged in, revalidate it:
    "mozilla_django_oidc.middleware.SessionRefresh",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

ROOT_URLCONF = "developerportal.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "developerportal.context_processors.directory_pages",
                "developerportal.context_processors.google_analytics",
                "developerportal.context_processors.mapbox_access_token",
                "developerportal.context_processors.pagination_constants",
                "developerportal.context_processors.filtering_constants",
                "developerportal.context_processors.topics_title",
            ],
            "libraries": {
                "app_filters": "developerportal.templatetags.app_filters",
                "app_tags": "developerportal.templatetags.app_tags",
                "survey_tags": "developerportal.templatetags.survey_tags",
            },
        },
    }
]

AUTHENTICATION_BACKENDS = (
    "mozilla_django_oidc.auth.OIDCAuthenticationBackend",
    # Deliberately disabled by default: OIDC or no entry
    # "django.contrib.auth.backends.ModelBackend",
)
# Note that AUTHENTICATION_BACKENDS are overridden in tests, so take care
# to check/amend those if you add additional auth backends

WSGI_APPLICATION = "developerportal.wsgi.application"

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("POSTGRES_DB"),
        "USER": os.environ.get("POSTGRES_USER"),
        "HOST": os.environ.get("POSTGRES_HOST"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "PORT": 5432,
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        )
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Email setup
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_PORT = int(os.environ.get("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS", "True") == "True"
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL")
SERVER_EMAIL = os.environ.get("SERVER_EMAIL", DEFAULT_FROM_EMAIL)


# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

STATICFILES_DIRS = [
    ("css", os.path.join(BASE_DIR, "dist/css")),
    ("js", os.path.join(BASE_DIR, "dist/js")),
    ("fonts", os.path.join(BASE_DIR, "src/fonts")),
    ("img", os.path.join(BASE_DIR, "src/img")),
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = "/static/"

# Django security settings (see `manage.py check --deploy`)

CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = os.environ.get("SECURE_SSL_REDIRECT", "False") == "True"
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"

# Set header Strict-Transport-Security header
SECURE_HSTS_SECONDS = int(os.environ.get("SECURE_HSTS_SECONDS", 3600))
# Start with an hour, move to a year once we're settled.
# Set to 0 via env to disable BEFORE deployment (!)

# Wagtail settings
WAGTAIL_SITE_NAME = "Mozilla Developer"

# Add support for CodePen oEmbed
WAGTAILEMBEDS_FINDERS = [
    {
        "class": "wagtail.embeds.finders.oembed",
        "providers": all_providers
        + [
            {
                "endpoint": "http://codepen.io/api/oembed",
                "urls": ["^http(?:s)?://codepen\\.io/.+/pen/.+$"],
            }
        ],
    }
]

WAGTAILIMAGES_IMAGE_MODEL = "mozimages.MozImage"

# Base URL to use when referring to full URLs within the Wagtail admin backend -
# e.g. in notification emails. Don't include '/admin' or a trailing slash
BASE_URL = os.environ.get("BASE_URL")  # eg https://cms.example.net

# Explicit configuration of where the CDNed site will be. This needs to match
# the root URL of the developerportal Site in Wagtail's configuration, because
# THAT value (Site.hostname) is what determines the domain used in any absolute
# URLs generated, and we want to ensure that means the CDN.
CDN_URL = os.environ.get("CDN_URL")  # eg https://cdn.example.net


AWS_REGION = os.environ.get("AWS_REGION")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

# This bucket is where user-media will be uploaded to
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % AWS_STORAGE_BUCKET_NAME
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
AWS_DEFAULT_ACL = "public-read"
# Ensure two files with the same name don't clash - see
# https://docs.wagtail.io/en/v2.6.3/advanced_topics/deploying.html#cloud-storage
AWS_S3_FILE_OVERWRITE = False

MEDIA_URL = "https://%s/" % AWS_S3_CUSTOM_DOMAIN
MEDIA_ROOT = None

S3_BUCKET = os.environ.get("S3_BUCKET")
AWS_CLOUDFRONT_DISTRIBUTION_ID = os.environ.get("AWS_CLOUDFRONT_DISTRIBUTION_ID")

LOGIN_ERROR_URL = "/admin/"
LOGIN_REDIRECT_URL = "/admin/"
LOGOUT_REDIRECT_URL = "/admin/"

GOOGLE_ANALYTICS = os.environ.get("GOOGLE_ANALYTICS", "")

# RSS Feed
RSS_MAX_ITEMS = 20

# Mapbox
MAPBOX_ACCESS_TOKEN = os.environ.get("MAPBOX_ACCESS_TOKEN")

COUNTRIES_FIRST = ["US", "GB"]

# Celery settings
CELERY_BROKER_URL = os.environ.get("REDIS_URL", "redis://redis:6379")
CELERY_RESULT_BACKEND = "django-db"  #  for django-celery-results
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_ENABLE_UTC = True

REDIS_CACHE_DB_NUMBER = os.environ.get("REDIS_CACHE_DB_NUMBER", "1")

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": _get_redis_url_for_cache(REDIS_CACHE_DB_NUMBER),
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}

CACHE_TIME_TINY = 60 * 5  # 5 mins
CACHE_TIME_SHORT = 60 * 60  # 1 hour
CACHE_TIME_MEDIUM = 60 * 60 * 24  # 1 day
CACHE_TIME_LONG = 60 * 60 * 24 * 7  # 1 week
CACHE_TIME_VERY_LONG = 60 * 60 * 24 * 28  # 28 days


# Mozilla OpenID Connect / Auth0 configuration

OIDC_RP_SIGN_ALGO = "RS256"

# How frequently do we check with the provider that the authenticated CMS user
# still exists and is authorised? It's 15 mins by default, but we're extending
# this. Why? It looks like renewal of an expired "lease" appears to give us a
# fresh CSRF token, which means pages that are edited over a period greater
# than this timeframe will fail to save because they feature the old token in
# their page and POST payload.
# So, we're going with a longer lease, with the minor trade-off that a revoked
# SSO account can still remain active within the CMS for up to an hour
OIDC_RENEW_ID_TOKEN_EXPIRY_SECONDS = 60 * 60  # 1 hour

OIDC_CREATE_USER = False  # We don't want stop drive-by signups

OIDC_RP_CLIENT_ID = os.environ.get("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = os.environ.get("OIDC_RP_CLIENT_SECRET")

OIDC_OP_AUTHORIZATION_ENDPOINT = "https://auth.mozilla.auth0.com/authorize"
OIDC_OP_TOKEN_ENDPOINT = "https://auth.mozilla.auth0.com/oauth/token"
OIDC_OP_USER_ENDPOINT = "https://auth.mozilla.auth0.com/userinfo"
OIDC_OP_DOMAIN = "auth.mozilla.auth0.com"
OIDC_OP_JWKS_ENDPOINT = "https://auth.mozilla.auth0.com/.well-known/jwks.json"

# If True (which should only be done in settings.local), then show username and
# password fields. You'll also need to enable the model backend in local settings
USE_CONVENTIONAL_AUTH = False

# Whether or not to automatically create content based on feeds configured in the DB
AUTOMATICALLY_INGEST_CONTENT = (
    os.environ.get("AUTOMATICALLY_INGEST_CONTENT", "False") == "True"
)
# Whether or not to email admins for each item of content automatically ingested
NOTIFY_AFTER_INGESTING_CONTENT = (
    os.environ.get("NOTIFY_AFTER_INGESTING_CONTENT", "True") == "True"
)

# Extra Wagtail config to disable password usage (SSO should be the only way in)
# https://docs.wagtail.io/en/v2.6.3/advanced_topics/settings.html#password-management
# Don't let users change or reset their password
WAGTAIL_PASSWORD_MANAGEMENT_ENABLED = False
WAGTAIL_PASSWORD_RESET_ENABLED = False

# Don't require a password when creating a user,
# and blank password means cannot log in unless SSO
WAGTAILUSERS_PASSWORD_ENABLED = False

# Don't allow a CMS user to change their email via Account Settings,
# because this will break SSO. (Note that Admins can still change email
# addresses for users via Settings > Users)
WAGTAIL_EMAIL_MANAGEMENT_ENABLED = False

# Maintain old/pre-2.8 behaviour for responsive images
WAGTAILEMBEDS_RESPONSIVE_HTML = True

# The task-completion survey is hosted by a third party
TASK_COMPLETION_SURVEY_URL = os.environ.get("TASK_COMPLETION_SURVEY_URL")
TASK_COMPLETION_SURVEY_PERCENTAGE = Decimal(
    os.environ.get("TASK_COMPLETION_SURVEY_PERCENTAGE", "5.0")
)

# Sentry logging
REVISION_HASH = os.environ.get("REVISION_HASH", "undefined")
SENTRY_DSN = os.environ.get("SENTRY_DSN")

if SENTRY_DSN:
    RAVEN_CONFIG = {"dsn": SENTRY_DSN}
    if REVISION_HASH and REVISION_HASH != "undefined":
        RAVEN_CONFIG["release"] = REVISION_HASH
    INSTALLED_APPS += ["raven.contrib.django.raven_compat"]

# Based on DEFAULT_LOGGING with some tweaks
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "require_debug_false": {"()": "django.utils.log.RequireDebugFalse"},
        "require_debug_true": {"()": "django.utils.log.RequireDebugTrue"},
    },
    "formatters": {
        "django.server": {
            "()": "django.utils.log.ServerFormatter",
            "format": "[{server_time}] {message}",
            "style": "{",
        }
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
        },
        "django.server": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "django.server",
        },
        "mail_admins": {
            "level": "ERROR",
            "filters": ["require_debug_false"],
            "class": "django.utils.log.AdminEmailHandler",
        },
        "null": {"class": "logging.NullHandler"},
    },
    "loggers": {
        "django": {"handlers": ["console", "mail_admins"], "level": "INFO"},
        "django.server": {
            "handlers": ["django.server"],
            "level": "INFO",
            "propagate": False,
        },
        "mozilla_django_oidc": {"handlers": ["console"], "level": "INFO"},
        "django.security.DisallowedHost": {
            # This is to silence warnings about hostname mismatches from bots, etc
            # See https://docs.djangoproject.com/en/2.2/topics/logging/#django-security
            "handlers": ["null"],
            "propagate": False,
        },
    },
}
