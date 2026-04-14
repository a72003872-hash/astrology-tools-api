# synastry_interpretations.py — Synastry House Overlays & Aspect Category System
# Professional-level interpretations for synastry analysis

# ═══════════════════════════════════════════════════════════════
# ASPECT CATEGORIZATION SYSTEM
# Categories: Loving, Key, Passion, Emotional, Easy, Conflict, Exact
# ═══════════════════════════════════════════════════════════════

# Define which planet pairs belong to which category
ASPECT_CATEGORIES = {
    "loving": {
        "label": "Loving Aspects",
        "color": "#e91e8c",
        "description": "Deep romantic and affectionate connections",
        "planet_pairs": [
            ("Venus", "Sun"), ("Venus", "Moon"), ("Venus", "Mars"),
            ("Venus", "Venus"), ("Venus", "Jupiter"), ("Venus", "Ascendant"),
            ("Sun", "Moon"),
        ],
    },
    "key": {
        "label": "Key Aspects",
        "color": "#d4a017",
        "description": "Major defining aspects that shape the relationship",
        "planet_pairs": [
            ("Sun", "Sun"), ("Moon", "Moon"), ("Sun", "Saturn"),
            ("Moon", "Saturn"), ("Sun", "Pluto"), ("Moon", "Pluto"),
            ("Venus", "Saturn"), ("Mars", "Saturn"),
            ("Sun", "Ascendant"), ("Moon", "Ascendant"),
        ],
    },
    "passion": {
        "label": "Passion Aspects",
        "color": "#e63946",
        "description": "Sexual chemistry and magnetic attraction",
        "planet_pairs": [
            ("Mars", "Mars"), ("Mars", "Pluto"), ("Venus", "Pluto"),
            ("Mars", "Venus"), ("Mars", "Uranus"), ("Venus", "Uranus"),
            ("Sun", "Mars"), ("Mars", "Ascendant"),
        ],
    },
    "emotional": {
        "label": "Emotional Aspects",
        "color": "#457b9d",
        "description": "Emotional bonds and nurturing connections",
        "planet_pairs": [
            ("Moon", "Venus"), ("Moon", "Mars"), ("Moon", "Jupiter"),
            ("Moon", "Neptune"), ("Moon", "Pluto"), ("Moon", "Uranus"),
            ("Sun", "Neptune"),
        ],
    },
    "easy": {
        "label": "Easy Aspects",
        "color": "#2a9d8f",
        "description": "Natural harmony and flowing energy",
        "aspect_types": ["Trine", "Sextile"],
    },
    "conflict": {
        "label": "Conflict Aspects",
        "color": "#c1121f",
        "description": "Tension that drives growth or creates friction",
        "aspect_types": ["Square", "Opposition"],
    },
}

# Aspect type classifications
HARMONIOUS_ASPECTS = {"Trine", "Sextile", "Conjunction"}
CHALLENGING_ASPECTS = {"Square", "Opposition"}
EXACT_ORB_THRESHOLD = 1.0  # Orb <= 1° is considered exact


def categorize_aspect(aspect):
    """
    Categorize a single aspect into one or more categories.
    Returns list of category keys.
    """
    p1 = aspect["planet1"]
    p2 = aspect["planet2"]
    asp_type = aspect["aspect"]
    orb = abs(aspect["orb"])
    categories = []

    # Check exact first (orb <= 1°)
    if orb <= EXACT_ORB_THRESHOLD:
        categories.append("exact")

    # Check planet-pair categories
    pair = (p1, p2)
    pair_rev = (p2, p1)

    for cat_key, cat_def in ASPECT_CATEGORIES.items():
        if cat_key in ("easy", "conflict"):
            continue  # these are aspect-type based, not planet-pair based
        pairs = cat_def.get("planet_pairs", [])
        if pair in pairs or pair_rev in pairs:
            categories.append(cat_key)

    # Check aspect-type categories (easy/conflict)
    if asp_type in ("Trine", "Sextile"):
        categories.append("easy")
    elif asp_type in ("Square", "Opposition"):
        categories.append("conflict")

    # If no specific category matched, assign based on aspect type
    if not categories:
        if asp_type in ("Trine", "Sextile"):
            categories.append("easy")
        elif asp_type in ("Square", "Opposition"):
            categories.append("conflict")
        elif asp_type == "Conjunction":
            categories.append("key")

    return categories


