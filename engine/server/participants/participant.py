##########################################################################
# Participant: A base class for game participants (i.e. Players and Bots)
##########################################################################


class Participant:
    def __init__(self, country_obj):
        self.country = country_obj
