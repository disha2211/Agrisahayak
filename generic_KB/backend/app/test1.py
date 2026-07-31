from knowledge_pipeline.utils import *

create_directories()

logger = get_logger()

logger.info("Pipeline Initialized Successfully")

session = create_session()

response = session.get(

    "https://agritech.tnau.ac.in"

)

print(response.status_code)