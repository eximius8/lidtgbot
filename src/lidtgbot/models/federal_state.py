from dataclasses import dataclass
from typing import Literal

# All 16 German federal states
FederalState = Literal[
    'baden_wuerttemberg',
    'bayern', 
    'berlin',
    'brandenburg',
    'bremen',
    'hamburg',
    'hessen',
    'mecklenburg_vorpommern',
    'niedersachsen',
    'nordrhein_westfalen',
    'rheinland_pfalz',
    'saarland',
    'sachsen',
    'sachsen_anhalt',
    'schleswig_holstein',
    'thueringen'
]

@dataclass
class FederalStateInfo:
    code: FederalState
    name_de: str
    name_en: str
    emoji: str

# Federal states data
FEDERAL_STATES = {
    'baden_wuerttemberg': FederalStateInfo('baden_wuerttemberg', 'Baden-Württemberg', 'Baden-Württemberg', '🏰'),
    'bayern': FederalStateInfo('bayern', 'Bayern', 'Bavaria', '🍺'),
    'berlin': FederalStateInfo('berlin', 'Berlin', 'Berlin', '🐻'),
    'brandenburg': FederalStateInfo('brandenburg', 'Brandenburg', 'Brandenburg', '🌲'),
    'bremen': FederalStateInfo('bremen', 'Bremen', 'Bremen', '⚓'),
    'hamburg': FederalStateInfo('hamburg', 'Hamburg', 'Hamburg', '🚢'),
    'hessen': FederalStateInfo('hessen', 'Hessen', 'Hesse', '🏛️'),
    'mecklenburg_vorpommern': FederalStateInfo('mecklenburg_vorpommern', 'Mecklenburg-Vorpommern', 'Mecklenburg-Vorpommern', '🏖️'),
    'niedersachsen': FederalStateInfo('niedersachsen', 'Niedersachsen', 'Lower Saxony', '🐎'),
    'nordrhein_westfalen': FederalStateInfo('nordrhein_westfalen', 'Nordrhein-Westfalen', 'North Rhine-Westphalia', '⚡'),
    'rheinland_pfalz': FederalStateInfo('rheinland_pfalz', 'Rheinland-Pfalz', 'Rhineland-Palatinate', '🍷'),
    'saarland': FederalStateInfo('saarland', 'Saarland', 'Saarland', '⚙️'),
    'sachsen': FederalStateInfo('sachsen', 'Sachsen', 'Saxony', '🎭'),
    'sachsen_anhalt': FederalStateInfo('sachsen_anhalt', 'Sachsen-Anhalt', 'Saxony-Anhalt', '🏰'),
    'schleswig_holstein': FederalStateInfo('schleswig_holstein', 'Schleswig-Holstein', 'Schleswig-Holstein', '🌊'),
    'thueringen': FederalStateInfo('thueringen', 'Thüringen', 'Thuringia', '🌿')
}