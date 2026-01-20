"""
Admin site configuration for LegalDocs Manager.

Customizes the Django admin site header, title, and index title
for proper branding of the legal document management system.
"""
from django.contrib import admin

# Customize admin site branding
admin.site.site_header = "LegalDocs Manager"
admin.site.site_title = "LegalDocs Manager"
admin.site.index_title = "Panel de Administración"
admin.site.site_url = "/api/v1/docs/"  # Link "Ver sitio" to Swagger documentation
