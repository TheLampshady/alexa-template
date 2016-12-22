from berry_intent import MemberRequest


def lambda_handler(event, context={}):
    return MemberRequest(event=event).response()
