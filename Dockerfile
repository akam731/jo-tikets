# Utilise Python 3.12
FROM python:3.12-slim

# Empêche Python d’écrire des fichiers .pyc et garde stdout lisible
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crée et utilise le répertoire de travail
WORKDIR /app

# Installe les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Copie le projet
COPY . .

# Crée le dossier logs (important)
RUN mkdir -p /app/logs

# Installe les dépendances Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Collecte les fichiers statiques
RUN python manage.py collectstatic --noinput

# Commande de lancement
CMD gunicorn jo_tickets.wsgi:application --bind 0.0.0.0:${PORT:-8000}
