import enum


class Bandeira(enum.Enum):
    VISA = "Visa"
    MASTERCARD = "Mastercard"
    HIPERCARD = "Hipercard"
    AMEX = "Amex"
    DINERS = "Diners"
    ELO = "Elo"
    AURA = "Aura"
    DISCOVER = "Discover"
    CASASHOW = "CasaShow"
    HAVAN = "Havan"
    HUGCARD = "HugCard"
    ANDARAKI = "AndarAki"
    LEARDERCARD = "LearderCard"

    @classmethod
    def choices(cls):
        return [(v.value, v.display) for _, v in cls._member_map_.items()]
