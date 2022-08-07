import vonage
from config.settings import VONAGE_API_KEY, VONAGE_API_SECRET
from .models import VerificationData


def request_verification(profile):
    recipient_number = profile.telephone
    client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
    response = client.verify.start_verification(number=recipient_number, brand="MyTube")

    if response["status"] == "0":
        VerificationData.objects.create(profile=profile, request_id=response["request_id"])
        print("Started verification request_id is %s" % (response["request_id"]))
    else:
        print("Error: %s" % response["error_text"])


def check_verification(profile, data):

    verification = VerificationData.objects.get(profile=profile)
    client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
    response = client.verify.check(verification.request_id, code=data.code)

    if response["status"] == "0":
        return True
    else:
        return False

