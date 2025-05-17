from enum import Enum


class EnumBaseClass:

    @classmethod
    def choices(cls):
        return [(x.value, x.name) for x in cls]

    @classmethod
    def values(cls):
        return [x.value for x in cls]


class OrderStatus(EnumBaseClass, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class PaymentStatus(EnumBaseClass, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class Courier(EnumBaseClass, Enum):
    DHL = "DHL"
    EXPRESS = "EXPRESS"


shipping_region = {
    "UK": "uk",
    "West Africa": "w_africa",
    "USA": "usa",
    "Europe": "europe",
    "East Africa": "e_africa",
    "Asia": "asia",
    "China": "china",
    "Caribbean": "caribbean",
}


custom_fee_percentage = {
    "0.5": 0.05,
    "0.10": 0.1,
    "0.15": 0.15,
    "0.20": 0.2,
    "0.25": 0.25,
    "0.30": 0.3,
    "0.35": 0.35,
    "0.40": 0.4,
    "0.45": 0.45,
    "0.50": 0.5,
    "0.55": 0.55,
    "0.60": 0.6,
    "0.65": 0.65,
    "0.70": 0.7,
    "0.75": 0.75,
    "0.80": 0.8,
    "0.85": 0.85,
    "0.90": 0.9,
    "0.95": 0.95,
    "0.100": 1.0,
}
custom_fee_percentage_list = list(custom_fee_percentage.items())


country_currency_map = {
    "AF": {"currency": "AFN", "symbol": "؋"},
    "AL": {"currency": "ALL", "symbol": "Lek"},
    "DZ": {"currency": "DZD", "symbol": "د.ج"},
    "AS": {"currency": "USD", "symbol": "$"},
    "AD": {"currency": "EUR", "symbol": "€"},
    "AO": {"currency": "AOA", "symbol": "Kz"},
    "AI": {"currency": "XCD", "symbol": "$"},
    "AG": {"currency": "XCD", "symbol": "$"},
    "AR": {"currency": "ARS", "symbol": "$"},
    "AM": {"currency": "AMD", "symbol": "Դ"},
    "AW": {"currency": "AWG", "symbol": "ƒ"},
    "AU": {"currency": "AUD", "symbol": "$"},
    "AT": {"currency": "EUR", "symbol": "€"},
    "AZ": {"currency": "AZN", "symbol": "₼"},
    "BS": {"currency": "BSD", "symbol": "$"},
    "BH": {"currency": "BHD", "symbol": ".د.ب"},
    "BD": {"currency": "BDT", "symbol": "৳"},
    "BB": {"currency": "BBD", "symbol": "$"},
    "BY": {"currency": "BYN", "symbol": "Br"},
    "BE": {"currency": "EUR", "symbol": "€"},
    "BZ": {"currency": "BZD", "symbol": "BZ$"},
    "BJ": {"currency": "XOF", "symbol": "CFA"},
    "BM": {"currency": "BMD", "symbol": "$"},
    "BT": {"currency": "BTN", "symbol": "Nu."},
    "BO": {"currency": "BOB", "symbol": "Bs."},
    "BA": {"currency": "BAM", "symbol": "KM"},
    "BW": {"currency": "BWP", "symbol": "P"},
    "BR": {"currency": "BRL", "symbol": "R$"},
    "BN": {"currency": "BND", "symbol": "$"},
    "BG": {"currency": "BGN", "symbol": "лв"},
    "BF": {"currency": "XOF", "symbol": "CFA"},
    "BI": {"currency": "BIF", "symbol": "FBu"},
    "KH": {"currency": "KHR", "symbol": "៛"},
    "CM": {"currency": "XAF", "symbol": "FCFA"},
    "CA": {"currency": "CAD", "symbol": "$"},
    "CV": {"currency": "CVE", "symbol": "$"},
    "KY": {"currency": "KYD", "symbol": "$"},
    "CF": {"currency": "XAF", "symbol": "FCFA"},
    "TD": {"currency": "XAF", "symbol": "FCFA"},
    "CL": {"currency": "CLP", "symbol": "$"},
    "CN": {"currency": "CNY", "symbol": "¥"},
    "CO": {"currency": "COP", "symbol": "$"},
    "KM": {"currency": "KMF", "symbol": "CF"},
    "CG": {"currency": "XAF", "symbol": "FCFA"},
    "CD": {"currency": "CDF", "symbol": "FC"},
    "CR": {"currency": "CRC", "symbol": "₡"},
    "CI": {"currency": "XOF", "symbol": "CFA"},
    "HR": {"currency": "HRK", "symbol": "kn"},
    "CU": {"currency": "CUP", "symbol": "₱"},
    "CY": {"currency": "EUR", "symbol": "€"},
    "CZ": {"currency": "CZK", "symbol": "Kč"},
    "DK": {"currency": "DKK", "symbol": "kr"},
    "DJ": {"currency": "DJF", "symbol": "Fdj"},
    "DM": {"currency": "XCD", "symbol": "$"},
    "DO": {"currency": "DOP", "symbol": "RD$"},
    "EC": {"currency": "USD", "symbol": "$"},
    "EG": {"currency": "EGP", "symbol": "£"},
    "SV": {"currency": "SVC", "symbol": "$"},
    "GQ": {"currency": "XAF", "symbol": "FCFA"},
    "ER": {"currency": "ERN", "symbol": "Nfk"},
    "EE": {"currency": "EUR", "symbol": "€"},
    "ET": {"currency": "ETB", "symbol": "Br"},
    "FJ": {"currency": "FJD", "symbol": "$"},
    "FI": {"currency": "EUR", "symbol": "€"},
    "FR": {"currency": "EUR", "symbol": "€"},
    "GA": {"currency": "XAF", "symbol": "FCFA"},
    "GM": {"currency": "GMD", "symbol": "D"},
    "GE": {"currency": "GEL", "symbol": "₾"},
    "DE": {"currency": "EUR", "symbol": "€"},
    "GH": {"currency": "GHS", "symbol": "¢"},
    "GR": {"currency": "EUR", "symbol": "€"},
    "GD": {"currency": "XCD", "symbol": "$"},
    "GT": {"currency": "GTQ", "symbol": "Q"},
    "GN": {"currency": "GNF", "symbol": "FG"},
    "GW": {"currency": "XOF", "symbol": "CFA"},
    "GY": {"currency": "GYD", "symbol": "$"},
    "HT": {"currency": "HTG", "symbol": "G"},
    "HN": {"currency": "HNL", "symbol": "L"},
    "HU": {"currency": "HUF", "symbol": "Ft"},
    "IS": {"currency": "ISK", "symbol": "kr"},
    "IN": {"currency": "INR", "symbol": "₹"},
    "ID": {"currency": "IDR", "symbol": "Rp"},
    "IR": {"currency": "IRR", "symbol": "﷼"},
    "IQ": {"currency": "IQD", "symbol": "ع.د"},
    "IE": {"currency": "EUR", "symbol": "€"},
    "IL": {"currency": "ILS", "symbol": "₪"},
    "IT": {"currency": "EUR", "symbol": "€"},
    "JM": {"currency": "JMD", "symbol": "J$"},
    "JP": {"currency": "JPY", "symbol": "¥"},
    "JO": {"currency": "JOD", "symbol": "د.ا"},
    "KZ": {"currency": "KZT", "symbol": "₸"},
    "KE": {"currency": "KES", "symbol": "KSh"},
    "KI": {"currency": "AUD", "symbol": "$"},
    "KP": {"currency": "KPW", "symbol": "₩"},
    "KR": {"currency": "KRW", "symbol": "₩"},
    "KW": {"currency": "KWD", "symbol": "د.ك"},
    "KG": {"currency": "KGS", "symbol": "лв"},
    "LA": {"currency": "LAK", "symbol": "₭"},
    "LV": {"currency": "EUR", "symbol": "€"},
    "LB": {"currency": "LBP", "symbol": "£"},
    "LS": {"currency": "LSL", "symbol": "L"},
    "LR": {"currency": "LRD", "symbol": "$"},
    "LY": {"currency": "LYD", "symbol": "ل.د"},
    "LI": {"currency": "CHF", "symbol": "CHF"},
    "LT": {"currency": "EUR", "symbol": "€"},
    "LU": {"currency": "EUR", "symbol": "€"},
    "MG": {"currency": "MGA", "symbol": "Ar"},
    "MW": {"currency": "MWK", "symbol": "MK"},
    "MY": {"currency": "MYR", "symbol": "RM"},
    "MV": {"currency": "MVR", "symbol": "Rf"},
    "ML": {"currency": "XOF", "symbol": "CFA"},
    "MT": {"currency": "EUR", "symbol": "€"},
    "MH": {"currency": "USD", "symbol": "$"},
    "MR": {"currency": "MRU", "symbol": "UM"},
    "MU": {"currency": "MUR", "symbol": "₨"},
    "MX": {"currency": "MXN", "symbol": "$"},
    "FM": {"currency": "USD", "symbol": "$"},
    "MD": {"currency": "MDL", "symbol": "L"},
    "MC": {"currency": "EUR", "symbol": "€"},
    "MN": {"currency": "MNT", "symbol": "₮"},
    "ME": {"currency": "EUR", "symbol": "€"},
    "MA": {"currency": "MAD", "symbol": "د.م."},
    "MZ": {"currency": "MZN", "symbol": "MT"},
    "MM": {"currency": "MMK", "symbol": "K"},
    "NA": {"currency": "NAD", "symbol": "$"},
    "NR": {"currency": "AUD", "symbol": "$"},
    "NP": {"currency": "NPR", "symbol": "₨"},
    "NL": {"currency": "EUR", "symbol": "€"},
    "NZ": {"currency": "NZD", "symbol": "$"},
    "NI": {"currency": "NIO", "symbol": "C$"},
    "NE": {"currency": "XOF", "symbol": "CFA"},
    "NG": {"currency": "NGN", "symbol": "₦"},
    # Added missing countries
    "OM": {"currency": "OMR", "symbol": "ر.ع."},
    "PK": {"currency": "PKR", "symbol": "₨"},
    "PW": {"currency": "USD", "symbol": "$"},
    "PS": {"currency": "ILS", "symbol": "₪"},
    "PA": {"currency": "PAB", "symbol": "B/."},
    "PG": {"currency": "PGK", "symbol": "K"},
    "PY": {"currency": "PYG", "symbol": "₲"},
    "PE": {"currency": "PEN", "symbol": "S/."},
    "PH": {"currency": "PHP", "symbol": "₱"},
    "PL": {"currency": "PLN", "symbol": "zł"},
    "PT": {"currency": "EUR", "symbol": "€"},
    "PR": {"currency": "USD", "symbol": "$"},
    "QA": {"currency": "QAR", "symbol": "ر.ق"},
    "RO": {"currency": "RON", "symbol": "lei"},
    "RU": {"currency": "RUB", "symbol": "₽"},
    "RW": {"currency": "RWF", "symbol": "FRw"},
    "KN": {"currency": "XCD", "symbol": "$"},
    "LC": {"currency": "XCD", "symbol": "$"},
    "VC": {"currency": "XCD", "symbol": "$"},
    "WS": {"currency": "WST", "symbol": "T"},
    "SM": {"currency": "EUR", "symbol": "€"},
    "ST": {"currency": "STN", "symbol": "Db"},
    "SA": {"currency": "SAR", "symbol": "ر.س"},
    "SN": {"currency": "XOF", "symbol": "CFA"},
    "RS": {"currency": "RSD", "symbol": "дин."},
    "SC": {"currency": "SCR", "symbol": "₨"},
    "SL": {"currency": "SLL", "symbol": "Le"},
    "SG": {"currency": "SGD", "symbol": "$"},
    "SK": {"currency": "EUR", "symbol": "€"},
    "SI": {"currency": "EUR", "symbol": "€"},
    "SB": {"currency": "SBD", "symbol": "$"},
    "SO": {"currency": "SOS", "symbol": "Sh.So."},
    "ZA": {"currency": "ZAR", "symbol": "R"},
    "SS": {"currency": "SSP", "symbol": "£"},
    "ES": {"currency": "EUR", "symbol": "€"},
    "LK": {"currency": "LKR", "symbol": "Rs"},
    "SD": {"currency": "SDG", "symbol": "ج.س."},
    "SR": {"currency": "SRD", "symbol": "$"},
    "SZ": {"currency": "SZL", "symbol": "L"},
    "SE": {"currency": "SEK", "symbol": "kr"},
    "CH": {"currency": "CHF", "symbol": "CHF"},
    "SY": {"currency": "SYP", "symbol": "£S"},
    "TW": {"currency": "TWD", "symbol": "NT$"},
    "TJ": {"currency": "TJS", "symbol": "ЅМ"},
    "TZ": {"currency": "TZS", "symbol": "TSh"},
    "TH": {"currency": "THB", "symbol": "฿"},
    "TL": {"currency": "USD", "symbol": "$"},
    "TG": {"currency": "XOF", "symbol": "CFA"},
    "TO": {"currency": "TOP", "symbol": "T$"},
    "TT": {"currency": "TTD", "symbol": "TT$"},
    "TN": {"currency": "TND", "symbol": "د.ت"},
    "TR": {"currency": "TRY", "symbol": "₺"},
    "TM": {"currency": "TMT", "symbol": "m"},
    "TV": {"currency": "AUD", "symbol": "$"},
    "UG": {"currency": "UGX", "symbol": "USh"},
    "UA": {"currency": "UAH", "symbol": "₴"},
    "AE": {"currency": "AED", "symbol": "د.إ"},
    "GB": {"currency": "GBP", "symbol": "£"},
    "US": {"currency": "USD", "symbol": "$"},
    "UY": {"currency": "UYU", "symbol": "$U"},
    "UZ": {"currency": "UZS", "symbol": "лв"},
    "VU": {"currency": "VUV", "symbol": "VT"},
    "VA": {"currency": "EUR", "symbol": "€"},
    "VE": {"currency": "VES", "symbol": "Bs.S"},
    "VN": {"currency": "VND", "symbol": "₫"},
    "YE": {"currency": "YER", "symbol": "﷼"},
    "ZM": {"currency": "ZMW", "symbol": "ZK"},
    "ZW": {"currency": "ZWL", "symbol": "Z$"},
    "UK": {"currency": "GBP", "symbol": "£"},
    # Additional territories/dependencies
    "AX": {"currency": "EUR", "symbol": "€"},  # Åland Islands
    "BL": {"currency": "EUR", "symbol": "€"},  # Saint Barthélemy
    "BQ": {"currency": "USD", "symbol": "$"},  # Bonaire, Sint Eustatius and Saba
    "BV": {"currency": "NOK", "symbol": "kr"},  # Bouvet Island
    "CC": {"currency": "AUD", "symbol": "$"},  # Cocos (Keeling) Islands
    "CW": {"currency": "ANG", "symbol": "ƒ"},  # Curaçao
    "CX": {"currency": "AUD", "symbol": "$"},  # Christmas Island
    "EH": {"currency": "MAD", "symbol": "د.م."},  # Western Sahara
    "FK": {"currency": "FKP", "symbol": "£"},  # Falkland Islands
    "FO": {"currency": "DKK", "symbol": "kr"},  # Faroe Islands
    "GF": {"currency": "EUR", "symbol": "€"},  # French Guiana
    "GG": {"currency": "GBP", "symbol": "£"},  # Guernsey
    "GI": {"currency": "GIP", "symbol": "£"},  # Gibraltar
    "GL": {"currency": "DKK", "symbol": "kr"},  # Greenland
    "GP": {"currency": "EUR", "symbol": "€"},  # Guadeloupe
    "GS": {
        "currency": "GBP",
        "symbol": "£",
    },  # South Georgia and the South Sandwich Islands
    "GU": {"currency": "USD", "symbol": "$"},  # Guam
    "HK": {"currency": "HKD", "symbol": "HK$"},  # Hong Kong
    "HM": {"currency": "AUD", "symbol": "$"},  # Heard Island and McDonald Islands
    "IM": {"currency": "GBP", "symbol": "£"},  # Isle of Man
    "IO": {"currency": "USD", "symbol": "$"},  # British Indian Ocean Territory
    "JE": {"currency": "GBP", "symbol": "£"},  # Jersey
    "MF": {"currency": "EUR", "symbol": "€"},  # Saint Martin
    "MO": {"currency": "MOP", "symbol": "MOP$"},  # Macau
    "MP": {"currency": "USD", "symbol": "$"},  # Northern Mariana Islands
    "MQ": {"currency": "EUR", "symbol": "€"},  # Martinique
    "MS": {"currency": "XCD", "symbol": "$"},  # Montserrat
    "NC": {"currency": "XPF", "symbol": "₣"},  # New Caledonia
    "NF": {"currency": "AUD", "symbol": "$"},  # Norfolk Island
    "NU": {"currency": "NZD", "symbol": "$"},  # Niue
    "PF": {"currency": "XPF", "symbol": "₣"},  # French Polynesia
    "PM": {"currency": "EUR", "symbol": "€"},  # Saint Pierre and Miquelon
    "PN": {"currency": "NZD", "symbol": "$"},  # Pitcairn
    "RE": {"currency": "EUR", "symbol": "€"},  # Réunion
    "SH": {"currency": "SHP", "symbol": "£"},  # Saint Helena
    "SJ": {"currency": "NOK", "symbol": "kr"},  # Svalbard and Jan Mayen
    "SX": {"currency": "ANG", "symbol": "ƒ"},  # Sint Maarten
    "TC": {"currency": "USD", "symbol": "$"},  # Turks and Caicos Islands
    "TF": {"currency": "EUR", "symbol": "€"},  # French Southern Territories
    "UM": {"currency": "USD", "symbol": "$"},  # United States Minor Outlying Islands
    "VI": {"currency": "USD", "symbol": "$"},  # U.S. Virgin Islands
    "VG": {"currency": "USD", "symbol": "$"},  # British Virgin Islands
    "WF": {"currency": "XPF", "symbol": "₣"},  # Wallis and Futuna
    "YT": {"currency": "EUR", "symbol": "€"},  # Mayotte
}
