import sys
from opsdroid.skill import Skill
from opsdroid.matchers import match_regex

ROOT_DIR = "/home/miirzamiir/codes/nlp/legal_chatbot"
sys.path.append(ROOT_DIR)

from setup import Run

class ExtractorSkill(Skill):
    @match_regex(r'^(?!راهنما$)')
    async def extract(self, message):
                
        result = "متن وارد شده پردازش و اطلاعات کلیدی زیر از آن استخراج شد:\n\n"
        await message.respond(result)
        result = ''

        runner = Run()
        features = runner.run(message.text)
        for feature in features:
            result += f"در جمله ی {feature['Sentence']}:\n"

            result += 'مواد اشاره شده در متن:\n'
            if feature['Article'] == []:
                result += 'هیچ عنوان ماده ای پیدا نشد.\n'
            else:
                for art in feature['Article']:
                    result += f'{art[0]}\n(از کاراکتر {art[1]} تا کاراکتر {art[2]})\n\n'
            
            result += '\nقوانین اشاره شده در متن:\n'
            if feature['Law'] == []:
                result += 'هیچ عنوان قانونی پیدا نشد.\n'
            else:
                for law in feature['Law']:
                    result += f'{law[0]}\n(از کاراکتر {law[1]} تا کاراکتر {law[2]})\n\n'

            result += '\nنام نهادهای اشاره شده در متن:\n'
            if feature['Organization'] == []:
                result += 'هیچ نام نهادی پیدا نشد.\n'
            else:
                for org in feature['Organization']:
                    result += f'{org[0]}\n(از کاراکتر {org[1]} تا کاراکتر {org[2]})\n\n'

            result += '\nتاریخ های اشاره شده در متن:\n'
            if feature['Date'] == []:
                result += 'هیچ تاریخی پیدا نشد.\n'
            else:
                for date in feature['Date']:
                    result += f'{date[0]}\n(از کاراکتر {date[1]} تا کاراکتر {date[2]})\n\n'

            await message.respond(result)
            result = ''


