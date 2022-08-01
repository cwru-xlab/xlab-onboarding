import re

from aws_lambda_powertools.utilities import data_classes
from aws_lambda_powertools.utilities.data_classes import SESEvent
from aws_lambda_powertools.utilities.typing import LambdaContext

SENDER = re.compile(r"systems@hubofallthings.net")


@data_classes.event_source(data_class=SESEvent)
def allow_dataswift(event: SESEvent, context: LambdaContext) -> dict[str, str]:
    sender = event.record.ses.mail.common_headers.get_from[0]
    disposition = "CONTINUE" if SENDER.match(sender) else "STOP_RULE_SET"
    return {"disposition": disposition}