def categorize_all_aspects(aspects):
    """
    Takes list of aspect dicts, returns categorized structure.
    """
    result = {
        "loving": [],
        "key": [],
        "passion": [],
        "emotional": [],
        "easy": [],
        "conflict": [],
        "exact": [],
    }

    for asp in aspects:
        cats = categorize_aspect(asp)
        for c in cats:
            enriched = dict(asp)
            enriched["categories"] = cats
            result[c].append(enriched)

    # Build summary counts
    summary = {}
    for cat_key, cat_aspects in result.items():
        label = ASPECT_CATEGORIES.get(cat_key, {}).get("label", cat_key.capitalize() + " Aspects")
        color = ASPECT_CATEGORIES.get(cat_key, {}).get("color", "#666")
        desc = ASPECT_CATEGORIES.get(cat_key, {}).get("description", "")
        if cat_key == "exact":
            label = "Exact Aspects"
            color = "#6c3ec1"
            desc = "Aspects with orb ≤ 1° — strongest influence"

        summary[cat_key] = {
            "label": label,
            "color": color,
            "description": desc,
            "count": len(cat_aspects),
        }

    return {
        "categorized_aspects": result,
        "category_summary": summary,
    }


# ═══════════════════════════════════════════════════════════════
# HOUSE OVERLAY INTERPRETATIONS
# Person 1's planets falling in Person 2's houses
# ═══════════════════════════════════════════════════════════════

