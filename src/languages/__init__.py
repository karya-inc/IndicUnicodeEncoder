from src.languages.lepcha import LepchaEncoder


def get_ecoder(lang: str):
    match lang:
        case "lepcha":
            return LepchaEncoder
        case _:
            raise AttributeError(f"Unsupported Language: {lang}")

