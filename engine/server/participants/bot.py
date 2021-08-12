##########################################################################
# Bot: A Participant sub-class where one instance controls one country
# with AI
##########################################################################

from engine.server.participants.participant import Participant

class Bot(Participant):
    
    def __init__(self, country_obj):
        super().__init__(country_obj)