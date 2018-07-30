import settings
from services.db_connector_service import database_update_service

database_update_service(settings.DB_HOST, settings.DB_NAME, settings.DB_USER, settings.DB_PASSWORD, False)
