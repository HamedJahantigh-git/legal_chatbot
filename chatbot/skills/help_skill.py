from opsdroid.skill import Skill
from opsdroid.matchers import match_regex

class HelpSkill(Skill):
    @match_regex(r'help')
    async def hello(self, message):
        await message.respond('hi')


# 'سلام\nبه legalchatbot خوش اومدی.\nدر این بات با وارد کردن یک متن حقوقی، \
                            #   ویژگی های موجود در آن متن استخراج شده و به کاربر نمایش داده می شوند. \
                            #   جهت استفاده از این قابلیت '