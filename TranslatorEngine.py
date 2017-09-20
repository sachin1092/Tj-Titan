import json
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator
from constants import translator_creds

language_translator = LanguageTranslator(
    username=translator_creds.get("username"),
    password=translator_creds.get("password"))

def translateSentence(text, src, tar):
    translation = language_translator.translate(
        text=text,
        source=src,
        target=tar)
    print translation
    return translation

if __name__ == '__main__':
    translateSentence('Good morning', 'en', 'de')
