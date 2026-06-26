"""
Script setup giao diện Login Nursing Home.
Chay: python setup_login.py
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

def write_file(rel_path, content):
    full_path = os.path.join(BASE, rel_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  [OK] {rel_path}")

print("=== Dang tao file giao dien Login ===\n")

# 1. apps/__init__.py
write_file("apps/__init__.py", "")

# 2. apps/accounts/apps.py
write_file("apps/accounts/apps.py", """from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'apps.accounts'
""")

# 3. apps/accounts/views.py
write_file("apps/accounts/views.py", """from django.shortcuts import render


def login_view(request):
    return render(request, 'accounts/login.html')
""")

# 4. apps/accounts/urls.py
write_file("apps/accounts/urls.py", """from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
]
""")

# 5. config/settings.py
write_file("config/settings.py", '''"""Django settings for config project."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-as_m(64vnn7bu#34ijbt53)-%5p%h+6x+bv$yjy9qxnrcyw%hi'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
''')

# 6. config/urls.py
write_file("config/urls.py", """from django.contrib import admin
from django.urls import path, include
from apps.accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', accounts_views.login_view, name='login'),
    path('', accounts_views.login_view, name='home'),
]
""")

# 7. static/images/spa-banner.svg
write_file("static/images/spa-banner.svg", """<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="600" viewBox="0 0 1920 600">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a4a3a;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#0D6E5C;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0a5a4b;stop-opacity:1" />
    </linearGradient>
  </defs>
  <rect width="1920" height="600" fill="url(#bg)"/>
  <circle cx="300" cy="300" r="200" fill="rgba(255,255,255,0.03)"/>
  <circle cx="1600" cy="200" r="250" fill="rgba(255,255,255,0.03)"/>
  <circle cx="960" cy="500" r="180" fill="rgba(255,255,255,0.02)"/>
  <text x="960" y="280" text-anchor="middle" font-family="Roboto, sans-serif" font-size="60" fill="rgba(255,255,255,0.08)" font-weight="bold">NURSING HOME</text>
  <text x="960" y="360" text-anchor="middle" font-family="Roboto, sans-serif" font-size="28" fill="rgba(255,255,255,0.06)">Care &amp; Wellness</text>
</svg>""")

# 8. static/css/bean_spa.css
CSS = r"""/* ============================================
   Nursing Home Theme - Login Page Styles
   Mau sac chu dao: Xanh la #0D6E5C, Cam #E67E22
   Nen: #F5F2ED (be/cream)
   Font: Roboto (Google Fonts)
   ============================================ */

/* === Reset & Base === */
*,
*::before,
*::after {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Roboto', sans-serif;
    background-color: #F5F2ED;
    color: #333333;
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

a {
    text-decoration: none;
    color: inherit;
    transition: color 0.3s ease;
}

ul {
    list-style: none;
}

img {
    max-width: 100%;
    height: auto;
}

/* === Header === */
.header {
    background-color: #FFFFFF;
    border-bottom: 1px solid #e0e0e0;
    position: sticky;
    top: 0;
    z-index: 1000;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.header__container {
    max-width: 1280px;
    margin: 0 auto;
    padding: 0 20px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    height: 70px;
}

.header__logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 24px;
    font-weight: 700;
}

.header__logo-icon {
    width: 40px;
    height: 40px;
    background-color: #0D6E5C;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #FFFFFF;
    font-size: 20px;
}

.header__logo-text {
    color: #0D6E5C;
}

.header__logo-text span {
    color: #E67E22;
}

/* Navigation */
.header__nav {
    display: flex;
    align-items: center;
    gap: 24px;
}

.header__nav-list {
    display: flex;
    align-items: center;
    gap: 20px;
}

.header__nav-link {
    font-size: 14px;
    font-weight: 500;
    color: #333333;
    padding: 8px 0;
    position: relative;
    transition: color 0.3s ease;
}

.header__nav-link:hover {
    color: #0D6E5C;
}

.header__nav-link::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background-color: #0D6E5C;
    transition: width 0.3s ease;
}

.header__nav-link:hover::after {
    width: 100%;
}

.header__nav-link.active {
    color: #0D6E5C;
}

/* Header icons */
.header__icons {
    display: flex;
    align-items: center;
    gap: 16px;
}

.header__icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 36px;
    height: 36px;
    border-radius: 50%;
    color: #555555;
    font-size: 16px;
    transition: all 0.3s ease;
    cursor: pointer;
}

.header__icon:hover {
    color: #0D6E5C;
    background-color: #f0f7f5;
}

.header__phone {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 14px;
    font-weight: 600;
    color: #0D6E5C;
}

.header__phone-number {
    color: #E67E22;
    font-size: 15px;
}

.header__btn-cta {
    background-color: #E67E22;
    color: #FFFFFF;
    padding: 8px 20px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.header__btn-cta:hover {
    background-color: #d35400;
}

/* === Banner === */
.banner {
    position: relative;
    height: 300px;
    background-image: url('/static/images/spa-banner.svg');
    background-size: cover;
    background-position: center;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
}

.banner::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(51, 51, 51, 0.7);
    z-index: 1;
}

.banner__content {
    position: relative;
    z-index: 2;
}

.banner__title {
    font-size: 36px;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.banner__breadcrumb {
    font-size: 14px;
    color: #E67E22;
}

.banner__breadcrumb a {
    color: #E67E22;
}

.banner__breadcrumb a:hover {
    text-decoration: underline;
}

.banner__breadcrumb span {
    color: #cccccc;
    margin: 0 8px;
}

/* === Main Content - Login Section === */
.login-section {
    flex: 1;
    padding: 40px 20px 60px;
    display: flex;
    justify-content: center;
    align-items: flex-start;
}

.login-card {
    background-color: #FFFFFF;
    border-radius: 8px;
    padding: 40px;
    width: 100%;
    max-width: 460px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
}

.login-card__title {
    font-size: 24px;
    font-weight: 700;
    color: #0D6E5C;
    text-align: center;
    margin-bottom: 30px;
    text-transform: uppercase;
    letter-spacing: 3px;
}

/* Form */
.login-form {
    display: flex;
    flex-direction: column;
    gap: 18px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 6px;
}

.form-group__label {
    font-size: 14px;
    font-weight: 500;
    color: #555555;
}

.form-group__input {
    width: 100%;
    padding: 12px 16px;
    border: 1px solid #dddddd;
    border-radius: 6px;
    font-size: 15px;
    color: #333333;
    font-family: 'Roboto', sans-serif;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
    outline: none;
}

.form-group__input:focus {
    border-color: #0D6E5C;
    box-shadow: 0 0 0 3px rgba(13, 110, 92, 0.1);
}

.form-group__input::placeholder {
    color: #aaaaaa;
}

/* Password toggle */
.form-group__password-wrapper {
    position: relative;
}

.form-group__password-toggle {
    position: absolute;
    right: 12px;
    top: 50%;
    transform: translateY(-50%);
    cursor: pointer;
    color: #999999;
    font-size: 16px;
    background: none;
    border: none;
    padding: 4px;
}

.form-group__password-toggle:hover {
    color: #0D6E5C;
}

/* Submit button */
.btn-login {
    width: 100%;
    padding: 14px;
    background-color: #0D6E5C;
    color: #FFFFFF;
    border: none;
    border-radius: 6px;
    font-size: 16px;
    font-weight: 600;
    font-family: 'Roboto', sans-serif;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.1s ease;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 6px;
}

.btn-login:hover {
    background-color: #0a5a4b;
}

.btn-login:active {
    transform: scale(0.98);
}

/* Links */
.login-card__links {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 16px;
    font-size: 14px;
}

.login-card__forgot {
    color: #888888;
    transition: color 0.3s ease;
}

.login-card__forgot:hover {
    color: #0D6E5C;
}

.login-card__register {
    color: #E67E22;
    font-weight: 600;
    transition: color 0.3s ease;
}

.login-card__register:hover {
    color: #d35400;
}

/* Divider */
.login-card__divider {
    display: flex;
    align-items: center;
    margin: 24px 0 20px;
    gap: 12px;
}

.login-card__divider::before,
.login-card__divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background-color: #e0e0e0;
}

.login-card__divider span {
    font-size: 13px;
    color: #999999;
    white-space: nowrap;
}

/* Social login buttons */
.social-login {
    display: flex;
    gap: 12px;
}

.btn-social {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 12px;
    border: 1px solid #e0e0e0;
    border-radius: 6px;
    font-size: 14px;
    font-weight: 500;
    font-family: 'Roboto', sans-serif;
    cursor: pointer;
    transition: all 0.3s ease;
    background-color: #FFFFFF;
}

.btn-social--facebook {
    color: #3B5998;
    border-color: #3B5998;
}

.btn-social--facebook:hover {
    background-color: #3B5998;
    color: #FFFFFF;
}

.btn-social--google {
    color: #DB4437;
    border-color: #DB4437;
}

.btn-social--google:hover {
    background-color: #DB4437;
    color: #FFFFFF;
}

.btn-social__icon {
    width: 20px;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* === Footer === */
.footer {
    background-color: #F5F2ED;
    border-top: 3px solid #0D6E5C;
    padding: 40px 20px 20px;
}

.footer__container {
    max-width: 1280px;
    margin: 0 auto;
}

.footer__top {
    display: grid;
    grid-template-columns: 1.5fr 1fr 1fr 1fr;
    gap: 30px;
    padding-bottom: 30px;
    border-bottom: 1px solid #e0dcd7;
}

/* Footer - About column */
.footer__about {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.footer__logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 22px;
    font-weight: 700;
    color: #0D6E5C;
}

.footer__logo span {
    color: #E67E22;
}

.footer__desc {
    font-size: 14px;
    color: #666666;
    line-height: 1.7;
}

.footer__contact-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 8px;
}

.footer__contact-item {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    color: #555555;
}

.footer__contact-item svg {
    width: 16px;
    height: 16px;
    color: #0D6E5C;
    flex-shrink: 0;
}

/* Footer - Link columns */
.footer__column-title {
    font-size: 15px;
    font-weight: 700;
    color: #333333;
    text-transform: uppercase;
    margin-bottom: 16px;
    letter-spacing: 0.5px;
}

.footer__link-list {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.footer__link {
    font-size: 14px;
    color: #555555;
    transition: color 0.3s ease;
}

.footer__link:hover {
    color: #0D6E5C;
}

/* Footer - Social */
.footer__social {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-top: 16px;
}

.footer__social-icon {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    border: 1px solid #d0ccc7;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #555555;
    font-size: 16px;
    transition: all 0.3s ease;
    cursor: pointer;
}

.footer__social-icon:hover {
    background-color: #0D6E5C;
    border-color: #0D6E5C;
    color: #FFFFFF;
}

/* Footer - Newsletter */
.footer__newsletter-form {
    display: flex;
    gap: 0;
    margin-top: 8px;
}

.footer__newsletter-input {
    flex: 1;
    padding: 10px 14px;
    border: 1px solid #d0ccc7;
    border-right: none;
    border-radius: 4px 0 0 4px;
    font-size: 14px;
    font-family: 'Roboto', sans-serif;
    outline: none;
    transition: border-color 0.3s ease;
}

.footer__newsletter-input:focus {
    border-color: #0D6E5C;
}

.footer__newsletter-btn {
    padding: 10px 18px;
    background-color: #0D6E5C;
    color: #FFFFFF;
    border: 1px solid #0D6E5C;
    border-radius: 0 4px 4px 0;
    font-size: 14px;
    font-weight: 600;
    font-family: 'Roboto', sans-serif;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.footer__newsletter-btn:hover {
    background-color: #0a5a4b;
}

/* Footer bottom */
.footer__bottom {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 20px;
    font-size: 13px;
    color: #888888;
}

.footer__bottom-links {
    display: flex;
    gap: 20px;
}

.footer__bottom-link {
    color: #888888;
    transition: color 0.3s ease;
}

.footer__bottom-link:hover {
    color: #0D6E5C;
}

/* === Responsive === */
@media (max-width: 1024px) {
    .header__nav-list {
        display: none;
    }

    .footer__top {
        grid-template-columns: 1fr 1fr;
    }
}

@media (max-width: 768px) {
    .header__container {
        height: 60px;
    }

    .header__logo-text {
        font-size: 20px;
    }

    .header__icons {
        gap: 10px;
    }

    .header__phone {
        display: none;
    }

    .banner {
        height: 200px;
    }

    .banner__title {
        font-size: 26px;
    }

    .login-section {
        padding: 30px 16px 40px;
    }

    .login-card {
        padding: 28px 24px;
    }

    .footer__top {
        grid-template-columns: 1fr;
        gap: 24px;
    }

    .footer__bottom {
        flex-direction: column;
        gap: 12px;
        text-align: center;
    }
}

@media (max-width: 480px) {
    .social-login {
        flex-direction: column;
    }

    .login-card__links {
        flex-direction: column;
        gap: 10px;
        text-align: center;
    }
}"""
write_file("static/css/bean_spa.css", CSS)

# 9. login.html
LOGIN_HTML = r"""{% load static %}
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dang nhap tai khoan</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;600;700&amp;display=swap" rel="stylesheet">
    <link rel="stylesheet" href="{% static 'css/bean_spa.css' %}">
</head>
<body>

    <!-- ========== HEADER ========== -->
    <header class="header">
        <div class="header__container">
            <a href="/" class="header__logo">
                <div class="header__logo-icon">
                    <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
                        <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                        <line x1="9" y1="9" x2="9.01" y2="9"/>
                        <line x1="15" y1="9" x2="15.01" y2="9"/>
                    </svg>
                </div>
                <div class="header__logo-text">Nursing <span>Home</span></div>
            </a>

            <nav class="header__nav">
                <ul class="header__nav-list">
                    <li><a href="/" class="header__nav-link">Trang chu</a></li>
                    <li><a href="#" class="header__nav-link">Ve chung toi</a></li>
                    <li><a href="#" class="header__nav-link">Cu dan</a></li>
                    <li><a href="#" class="header__nav-link">Dich vu</a></li>
                    <li><a href="#" class="header__nav-link">Nhan vien</a></li>
                    <li><a href="#" class="header__nav-link">Ho so y te</a></li>
                    <li><a href="#" class="header__nav-link">Cau hoi thuong gap</a></li>
                    <li><a href="#" class="header__nav-link">Lien he</a></li>
                </ul>

                <div class="header__icons">
                    <div class="header__icon" title="Ngon ngu">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="12" cy="12" r="10"/>
                            <line x1="2" y1="12" x2="22" y2="12"/>
                            <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                        </svg>
                    </div>
                    <div class="header__icon" title="Tai khoan">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                            <circle cx="12" cy="7" r="4"/>
                        </svg>
                    </div>
                    <div class="header__icon" title="Gio hang">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/>
                            <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/>
                        </svg>
                    </div>
                    <div class="header__icon" title="Tim kiem">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="11" cy="11" r="8"/>
                            <line x1="21" y1="21" x2="16.65" y2="16.65"/>
                        </svg>
                    </div>
                    <div class="header__icon" title="He thong chi nhanh">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/>
                            <circle cx="12" cy="10" r="3"/>
                        </svg>
                    </div>
                    <div class="header__phone">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                        </svg>
                        <span class="header__phone-number">1900 6750</span>
                    </div>
                    <button class="header__btn-cta">Dat lich kham</button>
                </div>
            </nav>
        </div>
    </header>

    <!-- ========== BANNER ========== -->
    <section class="banner">
        <div class="banner__content">
            <h1 class="banner__title">Dang nhap tai khoan</h1>
            <div class="banner__breadcrumb">
                <a href="/">Trang chu</a>
                <span>&gt;</span>
                <span>Dang nhap tai khoan</span>
            </div>
        </div>
    </section>

    <!-- ========== LOGIN FORM ========== -->
    <section class="login-section">
        <div class="login-card">
            <h2 class="login-card__title">Dang nhap</h2>

            {% if messages %}
                {% for message in messages %}
                    <div style="padding:10px 14px;border-radius:6px;margin-bottom:16px;font-size:14px;
                        {% if message.tags == 'error' %}background:#fde8e8;color:#e74c3c;border:1px solid #f5c6cb;
                        {% elif message.tags == 'success' %}background:#e8f8f5;color:#0D6E5C;border:1px solid #a3d9cc;
                        {% endif %}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}

            <form class="login-form" method="post" action="{% url 'login' %}">
                {% csrf_token %}

                <div class="form-group">
                    <label class="form-group__label" for="email">Email</label>
                    <input type="email" class="form-group__input" id="email" name="email" placeholder="Nhap email cua ban" required autocomplete="email">
                </div>

                <div class="form-group">
                    <label class="form-group__label" for="password">Mat khau</label>
                    <div class="form-group__password-wrapper">
                        <input type="password" class="form-group__input" id="password" name="password" placeholder="Nhap mat khau" required autocomplete="current-password">
                        <button type="button" class="form-group__password-toggle" onclick="togglePassword()">
                            <svg id="eye-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/>
                                <circle cx="12" cy="12" r="3"/>
                            </svg>
                        </button>
                    </div>
                </div>

                <button type="submit" class="btn-login">Dang nhap</button>
            </form>

            <div class="login-card__links">
                <a href="#" class="login-card__forgot">Quen mat khau?</a>
                <a href="#" class="login-card__register">Dang ky tai khoan</a>
            </div>

            <div class="login-card__divider">
                <span>hoac dang nhap qua</span>
            </div>

            <div class="social-login">
                <button class="btn-social btn-social--facebook" type="button">
                    <span class="btn-social__icon">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="#3B5998">
                            <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/>
                        </svg>
                    </span>
                    Facebook
                </button>
                <button class="btn-social btn-social--google" type="button">
                    <span class="btn-social__icon">
                        <svg width="20" height="20" viewBox="0 0 24 24">
                            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4"/>
                            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853"/>
                            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05"/>
                            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                        </svg>
                    </span>
                    Google
                </button>
            </div>
        </div>
    </section>

    <!-- ========== FOOTER (Placeholder) ========== -->
    <footer class="footer">
        <div class="footer__container">
            <div class="footer__top">
                <div class="footer__about">
                    <div class="footer__logo">
                        <div class="header__logo-icon" style="width:36px;height:36px;font-size:18px;">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2z"/>
                                <path d="M8 14s1.5 2 4 2 4-2 4-2"/>
                                <line x1="9" y1="9" x2="9.01" y2="9"/>
                                <line x1="15" y1="9" x2="15.01" y2="9"/>
                            </svg>
                        </div>
                        Nursing <span>Home</span>
                    </div>
                    <p class="footer__desc">
                        Nursing Home - He thong quan ly cham soc nguoi cao tuoi.
                        Chung toi cung cap dich vu cham soc suc khoe toan dien voi doi ngu dieu duong chuyen nghiep.
                    </p>
                    <ul class="footer__contact-list">
                        <li class="footer__contact-item">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
                            70 Ly Gia, Phuong 15, Quan 11, TP Ho Chi Minh
                        </li>
                        <li class="footer__contact-item">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
                            1900 6750
                        </li>
                        <li class="footer__contact-item">
                            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/><polyline points="22,6 12,13 2,6"/></svg>
                            support@nursinghome.vn
                        </li>
                    </ul>
                    <div class="footer__social">
                        <div class="footer__social-icon" title="Facebook">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
                        </div>
                        <div class="footer__social-icon" title="Instagram">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg>
                        </div>
                        <div class="footer__social-icon" title="YouTube">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814z"/><polygon points="9.545,15.568 15.818,12 9.545,8.432" fill="#fff"/></svg>
                        </div>
                        <div class="footer__social-icon" title="TikTok">
                            <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>
                        </div>
                    </div>
                </div>

                <div class="footer__column">
                    <h4 class="footer__column-title">Cac phan he thong</h4>
                    <ul class="footer__link-list">
                        <li><a href="#" class="footer__link">Quan ly Cu dan</a></li>
                        <li><a href="#" class="footer__link">Quan ly Nhan vien</a></li>
                        <li><a href="#" class="footer__link">Ho so Y te</a></li>
                        <li><a href="#" class="footer__link">Thanh toan &amp; Hoa don</a></li>
                        <li><a href="#" class="footer__link">Quan ly Phong</a></li>
                        <li><a href="#" class="footer__link">Nhat ky he thong</a></li>
                    </ul>
                </div>

                <div class="footer__column">
                    <h4 class="footer__column-title">Tai nguyen ho tro</h4>
                    <ul class="footer__link-list">
                        <li><a href="#" class="footer__link">Cham soc nguoi cao tuoi</a></li>
                        <li><a href="#" class="footer__link">Tieu chuan bao mat</a></li>
                        <li><a href="#" class="footer__link">Giai phap cho he thong</a></li>
                        <li><a href="#" class="footer__link">Trang thai he thong</a></li>
                        <li><a href="#" class="footer__link">Video bai giang</a></li>
                        <li><a href="#" class="footer__link">Cap nhat phien ban</a></li>
                    </ul>
                </div>

                <div class="footer__column">
                    <h4 class="footer__column-title">Dang ky nhan tin</h4>
                    <p style="font-size:14px;color:#666;margin-bottom:12px;line-height:1.6;">
                        Dang ky de nhan thong tin va cap nhat moi nhat tu Nursing Home.
                    </p>
                    <form class="footer__newsletter-form" onsubmit="return false;">
                        <input type="email" class="footer__newsletter-input" placeholder="Email cua ban...">
                        <button type="submit" class="footer__newsletter-btn">Dang ky</button>
                    </form>
                </div>
            </div>

            <div class="footer__bottom">
                <p>Ban quoc thuoc ve Nursing Home | Nhom 8 - MockProject 062026</p>
                <div class="footer__bottom-links">
                    <a href="#" class="footer__bottom-link">Trung tam ho tro</a>
                    <a href="#" class="footer__bottom-link">Dieu khoan &amp; Dieu kien</a>
                </div>
            </div>
        </div>
    </footer>

    <script>
        function togglePassword() {
            var pw = document.getElementById('password');
            var icon = document.getElementById('eye-icon');
            if (pw.type === 'password') {
                pw.type = 'text';
                icon.innerHTML = '<path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/>';
            } else {
                pw.type = 'password';
                icon.innerHTML = '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/>';
            }
        }
    </script>

</body>
</html>"""
write_file("apps/accounts/templates/accounts/login.html", LOGIN_HTML)

print("\n=== HOAN TAT! ===")
print("Chay: python manage.py runserver")
print("Mo trinh duyet: http://localhost:8000/")