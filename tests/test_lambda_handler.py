from tests.base import TestBaseIntent
from src.lambda_function import lambda_handler


class TestLambda(TestBaseIntent):

    def test_lambda_cancel_response(self):
        mock_intent = {
                    "name": "AMAZON_CancelIntent",
                    "slots": {}
                }
        mock_event = self.get_mock_event(intent=mock_intent)

        result = lambda_handler(mock_event)
        self.assertTrue(result)
        response = result.get("response")

        self.assertTrue(response.get("shouldEndSession", False), "The session did not end.")

    def test_lambda_gets_context_attributes(self):
        mock_intent = {
            "name": "AMAZON_HelpIntent",
        }
        mock_event = self.get_mock_event(intent=mock_intent)

        result = lambda_handler(mock_event, {})
        self.assertTrue(result)

        response = result.get("response")
        attributes = result.get("sessionAttributes")
        context = attributes.get('context')

        self.assertFalse(response.get("shouldEndSession", True), "The session ended.")
        self.assertFalse(context, "Context found")

    def test_lambda_launch_request(self):
        mock_event = self.launch_request()

        result = lambda_handler(mock_event, {})
        self.assertTrue(result)
