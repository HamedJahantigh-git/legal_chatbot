import os
import sys
from opsdroid.skill import Skill
from opsdroid.matchers import match_regex, match_parse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from model.feature_extraction.feature_extractor import FeatureExtractor

class ExtractorSkill(Skill):
    @match_regex(r'extract')
    async def extract(self, message):
        await message.respond("Please provide the text to extract organization names from.")
        
        response = await self.opsdroid.listen(match_parse(".*"), timeout=60)
        if response:
            ext = FeatureExtractor(response.text)
            response.respond(ext.extract())
            