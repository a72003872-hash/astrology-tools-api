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
import swisseph as swe
import math
from interpretations import (
    SUN_INTERPRETATIONS, MOON_INTERPRETATIONS, RISING_INTERPRETATIONS,
    VENUS_INTERPRETATIONS, MARS_INTERPRETATIONS, MERCURY_INTERPRETATIONS,
    CHIRON_INTERPRETATIONS, LILITH_INTERPRETATIONS, NORTH_NODE_INTERPRETATIONS,
    PART_OF_FORTUNE_INTERPRETATIONS, VERTEX_INTERPRETATIONS,
    JUPITER_INTERPRETATIONS, SATURN_INTERPRETATIONS,
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
    ("Fire","Fire"):90,("Fire","Air"):85,("Fire","Earth"):50,("Fire","Water"):40,
    ("Air","Air"):85,("Air","Earth"):45,("Air","Water"):55,
    ("Earth","Earth"):88,("Earth","Water"):82,
    ("Water","Water"):90,
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
# TOOL 1: BIRTH CHART CALCULATOR
# ═══════════════════════════════════════════════════════════════

@app.route("/api/birth-chart", methods=["POST"])
def birth_chart():
    """Full birth chart — planets, houses, aspects, elements, qualities, interpretations."""
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        planets = get_all_planets(s)
        houses = get_all_houses(s)
        aspects = [fmt_aspect(a) for a in NatalAspects(s).all_aspects]

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

        return jsonify({
            "success": True, "tool": "birth_chart",
            "name": data.get("name","User"),
            "summary": {
                "sun_sign": planets["sun"]["sign"],
                "moon_sign": planets["moon"]["sign"],
                "rising_sign": houses[0]["sign"],
            },
            "planets": planets, "houses": houses, "aspects": aspects,
            "elements": get_element_dist(planets),
            "qualities": get_quality_dist(planets),
            "interpretations": interps,
        })
    except Exception as e:
        return jsonify({"error":str(e)}), 500


@app.route("/api/birth-chart/svg", methods=["POST"])
def birth_chart_svg():
    """Generate birth chart SVG image."""
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

        # SVG
        chart_data = ChartDataFactory.create_synastry_chart_data(s1, s2)
        svg = ChartDrawer(chart_data=chart_data).generate_svg_string()

        return jsonify({
            "success": True, "tool": "synastry_chart",
            "person1": {
                "name": data["person1"].get("name","Person 1"),
                "planets": p1_planets,
            },
            "person2": {
                "name": data["person2"].get("name","Person 2"),
                "planets": p2_planets,
            },
            "aspects": aspects,
            "aspects_summary": {
                "total": len(aspects),
                "harmonious": harmonious,
                "challenging": challenging,
            },
            "synastry_summary": synastry_summary,
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

        # Aspect-based scoring
        aspects = SynastryAspects(s1, s2).all_aspects
        aspect_bonus = 0
        harmonious = 0
        challenging = 0
        for a in aspects:
            if a.aspect in ["conjunction","trine","sextile"]:
                harmonious += 1
                if a.p1_name in ["Sun","Moon","Venus"] or a.p2_name in ["Sun","Moon","Venus"]:
                    aspect_bonus += 3
            elif a.aspect in ["square","opposition"]:
                challenging += 1
                if a.p1_name in ["Sun","Moon","Venus"] or a.p2_name in ["Sun","Moon","Venus"]:
                    aspect_bonus -= 1

        # Overall score
        base = (sun_score * 0.30 + moon_score * 0.30 + venus_score * 0.25 + mars_score * 0.15)
        overall = min(99, max(10, int(base + aspect_bonus)))

        # Score interpretation text
        if overall >= 80:
            score_meaning = "Exceptional compatibility. Your planetary energies flow together with remarkable ease across emotional, romantic, and physical dimensions. This level of natural alignment is rare and suggests a deeply intuitive connection."
        elif overall >= 65:
            score_meaning = "Strong compatibility with natural chemistry. You share meaningful harmony in several key areas, with enough difference to keep the relationship dynamic. This is a solid foundation for long-term partnership."
        elif overall >= 50:
            score_meaning = "Moderate compatibility with a healthy balance of harmony and challenge. Many successful long-term relationships fall in this range because the friction keeps both partners growing while the harmony keeps them connected."
        elif overall >= 35:
            score_meaning = "Below average compatibility that requires conscious effort. The planetary tensions between your charts create intensity and passion but also frequent misunderstandings. Communication and patience are essential."
        else:
            score_meaning = "Significant planetary contrast between your charts. This does not mean the relationship cannot work, but it does mean both partners will need to actively bridge differences in emotional style, communication, and desire. The attraction may be strong despite the challenges."

        return jsonify({
            "success": True, "tool": "love_compatibility",
            "person1": {"name":data["person1"].get("name","Person 1"),
                        "sun":p1["sun"]["sign"],"moon":p1["moon"]["sign"],
                        "venus":p1["venus"]["sign"],"mars":p1["mars"]["sign"]},
            "person2": {"name":data["person2"].get("name","Person 2"),
                        "sun":p2["sun"]["sign"],"moon":p2["moon"]["sign"],
                        "venus":p2["venus"]["sign"],"mars":p2["mars"]["sign"]},
            "scores": {
                "overall": overall,
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
    GET /api/geocode?city=Lahore
    GET /api/geocode?city=New York
    """
    city = request.args.get("city", "").strip()
    if not city or len(city) < 2:
        return jsonify({"error": "City name required (min 2 chars)"}), 400

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
            "User-Agent": "AstrologyToolsAPI/1.0 (astrology-tools-api)"
        })
        resp = urllib.request.urlopen(req, timeout=10)
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

        return jsonify({
            "success": True,
            "query": city,
            "results": cities,
        })

    except Exception as e:
        return jsonify({"error": f"Geocoding failed: {str(e)}"}), 500


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
