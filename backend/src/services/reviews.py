import uuid
from src.models import GroupReview
from src.services.runs import require_completed
from src.utils.time import now
from src.utils.serialization import serialize
def create(db,payload,user):
 require_completed(db,payload.run_id)
 item=GroupReview(id=str(uuid.uuid4()),author=user["email"],created_at=now(),**payload.model_dump());db.add(item);db.commit();return serialize(item)