HOUSE_OVERLAY_INTERPRETATIONS = {
    "Sun": {
        1: "When your Sun falls in your partner's 1st house, you illuminate their sense of self. They feel more confident, more visible, and more alive around you. You naturally validate who they are at their core. This is one of the strongest placements for mutual recognition — they see you as a reflection of who they want to become.",
        2: "Your Sun in their 2nd house energizes their relationship with money, possessions, and self-worth. You may inspire them to earn more, spend differently, or reassess what they truly value. Financial matters and material security become central themes in this connection.",
        3: "Your Sun lights up their 3rd house of communication. Conversations between you feel stimulating and important. You inspire their thinking, writing, and learning. Daily communication flows easily, and you may bond strongly over shared intellectual interests or neighborhood/community activities.",
        4: "Your Sun in their 4th house touches their deepest foundations — home, family, and emotional roots. You feel like home to them on a fundamental level. This placement creates a sense of belonging and ancestral familiarity. Family life together feels natural and destined.",
        5: "This is one of the most romantic house overlays possible. Your Sun in their 5th house ignites joy, playfulness, creativity, and romantic excitement. You bring fun and passion into their life. Children, creative projects, and spontaneous adventures are highlighted themes.",
        6: "Your Sun in their 6th house influences their daily routines, health habits, and work life. You may inspire them to take better care of themselves or restructure how they approach responsibilities. This placement works well for partners who share practical daily life together.",
        7: "Your Sun in their 7th house is a classic partnership indicator. They instinctively see you as partner material — someone who complements and completes their sense of self. This is one of the strongest placements for marriage and committed long-term relationships.",
        8: "Your Sun illuminates their 8th house of transformation, intimacy, and shared resources. This creates an intensely deep, psychologically rich bond. You trigger their desire for emotional and physical depth. Trust, vulnerability, and power dynamics feature prominently.",
        9: "Your Sun in their 9th house expands their world. You inspire their sense of adventure, higher learning, philosophy, and spiritual exploration. Travel together feels meaningful. You challenge their worldview in ways that promote growth and open-mindedness.",
        10: "Your Sun in their 10th house highlights their career and public image. They may see you as someone who elevates their status or professional ambitions. You inspire their goals and may play a significant role in their public life or career direction.",
        11: "Your Sun in their 11th house connects you through friendship, shared ideals, and community involvement. You fit naturally into their social circle and may share a vision for the future. This placement emphasizes intellectual companionship and shared hopes.",
        12: "Your Sun in their 12th house creates a deeply spiritual, karmic connection that operates beneath the surface. They may feel an unexplainable familiarity with you, as if you share a past-life bond. This placement can bring hidden dynamics — both healing and challenging — that require awareness.",
    },
    "Moon": {
        1: "Your Moon in their 1st house means they instinctively sense your emotions and you strongly influence their mood. Emotional transparency is high — you cannot easily hide how you feel around them. This creates immediate emotional intimacy and empathetic connection.",
        2: "Your Moon in their 2nd house creates emotional ties around security and finances. You influence their sense of safety and self-worth on a deep emotional level. Nurturing through material comfort, cooking, and creating a stable home environment feels natural.",
        3: "Your Moon in their 3rd house means your emotional needs and moods naturally enter daily conversations. Communication between you is emotionally charged and intuitive. You understand each other's unspoken feelings through subtle cues and familiar rhythms.",
        4: "This is one of the strongest domestic placements. Your Moon in their 4th house means you feel like family to them — like someone who belongs in their innermost private world. Creating a home together feels deeply satisfying and emotionally necessary for both of you.",
        5: "Your Moon in their 5th house adds emotional warmth to romance, creativity, and fun. Your feelings fuel creative expression between you. This is an affectionate, playful placement that makes the relationship feel emotionally nourishing and romantically alive.",
        6: "Your Moon in their 6th house connects your emotions to their daily life structure. You may naturally take care of their health and routines, or your emotional needs become woven into the practical fabric of their everyday existence.",
        7: "Your Moon in their 7th house is a powerful marriage indicator. They emotionally need partnership with you — you satisfy a deep relational hunger. Emotional commitment feels instinctive rather than calculated. This placement fosters long-term bonding.",
        8: "Your Moon in their 8th house creates an emotionally intense, transformative bond. Deep psychological intimacy, shared vulnerability, and emotional power dynamics are themes. You access parts of each other that no one else can reach — for better or worse.",
        9: "Your Moon in their 9th house means your emotions inspire their spiritual and philosophical growth. You feel emotionally safe exploring big life questions together. Travel, education, and cultural exploration carry emotional significance in this partnership.",
        10: "Your Moon in their 10th house means your emotional presence directly impacts their career and public standing. You may play a supportive nurturing role in their professional life, or your emotional bond is visible and acknowledged publicly.",
        11: "Your Moon in their 11th house connects your emotional world to their friendships and future vision. You nurture their social connections and shared dreams. Emotional belonging within a community or friend group becomes meaningful.",
        12: "Your Moon in their 12th house creates one of the most psychically connected placements. You sense each other's emotions across distance. Dreams, intuition, and unspoken understanding define this bond. There may be a karmic quality — a feeling of having known each other before.",
    },
    "Mercury": {
        1: "Your Mercury in their 1st house means your ideas and communication style strongly influence how they see themselves. Conversations with you shape their self-perception. They find your mind stimulating and may adopt your way of thinking.",
        2: "Your Mercury in their 2nd house connects your ideas to their finances and values. You may influence their financial decisions through advice, planning, or shared economic conversations. Discussions about money and worth are central themes.",
        3: "This is a natural placement for Mercury — your communication styles mesh effortlessly. Conversations are lively, frequent, and mutually stimulating. You likely text constantly, finish each other's sentences, and share a love of learning.",
        4: "Your Mercury in their 4th house means your words and ideas penetrate their emotional foundations. Family conversations, home planning, and discussions about roots and heritage carry special weight between you.",
        5: "Your Mercury in their 5th house adds wit and intellectual play to romance. Flirty banter, creative conversations, and mental games keep the relationship exciting. Communication style is lighthearted, warm, and creatively inspired.",
        6: "Your Mercury in their 6th house is practical and productive. Conversations about work, health, routines, and problem-solving flow easily. You help them organize their thinking and approach daily life more efficiently.",
        7: "Your Mercury in their 7th house makes communication a cornerstone of partnership. They see your mind as complementary to theirs. Negotiation, discussion, and mutual decision-making define how you function together as a team.",
        8: "Your Mercury in their 8th house brings deep, probing conversations about psychology, secrets, finances, and taboo subjects. You draw out their hidden thoughts. Communication is intimate, sometimes uncomfortably honest, and transformative.",
        9: "Your Mercury in their 9th house stimulates philosophical and spiritual discussion. You expand their thinking, challenge their beliefs, and inspire intellectual growth. Conversations about meaning, travel, and education are highlighted.",
        10: "Your Mercury in their 10th house means your ideas influence their career and public reputation. You may offer valuable professional advice, or your communication style directly supports their ambitions and public image.",
        11: "Your Mercury in their 11th house connects your mind to their social network and future vision. You share ideas about community, technology, progress, and humanitarian goals. Friendship and intellectual companionship are strong.",
        12: "Your Mercury in their 12th house means your words reach their subconscious. Communication may happen on an intuitive level — you understand what they mean before they finish speaking. Conversations about dreams, spirituality, and hidden matters are significant.",
    },
    "Venus": {
        1: "Your Venus in their 1st house means they find you attractive on a fundamental level — your presence feels pleasing, harmonious, and aesthetically appealing. Physical attraction is strong and immediate. You make them feel beautiful by association.",
        2: "Your Venus in their 2nd house creates a deep link between love and material security. You enhance their sense of self-worth and may bring financial harmony or shared luxurious experiences. Gift-giving and sensual comfort are natural expressions of affection.",
        3: "Your Venus in their 3rd house adds charm and sweetness to daily communication. Love is expressed through words — compliments, love notes, sweet texts, and affectionate conversation. You enjoy sharing ideas and learning together in a harmonious way.",
        4: "Your Venus in their 4th house creates a beautiful domestic bond. Home life together feels warm, harmonious, and aesthetically pleasing. You bring beauty and love into their most private spaces. Family life together is genuinely nourishing.",
        5: "This is one of the best placements for romantic love. Your Venus in their 5th house creates magical romantic chemistry — dates feel special, creative collaboration sparkles, and the joy you share is effortless. True romance thrives here.",
        6: "Your Venus in their 6th house means love is expressed through acts of service. You help make their daily life more pleasant, organized, and beautiful. Health routines done together, workplace harmony, and practical affection define this placement.",
        7: "Your Venus in their 7th house is a textbook partnership indicator. They see you as their ideal partner — someone who brings beauty, balance, and harmony to their life. This is one of the strongest marriage placements in synastry.",
        8: "Your Venus in their 8th house creates an intensely passionate, transformative love bond. Attraction runs deep — beyond the surface into psychological and sexual territory. Shared finances, inheritances, and emotional vulnerability are intertwined with love.",
        9: "Your Venus in their 9th house means love expands through shared adventures, philosophical discussions, and spiritual exploration. Traveling together deepens your bond. You may come from different cultural backgrounds that enrich the relationship.",
        10: "Your Venus in their 10th house means your love supports and enhances their career and public image. You may be seen as a power couple. Their professional life benefits from your presence, charm, and social connections.",
        11: "Your Venus in their 11th house creates a love that is rooted in friendship and shared ideals. You genuinely like each other as people, not just as lovers. Social activities, group involvement, and future planning together feel harmonious.",
        12: "Your Venus in their 12th house creates a secret, spiritual, deeply karmic love connection. The bond operates beneath the surface — others may not understand its depth. There is a past-life quality to this love. Privacy and spiritual intimacy are strong themes.",
    },
    "Mars": {
        1: "Your Mars in their 1st house creates immediate physical attraction and energy. You activate their assertiveness, confidence, and physicality. The chemistry is electric but can also trigger irritation or competition if not channeled well.",
        2: "Your Mars in their 2nd house energizes their earning power and financial drive. You motivate them to pursue material goals more aggressively. Conflicts about money or possessions are possible, but so is productive financial teamwork.",
        3: "Your Mars in their 3rd house adds intensity and sometimes sharp edge to communication. Debates are stimulating but can become heated. You push them to speak up, assert their ideas, and engage in more direct communication.",
        4: "Your Mars in their 4th house stirs up their emotional foundations. Home life can be passionate or volatile — often both. You activate their deepest emotions, family patterns, and domestic energy for better or worse.",
        5: "Your Mars in their 5th house creates strong sexual attraction and passionate romance. Creative projects together have intense energy. This placement fuels excitement, adventure, and competitive playfulness in the relationship.",
        6: "Your Mars in their 6th house energizes their work ethic and daily routines. You motivate them to exercise, work harder, and improve their health habits. Potential for workplace tension but also productive partnership in practical matters.",
        7: "Your Mars in their 7th house creates a magnetically attractive but potentially combative partnership dynamic. They see you as a strong, assertive partner. Arguments are likely but so is passionate makeup energy. Active, dynamic partnership.",
        8: "Your Mars in their 8th house is one of the most sexually intense placements. Power dynamics, jealousy, passion, and deep psychological transformation run through this connection. The attraction is compulsive and transformative.",
        9: "Your Mars in their 9th house motivates their adventurous and philosophical side. You push them to take risks, travel boldly, and fight for their beliefs. Spirited debates about religion, politics, and life philosophy are common.",
        10: "Your Mars in their 10th house drives their career ambitions. You may be a powerful motivator or competitor in their professional life. Public conflicts or dynamic professional collaboration are possible themes.",
        11: "Your Mars in their 11th house energizes their social life and future goals. You push them to take action on their ideals and can be a dynamic force within their friend group. Potential for social activism together.",
        12: "Your Mars in their 12th house activates their subconscious drives and hidden desires. Passion operates beneath the surface — private, secret, and deeply instinctive. This placement can bring suppressed anger to light for healing.",
    },
    "Jupiter": {
        1: "Your Jupiter in their 1st house makes them feel expansive, lucky, and optimistic around you. You boost their confidence and encourage them to aim higher. Your presence feels generous, warm, and growth-oriented.",
        2: "Your Jupiter in their 2nd house can bring financial luck and abundance. You expand their earning potential and may encourage more generous spending or bigger financial vision. Material growth through the relationship is highlighted.",
        3: "Your Jupiter in their 3rd house broadens their communication, learning, and intellectual horizons. Conversations with you feel expansive and enlightening. Education, writing, and media projects benefit from your influence.",
        4: "Your Jupiter in their 4th house brings abundance and expansion to home and family life. Living together feels blessed — the home environment grows warmer, more generous, and more culturally enriched through your presence.",
        5: "Your Jupiter in their 5th house amplifies romantic joy, creative inspiration, and fun. Dates feel like celebrations. This placement is excellent for having children together and for any creative partnership. Joy multiplies.",
        6: "Your Jupiter in their 6th house improves their daily life, work conditions, and health outlook. You bring optimism to their routine and may help them find better work opportunities or healthier lifestyle patterns.",
        7: "Your Jupiter in their 7th house is a highly favorable partnership indicator. They see you as someone who brings growth, wisdom, and luck into their partnership life. Marriage is blessed and expansive under this influence.",
        8: "Your Jupiter in their 8th house can bring financial benefit through shared resources, inheritance, or joint investments. Emotional and sexual intimacy is deepened with a sense of meaning and trust. Transformative growth occurs together.",
        9: "This is Jupiter's natural house. Your Jupiter here expands their worldview, spiritual understanding, and love of travel in the most profound way. You feel like a teacher, guide, or fellow adventurer in the journey of life.",
        10: "Your Jupiter in their 10th house brings professional luck and career expansion. Your presence supports their ambitions and public reputation. They may achieve more with you than without you in their professional life.",
        11: "Your Jupiter in their 11th house expands their social circle, friend network, and future aspirations. Through you, they meet new people, join new groups, and dream bigger. This placement fosters humanitarian connection.",
        12: "Your Jupiter in their 12th house brings spiritual expansion and karmic blessings. You act as a guardian angel figure — offering protection, healing, and spiritual insight. Meditation, retreat, and inner growth are enhanced together.",
    },
    "Saturn": {
        1: "Your Saturn in their 1st house creates a serious, potentially restricting influence on their identity. They may feel judged or pressured to mature around you. This placement builds lasting structure but can initially feel heavy or intimidating.",
        2: "Your Saturn in their 2nd house brings financial discipline and reality checks about self-worth. You may help them budget better but could also trigger insecurities about money and personal value. Long-term financial stability is the goal.",
        3: "Your Saturn in their 3rd house adds structure and seriousness to communication. Conversations carry weight. You may help them think more carefully but can also make them self-conscious about expressing ideas freely.",
        4: "Your Saturn in their 4th house touches their emotional foundations with lessons about responsibility, family duty, and emotional maturity. Home life together requires conscious effort but builds genuine, lasting security over time.",
        5: "Your Saturn in their 5th house can initially dampen spontaneity and romantic expression. Fun feels earned rather than free. However, over time, this placement builds deeply committed, enduring romantic bonds and structured creative expression.",
        6: "Your Saturn in their 6th house brings discipline to their daily life and work habits. You help them structure routines and take responsibilities seriously. Health improvements may come through sustained effort and accountability.",
        7: "Your Saturn in their 7th house is a powerful commitment indicator — but it requires work. They feel a strong sense of obligation and karmic duty in the partnership. Marriage under this influence is meant to teach and endure.",
        8: "Your Saturn in their 8th house brings lessons about trust, control, and shared power. Intimacy requires earning through patience and consistent reliability. Financial dealings together need careful management and transparency.",
        9: "Your Saturn in their 9th house structures their philosophical and spiritual development. You challenge their beliefs with practical reality. Travel and education may have restrictions but carry more purposeful, lasting impact.",
        10: "Your Saturn in their 10th house significantly impacts their career with lessons about ambition, authority, and professional maturity. You may serve as mentor or critic. Career achievements earned together are substantial and lasting.",
        11: "Your Saturn in their 11th house brings structure to their friendships and future plans. You help them set realistic goals and may limit their social spontaneity in favor of more purposeful connections and long-term vision.",
        12: "Your Saturn in their 12th house activates deep karmic lessons around hidden fears and spiritual growth. Past-life dynamics are strong — you may trigger their deepest anxieties but also offer the structure needed to heal them.",
    },
    "Uranus": {
        1: "Your Uranus in their 1st house electrifies their self-expression. Around you, they feel liberated, unconventional, and excitingly unpredictable. The relationship breaks their usual patterns and accelerates personal evolution.",
        2: "Your Uranus in their 2nd house disrupts their financial patterns and value system. Income may become unpredictable but also innovative. You challenge what they consider valuable and worth holding onto.",
        3: "Your Uranus in their 3rd house revolutionizes their thinking and communication. Conversations are unpredictable, brilliant, and sometimes shocking. You introduce entirely new perspectives and ideas into their mental world.",
        4: "Your Uranus in their 4th house disrupts their home life and family patterns. Living together may be unconventional. You break generational patterns and introduce freedom into their most private, domestic spaces.",
        5: "Your Uranus in their 5th house makes romance exciting and unpredictable. Creative projects together are innovative and unconventional. The love affair has a thrilling, electric quality that resists routine.",
        6: "Your Uranus in their 6th house changes their daily routines and work patterns. You introduce technological innovation, flexible schedules, and unconventional health approaches into their everyday existence.",
        7: "Your Uranus in their 7th house creates an exciting but unpredictable partnership. The relationship itself may be unconventional — long-distance, open, or simply unlike what either person expected. Freedom within commitment is the lesson.",
        8: "Your Uranus in their 8th house triggers sudden transformations in intimacy and shared resources. The psychological bond is electric and sometimes unsettling. Breakthroughs in trust and vulnerability come suddenly and unexpectedly.",
        9: "Your Uranus in their 9th house radically expands their worldview. You introduce revolutionary ideas about philosophy, spirituality, and life meaning. Travel together is spontaneous and perspective-shifting.",
        10: "Your Uranus in their 10th house disrupts their career trajectory — potentially for the better. You inspire career changes, unconventional professional paths, and innovative public roles. Status quo is not an option.",
        11: "Your Uranus in their 11th house supercharges their social life and future vision. Through you, they connect with progressive communities, activist movements, and technology-forward groups. Shared ideals are unconventional but inspiring.",
        12: "Your Uranus in their 12th house awakens hidden parts of their psyche. Sudden spiritual insights, dream revelations, and subconscious breakthroughs occur through the relationship. The connection operates on a higher frequency.",
    },
    "Neptune": {
        1: "Your Neptune in their 1st house creates an almost dreamy, idealized perception. They may see you through rose-colored glasses. The connection feels spiritual, artistic, and mystical — but requires grounding to avoid disillusionment.",
        2: "Your Neptune in their 2nd house can create confusion around money and values in the relationship. Financial boundaries may blur. However, you can also inspire them to value spiritual wealth over material accumulation.",
        3: "Your Neptune in their 3rd house adds poetry, imagination, and sometimes confusion to communication. Conversations drift into creative, spiritual, or fantasy territory. Misunderstandings are possible but so is profound intuitive understanding.",
        4: "Your Neptune in their 4th house creates an ethereal, dreamlike quality to home life. The domestic environment may have artistic or spiritual character. Family boundaries may blur — unconditional love and sacrifice are strong themes.",
        5: "Your Neptune in their 5th house creates a romantic fairy tale quality. Romance feels magical, idealized, and creatively inspired. Art, music, and imaginative play together flourish. Guard against seeing only what you want to see.",
        6: "Your Neptune in their 6th house can create confusion in daily routines or health matters. You may inspire more compassionate work or healing practices but can also blur practical boundaries that need clarity.",
        7: "Your Neptune in their 7th house creates an idealized partnership vision. They may project qualities onto you that are partly imaginary. The spiritual bond is genuine but requires honest communication to stay grounded in reality.",
        8: "Your Neptune in their 8th house creates profoundly mystical intimacy. The emotional and physical bond transcends ordinary experience. Psychic connection and spiritual transformation through vulnerability are highlighted — powerful but potentially confusing.",
        9: "Your Neptune in their 9th house inspires spiritual seeking, mystical experiences, and transcendent travel. You expand their consciousness beyond material reality. Shared meditation, pilgrimage, or spiritual study deepens the bond immeasurably.",
        10: "Your Neptune in their 10th house adds a dreamy, artistic quality to their career and public image. You may inspire them toward creative or healing professions. Public perception of the relationship may differ from private reality.",
        11: "Your Neptune in their 11th house idealized shared dreams and social vision. You inspire humanitarian compassion and artistic community involvement. However, shared goals may need reality checks to ensure they are achievable.",
        12: "Your Neptune in their 12th house creates one of the most spiritually profound connections possible. Past-life recognition is intense. The psychic bond operates beyond words. Healing, artistic creation, and spiritual dissolution of ego are major themes.",
    },
    "Pluto": {
        1: "Your Pluto in their 1st house creates an intense, transformative impact on their sense of self. They may feel both fascinated and intimidated by you. You trigger deep personal evolution — their identity will not be the same after knowing you.",
        2: "Your Pluto in their 2nd house transforms their relationship with money, possessions, and self-worth. Power dynamics around finances are likely. You challenge their deepest values and force reassessment of what truly matters.",
        3: "Your Pluto in their 3rd house intensifies communication. Conversations go deep — past small talk into psychology, secrets, and transformative truths. You change how they think and speak. Words carry enormous power between you.",
        4: "Your Pluto in their 4th house reaches into the deepest emotional foundations. Family patterns, childhood wounds, and ancestral dynamics surface through the relationship. The home together is a place of profound emotional transformation.",
        5: "Your Pluto in their 5th house creates obsessively passionate romance. Creative expression together has a cathartic, transformative quality. Love feels like a force of nature — consuming, powerful, and impossible to ignore.",
        6: "Your Pluto in their 6th house transforms their daily habits, health practices, and work life. You push them to eliminate unhealthy patterns and rebuild routines from the ground up. The transformation is practical and lasting.",
        7: "Your Pluto in their 7th house creates an intensely powerful partnership dynamic. Power struggles, control issues, and deep psychological mirroring define the relationship. The bond transforms both people fundamentally — separation is difficult.",
        8: "This is Pluto's natural house. Your Pluto here creates the deepest possible psychological and sexual bond. Trust is earned through fire. Secrets, shared resources, and emotional vulnerability reach extreme depths. Life-changing transformation is guaranteed.",
        9: "Your Pluto in their 9th house transforms their worldview, beliefs, and philosophical framework. You challenge their assumptions about meaning, truth, and morality at a fundamental level. Travel together catalyzes deep personal evolution.",
        10: "Your Pluto in their 10th house powerfully impacts their career and public reputation. You may enable dramatic career transformation or trigger power struggles around status and authority. The influence on their life direction is profound.",
        11: "Your Pluto in their 11th house transforms their social circle and future vision. Friendships shift, group affiliations change, and shared goals carry intense psychological weight. Together you may pursue powerful social or activist causes.",
        12: "Your Pluto in their 12th house creates the deepest karmic, psychological bond. Subconscious material surfaces for healing — past lives, ancestral trauma, hidden fears. The relationship operates in the invisible realm and transforms both people at a soul level.",
    },
}


