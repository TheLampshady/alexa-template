import logging


class SingleLog(object):

    def __init__(self):
        self.error = ""

    def log_error(self, user_key, message):
        self.error = message

    def get_error(self, user_key):
        return self.error

single_log = SingleLog()


class BaseAlexaRequest(object):

    BREAK = " <break /> "

    @property
    def intent(self):
        return self.event['request']['intent']

    @property
    def intent_name(self):
        return self.event['request']['intent']['name']

    @property
    def request_type(self):
        return self.event['request']['type']

    @property
    def user(self):
        return self.event['session']['user']['userId']

    def __init__(self, event, is_ssml=True, user_logger=single_log):
        self.event = event
        self.is_ssml = is_ssml
        self.user_logger = user_logger

        session = self.event.get("session", dict())

        self.session_attributes = session.get("attributes", dict())

        self._context = self.session_attributes.get('context', list())

    def build_response(self, speechletResponse):
        if self._context:
            self.session_attributes['context'] = self._context
        return dict(
            version='1.0',
            sessionAttributes=self.session_attributes,
            response=speechletResponse,
        )

    def get_slot(self, name):
        try:
            return self.intent['slots'][name]['value']
        except KeyError as ke:
            logging.warning("No Slot Attribute ")
            return None

    def add_context(self, value):
        self._context.insert(0, value)

    def clear_context(self):
        self._context = []

    @property
    def current_context(self):
        return self._context[0] if self._context else None

    def format_output_speech(self, value):
        output_speech = dict(type="SSML" if self.is_ssml else "PlainText")
        if self.is_ssml:
            wrap = "<speak>%s</speak>" % value
            output_speech["ssml"] = wrap.replace(". ", self.BREAK).replace(", ", self.BREAK)
        else:
            output_speech["text"] = value

        return output_speech

    def build_speechlet_response(self, title, response_text, reprompt_text=None):
        output = dict(
            outputSpeech=self.format_output_speech(response_text),
            card=dict(
                type='Simple',
                title=title,
                content=response_text,
            ),
            shouldEndSession=True,
        )
        if reprompt_text is not None:
            output['reprompt'] = dict(
                outputSpeech=dict(
                    type='PlainText',
                    text=reprompt_text,
                )
            )
            output['shouldEndSession'] = False
        return output

    def response(self):
        try:
            if self.request_type == 'IntentRequest':
                intent_name = self.intent_name.replace('.', '_')
                try:
                    return getattr(self, intent_name)()
                except Exception as e:
                    logging.warning(e)
                    raise e
            elif self.request_type == "LaunchRequest":
                return self.LaunchRequest()
            return 'intentType: {s.request_type}'.format(s=self)
        except Exception as e:
            self.user_logger.log_error(self.user, e.message)
            return self.ErrorIntent()

    def LaunchRequest(self):
        return self.build_response(
            speechletResponse=self.build_speechlet_response(
                title='Launch',
                response_text="Welcome!",
            )
        )

    def AMAZON_CancelIntent(self):
        self.clear_context()
        return self.build_response(
            speechletResponse=self.build_speechlet_response(
                title='Cancel Intent',
                response_text='goodbye',
            )
        )

    def AMAZON_StopIntent(self):
        self.clear_context()
        return self.build_response(
            speechletResponse=self.build_speechlet_response(
                title='Stop Intent',
                response_text='goodbye',
            )
        )

    def AMAZON_HelpIntent(self):
        return self.build_response(
            speechletResponse=self.build_speechlet_response(
                title='Help Intent',
                response_text="Read the Manual.",
                reprompt_text="R T F M"
            )
        )

    def ErrorIntent(self, error):
        return self.build_response(
            speechletResponse=self.build_speechlet_response(
                title='Error',
                response_text="There was an error with the intent: %s." % self.intent_name,
                reprompt_text="Say Diagnostic for details."
            )
        )

    def DiagnosticIntent(self):
        speech_output = self.user_logger.get_error(self.user) or "Nothing is wrong"
        return self.build_response(
            speechletResponse=self.build_speechlet_response(
                title='Diagnostic',
                response_text=speech_output,
                reprompt_text="Does that help."
            )
        )