from opsdroid.skill import Skill
from opsdroid.matchers import match_regex

class HelpSkill(Skill):
    @match_regex(r'راهنما')
    async def hello(self, message):
        await message.respond('سلام\nبه چت بات حقوقی خوش آمدید.\nدر این بات با وارد کردن یک متن حقوقی،  ویژگی های موجود در آن متن استخراج شده و به کاربر نمایش داده می شوند.\nجهت استفاده از این قابلیت متن حقوقی مورد نظر خود را ارسال کنید. ')