def calculate_house_overlays(p1_planets, p2_houses):
    """
    Calculate which of Person 1's planets fall in which of Person 2's houses.
    Returns list of overlay dicts with interpretations.

    p1_planets: dict of planet data (from get_all_planets)
    p2_houses: list of house dicts (from get_all_houses)
    """
    overlays = []

    # Build house boundaries from Person 2's houses
    house_cusps = []
    for h in p2_houses:
        signs_list = [
            "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
            "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
        ]
        sign_idx = signs_list.index(h["sign"]) if h["sign"] in signs_list else 0
        abs_pos = sign_idx * 30 + h["degree"]
        house_cusps.append(abs_pos)

    def find_house(abs_deg):
        """Find which house a given absolute degree falls in."""
        for i in range(12):
            start = house_cusps[i]
            end = house_cusps[(i + 1) % 12]
            if end < start:
                # Wraps around 360°
                if abs_deg >= start or abs_deg < end:
                    return i + 1
            else:
                if start <= abs_deg < end:
                    return i + 1
        return 1  # fallback

    planet_order = ["sun", "moon", "mercury", "venus", "mars",
                    "jupiter", "saturn", "uranus", "neptune", "pluto"]

    for pkey in planet_order:
        if pkey not in p1_planets:
            continue
        planet = p1_planets[pkey]
        abs_deg = planet.get("abs_degree", 0)
        house_num = find_house(abs_deg)
        planet_name = planet["name"]

        interp_text = HOUSE_OVERLAY_INTERPRETATIONS.get(planet_name, {}).get(house_num, "")

        overlays.append({
            "planet": planet_name,
            "planet_sign": planet["sign"],
            "planet_degree": planet["degree"],
            "in_house": house_num,
            "interpretation": interp_text,
        })

    return overlays
