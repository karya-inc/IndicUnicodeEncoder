from indic_unicode_encoder.languages.lepcha import LepchaEncoder
from indic_unicode_encoder.languages.limbu import LimbuEncoder


def get_ecoder(lang: str):
    match lang:
        case "lepcha":
            return LepchaEncoder
        case "limbu":
            return LimbuEncoder
        case _:
            raise AttributeError(f"Unsupported Language: {lang}")

