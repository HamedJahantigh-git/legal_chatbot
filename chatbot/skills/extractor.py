import sys
from opsdroid.skill import Skill
from opsdroid.matchers import match_regex
ROOT_DIR = "/home/miirzamiir/codes/nlp/legal_chatbot"
sys.path.append(ROOT_DIR)
from setup import Run

class ExtractorSkill(Skill):
    @match_regex(r'^(?!راهنما$)')
    async def extract(self, message):
        
        await message.respond()
