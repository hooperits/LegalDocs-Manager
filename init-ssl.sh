#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Load environment variables
if [ -f .env ]; then
    # Export vars, ignoring comments
    export $(grep -v '^#' .env | xargs)
else
    echo "Error: .env file not found."
    echo "Please copy .env.example to .env and set DOMAIN_NAME and CERTBOT_EMAIL."
    exit 1
fi

if [ -z "$DOMAIN_NAME" ]; then
    echo "Error: DOMAIN_NAME is not set in .env."
    exit 1
fi

if [ -z "$CERTBOT_EMAIL" ]; then
    echo "Error: CERTBOT_EMAIL is not set in .env."
    exit 1
fi

# Check for staging flag
STAGING_ARG=""
STAGING_MSG="production"
if [[ "$1" == "--staging" || "$1" == "-s" ]]; then
    STAGING_ARG="--staging"
    STAGING_MSG="staging (test)"
fi

echo "========================================================================="
echo "LegalDocs Manager - SSL/TLS Setup"
echo "Domain: ${DOMAIN_NAME} (and www.${DOMAIN_NAME})"
echo "Email:  ${CERTBOT_EMAIL}"
echo "Mode:   ${STAGING_MSG}"
echo "========================================================================="

# Helper function to check if certificates exist in the volume
check_certs_exist() {
    docker compose -f docker-compose.prod.yml run --rm --entrypoint \
        "sh -c '[ -f /etc/letsencrypt/live/${DOMAIN_NAME}/privkey.pem ]'" certbot >/dev/null 2>&1
}

if check_certs_exist; then
    echo "Existing certificates found for ${DOMAIN_NAME}."
    echo "Starting services..."
    docker compose -f docker-compose.prod.yml up -d
    exit 0
fi

echo "No existing certificates found."
echo "Step 1: Generating temporary self-signed certificates..."

docker compose -f docker-compose.prod.yml run --rm --entrypoint \
    "sh -c 'mkdir -p /etc/letsencrypt/live/${DOMAIN_NAME} && \
     openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
     -keyout /etc/letsencrypt/live/${DOMAIN_NAME}/privkey.pem \
     -out /etc/letsencrypt/live/${DOMAIN_NAME}/fullchain.pem \
     -subj \"/CN=${DOMAIN_NAME}\"'" certbot

echo "Step 2: Starting Nginx..."
docker compose -f docker-compose.prod.yml up --build -d nginx

# Check for local fallback mode
if [[ "$DOMAIN_NAME" == "localhost" || "$DOMAIN_NAME" == "127.0.0.1" ]]; then
    echo "------------------------------------------------------------------------"
    echo "Local domain detected (${DOMAIN_NAME})."
    echo "Keeping self-signed certificates for local testing."
    echo "Nginx is now running at https://${DOMAIN_NAME}."
    echo "Note: Your browser will display a security warning (this is expected)."
    echo "------------------------------------------------------------------------"
    exit 0
fi

echo "Step 3: Requesting real Let's Encrypt certificates..."

# Remove dummy certificates before requesting real ones (otherwise Certbot gets confused)
echo "Removing dummy certificates..."
docker compose -f docker-compose.prod.yml run --rm --entrypoint \
    "sh -c 'rm -rf /etc/letsencrypt/live/${DOMAIN_NAME} /etc/letsencrypt/archive/${DOMAIN_NAME} /etc/letsencrypt/renewal/${DOMAIN_NAME}.conf'" certbot

# Request Let's Encrypt certificates
if docker compose -f docker-compose.prod.yml run --rm --entrypoint \
    "certbot certonly --webroot -w /var/www/certbot \
     --email ${CERTBOT_EMAIL} \
     -d ${DOMAIN_NAME} -d www.${DOMAIN_NAME} \
     --agree-tos --no-eff-email --no-self-upgrade \
     ${STAGING_ARG}" certbot; then

    echo "Step 4: Reloading Nginx configuration..."
    docker compose -f docker-compose.prod.yml exec nginx nginx -s reload
    echo "Success! SSL certificates have been successfully provisioned and loaded."
else
    echo "Error: Certbot failed to obtain certificates."
    echo "Restoring temporary self-signed certificates to keep services running..."
    docker compose -f docker-compose.prod.yml run --rm --entrypoint \
        "sh -c 'mkdir -p /etc/letsencrypt/live/${DOMAIN_NAME} && \
         openssl req -x509 -nodes -newkey rsa:2048 -days 365 \
         -keyout /etc/letsencrypt/live/${DOMAIN_NAME}/privkey.pem \
         -out /etc/letsencrypt/live/${DOMAIN_NAME}/fullchain.pem \
         -subj \"/CN=${DOMAIN_NAME}\"'" certbot
    docker compose -f docker-compose.prod.yml exec nginx nginx -s reload
    exit 1
fi
