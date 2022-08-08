from dotenv import load_dotenv
from split_settings.tools import include


load_dotenv()

# Application definition

include(
    'components/base.py',
)

# Database

include(
    'components/database.py',
)

# Localization

include(
    'components/localization.py'
)

# Static files (CSS, JavaScript, Images)

include(
    'components/static.py'
)

# logging

include(
    'components/logging.py'
)
