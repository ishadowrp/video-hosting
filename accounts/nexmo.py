import vonage
from config.settings import VONAGE_API_KEY, VONAGE_API_SECRET
from .models import VerificationData


def request_verification(profile):
    recipient_number = profile.telephone
    client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
    response = client.verify.start_verification(number=recipient_number, brand="MyTube")

    if response["status"] == "0":
        try:
            verification_data = VerificationData.objects.create(profile=profile, request_id=response["request_id"])
            verification_data.save()
        except:
            print('Error with save verification data!')

        print("Started verification request_id is %s" % (response["request_id"]))
    else:
        print("Error: %s" % response["error_text"])


def check_verification(profile, data):
    verifications = VerificationData.objects.filter(profile=profile).order_by('-created',)
    client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
    if len(verifications) > 0:
        response = client.verify.check(verifications[0].request_id, code=data.code)
    else:
        return False

    if response["status"] == "0":
        return True
    else:
        return False
