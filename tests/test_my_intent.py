from base import TestBaseIntent
from src.lambda_function import lambda_handler


class TestLambda(TestBaseIntent):

    def test_lambda_sets_berry(self):
        mock_intent = {
            "name": "SetMember",
            "slots": {
                "berry": {
                  "name": "berry",
                  "value": "star wars"
                }
            }
        }
        mock_event = self.get_mock_event(intent=mock_intent)

        result = lambda_handler(mock_event, {})
        self.assertTrue(result)
        response = result.get("response")
        attributes = result.get("sessionAttributes")

        self.assertFalse(response.get("shouldEndSession", True), "The session ended.")
        self.assertEqual(attributes.get("berry", ""), "star wars", "I don't memeber")

    def test_lambda_gets_berry(self):
        mock_intent = {
            "name": "GetMember",
        }
        mock_event = self.get_mock_event(intent=mock_intent)

        result = lambda_handler(mock_event, {})
        self.assertTrue(result)
        response = result.get("response")
        attributes = result.get("sessionAttributes")

        self.assertFalse(response.get("shouldEndSession", True), "The session ended.")
        self.assertFalse(attributes, "Attributes found")
