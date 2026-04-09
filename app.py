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
    """Full birth chart — planets, houses, aspects, elements, qualities."""
    data = request.get_json()
    if not data: return jsonify({"error":"No JSON data"}), 400
    valid, err = validate(data)
    if not valid: return jsonify({"error":err}), 400

    try:
        s = make_subject(data)
        planets = get_all_planets(s)
        houses = get_all_houses(s)
        aspects = [fmt_aspect(a) for a in NatalAspects(s).all_aspects]

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
        aspects = [fmt_aspect(a) for a in SynastryAspects(s1, s2).all_aspects]

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

        return jsonify({
            "success": True, "tool": "love_compatibility",
            "person1": {"name":data["person1"].get("name","Person 1"),
                        "sun":p1["sun"]["sign"],"moon":p1["moon"]["sign"],"venus":p1["venus"]["sign"]},
            "person2": {"name":data["person2"].get("name","Person 2"),
                        "sun":p2["sun"]["sign"],"moon":p2["moon"]["sign"],"venus":p2["venus"]["sign"]},
            "scores": {
                "overall": overall,
                "sun_compatibility": sun_score,
                "moon_compatibility": moon_score,
                "venus_compatibility": venus_score,
                "mars_compatibility": mars_score,
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
        return jsonify({
            "success":True, "tool":"sun_sign",
            "name": data.get("name","User"),
            "sun": p,
            "description": f"Your Sun is in {p['sign']} at {p['degree']}° in House {p['house']}.",
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
        return jsonify({
            "success":True, "tool":"moon_sign",
            "name": data.get("name","User"),
            "moon": p,
            "description": f"Your Moon is in {p['sign']} at {p['degree']}° in House {p['house']}.",
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
        return jsonify({
            "success":True, "tool":"rising_sign",
            "name": data.get("name","User"),
            "rising": {
                "sign": sign, "degree": round(h.position,2),
                "element": SIGN_ELEMENT.get(sign,""),
                "quality": SIGN_QUALITY.get(sign,""),
                "ruler": SIGN_RULER.get(sign,""),
            },
            "description": f"Your Rising Sign (Ascendant) is {sign} at {round(h.position,2)}°.",
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
        rising_sign = SIGN_FULL.get(h.sign, h.sign)

        return jsonify({
            "success":True, "tool":"big_three",
            "name": data.get("name","User"),
            "sun": sun,
            "moon": moon,
            "rising": {
                "sign": rising_sign, "degree": round(h.position,2),
                "element": SIGN_ELEMENT.get(rising_sign,""),
                "quality": SIGN_QUALITY.get(rising_sign,""),
                "ruler": SIGN_RULER.get(rising_sign,""),
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
        return jsonify({
            "success":True, "tool":"venus_sign",
            "name": data.get("name","User"),
            "venus": p,
            "description": f"Your Venus is in {p['sign']} at {p['degree']}° in House {p['house']}.",
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
        return jsonify({
            "success":True, "tool":"chiron_sign",
            "name": data.get("name","User"),
            "chiron": p,
            "description": f"Your Chiron (Wounded Healer) is in {p['sign']} at {p['degree']}° in House {p['house']}.",
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
        return jsonify({
            "success":True, "tool":"lilith_sign",
            "name": data.get("name","User"),
            "lilith": p,
            "description": f"Your Black Moon Lilith is in {p['sign']} at {p['degree']}° in House {p['house']}.",
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
        return jsonify({
            "success":True, "tool":"north_node",
            "name": data.get("name","User"),
            "north_node": nn,
            "south_node": sn,
            "description": f"Your North Node is in {nn['sign']} at {nn['degree']}° (House {nn['house']}). South Node is in {sn['sign']}.",
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
            "description": f"Your Part of Fortune is in {pof['sign']} at {pof['degree']}° ({pof['chart_type']} chart formula used).",
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
            "description": f"Your Vertex is in {vtx['sign']} at {vtx['degree']}°. Anti-Vertex is in {anti_sign}.",
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


# ─── Run ──────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
