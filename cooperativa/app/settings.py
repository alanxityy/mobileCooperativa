import os
from pathlib import Path
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# ========= Segurança / Dev =========
SECRET_KEY = "troque-esta-chave-em-producao"
DEBUG = True
ALLOWED_HOSTS = ["*"]

# ========= Apps =========
INSTALLED_APPS = [
    # Jazzmin deve vir ANTES do admin
    "jazzmin",
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    'django.contrib.humanize',
    "django.contrib.staticfiles",

    "accounts.apps.AccountsConfig",

    # Apps do projeto
    "coletores",
    "materiais",
    "caixa",
    "pagina",
    

    # App utilitário com urls.py raiz
    "app",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.AdminAccessMiddleware',
]

# Roteador principal e WSGI dentro de app/
ROOT_URLCONF = "app.urls"
WSGI_APPLICATION = "app.wsgi.application"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # templates globais em app/templates
        "DIRS": [BASE_DIR / "app" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                # opcional: útil se usar {% static %} fora de load static
                # "django.template.context_processors.static",
            ],
        },
    },
]

# ========= Banco de Dados =========
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', 
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=8),

    # Define quanto tempo o token de renovação dura.
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),

    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,

    'AUTH_HEADER_TYPES': ('Bearer',),
}


# ========= Senhas =========
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ========= i18n / tz =========
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ========= Static / Media =========
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "app" / "static",   # seus estáticos globais
]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ========= Login redirects =========
LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/login/"

JAZZMIN_SETTINGS = {
    "site_title": "Cooperativa Suzanápolis",
    "site_header": "Admin • Cooperativa",
    "site_brand": "Cooperativa Suzanápolis",
    "welcome_sign": "Bem-vindo à área administrativa",
    "copyright": "Cooperativa de Reciclagem • Suzanápolis/SP",

    "site_logo": "img/logo_suzanapolis.png",
    "site_logo_classes": "img-fluid",
    "login_logo": "img/logo_suzanapolis.png",
    "login_logo_dark": None,

    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "custom_css": "css/jazzmin_custom.css",

    "topmenu_links": [
        {"name": "Admin", "url": "admin:index"},
        {"name": "Dashboard do Site", "url": "dashboard", "icon": "fas fa-home"},
        {"name": "Sair", "url": "admin_logout", "icon": "fas fa-sign-out-alt"},
    ],
    "usermenu_links": [
        {"name": "Alterar senha", "url": "admin:password_change", "icon": "fas fa-key"},
        {"name": "Sair", "url": "admin_logout", "icon": "fas fa-sign-out-alt"},
    ],

    "icons": {
        "coletores.Coletor": "fas fa-user-friends",
        "materiais.Material": "fas fa-recycle",
        "caixa.LancamentoCaixa": "fas fa-cash-register",
        "auth.User": "fas fa-user",
        "auth.Group": "fas fa-users-cog",
        "accounts.Profile": "fas fa-id-badge",  # se você criou o app de perfil
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-angle-right",

    "related_modal_active": True,
    "order_with_respect_to": ["coletores", "materiais", "caixa", "accounts"],

    # ▶ Para destravar a edição (sem depender das abas)
    "changeform_format": "collapsible",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "accounts.profile": "collapsible",  # se existir
    },
}

JAZZMIN_UI_TWEAKS = {
    "theme": "flatly",
    "dark_mode_theme": "slate",

    "navbar": "navbar-dark",
    "brand_colour": "navbar-primary",
    "accent": "accent-warning",

    "no_navbar_border": True,

    "sidebar": "sidebar-dark-success",
    "sidebar_fixed": True,
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_flat_style": True,

    "footer_fixed": False,
    "body_small_text": False,
    "footer_small_text": True,
}

CORS_ALLOW_ALL_ORIGINS = True  # Libera qualquer origem (incluindo seu 8081)
CORS_ALLOW_CREDENTIALS = True  # Permite envio de tokens/cookies
