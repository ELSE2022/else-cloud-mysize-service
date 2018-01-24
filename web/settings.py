import os

# Flask settings
FLASK_DEBUG = True  # Do not use debug mode in production

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, "attachments")
SCANNER_STORAGE_BASE_URL = 'https://else:7kjfWVWcRN@avatar3d.ibv.org:8443/webdav/ELSE/'
ELSE_3D_SERVICE_URL = u"http://else-3d-service.cloudapp.net/api/"

IMPORT_DATA_FROM_POSTGRES = False
