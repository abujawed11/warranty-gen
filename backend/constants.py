import os

from reportlab.lib import colors

C_YELLOW       = colors.HexColor("#F5C200")
C_BLACK        = colors.HexColor("#1A1A1A")
C_YELLOW_LIGHT = colors.HexColor("#FFF8D6")
C_BORDER       = colors.HexColor("#AAAAAA")
C_ORANGE       = colors.HexColor("#C8860A")

TERMS = [
    "M/s Sunrack Technologies, only provides the warranty against manufacturing "
    "defects and workmanship on the products supplied. Sunrack will, at its option, "
    "either repair the defect or replace the defective product or part there of with "
    "a new or remanufactured equivalent at cost within 15 working days of intimation.",

    "Sunrack's total liability here under for such repair of replacement shall not "
    "exceed the original purchase price of the product. This will not provide the warranty "
    "replacements for structure products going faulty while operating due to conditions "
    "beyond specifications, improper installation, improper site conditions and/or act of "
    "god, cosmetic damage, damage from accident, negligence same shall not be covered under "
    "warranty and the service would be provided on chargeable basis as per mutual agreement",

    "Any failure/damage arising out of improper unloading, stacking or moving to the site "
    "will not be covered under warranty.",

    "In the event of any non-payment issues, this warranty becomes null and void. Shall also "
    "be void if the product has been modified, repaired, or reworked in a manner not previously "
    "authorized by Sunrack in writing.",

    "Warranty shall not cover the consumable items & accessories supplied with viz. M8 Allen "
    "Bolt + Nut, tapered upper foot. Sunrack is not responsible for delay in delivering the "
    "warranty service/spares due to natural calamity or force majeure condition.",

    "The foregoing warranties are in addition of all other warranties, whether express or implied "
    "and Sunrack does not make any warranty of Merchant ability or any warranty for fitness for a "
    "particular purpose. In no event, Sunrack be liable for or responsible to purchaser or any "
    "other party for any consequential, incidental or other damages, losses or expenses arising in "
    "connection with the use of or the inability to use the product.",

    "All Claims related to this Warranty are subjected to Indian Law.",
]

BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.normpath(os.path.join(BASE_DIR, "..", "frontend", "public"))
