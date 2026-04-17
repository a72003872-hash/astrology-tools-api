"""
Astrology Tools API — All 14 Tools in One Server
=================================================
Free, open-source. Powered by Kerykeion + Swiss Ephemeris.
Deploy on Render.com free tier (1 service = 750 hrs = enough!)

Tools:
  1.  Birth Chart Calculator
  2.  Synastry Chart Calculator
  3.  Love Compatibility Calculator
  4.  Sun Sign Calculator
  5.  Moon Sign Calculator
  6.  Rising Sign Calculator
  7.  Sun, Moon, Rising Calculator
  8.  Venus Sign Calculator
  9.  Chiron Sign Calculator
  10. Lilith Sign Calculator
  11. North Node Calculator
  12. Part of Fortune Calculator
  13. Vertex Calculator
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from kerykeion import (
    AstrologicalSubjectFactory,
    NatalAspects,
    SynastryAspects,
    ChartDataFactory,
    ChartDrawer,
)
# RelationshipScoreFactory — import safely (may not exist in older Kerykeion)
try:
    from kerykeion import RelationshipScoreFactory
    HAS_RELATIONSHIP_SCORE = True
except ImportError:
    try:
        from kerykeion.relationship_score_factory import RelationshipScoreFactory
        HAS_RELATIONSHIP_SCORE = True
    except ImportError:
        HAS_RELATIONSHIP_SCORE = False
        RelationshipScoreFactory = None
import swisseph as swe
import math
from interpretations import (
    SUN_INTERPRETATIONS, MOON_INTERPRETATIONS, RISING_INTERPRETATIONS,
    VENUS_INTERPRETATIONS, MARS_INTERPRETATIONS, MERCURY_INTERPRETATIONS,
    CHIRON_INTERPRETATIONS, LILITH_INTERPRETATIONS, NORTH_NODE_INTERPRETATIONS,
    PART_OF_FORTUNE_INTERPRETATIONS, VERTEX_INTERPRETATIONS,
    JUPITER_INTERPRETATIONS, SATURN_INTERPRETATIONS,
)
from synastry_interpretations import (
    categorize_all_aspects,
    calculate_house_overlays,
)

app = Flask(__name__)

# ─── CORS ─────────────────────────────────────────────────────
CORS(app, origins=[
    "http://localhost",
    "http://localhost:8000",
    "https://your-wordpress-site.com",  # <-- Apna domain daalein
    "*"  # Dev ke liye, production mein hatayein
])

# ─── CONSTANTS ────────────────────────────────────────────────
SIGN_FULL = {
    "Ari": "Aries",     "Tau": "Taurus",    "Gem": "Gemini",
    "Can": "Cancer",     "Leo": "Leo",       "Vir": "Virgo",
    "Lib": "Libra",      "Sco": "Scorpio",   "Sag": "Sagittarius",
    "Cap": "Capricorn",  "Aqu": "Aquarius",  "Pis": "Pisces",
}
SIGNS_LIST = [
    "Aries","Taurus","Gemini","Cancer","Leo","Virgo",
    "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"
]
SIGN_ELEMENT = {
    "Aries":"Fire","Taurus":"Earth","Gemini":"Air","Cancer":"Water",
    "Leo":"Fire","Virgo":"Earth","Libra":"Air","Scorpio":"Water",
    "Sagittarius":"Fire","Capricorn":"Earth","Aquarius":"Air","Pisces":"Water",
}
SIGN_QUALITY = {
    "Aries":"Cardinal","Taurus":"Fixed","Gemini":"Mutable","Cancer":"Cardinal",
    "Leo":"Fixed","Virgo":"Mutable","Libra":"Cardinal","Scorpio":"Fixed",
    "Sagittarius":"Mutable","Capricorn":"Cardinal","Aquarius":"Fixed","Pisces":"Mutable",
}
SIGN_RULER = {
    "Aries":"Mars","Taurus":"Venus","Gemini":"Mercury","Cancer":"Moon",
    "Leo":"Sun","Virgo":"Mercury","Libra":"Venus","Scorpio":"Pluto",
    "Sagittarius":"Jupiter","Capricorn":"Saturn","Aquarius":"Uranus","Pisces":"Neptune",
}
HOUSE_NUM = {
    "First_House":1,"Second_House":2,"Third_House":3,"Fourth_House":4,
    "Fifth_House":5,"Sixth_House":6,"Seventh_House":7,"Eighth_House":8,
    "Ninth_House":9,"Tenth_House":10,"Eleventh_House":11,"Twelfth_House":12,
}

# ─── Compatibility scores (simplified element-based) ─────────
ELEMENT_COMPAT = {
    ("Fire","Fire"):80,("Fire","Air"):78,("Fire","Earth"):45,("Fire","Water"):38,
    ("Air","Air"):78,("Air","Earth"):42,("Air","Water"):50,
    ("Earth","Earth"):78,("Earth","Water"):75,
    ("Water","Water"):80,
}


# ═══════════════════════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════════════════════

def validate(data):
    required = ["year","month","day","hour","minute","latitude","longitude","timezone"]
    missing = [f for f in required if f not in data]
    if missing:
        return False, f"Missing: {', '.join(missing)}"
    try:
        y=int(data["year"]); m=int(data["month"]); d=int(data["day"])
        h=int(data["hour"]); mi=int(data["minute"])
        lat=float(data["latitude"]); lng=float(data["longitude"])
        if not(1900<=y<=2100): return False,"Year: 1900-2100"
        if not(1<=m<=12): return False,"Month: 1-12"
        if not(1<=d<=31): return False,"Day: 1-31"
        if not(0<=h<=23): return False,"Hour: 0-23"
        if not(0<=mi<=59): return False,"Minute: 0-59"
        if not(-90<=lat<=90): return False,"Latitude: -90 to 90"
        if not(-180<=lng<=180): return False,"Longitude: -180 to 180"
    except (ValueError,TypeError):
        return False,"Invalid data types"
    return True, None


def make_subject(data, name_key="name", default_name="User"):
    return AstrologicalSubjectFactory.from_birth_data(
        name=data.get(name_key, default_name),
        year=int(data["year"]), month=int(data["month"]), day=int(data["day"]),
        hour=int(data["hour"]), minute=int(data["minute"]),
        lng=float(data["longitude"]), lat=float(data["latitude"]),
        tz_str=str(data["timezone"]), online=False,
    )


def fmt_planet(p):
    sign = SIGN_FULL.get(p.sign, p.sign)
    house = HOUSE_NUM.get(p.house, 0) if p.house else 0
    return {
        "name": p.name, "sign": sign, "sign_short": p.sign,
        "degree": round(p.position, 2), "abs_degree": round(p.abs_pos, 2),
        "house": house, "retrograde": p.retrograde or False,
        "element": SIGN_ELEMENT.get(sign,""), "quality": SIGN_QUALITY.get(sign,""),
        "ruler": SIGN_RULER.get(sign,""),
    }


def fmt_house(h, num):
    sign = SIGN_FULL.get(h.sign, h.sign)
    return {"number":num, "sign":sign, "sign_short":h.sign, "degree":round(h.position,2)}


def fmt_aspect(a):
    return {
        "planet1":a.p1_name, "planet2":a.p2_name,
        "aspect":a.aspect.capitalize(), "aspect_degrees":a.aspect_degrees,
        "orb":round(a.orbit,2), "movement":a.aspect_movement,
    }


def sign_from_abs(abs_pos):
    """Convert absolute position to sign name and degree."""
    idx = int(abs_pos / 30) % 12
    return SIGNS_LIST[idx], round(abs_pos % 30, 2)


def get_all_planets(subject):
    names = ["sun","moon","mercury","venus","mars","jupiter","saturn","uranus","neptune","pluto"]
    return {n: fmt_planet(getattr(subject, n)) for n in names}


def get_all_houses(subject):
    attrs = ["first_house","second_house","third_house","fourth_house",
             "fifth_house","sixth_house","seventh_house","eighth_house",
             "ninth_house","tenth_house","eleventh_house","twelfth_house"]
    return [fmt_house(getattr(subject, a), i+1) for i, a in enumerate(attrs)]


def get_element_dist(planets):
    elements = {"Fire":0,"Earth":0,"Air":0,"Water":0}
    for p in planets.values():
        if p["element"] in elements: elements[p["element"]] += 1
    return elements


def get_quality_dist(planets):
    qualities = {"Cardinal":0,"Fixed":0,"Mutable":0}
    for p in planets.values():
        if p["quality"] in qualities: qualities[p["quality"]] += 1
    return qualities


def calc_part_of_fortune(subject):
    """Part of Fortune = ASC + Moon - Sun (day) or ASC + Sun - Moon (night)."""
    asc = subject.first_house.abs_pos
    moon = subject.moon.abs_pos
    sun = subject.sun.abs_pos
    sun_h = HOUSE_NUM.get(subject.sun.house, 1)
    is_day = 7 <= sun_h <= 12
    if is_day:
        pof = (asc + moon - sun) % 360
    else:
        pof = (asc + sun - moon) % 360
    sign, degree = sign_from_abs(pof)
    return {
        "sign": sign, "degree": degree, "abs_degree": round(pof, 2),
        "chart_type": "Day" if is_day else "Night",
        "element": SIGN_ELEMENT.get(sign,""), "quality": SIGN_QUALITY.get(sign,""),
        "ruler": SIGN_RULER.get(sign,""),
    }


def calc_vertex(data):
    """Vertex from Swiss Ephemeris house calculation."""
    swe.set_ephe_path('')
    tz_offset = get_tz_offset(data["timezone"], data["year"], data["month"], data["day"],
                              data["hour"], data["minute"])
    ut_hour = int(data["hour"]) + int(data["minute"])/60.0 - tz_offset
    jd = swe.julday(int(data["year"]), int(data["month"]), int(data["day"]), ut_hour)
    cusps, ascmc = swe.houses(jd, float(data["latitude"]), float(data["longitude"]), b'P')
    vertex_abs = ascmc[3]
    sign, degree = sign_from_abs(vertex_abs)
    return {
        "sign": sign, "degree": degree, "abs_degree": round(vertex_abs, 2),
        "element": SIGN_ELEMENT.get(sign,""), "quality": SIGN_QUALITY.get(sign,""),
        "ruler": SIGN_RULER.get(sign,""),
    }


def get_tz_offset(tz_str, year, month, day, hour, minute):
    """Get UTC offset for a timezone string."""
    try:
        import pytz
        from datetime import datetime
        tz = pytz.timezone(tz_str)
        dt = datetime(int(year), int(month), int(day), int(hour), int(minute))
        offset = tz.utcoffset(dt)
        if offset is None:
            offset = tz.localize(dt).utcoffset()
        return offset.total_seconds() / 3600.0
    except:
        # Fallback: common offsets
        common = {
            "Asia/Karachi":5,"Asia/Kolkata":5.5,"Asia/Dubai":4,
            "Europe/London":0,"America/New_York":-5,"America/Los_Angeles":-8,
            "Asia/Tokyo":9,"Australia/Sydney":10,"Europe/Paris":1,
        }
        return common.get(tz_str, 0)


def get_compat_score(elem1, elem2):
    """Element-based compatibility score."""
    pair = tuple(sorted([elem1, elem2]))
    return ELEMENT_COMPAT.get(pair, ELEMENT_COMPAT.get((pair[1],pair[0]), 50))


# ═══════════════════════════════════════════════════════════════
# CHART PATTERNS DETECTION (for Birth Chart upgrade)
# ═══════════════════════════════════════════════════════════════

def detect_chart_patterns(aspects, planets):
    """
    Detect major chart patterns:
    - Stellium (3+ planets in same sign OR same house)
    - Grand Trine (3 planets in trine to each other, all same element)
    - T-Square (2 planets in opposition, 3rd square to both)
    - Grand Cross (4 planets forming 2 oppositions + 4 squares)
    - Yod (2 planets in sextile, both quincunx to 3rd)
    - Kite (Grand Trine + 1 planet opposite one corner)
    """
    patterns = []
    planet_names = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"]

    # ── STELLIUM: 3+ planets in same sign ──
    sign_groups = {}
    house_groups = {}
    for name, p in planets.items():
        sign = p.get("sign")
        house = p.get("house")
        if sign:
            sign_groups.setdefault(sign, []).append(p.get("name", name.title()))
        if house:
            house_groups.setdefault(house, []).append(p.get("name", name.title()))

    for sign, plist in sign_groups.items():
        if len(plist) >= 3:
            patterns.append({
                "name": "Stellium",
                "type": "stellium_sign",
                "planets": plist,
                "location": sign,
                "description": f"A powerful concentration of {len(plist)} planets ({', '.join(plist)}) in {sign}. This creates an intense focus of {sign} energy in your personality — themes of this sign dominate your life path."
            })

    for house, plist in house_groups.items():
        if len(plist) >= 3 and house > 0:
            patterns.append({
                "name": "House Stellium",
                "type": "stellium_house",
                "planets": plist,
                "location": f"House {house}",
                "description": f"A concentration of {len(plist)} planets ({', '.join(plist)}) in House {house}. The life area governed by this house becomes a central arena of your experience and growth."
            })

    # ── Build aspect lookup for pattern detection ──
    aspect_map = {}  # (p1, p2) -> aspect_type
    for a in aspects:
        p1, p2 = a["planet1"], a["planet2"]
        asp = a["aspect"].lower()
        key = tuple(sorted([p1, p2]))
        aspect_map[key] = asp

    def has_aspect(p1, p2, asp_type):
        key = tuple(sorted([p1, p2]))
        return aspect_map.get(key) == asp_type

    # ── GRAND TRINE: 3 planets, all trine to each other ──
    checked_trines = set()
    for i, p1 in enumerate(planet_names):
        for j, p2 in enumerate(planet_names[i+1:], i+1):
            for k, p3 in enumerate(planet_names[j+1:], j+1):
                trio = tuple(sorted([p1, p2, p3]))
                if trio in checked_trines: continue
                checked_trines.add(trio)
                if (has_aspect(p1, p2, "trine") and
                    has_aspect(p2, p3, "trine") and
                    has_aspect(p1, p3, "trine")):
                    # Check element
                    e1 = planets.get(p1.lower(), {}).get("element")
                    e2 = planets.get(p2.lower(), {}).get("element")
                    e3 = planets.get(p3.lower(), {}).get("element")
                    element = e1 if (e1 == e2 == e3) else "Mixed"
                    patterns.append({
                        "name": "Grand Trine",
                        "type": "grand_trine",
                        "planets": [p1, p2, p3],
                        "location": f"{element} Element" if element != "Mixed" else "Mixed Elements",
                        "description": f"A rare harmonious pattern — {p1}, {p2}, and {p3} form a perfect triangle of trines. This creates natural talent and effortless flow in {element.lower() if element != 'Mixed' else 'these'} areas. The gift can feel so natural that you may take it for granted."
                    })

    # ── T-SQUARE: 2 planets opposite, 3rd squares both ──
    checked_tsquares = set()
    for i, p1 in enumerate(planet_names):
        for j, p2 in enumerate(planet_names[i+1:], i+1):
            if has_aspect(p1, p2, "opposition"):
                for k, p3 in enumerate(planet_names):
                    if p3 in [p1, p2]: continue
                    if has_aspect(p1, p3, "square") and has_aspect(p2, p3, "square"):
                        trio = tuple(sorted([p1, p2, p3]))
                        if trio in checked_tsquares: continue
                        checked_tsquares.add(trio)
                        patterns.append({
                            "name": "T-Square",
                            "type": "t_square",
                            "planets": [p1, p2, p3],
                            "focal_planet": p3,
                            "location": f"Focal point: {p3}",
                            "description": f"A dynamic tension pattern — {p1} opposes {p2}, and {p3} squares both. {p3} becomes the focal point where the tension must be resolved. T-Squares drive achievement through challenge; people with this pattern often become exceptional in the area ruled by {p3}."
                        })

    # ── YOD (Finger of God): 2 sextile, both quincunx to 3rd ──
    checked_yods = set()
    for i, p1 in enumerate(planet_names):
        for j, p2 in enumerate(planet_names[i+1:], i+1):
            if has_aspect(p1, p2, "sextile"):
                for k, p3 in enumerate(planet_names):
                    if p3 in [p1, p2]: continue
                    if has_aspect(p1, p3, "quincunx") and has_aspect(p2, p3, "quincunx"):
                        trio = tuple(sorted([p1, p2, p3]))
                        if trio in checked_yods: continue
                        checked_yods.add(trio)
                        patterns.append({
                            "name": "Yod (Finger of Fate)",
                            "type": "yod",
                            "planets": [p1, p2, p3],
                            "focal_planet": p3,
                            "location": f"Apex: {p3}",
                            "description": f"A rare karmic pattern also called the 'Finger of God'. {p1} and {p2} work in harmony (sextile) while both point awkwardly at {p3}. This creates a sense of destiny around {p3} — a specific mission that feels unusual, sometimes uncomfortable, but deeply meaningful."
                        })

    return patterns


def get_dominant_element(elements):
    """Returns the strongest element and its percentage."""
    if not elements: return {"element": "Balanced", "percentage": 0}
    total = sum(elements.values()) or 1
    dominant = max(elements, key=elements.get)
    return {
        "element": dominant,
        "count": elements[dominant],
        "percentage": round((elements[dominant] / total) * 100, 1)
    }


def get_dominant_modality(qualities):
    """Returns the strongest modality (Cardinal/Fixed/Mutable)."""
    if not qualities: return {"modality": "Balanced", "percentage": 0}
    total = sum(qualities.values()) or 1
    dominant = max(qualities, key=qualities.get)
    return {
        "modality": dominant,
        "count": qualities[dominant],
        "percentage": round((dominant and (qualities[dominant] / total) * 100) or 0, 1)
    }


def count_hemisphere_distribution(planets):
    """
    Count planets in each hemisphere:
    - North/South: Houses 7-12 (above horizon) vs 1-6 (below)
    - East/West: Houses 10-3 (east) vs 4-9 (west)
    """
    north, south, east, west = 0, 0, 0, 0
    for p in planets.values():
        h = p.get("house", 0)
        if 7 <= h <= 12: north += 1
        elif 1 <= h <= 6: south += 1
        if h in [10, 11, 12, 1, 2, 3]: east += 1
        elif h in [4, 5, 6, 7, 8, 9]: west += 1
    return {"north": north, "south": south, "east": east, "west": west}


def get_chart_shape(planets):
    """
    Detect chart shape based on planet distribution:
    - Bundle: all planets within 120°
    - Bowl: all planets within 180°
    - Bucket: bowl + 1 planet opposite (handle)
    - Locomotive: all planets within 240° (gap of 120°+)
    - Splash: planets spread relatively evenly
    - Seesaw: two groups opposite each other
    - Splay: uneven distribution with multiple clusters
    """
    positions = sorted([p["abs_degree"] for p in planets.values() if "abs_degree" in p])
    if len(positions) < 8:
        return {"shape": "Unknown", "description": "Not enough data to determine chart shape."}

    # Find the largest gap
    gaps = []
    for i in range(len(positions)):
        next_pos = positions[(i+1) % len(positions)]
        gap = (next_pos - positions[i]) % 360
        if gap < 0: gap += 360
        gaps.append(gap)

    max_gap = max(gaps)
    span = 360 - max_gap

    if span <= 120:
        return {"shape": "Bundle", "description": "All planets are concentrated within 120°, creating intense focus on a narrow range of life themes. You pursue a specific direction with unusual concentration."}
    elif span <= 180:
        # Check for bucket (bowl + handle)
        second_gap = sorted(gaps, reverse=True)[1] if len(gaps) > 1 else 0
        if second_gap > 60:
            return {"shape": "Bucket", "description": "Most planets form a bowl with one or two isolated planets acting as a 'handle'. The handle planet becomes the focal point through which you channel the energy of the rest of the chart."}
        return {"shape": "Bowl", "description": "Planets occupy only one half of the chart. You carry a sense of specialization or self-contained purpose, sometimes feeling you must complete what the empty half represents."}
    elif span <= 240:
        return {"shape": "Locomotive", "description": "Planets span about two-thirds of the chart with a clear empty section. The planet leading the pack (in zodiacal order) becomes an engine of drive and ambition."}
    elif max_gap < 60:
        return {"shape": "Splash", "description": "Planets are spread relatively evenly around the chart. You have diverse interests, multifaceted abilities, and find meaning across many life areas."}
    else:
        return {"shape": "Splay", "description": "Planets cluster in two or three distinct groups with clear gaps. You have pronounced areas of focus with notable blind spots — your strengths are concentrated rather than spread thin."}


# ═══════════════════════════════════════════════════════════════
# RELATIONSHIP SCORE (for Synastry upgrade)
# ═══════════════════════════════════════════════════════════════

def calculate_relationship_score(s1, s2, aspects_raw):
    """
    Calculate relationship compatibility score (0-100).

    Primary: Uses Kerykeion's RelationshipScoreFactory (Ciro Discepolo method)
    Fallback: Calculates our own score from aspects if library version doesn't support it

    Returns dict with:
        - score: int (0-100)
        - rating: str (e.g., "Excellent", "Strong", "Moderate", "Challenging", "Difficult")
        - description: str (summary paragraph)
        - breakdown: list of contributing factors (if available)
    """
    # ─── Attempt 1: Use Kerykeion's RelationshipScoreFactory ───
    if HAS_RELATIONSHIP_SCORE and RelationshipScoreFactory is not None:
        try:
            score_factory = RelationshipScoreFactory(s1, s2)

            # API varies across versions — try multiple method names
            result = None
            for method_name in ("get_relationship_score", "get_score"):
                if hasattr(score_factory, method_name):
                    result = getattr(score_factory, method_name)()
                    break

            if result is not None:
                # Extract score value (field name varies by version)
                score_val = None
                for attr in ("score_value", "score"):
                    if hasattr(result, attr):
                        score_val = getattr(result, attr)
                        break

                # Extract description
                desc = None
                for attr in ("score_description", "description"):
                    if hasattr(result, attr):
                        desc = getattr(result, attr)
                        break

                # Extract breakdown (newer versions)
                breakdown_items = []
                if hasattr(result, "score_breakdown") and result.score_breakdown:
                    for item in result.score_breakdown:
                        breakdown_items.append({
                            "rule": getattr(item, "rule", "") or "",
                            "description": getattr(item, "description", "") or "",
                            "points": getattr(item, "points", 0) or 0,
                        })

                if score_val is not None:
                    # Ciro Discepolo method outputs 0-40+ — normalize to 0-100
                    # Typical scale: 0-5 = weak, 5-10 = mediocre, 10-15 = important,
                    #                15-20 = very important, 20+ = exceptional
                    raw = float(score_val)
                    normalized = min(100, max(0, int((raw / 30.0) * 100)))

                    return {
                        "score": normalized,
                        "raw_score": round(raw, 1),
                        "rating": _get_rating(normalized),
                        "description": desc or _get_score_description(normalized),
                        "breakdown": breakdown_items,
                        "method": "Ciro Discepolo (Kerykeion)",
                    }
        except Exception:
            pass  # Fall through to manual calculation

    # ─── Attempt 2: Manual calculation from aspects ───
    return _calculate_manual_score(s1, s2, aspects_raw)


def _calculate_manual_score(s1, s2, aspects_raw):
    """
    Manual relationship score calculation based on key synastry factors.
    Used when Kerykeion's RelationshipScoreFactory is unavailable.

    Scoring logic (0-100 scale):
    - Base score: 50
    - Sun-Moon aspects: ±8 pts each
    - Venus-Mars aspects: ±6 pts each
    - Ascendant contacts: ±5 pts each
    - Other harmonious aspects: +1 pt each
    - Other challenging aspects: -1 pt each
    - Element compatibility bonus: up to +10
    """
    score = 50  # Base score
    breakdown = []

    # Key pairs worth more weight
    KEY_HARMONIOUS_PAIRS = [
        ("Sun", "Moon"), ("Moon", "Sun"),
        ("Venus", "Mars"), ("Mars", "Venus"),
        ("Sun", "Venus"), ("Venus", "Sun"),
        ("Moon", "Venus"), ("Venus", "Moon"),
    ]

    for a in aspects_raw:
        p1_name = getattr(a, "p1_name", "")
        p2_name = getattr(a, "p2_name", "")
        asp = (getattr(a, "aspect", "") or "").lower()
        pair = (p1_name, p2_name)

        is_key_pair = pair in KEY_HARMONIOUS_PAIRS
        is_harmonious = asp in ("trine", "sextile", "conjunction")
        is_challenging = asp in ("square", "opposition")

        if is_key_pair:
            if is_harmonious:
                pts = 8 if asp in ("trine", "conjunction") else 5
                score += pts
                breakdown.append({
                    "rule": f"key_{asp}",
                    "description": f"{p1_name} {asp} {p2_name} (key pair)",
                    "points": pts,
                })
            elif is_challenging:
                pts = -3  # Key pair challenging still generates chemistry
                score += pts
                breakdown.append({
                    "rule": f"key_{asp}",
                    "description": f"{p1_name} {asp} {p2_name} (key pair, growth tension)",
                    "points": pts,
                })
        else:
            # Regular aspects
            if is_harmonious:
                score += 1
            elif is_challenging:
                score -= 1

    # Element compatibility bonus (Sun-Sun element match)
    try:
        s1_sun_elem = SIGN_ELEMENT.get(SIGN_FULL.get(s1.sun.sign, ""), "")
        s2_sun_elem = SIGN_ELEMENT.get(SIGN_FULL.get(s2.sun.sign, ""), "")
        if s1_sun_elem and s2_sun_elem:
            compat = get_compat_score(s1_sun_elem, s2_sun_elem)
            bonus = int((compat - 50) / 5)  # -10 to +10
            score += bonus
            if bonus != 0:
                breakdown.append({
                    "rule": "element_compatibility",
                    "description": f"{s1_sun_elem} Sun × {s2_sun_elem} Sun element compatibility",
                    "points": bonus,
                })
    except Exception:
        pass

    # Clamp to 0-100
    score = min(99, max(10, score))

    return {
        "score": score,
        "raw_score": score,
        "rating": _get_rating(score),
        "description": _get_score_description(score),
        "breakdown": breakdown,
        "method": "Synastry Aspects (AstroCalcPro method)",
    }


def _get_rating(score):
    """Get text rating from numeric score."""
    if score >= 85: return "Exceptional"
    if score >= 70: return "Strong"
    if score >= 55: return "Good"
    if score >= 40: return "Moderate"
    if score >= 25: return "Challenging"
    return "Difficult"


def _get_score_description(score):
    """Get descriptive paragraph based on score range."""
    if score >= 85:
        return "An exceptional astrological match. The planetary connections between these two charts flow with remarkable ease across multiple dimensions — emotional, romantic, intellectual, and physical. Relationships with this level of synastry often feel destined and produce deep, lasting bonds. Watch for complacency: such natural compatibility can sometimes reduce growth motivation."
    elif score >= 70:
        return "A strong compatibility profile with natural chemistry and meaningful connection points. You share significant harmony in core areas of the chart, with enough contrast to keep the dynamic alive and growing. This is the classic foundation for committed, evolving partnerships that stand the test of time."
    elif score >= 55:
        return "A well-balanced relationship profile. The synastry shows genuine connection points alongside productive differences. Many of the most enduring partnerships fall into this range — the harmony keeps you connected, and the tension keeps you both growing. Communication and mutual respect amplify this potential."
    elif score >= 40:
        return "A moderately compatible profile with real strengths and meaningful challenges. This relationship will require more conscious effort than high-score matches, but that investment often produces deeper growth. The connection may feel less effortless, but the rewards come from working through differences together."
    elif score >= 25:
        return "A challenging synastry with significant planetary tensions alongside pockets of attraction. These relationships often generate strong chemistry and intense emotional dynamics but require exceptional emotional maturity, self-awareness, and direct communication to flourish. Not impossible — but demanding."
    else:
        return "A difficult astrological profile with substantial planetary contrast. This does not mean the relationship cannot work, but both partners will need to actively bridge fundamental differences in emotional style, communication, and desire. The attraction may be magnetic, and the lessons profound, but the work is real and ongoing."




@app.route("/api/birth-chart", methods=["POST"])
def birth_chart():
    """
    Full birth chart with ALL features:
    - Planets, houses, aspects, elements, qualities
    - Chart patterns (Stellium, Grand Trine, T-Square, Yod)
    - Chart shape (Bundle, Bowl, Bucket, etc.)
    - Hemisphere distribution (North/South, East/West)
    - Dominant element & modality
    - Full interpretations for all placements
    - SVG chart wheel (included directly for performance)
    """
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        planets = get_all_planets(s)
        houses = get_all_houses(s)
        aspects = [fmt_aspect(a) for a in NatalAspects(s).all_aspects]

        # Get elements and qualities
        elements = get_element_dist(planets)
        qualities = get_quality_dist(planets)

        # Build comprehensive interpretations
        interps = {
            "sun": SUN_INTERPRETATIONS.get(planets["sun"]["sign"], {}),
            "moon": MOON_INTERPRETATIONS.get(planets["moon"]["sign"], {}),
            "rising": RISING_INTERPRETATIONS.get(houses[0]["sign"], {}),
            "mercury": MERCURY_INTERPRETATIONS.get(planets["mercury"]["sign"], {}),
            "venus": VENUS_INTERPRETATIONS.get(planets["venus"]["sign"], {}),
            "mars": MARS_INTERPRETATIONS.get(planets["mars"]["sign"], {}),
            "jupiter": JUPITER_INTERPRETATIONS.get(planets["jupiter"]["sign"], {}),
            "saturn": SATURN_INTERPRETATIONS.get(planets["saturn"]["sign"], {}),
        }

        # Detect chart patterns
        patterns = detect_chart_patterns(aspects, planets)

        # Additional analysis
        chart_shape = get_chart_shape(planets)
        hemispheres = count_hemisphere_distribution(planets)
        dominant_element = get_dominant_element(elements)
        dominant_modality = get_dominant_modality(qualities)

        # Aspect summary
        harmonious_count = sum(1 for a in aspects if a["aspect"].lower() in ["conjunction", "trine", "sextile"])
        challenging_count = sum(1 for a in aspects if a["aspect"].lower() in ["square", "opposition"])
        exact_count = sum(1 for a in aspects if a["orb"] <= 1)

        # Generate SVG chart wheel (single API call instead of two)
        # Using wheel-only mode (no birth data text inside wheel)
        svg_chart = None
        try:
            chart_data = ChartDataFactory.create_natal_chart_data(s)
            drawer = ChartDrawer(chart_data=chart_data)
            # Try wheel-only first (cleaner look), fallback to full chart
            if hasattr(drawer, 'generate_wheel_only_svg_string'):
                svg_chart = drawer.generate_wheel_only_svg_string()
            else:
                svg_chart = drawer.generate_svg_string()
        except Exception:
            svg_chart = None  # Don't fail the whole request if SVG fails

        return jsonify({
            "success": True, "tool": "birth_chart",
            "name": data.get("name","User"),
            "birth_data": {
                "date": f"{int(data['day']):02d}/{int(data['month']):02d}/{int(data['year'])}",
                "time": f"{int(data['hour']):02d}:{int(data['minute']):02d}",
                "latitude": round(float(data['latitude']), 4),
                "longitude": round(float(data['longitude']), 4),
                "timezone": data.get('timezone', 'UTC'),
                "city": data.get('city', ''),
            },
            "summary": {
                "sun_sign": planets["sun"]["sign"],
                "moon_sign": planets["moon"]["sign"],
                "rising_sign": houses[0]["sign"],
                "sun_house": planets["sun"]["house"],
                "moon_house": planets["moon"]["house"],
            },
            "planets": planets,
            "houses": houses,
            "aspects": aspects,
            "aspects_summary": {
                "total": len(aspects),
                "harmonious": harmonious_count,
                "challenging": challenging_count,
                "exact": exact_count,
            },
            "elements": elements,
            "qualities": qualities,
            "dominant_element": dominant_element,
            "dominant_modality": dominant_modality,
            "chart_shape": chart_shape,
            "hemispheres": hemispheres,
            "patterns": patterns,
            "interpretations": interps,
            "svg": svg_chart,
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


@app.route("/api/birth-chart/svg", methods=["POST"])
def birth_chart_svg():
    """Generate birth chart SVG image only (kept for backward compatibility)."""
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        chart_data = ChartDataFactory.create_natal_chart_data(s)
        svg = ChartDrawer(chart_data=chart_data).generate_svg_string()
        return jsonify({"success":True, "svg":svg})
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# TOOL 2: SYNASTRY CHART CALCULATOR
# ═══════════════════════════════════════════════════════════════

@app.route("/api/synastry-chart", methods=["POST"])
def synastry_chart():
    """
    Synastry chart — compare two people's charts.
    Includes: categorized aspects, house overlays, bi-wheel SVG.
    Requires person1 and person2 objects in JSON.
    """
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400

    for person in ["person1","person2"]:
        if person not in data:
            return jsonify({"error":f"Missing {person} data"}), 400
        valid, err = validate(data[person])
        if not valid: return jsonify({"error":f"{person}: {err}"}), 400

    try:
        s1 = make_subject(data["person1"], default_name="Person 1")
        s2 = make_subject(data["person2"], default_name="Person 2")

        p1_planets = get_all_planets(s1)
        p2_planets = get_all_planets(s2)
        p1_houses = get_all_houses(s1)
        p2_houses = get_all_houses(s2)

        raw_aspects = SynastryAspects(s1, s2).all_aspects
        aspects = [fmt_aspect(a) for a in raw_aspects]

        # Count aspect types for summary
        harmonious = sum(1 for a in raw_aspects if a.aspect in ["conjunction","trine","sextile"])
        challenging = sum(1 for a in raw_aspects if a.aspect in ["square","opposition"])

        if harmonious > challenging * 1.5:
            synastry_summary = "This synastry chart shows predominantly harmonious energy between the two charts. The relationship likely feels natural and supportive, with strong areas of mutual understanding. Watch for complacency — ease can sometimes reduce growth motivation."
        elif challenging > harmonious * 1.5:
            synastry_summary = "This synastry chart shows significant dynamic tension between the two charts. The relationship likely generates intense attraction alongside frequent friction. This combination often produces the most passionate and growth-oriented partnerships when both people communicate well."
        else:
            synastry_summary = "This synastry chart shows a balanced mix of harmonious and challenging aspects. The relationship offers both comfort and stimulation — enough ease to feel connected and enough tension to keep both partners evolving. This is often the hallmark of enduring partnerships."

        # ── Phase 1: Categorize aspects ──
        aspect_categories = categorize_all_aspects(aspects)

        # ── Phase 2: House overlays ──
        p1_in_p2_houses = calculate_house_overlays(p1_planets, p2_houses)
        p2_in_p1_houses = calculate_house_overlays(p2_planets, p1_houses)

        # ── Phase 3: SVG bi-wheel ──
        chart_data = ChartDataFactory.create_synastry_chart_data(s1, s2)
        svg = ChartDrawer(chart_data=chart_data).generate_svg_string()

        # ── Phase 4: Relationship Score (NEW) ──
        relationship_score = calculate_relationship_score(s1, s2, raw_aspects)

        return jsonify({
            "success": True, "tool": "synastry_chart",
            "person1": {
                "name": data["person1"].get("name","Person 1"),
                "planets": p1_planets,
                "houses": p1_houses,
            },
            "person2": {
                "name": data["person2"].get("name","Person 2"),
                "planets": p2_planets,
                "houses": p2_houses,
            },
            "aspects": aspects,
            "aspects_summary": {
                "total": len(aspects),
                "harmonious": harmonious,
                "challenging": challenging,
            },
            "aspect_categories": aspect_categories,
            "house_overlays": {
                "person1_in_person2": p1_in_p2_houses,
                "person2_in_person1": p2_in_p1_houses,
            },
            "synastry_summary": synastry_summary,
            "relationship_score": relationship_score,
            "svg": svg,
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# TOOL 3: LOVE COMPATIBILITY CALCULATOR
# ═══════════════════════════════════════════════════════════════

@app.route("/api/love-compatibility", methods=["POST"])
def love_compatibility():
    """
    Love compatibility — element-based + aspect scoring.
    Requires person1 and person2.
    """
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400

    for person in ["person1","person2"]:
        if person not in data:
            return jsonify({"error":f"Missing {person} data"}), 400
        valid, err = validate(data[person])
        if not valid: return jsonify({"error":f"{person}: {err}"}), 400

    try:
        s1 = make_subject(data["person1"], default_name="Person 1")
        s2 = make_subject(data["person2"], default_name="Person 2")

        p1 = get_all_planets(s1)
        p2 = get_all_planets(s2)

        # Sun compatibility
        sun_score = get_compat_score(p1["sun"]["element"], p2["sun"]["element"])
        # Moon compatibility (emotional)
        moon_score = get_compat_score(p1["moon"]["element"], p2["moon"]["element"])
        # Venus compatibility (love style)
        venus_score = get_compat_score(p1["venus"]["element"], p2["venus"]["element"])
        # Mars compatibility (passion)
        mars_score = get_compat_score(p1["mars"]["element"], p2["mars"]["element"])

        # Aspect-based scoring — BALANCED (v2.7.0)
        # Only count tight orbs (< 6°) for personal planets.
        # Cap bonuses and penalties to prevent score inflation.
        aspects = SynastryAspects(s1, s2).all_aspects
        aspect_bonus = 0
        harmonious = 0
        challenging = 0
        personal_planets = ["Sun", "Moon", "Mercury", "Venus", "Mars"]

        for a in aspects:
            # Both planets must be personal for a meaningful aspect
            is_personal = a.p1_name in personal_planets and a.p2_name in personal_planets
            # Tighter orb = stronger aspect
            orb = getattr(a, "orbit", None) or getattr(a, "orb", 10)
            try:
                orb = abs(float(orb))
            except (TypeError, ValueError):
                orb = 10

            if a.aspect in ["conjunction", "trine", "sextile"]:
                harmonious += 1
                if is_personal:
                    if orb <= 2:
                        aspect_bonus += 2    # Very tight harmonious — strong
                    elif orb <= 4:
                        aspect_bonus += 1    # Moderate
                    # > 4° orb: no bonus (too loose)
            elif a.aspect in ["square", "opposition"]:
                challenging += 1
                if is_personal:
                    if orb <= 2:
                        aspect_bonus -= 2    # Very tight challenging — real friction
                    elif orb <= 4:
                        aspect_bonus -= 1

        # Cap the bonus so no couple gets runaway inflation
        aspect_bonus = max(-10, min(12, aspect_bonus))

        # Overall score (weighted average of 4 elements + capped aspect adjustment)
        base = (sun_score * 0.30 + moon_score * 0.30 + venus_score * 0.25 + mars_score * 0.15)
        overall = min(95, max(20, int(round(base + aspect_bonus))))

        # Score interpretation text — calibrated thresholds (v2.7.0)
        if overall >= 85:
            rating = "Exceptional"
            score_meaning = "Exceptional compatibility. Your planetary energies flow together with remarkable ease across emotional, romantic, and physical dimensions. This level of natural alignment is rare and suggests a deeply intuitive connection."
        elif overall >= 70:
            rating = "Strong"
            score_meaning = "Strong compatibility with natural chemistry. You share meaningful harmony in several key areas, with enough difference to keep the relationship dynamic. This is a solid foundation for long-term partnership."
        elif overall >= 55:
            rating = "Good"
            score_meaning = "Good compatibility with a healthy balance of harmony and challenge. Many successful long-term relationships fall in this range because the friction keeps both partners growing while the harmony keeps them connected."
        elif overall >= 40:
            rating = "Moderate"
            score_meaning = "Moderate compatibility that works best with conscious effort. The planetary tensions between your charts create intensity and passion but also frequent misunderstandings. Communication, patience, and mutual respect are essential."
        else:
            rating = "Challenging"
            score_meaning = "Significant planetary contrast between your charts. This does not mean the relationship cannot work, but both partners will need to actively bridge differences in emotional style, communication, and desire. The attraction may be strong despite the challenges."

        return jsonify({
            "success": True, "tool": "love_compatibility",
            "person1": {
                "name": data["person1"].get("name","Person 1"),
                "sun": p1["sun"]["sign"], "moon": p1["moon"]["sign"],
                "venus": p1["venus"]["sign"], "mars": p1["mars"]["sign"],
                "sun_element": p1["sun"].get("element",""),
                "moon_element": p1["moon"].get("element",""),
                "venus_element": p1["venus"].get("element",""),
                "mars_element": p1["mars"].get("element",""),
                "sun_degree": p1["sun"].get("degree",0),
                "moon_degree": p1["moon"].get("degree",0),
                "venus_degree": p1["venus"].get("degree",0),
                "mars_degree": p1["mars"].get("degree",0),
            },
            "person2": {
                "name": data["person2"].get("name","Person 2"),
                "sun": p2["sun"]["sign"], "moon": p2["moon"]["sign"],
                "venus": p2["venus"]["sign"], "mars": p2["mars"]["sign"],
                "sun_element": p2["sun"].get("element",""),
                "moon_element": p2["moon"].get("element",""),
                "venus_element": p2["venus"].get("element",""),
                "mars_element": p2["mars"].get("element",""),
                "sun_degree": p2["sun"].get("degree",0),
                "moon_degree": p2["moon"].get("degree",0),
                "venus_degree": p2["venus"].get("degree",0),
                "mars_degree": p2["mars"].get("degree",0),
            },
            "scores": {
                "overall": overall,
                "rating": rating,
                "sun_compatibility": sun_score,
                "moon_compatibility": moon_score,
                "venus_compatibility": venus_score,
                "mars_compatibility": mars_score,
            },
            "score_meaning": score_meaning,
            "score_details": {
                "sun_meaning": f"Sun compatibility ({sun_score}%) reflects how well your core personalities align. {p1['sun']['sign']} Sun and {p2['sun']['sign']} Sun {'share the same element, creating natural understanding.' if p1['sun']['element'] == p2['sun']['element'] else 'belong to different elements, bringing contrasting but potentially complementary energies.'}",
                "moon_meaning": f"Moon compatibility ({moon_score}%) reveals emotional attunement. {p1['moon']['sign']} Moon and {p2['moon']['sign']} Moon {'share emotional wavelengths, making comfort and nurturing feel instinctive.' if p1['moon']['element'] == p2['moon']['element'] else 'process emotions differently, which can create growth opportunities if both partners stay patient.'}",
                "venus_meaning": f"Venus compatibility ({venus_score}%) measures romantic and aesthetic harmony. {p1['venus']['sign']} Venus and {p2['venus']['sign']} Venus {'express love in similar ways, creating natural romantic flow.' if p1['venus']['element'] == p2['venus']['element'] else 'have different love languages, requiring conscious effort to make each partner feel appreciated.'}",
                "mars_meaning": f"Mars compatibility ({mars_score}%) indicates physical chemistry and conflict style. {p1['mars']['sign']} Mars and {p2['mars']['sign']} Mars {'share a similar drive and energy level, supporting passion and teamwork.' if p1['mars']['element'] == p2['mars']['element'] else 'channel energy differently, which can create exciting tension or frustrating clashes depending on maturity.'}",
            },
            "aspects_summary": {
                "total": len(aspects),
                "harmonious": harmonious,
                "challenging": challenging,
            },
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# TOOL 4: SUN SIGN CALCULATOR
# ═══════════════════════════════════════════════════════════════

@app.route("/api/sun-sign", methods=["POST"])
def sun_sign():
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        p = fmt_planet(s.sun)
        interp = SUN_INTERPRETATIONS.get(p["sign"], {})
        return jsonify({
            "success":True, "tool":"sun_sign",
            "name": data.get("name","User"),
            "sun": p,
            "description": f"Your Sun is in {p['sign']} at {p['degree']}\u00b0 in House {p['house']}.",
            "interpretation": interp,
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# TOOL 5: MOON SIGN CALCULATOR
# ═══════════════════════════════════════════════════════════════

@app.route("/api/moon-sign", methods=["POST"])
def moon_sign():
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        p = fmt_planet(s.moon)
        interp = MOON_INTERPRETATIONS.get(p["sign"], {})
        return jsonify({
            "success":True, "tool":"moon_sign",
            "name": data.get("name","User"),
            "moon": p,
            "description": f"Your Moon is in {p['sign']} at {p['degree']}\u00b0 in House {p['house']}.",
            "interpretation": interp,
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# TOOL 6: RISING SIGN CALCULATOR
# ═══════════════════════════════════════════════════════════════

@app.route("/api/rising-sign", methods=["POST"])
def rising_sign():
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        h = s.first_house
        sign = SIGN_FULL.get(h.sign, h.sign)
        interp = RISING_INTERPRETATIONS.get(sign, {})
        return jsonify({
            "success":True, "tool":"rising_sign",
            "name": data.get("name","User"),
            "rising": {
                "sign": sign, "degree": round(h.position,2),
                "element": SIGN_ELEMENT.get(sign,""),
                "quality": SIGN_QUALITY.get(sign,""),
                "ruler": SIGN_RULER.get(sign,""),
            },
            "description": f"Your Rising Sign (Ascendant) is {sign} at {round(h.position,2)}\u00b0.",
            "interpretation": interp,
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# TOOL 7: SUN, MOON, RISING CALCULATOR (Big Three)
# ═══════════════════════════════════════════════════════════════

@app.route("/api/big-three", methods=["POST"])
def big_three():
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        sun = fmt_planet(s.sun)
        moon = fmt_planet(s.moon)
        h = s.first_house
        rising_s = SIGN_FULL.get(h.sign, h.sign)

        return jsonify({
            "success":True, "tool":"big_three",
            "name": data.get("name","User"),
            "sun": sun,
            "moon": moon,
            "rising": {
                "sign": rising_s, "degree": round(h.position,2),
                "element": SIGN_ELEMENT.get(rising_s,""),
                "quality": SIGN_QUALITY.get(rising_s,""),
                "ruler": SIGN_RULER.get(rising_s,""),
            },
            "interpretations": {
                "sun": SUN_INTERPRETATIONS.get(sun["sign"], {}),
                "moon": MOON_INTERPRETATIONS.get(moon["sign"], {}),
                "rising": RISING_INTERPRETATIONS.get(rising_s, {}),
            },
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# TOOL 8: VENUS SIGN CALCULATOR
# ═══════════════════════════════════════════════════════════════

@app.route("/api/venus-sign", methods=["POST"])
def venus_sign():
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        p = fmt_planet(s.venus)
        interp = VENUS_INTERPRETATIONS.get(p["sign"], {})
        return jsonify({
            "success":True, "tool":"venus_sign",
            "name": data.get("name","User"),
            "venus": p,
            "description": f"Your Venus is in {p['sign']} at {p['degree']}\u00b0 in House {p['house']}.",
            "interpretation": interp,
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# TOOL 9: CHIRON SIGN CALCULATOR
# ═══════════════════════════════════════════════════════════════

@app.route("/api/chiron-sign", methods=["POST"])
def chiron_sign():
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        p = fmt_planet(s.chiron)
        interp = CHIRON_INTERPRETATIONS.get(p["sign"], {})
        return jsonify({
            "success":True, "tool":"chiron_sign",
            "name": data.get("name","User"),
            "chiron": p,
            "description": f"Your Chiron (Wounded Healer) is in {p['sign']} at {p['degree']}\u00b0 in House {p['house']}.",
            "interpretation": interp,
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# TOOL 10: LILITH SIGN CALCULATOR
# ═══════════════════════════════════════════════════════════════

@app.route("/api/lilith-sign", methods=["POST"])
def lilith_sign():
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        p = fmt_planet(s.mean_lilith)
        interp = LILITH_INTERPRETATIONS.get(p["sign"], {})
        return jsonify({
            "success":True, "tool":"lilith_sign",
            "name": data.get("name","User"),
            "lilith": p,
            "description": f"Your Black Moon Lilith is in {p['sign']} at {p['degree']}\u00b0 in House {p['house']}.",
            "interpretation": interp,
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# TOOL 11: NORTH NODE CALCULATOR
# ═══════════════════════════════════════════════════════════════

@app.route("/api/north-node", methods=["POST"])
def north_node():
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        nn = fmt_planet(s.true_north_lunar_node)
        sn = fmt_planet(s.true_south_lunar_node)
        interp = NORTH_NODE_INTERPRETATIONS.get(nn["sign"], {})
        return jsonify({
            "success":True, "tool":"north_node",
            "name": data.get("name","User"),
            "north_node": nn,
            "south_node": sn,
            "description": f"Your North Node is in {nn['sign']} at {nn['degree']}\u00b0 (House {nn['house']}). South Node is in {sn['sign']}.",
            "interpretation": interp,
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# TOOL 12: PART OF FORTUNE CALCULATOR
# ═══════════════════════════════════════════════════════════════

@app.route("/api/part-of-fortune", methods=["POST"])
def part_of_fortune():
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        pof = calc_part_of_fortune(s)

        # Find which house it falls in
        houses = get_all_houses(s)
        pof_house = 1
        abs_deg = pof["abs_degree"]
        for i in range(12):
            h_start = houses[i]["degree"] + (SIGNS_LIST.index(houses[i]["sign"]) * 30)
            h_end = houses[(i+1)%12]["degree"] + (SIGNS_LIST.index(houses[(i+1)%12]["sign"]) * 30)
            if h_end < h_start: h_end += 360
            check = abs_deg if abs_deg >= h_start else abs_deg + 360
            if h_start <= check < h_end:
                pof_house = i + 1
                break

        pof["house"] = pof_house

        return jsonify({
            "success":True, "tool":"part_of_fortune",
            "name": data.get("name","User"),
            "part_of_fortune": pof,
            "description": f"Your Part of Fortune is in {pof['sign']} at {pof['degree']}\u00b0 ({pof['chart_type']} chart formula used).",
            "interpretation": PART_OF_FORTUNE_INTERPRETATIONS.get(pof["sign"], {}),
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# TOOL 13: VERTEX CALCULATOR
# ═══════════════════════════════════════════════════════════════

@app.route("/api/vertex", methods=["POST"])
def vertex():
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        vtx = calc_vertex(data)

        # Anti-Vertex is exactly opposite
        anti_abs = (vtx["abs_degree"] + 180) % 360
        anti_sign, anti_deg = sign_from_abs(anti_abs)

        return jsonify({
            "success":True, "tool":"vertex",
            "name": data.get("name","User"),
            "vertex": vtx,
            "anti_vertex": {
                "sign": anti_sign, "degree": anti_deg,
                "abs_degree": round(anti_abs, 2),
                "element": SIGN_ELEMENT.get(anti_sign,""),
            },
            "description": f"Your Vertex is in {vtx['sign']} at {vtx['degree']}\u00b0. Anti-Vertex is in {anti_sign}.",
            "interpretation": VERTEX_INTERPRETATIONS.get(vtx["sign"], {}),
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# UTILITY ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status":"ok",
        "service":"Astrology Tools API",
        "tools": 13,
        "engine":"Kerykeion + Swiss Ephemeris",
        "endpoints": [
            "/api/birth-chart", "/api/birth-chart/svg",
            "/api/synastry-chart", "/api/love-compatibility",
            "/api/sun-sign", "/api/moon-sign", "/api/rising-sign",
            "/api/big-three", "/api/venus-sign", "/api/chiron-sign",
            "/api/lilith-sign", "/api/north-node",
            "/api/part-of-fortune", "/api/vertex",
            "/api/geocode", "/api/geocode/timezone",
        ]
    })


@app.route("/api/all-points", methods=["POST"])
def all_points():
    """Quick endpoint: all celestial points at once (for single page tools)."""
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        planets = get_all_planets(s)
        houses = get_all_houses(s)

        return jsonify({
            "success":True, "tool":"all_points",
            "name": data.get("name","User"),
            "sun": planets["sun"],
            "moon": planets["moon"],
            "rising": {"sign": houses[0]["sign"], "degree": houses[0]["degree"]},
            "mercury": planets["mercury"],
            "venus": planets["venus"],
            "mars": planets["mars"],
            "jupiter": planets["jupiter"],
            "saturn": planets["saturn"],
            "uranus": planets["uranus"],
            "neptune": planets["neptune"],
            "pluto": planets["pluto"],
            "chiron": fmt_planet(s.chiron),
            "lilith": fmt_planet(s.mean_lilith),
            "north_node": fmt_planet(s.true_north_lunar_node),
            "south_node": fmt_planet(s.true_south_lunar_node),
            "part_of_fortune": calc_part_of_fortune(s),
            "vertex": calc_vertex(data),
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


# ═══════════════════════════════════════════════════════════════
# GEOCODING — City name → Lat/Lng/Timezone
# ═══════════════════════════════════════════════════════════════

# Country → Timezone mapping (covers 95%+ of astrology users)
COUNTRY_TZ = {
    "Pakistan": "Asia/Karachi", "India": "Asia/Kolkata",
    "Bangladesh": "Asia/Dhaka", "Sri Lanka": "Asia/Colombo",
    "Nepal": "Asia/Kathmandu", "Afghanistan": "Asia/Kabul",
    "Iran": "Asia/Tehran", "Iraq": "Asia/Baghdad",
    "United Arab Emirates": "Asia/Dubai", "Saudi Arabia": "Asia/Riyadh",
    "Qatar": "Asia/Qatar", "Kuwait": "Asia/Kuwait",
    "Bahrain": "Asia/Bahrain", "Oman": "Asia/Muscat",
    "Turkey": "Europe/Istanbul", "Egypt": "Africa/Cairo",
    "United Kingdom": "Europe/London", "England": "Europe/London",
    "France": "Europe/Paris", "Germany": "Europe/Berlin",
    "Italy": "Europe/Rome", "Spain": "Europe/Madrid",
    "Netherlands": "Europe/Amsterdam", "Belgium": "Europe/Brussels",
    "Switzerland": "Europe/Zurich", "Austria": "Europe/Vienna",
    "Poland": "Europe/Warsaw", "Sweden": "Europe/Stockholm",
    "Norway": "Europe/Oslo", "Denmark": "Europe/Copenhagen",
    "Finland": "Europe/Helsinki", "Portugal": "Europe/Lisbon",
    "Greece": "Europe/Athens", "Romania": "Europe/Bucharest",
    "Russia": "Europe/Moscow", "Ukraine": "Europe/Kyiv",
    "United States": "America/New_York",
    "United States of America": "America/New_York",
    "Canada": "America/Toronto", "Mexico": "America/Mexico_City",
    "Brazil": "America/Sao_Paulo",
    "Argentina": "America/Argentina/Buenos_Aires",
    "Colombia": "America/Bogota", "Chile": "America/Santiago",
    "Peru": "America/Lima", "Venezuela": "America/Caracas",
    "China": "Asia/Shanghai", "Japan": "Asia/Tokyo",
    "South Korea": "Asia/Seoul", "Taiwan": "Asia/Taipei",
    "Thailand": "Asia/Bangkok", "Vietnam": "Asia/Ho_Chi_Minh",
    "Malaysia": "Asia/Kuala_Lumpur", "Singapore": "Asia/Singapore",
    "Indonesia": "Asia/Jakarta", "Philippines": "Asia/Manila",
    "Australia": "Australia/Sydney", "New Zealand": "Pacific/Auckland",
    "South Africa": "Africa/Johannesburg", "Nigeria": "Africa/Lagos",
    "Kenya": "Africa/Nairobi", "Morocco": "Africa/Casablanca",
    "Israel": "Asia/Jerusalem", "Jordan": "Asia/Amman",
    "Lebanon": "Asia/Beirut", "Syria": "Asia/Damascus",
}

# ─── Geocode Cache & Rate Limiter ─────────────────────────
_geocode_cache = {}
_last_nominatim_call = 0

# ─── Built-in City Database (covers 95%+ of astrology users) ──
# Eliminates Nominatim dependency for common cities
CITIES_DB = [
    # Pakistan
    {"name":"Karachi","search":"karachi","lat":24.8607,"lng":67.0011,"tz":"Asia/Karachi","country":"Pakistan","state":"Sindh"},
    {"name":"Lahore","search":"lahore","lat":31.5204,"lng":74.3587,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Islamabad","search":"islamabad","lat":33.6844,"lng":73.0479,"tz":"Asia/Karachi","country":"Pakistan","state":"Islamabad"},
    {"name":"Rawalpindi","search":"rawalpindi","lat":33.5651,"lng":73.0169,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Faisalabad","search":"faisalabad","lat":31.4504,"lng":73.135,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Multan","search":"multan","lat":30.1575,"lng":71.5249,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Peshawar","search":"peshawar","lat":34.0151,"lng":71.5249,"tz":"Asia/Karachi","country":"Pakistan","state":"KPK"},
    {"name":"Quetta","search":"quetta","lat":30.1798,"lng":66.975,"tz":"Asia/Karachi","country":"Pakistan","state":"Balochistan"},
    {"name":"Sialkot","search":"sialkot","lat":32.4945,"lng":74.5229,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Gujranwala","search":"gujranwala","lat":32.1877,"lng":74.1945,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Bahawalpur","search":"bahawalpur","lat":29.3956,"lng":71.6836,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Sargodha","search":"sargodha","lat":32.0836,"lng":72.6711,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Sukkur","search":"sukkur","lat":27.7052,"lng":68.8574,"tz":"Asia/Karachi","country":"Pakistan","state":"Sindh"},
    {"name":"Hyderabad","search":"hyderabad pakistan","lat":25.396,"lng":68.3578,"tz":"Asia/Karachi","country":"Pakistan","state":"Sindh"},
    {"name":"Abbottabad","search":"abbottabad","lat":34.1688,"lng":73.2215,"tz":"Asia/Karachi","country":"Pakistan","state":"KPK"},
    {"name":"Mardan","search":"mardan","lat":34.1986,"lng":72.0404,"tz":"Asia/Karachi","country":"Pakistan","state":"KPK"},
    {"name":"Larkana","search":"larkana","lat":27.5583,"lng":68.2121,"tz":"Asia/Karachi","country":"Pakistan","state":"Sindh"},
    {"name":"Sahiwal","search":"sahiwal","lat":30.6682,"lng":73.1114,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Rahim Yar Khan","search":"rahim yar khan","lat":28.4202,"lng":70.2952,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Okara","search":"okara","lat":30.8138,"lng":73.4534,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Jhang","search":"jhang","lat":31.2681,"lng":72.3181,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Dera Ghazi Khan","search":"dera ghazi khan","lat":30.0489,"lng":70.6455,"tz":"Asia/Karachi","country":"Pakistan","state":"Punjab"},
    {"name":"Mirpur Khas","search":"mirpur khas","lat":25.5276,"lng":69.0159,"tz":"Asia/Karachi","country":"Pakistan","state":"Sindh"},
    {"name":"Nawabshah","search":"nawabshah","lat":26.2483,"lng":68.41,"tz":"Asia/Karachi","country":"Pakistan","state":"Sindh"},
    {"name":"Mingora","search":"mingora","lat":34.7717,"lng":72.36,"tz":"Asia/Karachi","country":"Pakistan","state":"KPK"},
    # India (top cities)
    {"name":"Mumbai","search":"mumbai","lat":19.076,"lng":72.8777,"tz":"Asia/Kolkata","country":"India","state":"Maharashtra"},
    {"name":"Delhi","search":"delhi","lat":28.7041,"lng":77.1025,"tz":"Asia/Kolkata","country":"India","state":"Delhi"},
    {"name":"New Delhi","search":"new delhi","lat":28.6139,"lng":77.209,"tz":"Asia/Kolkata","country":"India","state":"Delhi"},
    {"name":"Bangalore","search":"bangalore bengaluru","lat":12.9716,"lng":77.5946,"tz":"Asia/Kolkata","country":"India","state":"Karnataka"},
    {"name":"Hyderabad","search":"hyderabad india","lat":17.385,"lng":78.4867,"tz":"Asia/Kolkata","country":"India","state":"Telangana"},
    {"name":"Chennai","search":"chennai madras","lat":13.0827,"lng":80.2707,"tz":"Asia/Kolkata","country":"India","state":"Tamil Nadu"},
    {"name":"Kolkata","search":"kolkata calcutta","lat":22.5726,"lng":88.3639,"tz":"Asia/Kolkata","country":"India","state":"West Bengal"},
    {"name":"Pune","search":"pune","lat":18.5204,"lng":73.8567,"tz":"Asia/Kolkata","country":"India","state":"Maharashtra"},
    {"name":"Ahmedabad","search":"ahmedabad","lat":23.0225,"lng":72.5714,"tz":"Asia/Kolkata","country":"India","state":"Gujarat"},
    {"name":"Jaipur","search":"jaipur","lat":26.9124,"lng":75.7873,"tz":"Asia/Kolkata","country":"India","state":"Rajasthan"},
    {"name":"Lucknow","search":"lucknow","lat":26.8467,"lng":80.9462,"tz":"Asia/Kolkata","country":"India","state":"Uttar Pradesh"},
    {"name":"Surat","search":"surat","lat":21.1702,"lng":72.8311,"tz":"Asia/Kolkata","country":"India","state":"Gujarat"},
    {"name":"Chandigarh","search":"chandigarh","lat":30.7333,"lng":76.7794,"tz":"Asia/Kolkata","country":"India","state":"Chandigarh"},
    {"name":"Indore","search":"indore","lat":22.7196,"lng":75.8577,"tz":"Asia/Kolkata","country":"India","state":"Madhya Pradesh"},
    {"name":"Bhopal","search":"bhopal","lat":23.2599,"lng":77.4126,"tz":"Asia/Kolkata","country":"India","state":"Madhya Pradesh"},
    {"name":"Patna","search":"patna","lat":25.6093,"lng":85.1376,"tz":"Asia/Kolkata","country":"India","state":"Bihar"},
    {"name":"Nagpur","search":"nagpur","lat":21.1458,"lng":79.0882,"tz":"Asia/Kolkata","country":"India","state":"Maharashtra"},
    {"name":"Amritsar","search":"amritsar","lat":31.634,"lng":74.8723,"tz":"Asia/Kolkata","country":"India","state":"Punjab"},
    {"name":"Varanasi","search":"varanasi banaras","lat":25.3176,"lng":82.9739,"tz":"Asia/Kolkata","country":"India","state":"Uttar Pradesh"},
    {"name":"Coimbatore","search":"coimbatore","lat":11.0168,"lng":76.9558,"tz":"Asia/Kolkata","country":"India","state":"Tamil Nadu"},
    # USA (major cities)
    {"name":"New York","search":"new york nyc manhattan","lat":40.7128,"lng":-74.006,"tz":"America/New_York","country":"United States","state":"New York"},
    {"name":"Los Angeles","search":"los angeles la","lat":34.0522,"lng":-118.2437,"tz":"America/Los_Angeles","country":"United States","state":"California"},
    {"name":"Chicago","search":"chicago","lat":41.8781,"lng":-87.6298,"tz":"America/Chicago","country":"United States","state":"Illinois"},
    {"name":"Houston","search":"houston","lat":29.7604,"lng":-95.3698,"tz":"America/Chicago","country":"United States","state":"Texas"},
    {"name":"Phoenix","search":"phoenix","lat":33.4484,"lng":-112.074,"tz":"America/Phoenix","country":"United States","state":"Arizona"},
    {"name":"Philadelphia","search":"philadelphia philly","lat":39.9526,"lng":-75.1652,"tz":"America/New_York","country":"United States","state":"Pennsylvania"},
    {"name":"San Antonio","search":"san antonio","lat":29.4241,"lng":-98.4936,"tz":"America/Chicago","country":"United States","state":"Texas"},
    {"name":"San Diego","search":"san diego","lat":32.7157,"lng":-117.1611,"tz":"America/Los_Angeles","country":"United States","state":"California"},
    {"name":"Dallas","search":"dallas","lat":32.7767,"lng":-96.797,"tz":"America/Chicago","country":"United States","state":"Texas"},
    {"name":"San Jose","search":"san jose california","lat":37.3382,"lng":-121.8863,"tz":"America/Los_Angeles","country":"United States","state":"California"},
    {"name":"Austin","search":"austin texas","lat":30.2672,"lng":-97.7431,"tz":"America/Chicago","country":"United States","state":"Texas"},
    {"name":"San Francisco","search":"san francisco sf","lat":37.7749,"lng":-122.4194,"tz":"America/Los_Angeles","country":"United States","state":"California"},
    {"name":"Seattle","search":"seattle","lat":47.6062,"lng":-122.3321,"tz":"America/Los_Angeles","country":"United States","state":"Washington"},
    {"name":"Denver","search":"denver","lat":39.7392,"lng":-104.9903,"tz":"America/Denver","country":"United States","state":"Colorado"},
    {"name":"Boston","search":"boston","lat":42.3601,"lng":-71.0589,"tz":"America/New_York","country":"United States","state":"Massachusetts"},
    {"name":"Atlanta","search":"atlanta","lat":33.749,"lng":-84.388,"tz":"America/New_York","country":"United States","state":"Georgia"},
    {"name":"Miami","search":"miami","lat":25.7617,"lng":-80.1918,"tz":"America/New_York","country":"United States","state":"Florida"},
    {"name":"Las Vegas","search":"las vegas vegas","lat":36.1699,"lng":-115.1398,"tz":"America/Los_Angeles","country":"United States","state":"Nevada"},
    {"name":"Portland","search":"portland oregon","lat":45.5152,"lng":-122.6784,"tz":"America/Los_Angeles","country":"United States","state":"Oregon"},
    {"name":"Detroit","search":"detroit","lat":42.3314,"lng":-83.0458,"tz":"America/New_York","country":"United States","state":"Michigan"},
    {"name":"Minneapolis","search":"minneapolis","lat":44.9778,"lng":-93.265,"tz":"America/Chicago","country":"United States","state":"Minnesota"},
    {"name":"Nashville","search":"nashville","lat":36.1627,"lng":-86.7816,"tz":"America/Chicago","country":"United States","state":"Tennessee"},
    # UK
    {"name":"London","search":"london","lat":51.5074,"lng":-0.1278,"tz":"Europe/London","country":"United Kingdom","state":"England"},
    {"name":"Manchester","search":"manchester","lat":53.4808,"lng":-2.2426,"tz":"Europe/London","country":"United Kingdom","state":"England"},
    {"name":"Birmingham","search":"birmingham uk","lat":52.4862,"lng":-1.8904,"tz":"Europe/London","country":"United Kingdom","state":"England"},
    {"name":"Edinburgh","search":"edinburgh","lat":55.9533,"lng":-3.1883,"tz":"Europe/London","country":"United Kingdom","state":"Scotland"},
    {"name":"Glasgow","search":"glasgow","lat":55.8642,"lng":-4.2518,"tz":"Europe/London","country":"United Kingdom","state":"Scotland"},
    {"name":"Liverpool","search":"liverpool","lat":53.4084,"lng":-2.9916,"tz":"Europe/London","country":"United Kingdom","state":"England"},
    {"name":"Leeds","search":"leeds","lat":53.8008,"lng":-1.5491,"tz":"Europe/London","country":"United Kingdom","state":"England"},
    {"name":"Bristol","search":"bristol","lat":51.4545,"lng":-2.5879,"tz":"Europe/London","country":"United Kingdom","state":"England"},
    # Canada
    {"name":"Toronto","search":"toronto","lat":43.6532,"lng":-79.3832,"tz":"America/Toronto","country":"Canada","state":"Ontario"},
    {"name":"Vancouver","search":"vancouver","lat":49.2827,"lng":-123.1207,"tz":"America/Vancouver","country":"Canada","state":"British Columbia"},
    {"name":"Montreal","search":"montreal","lat":45.5017,"lng":-73.5673,"tz":"America/Toronto","country":"Canada","state":"Quebec"},
    {"name":"Calgary","search":"calgary","lat":51.0447,"lng":-114.0719,"tz":"America/Edmonton","country":"Canada","state":"Alberta"},
    {"name":"Ottawa","search":"ottawa","lat":45.4215,"lng":-75.6972,"tz":"America/Toronto","country":"Canada","state":"Ontario"},
    # Middle East
    {"name":"Dubai","search":"dubai","lat":25.2048,"lng":55.2708,"tz":"Asia/Dubai","country":"United Arab Emirates","state":"Dubai"},
    {"name":"Abu Dhabi","search":"abu dhabi","lat":24.4539,"lng":54.3773,"tz":"Asia/Dubai","country":"United Arab Emirates","state":"Abu Dhabi"},
    {"name":"Riyadh","search":"riyadh","lat":24.7136,"lng":46.6753,"tz":"Asia/Riyadh","country":"Saudi Arabia","state":"Riyadh"},
    {"name":"Jeddah","search":"jeddah jiddah","lat":21.4858,"lng":39.1925,"tz":"Asia/Riyadh","country":"Saudi Arabia","state":"Makkah"},
    {"name":"Mecca","search":"mecca makkah","lat":21.3891,"lng":39.8579,"tz":"Asia/Riyadh","country":"Saudi Arabia","state":"Makkah"},
    {"name":"Medina","search":"medina madinah","lat":24.4709,"lng":39.6119,"tz":"Asia/Riyadh","country":"Saudi Arabia","state":"Madinah"},
    {"name":"Doha","search":"doha","lat":25.2854,"lng":51.531,"tz":"Asia/Qatar","country":"Qatar","state":""},
    {"name":"Kuwait City","search":"kuwait","lat":29.3759,"lng":47.9774,"tz":"Asia/Kuwait","country":"Kuwait","state":""},
    {"name":"Muscat","search":"muscat","lat":23.588,"lng":58.3829,"tz":"Asia/Muscat","country":"Oman","state":""},
    {"name":"Manama","search":"manama bahrain","lat":26.2285,"lng":50.5860,"tz":"Asia/Bahrain","country":"Bahrain","state":""},
    {"name":"Tehran","search":"tehran","lat":35.6892,"lng":51.389,"tz":"Asia/Tehran","country":"Iran","state":"Tehran"},
    {"name":"Baghdad","search":"baghdad","lat":33.3152,"lng":44.3661,"tz":"Asia/Baghdad","country":"Iraq","state":"Baghdad"},
    {"name":"Istanbul","search":"istanbul","lat":41.0082,"lng":28.9784,"tz":"Europe/Istanbul","country":"Turkey","state":"Istanbul"},
    {"name":"Ankara","search":"ankara","lat":39.9334,"lng":32.8597,"tz":"Europe/Istanbul","country":"Turkey","state":"Ankara"},
    {"name":"Cairo","search":"cairo","lat":30.0444,"lng":31.2357,"tz":"Africa/Cairo","country":"Egypt","state":"Cairo"},
    {"name":"Alexandria","search":"alexandria egypt","lat":31.2001,"lng":29.9187,"tz":"Africa/Cairo","country":"Egypt","state":"Alexandria"},
    {"name":"Beirut","search":"beirut","lat":33.8938,"lng":35.5018,"tz":"Asia/Beirut","country":"Lebanon","state":""},
    {"name":"Amman","search":"amman","lat":31.9454,"lng":35.9284,"tz":"Asia/Amman","country":"Jordan","state":""},
    {"name":"Damascus","search":"damascus","lat":33.5138,"lng":36.2765,"tz":"Asia/Damascus","country":"Syria","state":""},
    # Europe
    {"name":"Paris","search":"paris","lat":48.8566,"lng":2.3522,"tz":"Europe/Paris","country":"France","state":"Ile-de-France"},
    {"name":"Berlin","search":"berlin","lat":52.52,"lng":13.405,"tz":"Europe/Berlin","country":"Germany","state":"Berlin"},
    {"name":"Munich","search":"munich munchen","lat":48.1351,"lng":11.582,"tz":"Europe/Berlin","country":"Germany","state":"Bavaria"},
    {"name":"Frankfurt","search":"frankfurt","lat":50.1109,"lng":8.6821,"tz":"Europe/Berlin","country":"Germany","state":"Hesse"},
    {"name":"Rome","search":"rome roma","lat":41.9028,"lng":12.4964,"tz":"Europe/Rome","country":"Italy","state":"Lazio"},
    {"name":"Milan","search":"milan milano","lat":45.4642,"lng":9.19,"tz":"Europe/Rome","country":"Italy","state":"Lombardy"},
    {"name":"Madrid","search":"madrid","lat":40.4168,"lng":-3.7038,"tz":"Europe/Madrid","country":"Spain","state":"Madrid"},
    {"name":"Barcelona","search":"barcelona","lat":41.3874,"lng":2.1686,"tz":"Europe/Madrid","country":"Spain","state":"Catalonia"},
    {"name":"Amsterdam","search":"amsterdam","lat":52.3676,"lng":4.9041,"tz":"Europe/Amsterdam","country":"Netherlands","state":"North Holland"},
    {"name":"Brussels","search":"brussels","lat":50.8503,"lng":4.3517,"tz":"Europe/Brussels","country":"Belgium","state":"Brussels"},
    {"name":"Zurich","search":"zurich","lat":47.3769,"lng":8.5417,"tz":"Europe/Zurich","country":"Switzerland","state":"Zurich"},
    {"name":"Vienna","search":"vienna wien","lat":48.2082,"lng":16.3738,"tz":"Europe/Vienna","country":"Austria","state":"Vienna"},
    {"name":"Warsaw","search":"warsaw","lat":52.2297,"lng":21.0122,"tz":"Europe/Warsaw","country":"Poland","state":"Masovia"},
    {"name":"Stockholm","search":"stockholm","lat":59.3293,"lng":18.0686,"tz":"Europe/Stockholm","country":"Sweden","state":"Stockholm"},
    {"name":"Oslo","search":"oslo","lat":59.9139,"lng":10.7522,"tz":"Europe/Oslo","country":"Norway","state":"Oslo"},
    {"name":"Copenhagen","search":"copenhagen","lat":55.6761,"lng":12.5683,"tz":"Europe/Copenhagen","country":"Denmark","state":"Capital Region"},
    {"name":"Helsinki","search":"helsinki","lat":60.1699,"lng":24.9384,"tz":"Europe/Helsinki","country":"Finland","state":"Uusimaa"},
    {"name":"Lisbon","search":"lisbon","lat":38.7223,"lng":-9.1393,"tz":"Europe/Lisbon","country":"Portugal","state":"Lisbon"},
    {"name":"Athens","search":"athens","lat":37.9838,"lng":23.7275,"tz":"Europe/Athens","country":"Greece","state":"Attica"},
    {"name":"Bucharest","search":"bucharest","lat":44.4268,"lng":26.1025,"tz":"Europe/Bucharest","country":"Romania","state":"Bucharest"},
    {"name":"Moscow","search":"moscow","lat":55.7558,"lng":37.6173,"tz":"Europe/Moscow","country":"Russia","state":"Moscow"},
    {"name":"Kyiv","search":"kyiv kiev","lat":50.4501,"lng":30.5234,"tz":"Europe/Kyiv","country":"Ukraine","state":"Kyiv"},
    {"name":"Prague","search":"prague","lat":50.0755,"lng":14.4378,"tz":"Europe/Prague","country":"Czech Republic","state":"Prague"},
    {"name":"Budapest","search":"budapest","lat":47.4979,"lng":19.0402,"tz":"Europe/Budapest","country":"Hungary","state":"Budapest"},
    {"name":"Dublin","search":"dublin","lat":53.3498,"lng":-6.2603,"tz":"Europe/Dublin","country":"Ireland","state":"Leinster"},
    # South Asia
    {"name":"Dhaka","search":"dhaka","lat":23.8103,"lng":90.4125,"tz":"Asia/Dhaka","country":"Bangladesh","state":"Dhaka"},
    {"name":"Colombo","search":"colombo","lat":6.9271,"lng":79.8612,"tz":"Asia/Colombo","country":"Sri Lanka","state":"Western"},
    {"name":"Kathmandu","search":"kathmandu","lat":27.7172,"lng":85.324,"tz":"Asia/Kathmandu","country":"Nepal","state":"Bagmati"},
    {"name":"Kabul","search":"kabul","lat":34.5553,"lng":69.2075,"tz":"Asia/Kabul","country":"Afghanistan","state":"Kabul"},
    # East & Southeast Asia
    {"name":"Tokyo","search":"tokyo","lat":35.6762,"lng":139.6503,"tz":"Asia/Tokyo","country":"Japan","state":"Tokyo"},
    {"name":"Osaka","search":"osaka","lat":34.6937,"lng":135.5023,"tz":"Asia/Tokyo","country":"Japan","state":"Osaka"},
    {"name":"Beijing","search":"beijing peking","lat":39.9042,"lng":116.4074,"tz":"Asia/Shanghai","country":"China","state":"Beijing"},
    {"name":"Shanghai","search":"shanghai","lat":31.2304,"lng":121.4737,"tz":"Asia/Shanghai","country":"China","state":"Shanghai"},
    {"name":"Hong Kong","search":"hong kong","lat":22.3193,"lng":114.1694,"tz":"Asia/Hong_Kong","country":"China","state":"Hong Kong"},
    {"name":"Seoul","search":"seoul","lat":37.5665,"lng":126.978,"tz":"Asia/Seoul","country":"South Korea","state":"Seoul"},
    {"name":"Taipei","search":"taipei","lat":25.033,"lng":121.5654,"tz":"Asia/Taipei","country":"Taiwan","state":"Taipei"},
    {"name":"Bangkok","search":"bangkok","lat":13.7563,"lng":100.5018,"tz":"Asia/Bangkok","country":"Thailand","state":"Bangkok"},
    {"name":"Singapore","search":"singapore","lat":1.3521,"lng":103.8198,"tz":"Asia/Singapore","country":"Singapore","state":""},
    {"name":"Kuala Lumpur","search":"kuala lumpur kl","lat":3.139,"lng":101.6869,"tz":"Asia/Kuala_Lumpur","country":"Malaysia","state":"Federal Territory"},
    {"name":"Jakarta","search":"jakarta","lat":-6.2088,"lng":106.8456,"tz":"Asia/Jakarta","country":"Indonesia","state":"Jakarta"},
    {"name":"Manila","search":"manila","lat":14.5995,"lng":120.9842,"tz":"Asia/Manila","country":"Philippines","state":"Metro Manila"},
    {"name":"Ho Chi Minh City","search":"ho chi minh saigon","lat":10.8231,"lng":106.6297,"tz":"Asia/Ho_Chi_Minh","country":"Vietnam","state":""},
    {"name":"Hanoi","search":"hanoi","lat":21.0278,"lng":105.8342,"tz":"Asia/Ho_Chi_Minh","country":"Vietnam","state":"Hanoi"},
    # Australia & NZ
    {"name":"Sydney","search":"sydney","lat":-33.8688,"lng":151.2093,"tz":"Australia/Sydney","country":"Australia","state":"NSW"},
    {"name":"Melbourne","search":"melbourne","lat":-37.8136,"lng":144.9631,"tz":"Australia/Melbourne","country":"Australia","state":"Victoria"},
    {"name":"Brisbane","search":"brisbane","lat":-27.4698,"lng":153.0251,"tz":"Australia/Brisbane","country":"Australia","state":"Queensland"},
    {"name":"Perth","search":"perth australia","lat":-31.9505,"lng":115.8605,"tz":"Australia/Perth","country":"Australia","state":"Western Australia"},
    {"name":"Auckland","search":"auckland","lat":-36.8485,"lng":174.7633,"tz":"Pacific/Auckland","country":"New Zealand","state":"Auckland"},
    # Africa
    {"name":"Johannesburg","search":"johannesburg","lat":-26.2041,"lng":28.0473,"tz":"Africa/Johannesburg","country":"South Africa","state":"Gauteng"},
    {"name":"Cape Town","search":"cape town","lat":-33.9249,"lng":18.4241,"tz":"Africa/Johannesburg","country":"South Africa","state":"Western Cape"},
    {"name":"Lagos","search":"lagos","lat":6.5244,"lng":3.3792,"tz":"Africa/Lagos","country":"Nigeria","state":"Lagos"},
    {"name":"Nairobi","search":"nairobi","lat":-1.2921,"lng":36.8219,"tz":"Africa/Nairobi","country":"Kenya","state":"Nairobi"},
    {"name":"Casablanca","search":"casablanca","lat":33.5731,"lng":-7.5898,"tz":"Africa/Casablanca","country":"Morocco","state":"Casablanca-Settat"},
    # South America
    {"name":"São Paulo","search":"sao paulo","lat":-23.5505,"lng":-46.6333,"tz":"America/Sao_Paulo","country":"Brazil","state":"São Paulo"},
    {"name":"Rio de Janeiro","search":"rio de janeiro","lat":-22.9068,"lng":-43.1729,"tz":"America/Sao_Paulo","country":"Brazil","state":"Rio de Janeiro"},
    {"name":"Buenos Aires","search":"buenos aires","lat":-34.6037,"lng":-58.3816,"tz":"America/Argentina/Buenos_Aires","country":"Argentina","state":"Buenos Aires"},
    {"name":"Bogotá","search":"bogota","lat":4.711,"lng":-74.0721,"tz":"America/Bogota","country":"Colombia","state":"Cundinamarca"},
    {"name":"Lima","search":"lima","lat":-12.0464,"lng":-77.0428,"tz":"America/Lima","country":"Peru","state":"Lima"},
    {"name":"Santiago","search":"santiago chile","lat":-33.4489,"lng":-70.6693,"tz":"America/Santiago","country":"Chile","state":"Santiago"},
    {"name":"Mexico City","search":"mexico city cdmx","lat":19.4326,"lng":-99.1332,"tz":"America/Mexico_City","country":"Mexico","state":"CDMX"},
]


def lookup_timezone(country, lng):
    """Get timezone from country name, fallback to longitude."""
    tz = COUNTRY_TZ.get(country, "")
    if tz:
        # Special US handling by longitude
        if country in ("United States", "United States of America"):
            if lng < -115: tz = "America/Los_Angeles"
            elif lng < -100: tz = "America/Denver"
            elif lng < -87: tz = "America/Chicago"
            else: tz = "America/New_York"
        return tz
    # Fallback: longitude-based UTC offset
    offset = round(lng / 15)
    return f"Etc/GMT{'+' if offset <= 0 else '-'}{abs(offset)}"


@app.route("/api/geocode", methods=["GET"])
def geocode_city():
    """
    Convert city name to latitude, longitude, and timezone.
    Uses built-in database first, Nominatim as fallback with caching.
    GET /api/geocode?city=Lahore
    """
    city = request.args.get("city", "").strip()
    if not city or len(city) < 2:
        return jsonify({"error": "City name required (min 2 chars)"}), 400

    query_lower = city.lower()

    # ── Step 1: Check in-memory cache ──
    if query_lower in _geocode_cache:
        return jsonify(_geocode_cache[query_lower])

    # ── Step 2: Search built-in city database ──
    matches = []
    for c in CITIES_DB:
        if query_lower in c["search"]:
            matches.append({
                "name": c["name"],
                "full_name": f"{c['name']}, {c.get('state', '')}, {c['country']}".replace(", ,", ","),
                "latitude": c["lat"],
                "longitude": c["lng"],
                "timezone": c["tz"],
                "country": c["country"],
                "state": c.get("state", ""),
            })
        if len(matches) >= 5:
            break

    if matches:
        result = {"success": True, "query": city, "results": matches}
        _geocode_cache[query_lower] = result
        return jsonify(result)

    # ── Step 3: Nominatim fallback (rate-limited) ──
    import time as _time
    global _last_nominatim_call
    now = _time.time()
    if now - _last_nominatim_call < 1.5:
        _time.sleep(1.5 - (now - _last_nominatim_call))

    try:
        import urllib.request
        import urllib.parse
        import json as json_lib

        encoded_city = urllib.parse.quote(city)
        url = (
            f"https://nominatim.openstreetmap.org/search"
            f"?q={encoded_city}"
            f"&format=json&limit=5&addressdetails=1"
        )
        req = urllib.request.Request(url, headers={
            "User-Agent": "AstroCalcPro/2.0 (https://astrocalcpro.com; contact@astrocalcpro.com)",
            "Accept": "application/json",
        })
        resp = urllib.request.urlopen(req, timeout=10)
        _last_nominatim_call = _time.time()
        results = json_lib.loads(resp.read())

        if not results:
            return jsonify({"error": f"City '{city}' not found"}), 404

        cities = []
        seen = set()

        for r in results[:5]:
            lat = float(r["lat"])
            lng = float(r["lon"])
            display = r.get("display_name", city)

            key = f"{round(lat,1)},{round(lng,1)}"
            if key in seen:
                continue
            seen.add(key)

            addr = r.get("address", {})
            country = addr.get("country", "")
            state = addr.get("state", "")
            tz = lookup_timezone(country, lng)

            cities.append({
                "name": display.split(",")[0].strip(),
                "full_name": display,
                "latitude": round(lat, 6),
                "longitude": round(lng, 6),
                "timezone": tz,
                "country": country,
                "state": state,
            })

        result = {"success": True, "query": city, "results": cities}
        _geocode_cache[query_lower] = result
        return jsonify(result)

    except Exception as e:
        err_str = str(e)
        # If rate-limited, return helpful message
        if "429" in err_str:
            return jsonify({"error": "Geocoding service is temporarily busy. Please try again in a few seconds."}), 429
        return jsonify({"error": f"Geocoding failed: {err_str}"}), 500


@app.route("/api/geocode/timezone", methods=["GET"])
def get_timezone():
    """
    Get timezone for given coordinates and country.
    GET /api/geocode/timezone?lat=31.5204&lng=74.3587&country=Pakistan
    """
    try:
        lat = float(request.args.get("lat", 0))
        lng = float(request.args.get("lng", 0))
    except (ValueError, TypeError):
        return jsonify({"error": "Valid lat and lng required"}), 400

    country = request.args.get("country", "")
    tz = lookup_timezone(country, lng)

    return jsonify({
        "success": True,
        "latitude": lat, "longitude": lng,
        "timezone": tz,
    })


# ─── Run ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
