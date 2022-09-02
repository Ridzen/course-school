from modeltranslation.translator import translator, TranslationOptions
from .models import MasterClass


class MasterClassTranslationOptions(TranslationOptions):
    fields = ('title', 'subtitle', 'overview', 'duration')


translator.register(MasterClass, MasterClassTranslationOptions)
