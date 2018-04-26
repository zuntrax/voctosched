import codecs
import re
import translitcodec
from string import ascii_letters, digits

from fahrplan.model.conference import Conference
from fahrplan.model.event import Event


class StandardSlugGenerator:
    def __init__(self, conference: Conference):
        if isinstance(conference, str):
            self.acronym = conference
        else:
            self.acronym = conference.acronym

    def __call__(self, event: Event):
        return self.generate(event.id, event.title)

    def generate(self, event_id, event_title):
        title = StandardSlugGenerator.normalize_name(event_title)
        return f"{self.acronym}-{event_id}-{title}"[:240]

    @staticmethod
    def normalize_name(name: str):
        name = codecs.encode(name, 'translit/long')
        name = re.sub(r"\W+", "_", name)
        legal_chars = ascii_letters + digits + "_"
        pattern = f"[^{legal_chars}]+"
        name = re.sub(pattern, "", name)
        name = name.lower()
        name = name.strip('_')
        return name
