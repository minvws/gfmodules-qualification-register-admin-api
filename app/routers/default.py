import logging

import json
from pathlib import Path
from fastapi import APIRouter, Response

logger = logging.getLogger(__name__)
router = APIRouter()

# https://www.patorjk.com/software/taag/#p=display&f=Doom&t=Skeleton
LOGO = r"""
________               .__  .__  _____.__               __  .__
\_____  \  __ _______  |  | |__|/ ____\__| ____ _____ _/  |_|__| ____   ____
 /  / \  \|  |  \__  \ |  | |  \   __\|  |/ ___\\__  \\   __\  |/  _ \ /    \
/   \_/.  \  |  // __ \|  |_|  ||  |  |  \  \___ / __ \|  | |  (  <_> )   |  \
\_____\ \_/____/(____  /____/__||__|  |__|\___  >____  /__| |__|\____/|___|  /
       \__>          \/                       \/     \/                    \/

"""


@router.get("/", include_in_schema=False)
def index() -> Response:
    content = LOGO

    try:
        with open(Path(__file__).parent.parent.parent / 'version.json', 'r') as file:
            data = json.load(file)
            content += "\nVersion: %s\nCommit: %s" % (data['version'], data['git_ref'])
    except BaseException as e:
        content += "\nNo version information found"
        logger.info("Version info could not be loaded: %s" % e)

    return Response(content)
