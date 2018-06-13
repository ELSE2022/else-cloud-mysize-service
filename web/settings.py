import os

# Flask settings
FLASK_DEBUG = True  # Do not use debug mode in production
REST_ADMIN_LOGIN = 'root'
REST_ADMIN_PASSWORD = 'rootpswd'

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_ROOT = os.path.join(BASE_DIR, "attachments")
SCANNER_STORAGE_BASE_URL = 'https://else:7kjfWVWcRN@avatar3d.ibv.org:8443/webdav/ELSE/'
ELSE_3D_SERVICE_URL = os.getenv('ELSE_3D_SERVICE', 'https://3d.else.shoes')
ELSE_STAGE_3D_SERVICE_URL = os.getenv('STAGE_ELSE_3D_SERVICE', 'https://stage.3d.else.shoes')
ELSE_3D_SERVICE_FULL = os.getenv('ELSE_3D_SERVICE_FULL', 'http://else-3d-service.cloudapp.net')
IMPORT_DATA_FROM_POSTGRES = False

DEFAULT_STORAGE_LOGIN = 'else'
DEFAULT_STORAGE_PASSWORD = '7kjfWVWcRN'
