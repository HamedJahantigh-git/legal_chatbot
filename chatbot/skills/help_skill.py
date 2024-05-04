from opsdroid.skill import Skill
from opsdroid.matchers import match_regex

class HelloSkill(Skill):
    @match_regex(r'help')
    async def hello(self, message):
        await message.respond('Hey there! this is the legal bot.\n Blah Blah Blah ...')