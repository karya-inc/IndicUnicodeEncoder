from indic_unicode_encoder.encoder import EncoderBuilder
from os import path

mappings_path = path.join(path.dirname(__file__), "char_mappings.csv")
prefix_path = path.join(path.dirname(__file__), "prefix_signs.csv")
sign_priorities_path = path.join(path.dirname(__file__), "sign_priorities.csv")

LepchaEncoder = (
    EncoderBuilder()
    .mappings_file(mappings_path)
    .prefix_file(prefix_path)
    .priorities_file(sign_priorities_path)
)
