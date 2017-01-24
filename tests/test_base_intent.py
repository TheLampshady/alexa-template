from base import TestBaseIntent
from src.base import BaseAlexaRequest


class TestLambda(TestBaseIntent):

    def test_ssml_builds_from_text(self):
        mock_intent = {
            "name": "mock_intent",
        }
        mock_event = self.get_mock_event(intent=mock_intent)

        alexa = BaseAlexaRequest(event=mock_event)
        result = alexa.format_output_speech("This is a response. Test me.")

        self.assertEqual(result['type'], "SSML")
        self.assertTrue("<speak>" in result['ssml'])
        self.assertTrue(BaseAlexaRequest.BREAK in result['ssml'])

        result = alexa.format_output_speech("This is a response. Test me.")
        self.assertTrue(BaseAlexaRequest.BREAK in result['ssml'])

    def test_lambda_handles_error(self):
        mock_intent = {
            "name": "ErrorIntent",
        }
        mock_event = self.get_mock_event(intent=mock_intent)

        result = BaseAlexaRequest(event=mock_event).response()
        self.assertTrue(result)
        response = result.get("response")

        self.assertFalse(response.get("shouldEndSession", True), "The session ended.")