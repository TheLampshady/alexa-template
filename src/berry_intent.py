import random
from base import BaseAlexaRequest


SLOT_NAME = 'berry'


member_list = [
    "Star Wars",
    "Chew Bacca",
    "Taun Tauns.",
    "Ice Planet Hoth.",
    "Han Solo.",
    "E walks."
]

member_response = [
    "I member {b}",
    "Oh yes, {b}. I member",
    "Oooo {b}, yes!",
    "Hahaha {b}, yes, i member!",
    "I love {b}! I member {b}",
    "Of course i member {b}! I love {b}",
]


class MemberRequest(BaseAlexaRequest):

    def GetMember(self):
        reprompt_text = None
        value = self.session_attributes.get(SLOT_NAME)
        if value:
            speech_output = random.choice(member_response).format(b=value) + \
                            "Lets member later."
        else:
            speech_output = "I do not member. What do you memeber?"
            reprompt_text = "Do you member?"
        return self.build_response(
            speechletResponse=self.build_speechlet_response(
                title='I Member',
                response_text=speech_output,
                reprompt_text=reprompt_text
            )
        )

    def SetMember(self):
        value = self.get_slot(name=SLOT_NAME)
        if value:
            speech_output = random.choice(member_response).format(b=value)
            reprompt_text = "Do you member?"
        else:
            speech_output = "Naw. You member?."
            reprompt_text = "Do you member?"

        self.session_attributes[SLOT_NAME] = value
        return self.build_response(
            speechletResponse=self.build_speechlet_response(
                title='You Member',
                response_text=speech_output,
                reprompt_text=reprompt_text
            )
        )

    def TellMember(self):
        response_text = "Do you Member, " +  \
                        random.choice(member_list) + "? " \

        return self.build_response(
            speechletResponse=self.build_speechlet_response(
                title='New Berry',
                response_text=response_text,
                reprompt_text="Tell me something you member."
            )
        )

    def LaunchRequest(self):
        response_text = "I member. I love " +  \
                        random.choice(member_list) + ". " \
                        "Do you Member?"
        reprompt_text = "Ask if I member."

        return self.build_response(
            speechletResponse=self.build_speechlet_response(
                title='Launch',
                response_text=response_text,
                reprompt_text=reprompt_text
            )
        )

    def AMAZON_HelpIntent(self):
        return self.build_response(
            speechletResponse=self.build_speechlet_response(
                title='Help Intent',
                response_text="Give member berries something to remember by saying. "
                              "Say, member followed by your favorite thing, or say, "
                              "I member to hear more.",
                reprompt_text="Say, you member X wings",
                card_text="Sample: \n"
                          "'you member science.'\n"
                          "'do you member."
            )
        )