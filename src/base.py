import logging


class BaseAlexaRequest(object):

    @property
    def intent(self):
        return self.event['request']['intent']

    @property
    def intent_name(self):
        return self.event['request']['intent']['name']

    @property
    def request_type(self):
        return self.event['request']['type']

    def __init__(self, event):
        self.event = event
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

    def build_speechlet_response(self, title, response_text, reprompt_text=None):
        output = dict(
            outputSpeech=dict(
                type='PlainText',
                text=response_text,
            ),
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
        if self.request_type == 'IntentRequest':
            intent_name = self.intent_name.replace('.', '_')
            try:
                return getattr(self, intent_name)()
            except Exception as e:
                logging.info("Intent Not Implemented: %s" % intent_name)
                raise e
        elif self.request_type == "LaunchRequest":
            return self.LaunchRequest()
        return 'intentType: {s.request_type}'.format(s=self)

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
                title='CancelIntent',
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