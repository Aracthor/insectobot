from enum import Enum

class Language(Enum):
    English = 0
    French = 1

LOCALIZATION = {
    "critical_failure": ["critical failure", "échec critique"],
    "failure": ["failure", "échec"],
    "success": ["success", "réussite"],
    "improved_success": ["improved success", "réussite amélioré"],
    "critical_success": ["critical success", "réussite critique"],

    "capacity": ["capacity", "capacité"],
    "1_more_skill_point": ["+1 skill point", "+1 point de compétence"],
    "2_more_skill_point": ["+2 skill points", "+2 points de compétence"],
    "1_more_skill_point_and_1_more_free_skill_point": ["+1 skill point and +1 free skill point (for any skill)", "+1 point de compétence et +1 point pour n'importe quelle compétence"],
    "characteristic_improved": ["characteristic improved by 1", "caractéristique augmentée de 1"],

    "wing": ["Wing", "Aile"],
    "antenna": ["Antenna", "Antenne"],
    "caste": ["Caste", "Caste"],
    "chitin": ["Chitin", "Chitine"],
    "spirit": ["Spirit", "Esprit"],
    "mandible": ["Mandible", "Mandibule"],
    "temperature": ["Temperature", "Température"],

    "invalid_arg_count": ["Invalid argument count.", "Nombre d'arguments invalide."],
    "invalid_argument": ["Invalid argument.", "Argument invalide."],
    "invalid_count_number": ["Invalid argument: count must be between 1 and 42.", "Argument invalide: nombre doit être entre 1 et 42."],
    "invalid_language": ["Invalid language.", "Langue invalide."],
    "usage": ["Usage: `!draw [count]` or `!draw born`", "Usage: `!draw [nombre]` ou `!draw born`"],

    "language_set": ["Language set to english.", "Langue configurée en français."],

    "you_have_drawn": ["Draw:\n", "Tirage:\n"],
}

class localization_dictionnary:

    def __init__(self):
        self.language = Language.French

    def get(self, token):
        return LOCALIZATION[token][self.language.value]

    def set_language(self, language):
        self.language = language
