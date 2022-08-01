import email
import io
from email.message import Message

import boto3
from aws_lambda_powertools.utilities import data_classes
from aws_lambda_powertools.utilities.typing import LambdaContext

ses = boto3.resource("sesv2")
s3 = boto3.resource("s3")

"""
    SES.Client.exceptions.MessageRejected
    SES.Client.exceptions.MailFromDomainNotVerifiedException
    SES.Client.exceptions.ConfigurationSetDoesNotExistException
    SES.Client.exceptions.ConfigurationSetSendingPausedException
    SES.Client.exceptions.AccountSendingPausedException
"""


# TODO Need to send to S3 and then pull to access body
@data_classes.event_source(data_class=data_classes.SESEvent)
def relay(event: data_classes.SESEvent, context: LambdaContext):
    while mail := event.mail:
        message = open_message(mail.message_id)
        message.
        ses.send_email(
            Source=mail.source,
            Destination={
                "ToAddresses": envelope.to,
                "CcAddresses": envelope.cc,
                "BccAddresses": envelope.bcc
            },
            ReplyToAddresses=envelope.reply_to,
            Message={
                "Subject": message_part(envelope.subject),
                "Body": {
                    "Text": message_part()  # TODO
                }
            },
            ReturnPath=envelope.return_path
        )


def open_message(msg_id: str) -> Message:
    # Ref: https://github.com/boto/boto3/issues/564#issuecomment-1063261967
    obj = s3.get_object(Bucket=bucket, Key=msg_id)
    fp = io.BytesIO(obj["Body"].read())
    return email.message_from_file(fp)


def message_part(data) -> dict[str, str]:
    return {"Data": data, "Charset": "UTF-8"}
