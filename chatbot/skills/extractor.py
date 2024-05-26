import sys
from opsdroid.skill import Skill
from opsdroid.matchers import match_regex
ROOT_DIR = "/home/miirzamiir/codes/nlp/legal_chatbot"
sys.path.append(ROOT_DIR)
from model.feature_extraction.feature_extractor import FeatureExtractor

class ExtractorSkill(Skill):
    @match_regex(r'^(?!راهنما$)')
    async def extract(self, message):
        ext = FeatureExtractor(message.text)
        await message.respond(ext.extract())
