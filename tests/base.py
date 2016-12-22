import unittest


class TestBaseIntent(unittest.TestCase):

    def get_mock_event(self, intent=None, session_id="SessionId.uuid", attributes=None):
        mock_event = {
            "session": {
                "sessionId": session_id,
                "application": {
                    "applicationId": "amzn1.ask.skill.1234"
                },
                "user": {
                    "userId": "user_id"
                },
                "new": False
            },
            "request": {
                "requestId": "EdwRequestId.24744310-0cfc-432e-a5fd-d5f42813b8b7",
                "locale": "en-US",
                "timestamp": "2016-12-16T16:27:31Z",
            },
            "version": "1.0"
        }
        if intent:
            mock_event["request"]["type"] = "IntentRequest"
            mock_event["request"]["intent"] = intent

        if attributes:
            mock_event["session"]["attributes"] = attributes

        return mock_event

    def launch_request(self):
        return dict(
            session={
                "sessionId": "SessionId.5",
                "application": {
                    "applicationId": "amzn1.ask.skill.7"
                },
                "user": {
                    "userId": "amzn1.ask.account.E"
                },
                "new": True
            }, request={
                "type": "LaunchRequest",
                "requestId": "EdwRequestId.3",
                "locale": "en-US",
                "timestamp": "2016-12-22T22:12:42Z"
            }, version="1.0"
        )
