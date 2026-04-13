# interpretations.py — Professional Astrology Interpretations
# Each sign has: personality, strengths, challenges, love style (where relevant)
# Written at professional astrologer level — no generic filler

# ═══════════════════════════════════════════════════════════════
# SUN SIGN INTERPRETATIONS
# ═══════════════════════════════════════════════════════════════

SUN_INTERPRETATIONS = {
    "Aries": {
        "title": "Sun in Aries — The Trailblazer",
        "personality": "You lead with instinct, not permission. Aries Sun individuals possess an unmistakable urgency — a need to act, to initiate, to be first. You process the world through direct experience rather than observation, which makes you bold but occasionally reckless. Your identity is built around courage and self-determination. You feel most alive when you are starting something new, competing, or standing up for yourself and others.",
        "strengths": "Natural leadership ability, physical vitality, decisiveness under pressure, honesty that cuts through pretense, ability to recover quickly from setbacks and bounce back stronger than before.",
        "challenges": "Impatience with slow-moving situations, tendency to start projects without finishing them, difficulty sitting with uncomfortable emotions instead of pushing through them, conflict avoidance through aggression rather than vulnerability.",
        "love_style": "In relationships, you pursue what you want directly and lose interest when the chase disappears. You need a partner who maintains their own independence and does not become predictable. Passion is non-negotiable for you — comfort alone is not enough.",
        "element_insight": "As a Fire sign with Cardinal modality, you are an igniter. You start movements, conversations, and conflicts with equal energy. Your ruling planet Mars gives you a competitive edge that is best channeled into physical activity and purposeful goals."
    },
    "Taurus": {
        "title": "Sun in Taurus — The Builder",
        "personality": "Stability is not your preference — it is your survival mechanism. Taurus Sun individuals build their lives brick by brick, valuing permanence over excitement. You experience the world through your senses more than most: touch, taste, sound, and beauty matter to you on a visceral level. Your identity is rooted in what you can create, accumulate, and sustain over time.",
        "strengths": "Remarkable patience and persistence, natural financial instinct, ability to create beauty and comfort in any environment, loyalty that does not waver under pressure, physical endurance that outlasts most people around you.",
        "challenges": "Resistance to change even when change is overdue, possessiveness in relationships and with material things, tendency to equate self-worth with net worth, stubbornness that can calcify into rigidity when you feel threatened.",
        "love_style": "You approach love with the same steadiness you bring to everything else — slowly, deliberately, and with full commitment once you decide someone is worth it. You express affection through physical closeness, acts of service, and financial generosity rather than dramatic declarations.",
        "element_insight": "As a Fixed Earth sign, you are the zodiac's anchor. Ruled by Venus, you have an innate understanding of value — what is worth keeping, what is worth building, and what is worth waiting for. Your greatest asset is endurance; your greatest risk is stagnation."
    },
    "Gemini": {
        "title": "Sun in Gemini — The Connector",
        "personality": "Your mind never sits still, and neither do you. Gemini Sun individuals are driven by curiosity — not the shallow kind, but the restless need to understand how things connect. You collect information, perspectives, and experiences the way others collect objects. Your identity is tied to your ability to communicate, translate, and move between different worlds with ease.",
        "strengths": "Exceptional verbal and written communication, ability to see multiple sides of any issue simultaneously, social adaptability that allows you to connect with almost anyone, quick learning speed, mental agility that keeps you relevant in changing environments.",
        "challenges": "Difficulty committing to a single path when all paths look interesting, nervous energy that manifests as anxiety when understimulated, tendency to intellectualize emotions rather than feeling them, scattered focus that can undermine deep expertise.",
        "love_style": "You need a partner who can hold a conversation that surprises you. Mental stimulation is your primary love language — without it, physical chemistry alone will not sustain your interest. You tend to keep things light early on and may struggle with emotional depth until you feel intellectually safe.",
        "element_insight": "As a Mutable Air sign ruled by Mercury, you are the zodiac's messenger. Your gift is translation — turning complex ideas into accessible language. Your challenge is depth. Breadth comes naturally; sustained focus requires conscious effort."
    },
    "Cancer": {
        "title": "Sun in Cancer — The Protector",
        "personality": "You feel everything — and you remember everything you feel. Cancer Sun individuals navigate life through emotional memory, building a rich inner world that few people are ever fully invited into. Your identity is wrapped around the people and places you call home. Protection is your default response to love: you guard the people you care about with a ferocity that surprises those who only see your gentle exterior.",
        "strengths": "Deep emotional intelligence that reads situations others miss entirely, fierce loyalty to family and close friends, ability to create safe spaces where people open up naturally, strong intuition that functions like a sixth sense, nurturing instinct that builds lasting bonds.",
        "challenges": "Difficulty letting go of past hurts, tendency to absorb other people's emotions as your own, moodiness that shifts without obvious external triggers, passive-aggressive communication when you feel unsafe expressing needs directly.",
        "love_style": "Security is the foundation of every relationship you build. You need to feel emotionally safe before you can relax into love. Once committed, you are deeply attentive to your partner's needs — sometimes to the point of neglecting your own. You remember every anniversary, every meaningful conversation, every wound.",
        "element_insight": "As a Cardinal Water sign ruled by the Moon, your emotional tides shift constantly, but your core direction remains fixed on home, family, and emotional belonging. Your mood is often linked to lunar cycles more literally than you might expect."
    },
    "Leo": {
        "title": "Sun in Leo — The Performer",
        "personality": "You were built to be seen, and you know it. Leo Sun individuals carry a warmth that draws people in — not because you demand attention, but because your genuine self-expression creates a gravitational pull. Your identity is tied to creative output, recognition, and the ability to inspire others through your presence. Generosity comes naturally to you because abundance feels like your default state.",
        "strengths": "Magnetic personal presence that inspires loyalty in others, creative confidence that takes risks most people avoid, genuine warmth and generosity that builds strong social networks, ability to lead through inspiration rather than authority, resilience rooted in unshakeable self-belief.",
        "challenges": "Sensitivity to criticism that feels disproportionate to the offense, need for external validation that can become dependency, difficulty sharing the spotlight or acknowledging when someone else deserves center stage, pride that prevents asking for help.",
        "love_style": "Love is your stage, and you perform it wholeheartedly. You are affectionate, demonstrative, and loyal — but you need to feel admired. A partner who takes you for granted will lose you faster than one who openly adores you. Romance is not a phase for you; it is a lifestyle.",
        "element_insight": "As a Fixed Fire sign ruled by the Sun itself, you embody sustained creative energy. Unlike Aries' spark or Sagittarius' blaze, your fire burns steadily. Your challenge is ensuring your light illuminates others rather than casting them in shadow."
    },
    "Virgo": {
        "title": "Sun in Virgo — The Analyst",
        "personality": "You notice what everyone else overlooks. Virgo Sun individuals process the world through careful observation, pattern recognition, and an almost compulsive drive to improve whatever they touch. Your identity is shaped by usefulness — you feel most yourself when your skills are solving real problems for real people. Perfectionism is not your goal; competence is.",
        "strengths": "Exceptional analytical ability and attention to detail, practical problem-solving that produces tangible results, work ethic that consistently outperforms expectations, ability to create order from chaos, genuine desire to be helpful without needing credit.",
        "challenges": "Self-criticism that sets impossible internal standards, difficulty accepting good enough when perfect is theoretically possible, anxiety driven by awareness of everything that could go wrong, tendency to over-explain or over-prepare when simplicity would serve better.",
        "love_style": "You show love through actions, not words. Fixing your partner's computer, remembering their medication schedule, organizing their workspace — these are your love letters. You need a partner who recognizes service as affection and does not mistake your practical nature for emotional coldness.",
        "element_insight": "As a Mutable Earth sign ruled by Mercury, you combine intellectual precision with practical application. You are the editor of the zodiac — not the one who writes the first draft, but the one who makes it publishable. Your value lies in refinement."
    },
    "Libra": {
        "title": "Sun in Libra — The Diplomat",
        "personality": "Harmony is not something you prefer — it is something you need. Libra Sun individuals are wired for balance, fairness, and aesthetic coherence. You process decisions through the lens of relationships: how will this affect the people involved? Your identity is shaped by your ability to create equilibrium in environments that tend toward conflict.",
        "strengths": "Natural diplomatic skill that resolves tension without creating winners and losers, refined aesthetic sense that elevates environments and experiences, ability to consider perspectives that others dismiss, charm that opens doors intellectual merit alone cannot, partnership instinct that builds alliances.",
        "challenges": "Indecisiveness that stalls momentum when you see merit on every side, people-pleasing that erodes your own boundaries, conflict avoidance that allows resentment to accumulate silently, difficulty forming opinions that might displease someone important to you.",
        "love_style": "Partnership is where you come alive. You are at your best in committed relationships and genuinely struggle with long periods of solitude. You seek a partner who is your intellectual and social equal — someone who looks good beside you and challenges you to grow simultaneously.",
        "element_insight": "As a Cardinal Air sign ruled by Venus, you initiate through connection. Your approach to new situations is inherently social — you assess the people before you assess the environment. Beauty and justice are intertwined in your worldview."
    },
    "Scorpio": {
        "title": "Sun in Scorpio — The Investigator",
        "personality": "Surface-level anything bores you to the point of hostility. Scorpio Sun individuals are driven by the need to understand what lies beneath — beneath appearances, beneath polite conversation, beneath the stories people tell themselves. Your identity is forged through transformation: you have survived things that would have broken others, and that survival defines how you move through the world.",
        "strengths": "Psychological depth that perceives hidden motivations and power dynamics, emotional resilience built through genuine hardship, laser focus that accomplishes what scattered effort cannot, loyalty that is absolute once earned, ability to transform pain into power.",
        "challenges": "Difficulty trusting even after someone has proven themselves, tendency to control situations and people as a defense mechanism, grudge-holding that keeps old wounds open, all-or-nothing thinking that eliminates middle ground in relationships and decisions.",
        "love_style": "You love with your entire being or not at all. Surface romance bores you — you want to merge, to know and be known at the deepest possible level. This intensity is magnetic to some and terrifying to others. Betrayal is the one thing you struggle to forgive.",
        "element_insight": "As a Fixed Water sign ruled by Pluto, you embody concentrated emotional power. You are the zodiac's alchemist — capable of turning destruction into creation, loss into wisdom, pain into strength. Your greatest transformation is always internal."
    },
    "Sagittarius": {
        "title": "Sun in Sagittarius — The Explorer",
        "personality": "Confinement of any kind triggers your escape instinct. Sagittarius Sun individuals are driven by expansion — intellectual, geographic, philosophical, and experiential. You process life as an ongoing adventure rather than a problem to solve. Your identity is built around the pursuit of meaning, truth, and direct experience of cultures, ideas, and landscapes beyond your starting point.",
        "strengths": "Infectious optimism that lifts the morale of everyone around you, natural philosophical intelligence that finds patterns across disciplines, honesty that people trust even when it stings, adventurous spirit that creates memorable experiences, ability to bounce back from failure by reframing it as education.",
        "challenges": "Commitment phobia triggered by anything that feels like a cage, bluntness that wounds when diplomacy was needed, tendency to overpromise and underdeliver because enthusiasm outpaces follow-through, restlessness that prevents deep expertise in any single area.",
        "love_style": "You need a travel partner, not a jailer. The fastest way to lose you is to make a relationship feel like an obligation. You thrive with someone who has their own adventures, their own passions, and their own reasons to come home — so that choosing each other every day feels like freedom, not duty.",
        "element_insight": "As a Mutable Fire sign ruled by Jupiter, you carry the energy of expansion and philosophical growth. Your fire is the bonfire at the campsite — social, warm, and illuminating. It spreads rather than concentrates."
    },
    "Capricorn": {
        "title": "Sun in Capricorn — The Architect",
        "personality": "You play long games. Capricorn Sun individuals operate with a timeline that most people cannot perceive — you are building structures (career, reputation, financial security, legacy) that are designed to outlast you. Your identity is shaped by achievement, but not the flashy kind. You value competence, discipline, and the quiet authority that comes from doing the work nobody else was willing to do.",
        "strengths": "Strategic thinking that plans three moves ahead, discipline that executes when motivation has evaporated, natural authority that earns respect without demanding it, financial intelligence that compounds over decades, dry humor that reveals sharp observation.",
        "challenges": "Workaholism that sacrifices relationships and health for professional achievement, emotional suppression masked as stoicism, difficulty asking for help because self-reliance became survival strategy early in life, pessimism that anticipates failure to avoid disappointment.",
        "love_style": "You take relationships as seriously as you take everything else — which means slowly, cautiously, and with a long-term view. You are unlikely to commit until you are certain, but once committed, you are remarkably dependable. You show love through providing, protecting, and building a stable life together.",
        "element_insight": "As a Cardinal Earth sign ruled by Saturn, you initiate through structure. You are the zodiac's CEO — not because you chase titles, but because you instinctively understand hierarchy, systems, and the patience required to build something that lasts."
    },
    "Aquarius": {
        "title": "Sun in Aquarius — The Visionary",
        "personality": "Conformity is not rebellion for you — it is suffocation. Aquarius Sun individuals define themselves through their difference from the group, even when they are deeply invested in the group's welfare. You process the world through systems and patterns rather than individual narratives. Your identity is tied to innovation, intellectual independence, and the conviction that the future can be deliberately designed.",
        "strengths": "Original thinking that solves problems others have accepted as permanent, ability to maintain objectivity in emotional situations, genuine commitment to fairness and equal treatment, capacity to see the bigger picture when others are trapped in details, comfort with being the outsider.",
        "challenges": "Emotional detachment that frustrates people who need warmth and vulnerability, contrarianism that opposes ideas simply because they are popular, difficulty with intimacy that requires dropping the intellectual shield, stubbornness disguised as principle.",
        "love_style": "You need intellectual respect before emotional closeness. Friendship is the foundation of every romantic relationship you sustain — you cannot love someone you would not choose as a friend first. You struggle with traditional relationship structures and function best with a partner who respects your need for autonomy.",
        "element_insight": "As a Fixed Air sign ruled by Uranus, you sustain ideas rather than initiate them. You are the zodiac's architect of the future — less interested in what has been done than in what has never been tried. Your fixedness gives your radical ideas staying power."
    },
    "Pisces": {
        "title": "Sun in Pisces — The Mystic",
        "personality": "The boundary between you and the world is thinner than it is for most people. Pisces Sun individuals absorb the emotions, energies, and atmospheres of their surroundings in ways that are both a gift and a burden. Your identity is fluid — you shape-shift across contexts, which makes you deeply empathetic but sometimes uncertain about who you are when you are alone.",
        "strengths": "Profound empathy that connects with people across every demographic, creative and artistic talent that channels unconscious material into art, spiritual sensitivity that perceives what logic cannot measure, ability to forgive in ways that heal rather than enable, adaptability that survives what rigidity cannot.",
        "challenges": "Difficulty maintaining boundaries between your emotions and other people's, escapist tendencies (through fantasy, substances, sleep, or avoidance) when reality becomes too abrasive, martyr complex that sacrifices your needs to avoid conflict, confusion about personal identity versus absorbed identity.",
        "love_style": "You love without reservation and sometimes without protection. Romance is spiritual for you — you seek a soul connection, not a practical partnership. You idealize partners early and can struggle when the real person emerges from beneath the projection. Your greatest relationship skill is unconditional acceptance.",
        "element_insight": "As a Mutable Water sign ruled by Neptune, you are the zodiac's channel — receiving impressions from the collective unconscious and translating them into art, compassion, or spiritual insight. Your mutability makes you adaptive; your water element makes you permeable."
    }
}

# ═══════════════════════════════════════════════════════════════
# MOON SIGN INTERPRETATIONS
# ═══════════════════════════════════════════════════════════════

MOON_INTERPRETATIONS = {
    "Aries": {
        "title": "Moon in Aries — Emotional Warrior",
        "emotional_nature": "Your emotional reactions are immediate, intense, and short-lived. You process feelings by taking action — sitting with discomfort is almost physically painful for you. Anger arrives first and clears quickly, like a summer storm. You need independence even in your closest relationships.",
        "needs": "You need freedom to express emotions without censorship, physical outlets for emotional energy, problems you can solve through direct action, and a partner who does not take your flare-ups personally.",
        "shadow": "Emotional impatience, tendency to bulldoze through other people's feelings, difficulty with vulnerability, using anger to avoid sadness or fear."
    },
    "Taurus": {
        "title": "Moon in Taurus — Emotional Anchor",
        "emotional_nature": "Your emotions move slowly and settle deeply. Once you feel something, it stays. You find emotional security through physical comfort — food, touch, familiar environments, financial stability. Change threatens your equilibrium more than most people realize.",
        "needs": "You need routine and predictability in your home life, physical affection and sensory pleasure, financial security as emotional foundation, and time to process feelings at your own pace without pressure.",
        "shadow": "Emotional stubbornness, clinging to situations that have expired, using material comfort to avoid emotional processing, possessiveness disguised as devotion."
    },
    "Gemini": {
        "title": "Moon in Gemini — Emotional Thinker",
        "emotional_nature": "You process feelings by talking about them, writing about them, or analyzing them from multiple angles. Emotion and intellect are intertwined for you in a way that confuses people who separate the two. Your moods shift quickly and you genuinely feel different emotions in rapid succession.",
        "needs": "You need verbal processing of emotions with a trusted person, mental stimulation to prevent emotional restlessness, variety in your daily environment, and permission to change your mind about how you feel without being called inconsistent.",
        "shadow": "Rationalizing emotions instead of feeling them, nervous anxiety from overstimulation, emotional superficiality as self-protection, using humor to deflect from genuine vulnerability."
    },
    "Cancer": {
        "title": "Moon in Cancer — Emotional Core",
        "emotional_nature": "The Moon rules Cancer, so this is the most natural and powerful lunar placement. Your emotions are tidal — they come in waves, influenced by memory, environment, and the feelings of people around you. Home is not just a place; it is a feeling you carry and seek to recreate everywhere.",
        "needs": "You need a safe and nurturing home environment above all else, close family bonds or a chosen family, emotional reciprocity from the people you care for, and regular solitude to discharge absorbed emotional energy.",
        "shadow": "Emotional manipulation through guilt or withdrawal, inability to release past wounds, smothering loved ones under the guise of protection, mood swings driven by perceived rejection."
    },
    "Leo": {
        "title": "Moon in Leo — Emotional Performer",
        "emotional_nature": "Your emotions are dramatic, warm, and visible. You feel things with your whole chest and struggle to hide it. Recognition and appreciation are not vanity for you — they are genuine emotional needs. When you feel loved, you radiate generosity. When you feel ignored, the light dims noticeably.",
        "needs": "You need regular acknowledgment and appreciation from loved ones, creative self-expression as emotional outlet, loyalty and devotion in your inner circle, and the freedom to be expressive without being told you are too much.",
        "shadow": "Emotional theatrics used to control attention, wounded pride that escalates minor slights, difficulty empathizing when the focus is not on you, confusing admiration with love."
    },
    "Virgo": {
        "title": "Moon in Virgo — Emotional Processor",
        "emotional_nature": "You process emotions through analysis, organization, and problem-solving. When something upsets you, your first instinct is to understand why, categorize the feeling, and develop a plan to address it. This makes you remarkably self-aware but can also prevent you from simply sitting with feelings.",
        "needs": "You need an orderly environment to feel emotionally stable, useful work that gives your anxiety a productive channel, a partner who appreciates acts of service as love language, and reassurance that you are good enough despite your inner critic.",
        "shadow": "Paralyzing self-criticism, anxiety masquerading as productivity, emotional unavailability disguised as practicality, criticizing others as a way to manage your own insecurity."
    },
    "Libra": {
        "title": "Moon in Libra — Emotional Diplomat",
        "emotional_nature": "Harmony is an emotional need, not a preference. You feel genuinely destabilized by conflict and will go to significant lengths to restore peace — sometimes at the cost of suppressing your own feelings. You process emotions in relationship context: how you feel is often shaped by how others feel around you.",
        "needs": "You need beauty and aesthetic order in your living space, partnership and companionship to feel emotionally complete, fair treatment and balanced reciprocity, and peaceful resolution of conflicts rather than explosive confrontation.",
        "shadow": "People-pleasing that erodes authenticity, inability to identify your own feelings separately from others, passive aggression when direct expression feels too confrontational, codependency masked as commitment."
    },
    "Scorpio": {
        "title": "Moon in Scorpio — Emotional Depth",
        "emotional_nature": "You feel everything at maximum intensity and remember emotional experiences with photographic precision. Trust is earned in millimeters and lost in miles. Your emotional world is rich, complex, and largely invisible to anyone who has not been granted access. You test people before you open up — and most people fail.",
        "needs": "You need emotional honesty from others even when the truth is uncomfortable, privacy and control over who accesses your inner world, deep intimate bonds rather than a wide social circle, and proof of loyalty before you invest trust.",
        "shadow": "Emotional manipulation as a power strategy, jealousy and possessiveness as expressions of fear, vindictiveness toward those who betrayed your trust, obsessive emotional patterns that resist release."
    },
    "Sagittarius": {
        "title": "Moon in Sagittarius — Emotional Explorer",
        "emotional_nature": "Your emotional instinct is to expand, explore, and reframe. When something painful happens, you naturally search for the meaning, the lesson, or the silver lining. This is genuinely how you cope — not denial, but philosophical processing. Emotional confinement triggers your flight response faster than almost anything else.",
        "needs": "You need freedom and space to process emotions in your own way, travel or new experiences as emotional reset, philosophical or spiritual framework that gives suffering meaning, and a partner who does not try to cage your emotional independence.",
        "shadow": "Bypassing genuine grief through toxic positivity, fear of emotional depth disguised as optimism, commitment avoidance triggered by anything that feels binding, bluntness that wounds when gentleness was needed."
    },
    "Capricorn": {
        "title": "Moon in Capricorn — Emotional Stoic",
        "emotional_nature": "You experience emotions as seriously as you experience everything else — which means you approach them with caution, control, and a long-term perspective. Vulnerability feels like risk. You learned early that emotional self-sufficiency was necessary, and that lesson shapes how you process feelings as an adult.",
        "needs": "You need respect and recognition for your emotional maturity, practical demonstrations of love rather than verbal declarations, time alone to process without being pressed for feelings, and a partner who does not mistake your composure for indifference.",
        "shadow": "Emotional suppression that eventually erupts as depression or burnout, using work to avoid feeling, difficulty accepting emotional support because it implies weakness, loneliness that results from an excessively guarded inner world."
    },
    "Aquarius": {
        "title": "Moon in Aquarius — Emotional Observer",
        "emotional_nature": "You experience emotions from a slight distance — as if observing them rather than being consumed by them. This is not coldness; it is your natural processing style. You understand feelings intellectually before you feel them viscerally. Group dynamics and social causes can trigger stronger emotional responses than personal relationships.",
        "needs": "You need intellectual connection as the foundation of emotional intimacy, space and independence within relationships, causes or communities that align with your values, and a partner who does not demand conventional emotional displays.",
        "shadow": "Emotional detachment that leaves partners feeling unloved, using ideology to avoid personal vulnerability, contrarianism in emotional discussions, difficulty distinguishing between independence and isolation."
    },
    "Pisces": {
        "title": "Moon in Pisces — Emotional Sponge",
        "emotional_nature": "Your emotional boundaries are exceptionally thin. You absorb the moods of rooms, the pain of strangers, and the unspoken feelings of everyone close to you. This gives you extraordinary empathy but also means your emotional state is rarely entirely your own. Dreams, music, and art affect you at a cellular level.",
        "needs": "You need regular solitude to discharge absorbed emotions, creative or spiritual outlets for emotional processing, a partner who provides grounding without dismissing your sensitivity, and environments that are calm, beautiful, and energetically clean.",
        "shadow": "Emotional martyrdom that seeks validation through suffering, escapism through fantasy or substances when reality is too harsh, difficulty distinguishing your emotions from others, victim mentality that avoids personal responsibility."
    }
}

# ═══════════════════════════════════════════════════════════════
# RISING SIGN (ASCENDANT) INTERPRETATIONS
# ═══════════════════════════════════════════════════════════════

RISING_INTERPRETATIONS = {
    "Aries": {
        "title": "Aries Rising — The First Impression of Action",
        "appearance": "You come across as direct, energetic, and physically present. People notice your assertive body language, quick movements, and competitive edge before they learn anything else about you. Your resting expression often reads as determined or slightly impatient.",
        "social_style": "You enter new situations ready to lead or at least ready to move. Small talk drains you; you prefer directness. First meetings with you feel energizing — or intimidating, depending on the other person's comfort with intensity.",
        "life_approach": "Your life unfolds through initiation. You attract experiences that require courage, independence, and quick decision-making. The first house ruled by Mars means your physical body and personal identity are closely tied to action and competition."
    },
    "Taurus": {
        "title": "Taurus Rising — The First Impression of Calm",
        "appearance": "You project steadiness, warmth, and sensory awareness. People often describe you as grounded, attractive in a classic way, and physically comfortable in your own skin. Your voice and physical presence tend to have a calming effect on others.",
        "social_style": "You move through social situations at your own pace and resist being rushed. First impressions of you are pleasant, approachable, and slightly reserved. People instinctively trust your stability.",
        "life_approach": "Your life unfolds through accumulation and patience. You attract experiences related to material security, beauty, and physical pleasure. With Venus ruling your Ascendant, your path through life is guided by what you value most deeply."
    },
    "Gemini": {
        "title": "Gemini Rising — The First Impression of Curiosity",
        "appearance": "You come across as youthful, animated, and intellectually engaged. People notice your expressive hands, quick eyes, and verbal energy before anything else. You often appear younger than your actual age throughout life.",
        "social_style": "You are the person who talks to everyone at the gathering — not superficially, but because you are genuinely curious about each person's perspective. First meetings with you feel stimulating and fast-paced.",
        "life_approach": "Your life unfolds through information gathering and communication. You attract varied experiences that keep you mentally stimulated. Mercury ruling your Ascendant means your identity is closely tied to what you know and how you express it."
    },
    "Cancer": {
        "title": "Cancer Rising — The First Impression of Warmth",
        "appearance": "You project nurturing energy, emotional sensitivity, and approachability. People often feel safe around you immediately — something about your presence invites vulnerability. Your facial expressions reveal your emotions more transparently than you realize.",
        "social_style": "You read the emotional temperature of a room before deciding how to present yourself. First impressions are gentle and receptive. You tend to attract people who need comfort or emotional support, even in casual settings.",
        "life_approach": "Your life unfolds through emotional connection and creating security. With the Moon ruling your Ascendant, your outer personality shifts with your moods more than most rising signs, and your appearance may literally change with your emotional state."
    },
    "Leo": {
        "title": "Leo Rising — The First Impression of Presence",
        "appearance": "You walk into a room and the room notices. Leo Rising individuals project confidence, warmth, and a natural magnetism that does not require effort. Your posture, hair, and personal style tend to make a statement.",
        "social_style": "You are generous with your attention and energy in social settings. People experience you as warm, entertaining, and slightly theatrical. First meetings feel like an event rather than a routine exchange.",
        "life_approach": "Your life unfolds through self-expression and creative visibility. The Sun ruling your Ascendant means your identity is tied to being seen and recognized. Your path requires finding authentic ways to shine without losing substance."
    },
    "Virgo": {
        "title": "Virgo Rising — The First Impression of Competence",
        "appearance": "You project precision, modesty, and quiet intelligence. People often describe you as put-together, detail-oriented, and somewhat reserved on first meeting. Your appearance tends toward clean, practical, and understated.",
        "social_style": "You observe before engaging and contribute to conversations with practical, well-considered input. First impressions are of someone who is helpful, thoughtful, and slightly self-contained. You attract people who need structure.",
        "life_approach": "Your life unfolds through service, analysis, and continuous improvement. Mercury ruling your Ascendant means your identity is shaped by your skills and your usefulness to others. Health and daily routines play an outsized role in your sense of self."
    },
    "Libra": {
        "title": "Libra Rising — The First Impression of Grace",
        "appearance": "You project elegance, charm, and social awareness. People often describe you as attractive, well-mannered, and easy to be around. Your personal style tends toward balanced, aesthetically considered choices.",
        "social_style": "You navigate social situations with diplomatic ease, making people feel valued and heard. First impressions are of someone pleasant, fair-minded, and socially skilled. You instinctively create harmony in group dynamics.",
        "life_approach": "Your life unfolds through relationships and partnerships. Venus ruling your Ascendant means your identity is shaped by your connections with others. You attract experiences that require negotiation, collaboration, and aesthetic judgment."
    },
    "Scorpio": {
        "title": "Scorpio Rising — The First Impression of Intensity",
        "appearance": "You project depth, intensity, and magnetic presence. People either feel drawn to you or slightly unsettled — rarely indifferent. Your eyes are often described as penetrating, and your overall demeanor carries weight.",
        "social_style": "You observe before revealing anything about yourself. First impressions are of someone who sees more than they say. You attract people who sense your depth and want access to it — and people who are intimidated by what they cannot read.",
        "life_approach": "Your life unfolds through transformation, crisis, and regeneration. Pluto ruling your Ascendant means your path involves repeated cycles of destruction and rebuilding. Your identity is forged through what you survive."
    },
    "Sagittarius": {
        "title": "Sagittarius Rising — The First Impression of Adventure",
        "appearance": "You project optimism, openness, and restless energy. People often describe you as friendly, enthusiastic, and physically expressive. Your smile tends to be wide and genuine, and your body language is expansive.",
        "social_style": "You approach new people and situations with curiosity and humor. First impressions are of someone fun, honest, and slightly unpredictable. You make people laugh and think simultaneously.",
        "life_approach": "Your life unfolds through exploration, education, and philosophical seeking. Jupiter ruling your Ascendant means your path is naturally expansive — you attract opportunities for growth, travel, and broadened horizons."
    },
    "Capricorn": {
        "title": "Capricorn Rising — The First Impression of Authority",
        "appearance": "You project seriousness, competence, and mature composure. People often perceive you as older or more responsible than your peers, especially in youth. Your demeanor carries natural authority that does not need to be announced.",
        "social_style": "You are selective in social situations and project quiet confidence. First impressions are of someone reliable, ambitious, and perhaps slightly reserved. You attract respect before you attract warmth.",
        "life_approach": "Your life unfolds through achievement, structure, and earned authority. Saturn ruling your Ascendant means your path requires patience — rewards come later in life but tend to be substantial and lasting."
    },
    "Aquarius": {
        "title": "Aquarius Rising — The First Impression of Uniqueness",
        "appearance": "You project individuality, intellectual energy, and a certain detachment from convention. People notice something unusual about you — your style, your perspective, or your refusal to follow expected social scripts.",
        "social_style": "You engage with people as equals regardless of social hierarchy. First impressions are of someone original, friendly in an unconventional way, and intellectually stimulating. You attract people who value authenticity over conformity.",
        "life_approach": "Your life unfolds through innovation, community involvement, and breaking established patterns. Uranus ruling your Ascendant means your path includes unexpected disruptions that redirect you toward more authentic self-expression."
    },
    "Pisces": {
        "title": "Pisces Rising — The First Impression of Mystery",
        "appearance": "You project gentleness, dreaminess, and a certain ethereal quality that people find difficult to pin down. Your appearance may shift significantly depending on your mood, and people often project their own ideals onto you.",
        "social_style": "You adapt to social environments like water adapts to its container. First impressions vary dramatically depending on who is observing you — you are a mirror that reflects what others want or need to see.",
        "life_approach": "Your life unfolds through intuition, creativity, and spiritual seeking. Neptune ruling your Ascendant means your path is non-linear and often guided by forces you cannot fully articulate. Your identity is fluid by design."
    }
}

# ═══════════════════════════════════════════════════════════════
# VENUS SIGN INTERPRETATIONS
# ═══════════════════════════════════════════════════════════════

VENUS_INTERPRETATIONS = {
    "Aries": {"title": "Venus in Aries", "love_style": "You fall fast, chase hard, and lose interest when the conquest is complete. You need a partner who keeps you on your toes — predictability kills your attraction faster than any conflict.", "attraction": "You are attracted to confidence, independence, and people who challenge you. Passivity repels you.", "gift": "Passionate pursuit, courageous vulnerability, willingness to fight for what you want."},
    "Taurus": {"title": "Venus in Taurus", "love_style": "Venus rules Taurus, making this one of the strongest placements for lasting love. You are sensual, loyal, and deeply committed once you choose someone. You express love through physical touch, quality meals, and material generosity.", "attraction": "You are attracted to stability, physical beauty, and people who demonstrate reliability through actions rather than promises.", "gift": "Unwavering devotion, sensory attentiveness, ability to create a beautiful shared life."},
    "Gemini": {"title": "Venus in Gemini", "love_style": "You need mental stimulation in love above all else. Conversation is foreplay, and a partner who bores you intellectually will never hold your heart regardless of other qualities. You flirt through wit and wordplay.", "attraction": "You are attracted to intelligence, verbal skill, humor, and versatility. You need variety in how love is expressed.", "gift": "Stimulating companionship, playful communication, ability to keep love feeling fresh through new experiences and ideas."},
    "Cancer": {"title": "Venus in Cancer", "love_style": "You love through nurturing, protection, and emotional attentiveness. Home is the center of your romantic world — you want to build a nest with your partner and fill it with memories. Emotional security is the prerequisite for everything else.", "attraction": "You are attracted to emotional openness, family orientation, and people who make you feel safe enough to be vulnerable.", "gift": "Deep emotional care, loyalty that weathers storms, ability to create a home that feels like a sanctuary."},
    "Leo": {"title": "Venus in Leo", "love_style": "Love is your grand production, and you are both the director and the star. You are generous, romantic, and demonstrative — grand gestures come naturally. You need to feel special, admired, and chosen above all others.", "attraction": "You are attracted to confidence, creativity, warmth, and people who are not afraid to be expressive with their affection.", "gift": "Wholehearted devotion, joyful romance, ability to make your partner feel like the most important person in the world."},
    "Virgo": {"title": "Venus in Virgo", "love_style": "You show love through practical care — remembering details, solving problems, improving your partner's daily life in tangible ways. You are selective in love and may take a long time to commit because your standards are specific.", "attraction": "You are attracted to intelligence, competence, cleanliness, and people who take care of themselves physically and financially.", "gift": "Attentive devotion to your partner's wellbeing, reliability, ability to love through consistent daily acts of care."},
    "Libra": {"title": "Venus in Libra", "love_style": "Venus rules Libra, giving you a natural gift for partnership and romance. You are charming, fair-minded, and deeply invested in creating harmonious relationships. You dislike vulgarity and are drawn to refined expressions of love.", "attraction": "You are attracted to beauty, intelligence, good manners, and people who treat you as an equal partner in every sense.", "gift": "Diplomatic partnership skills, aesthetic romance, ability to create a relationship that feels balanced and mutually enriching."},
    "Scorpio": {"title": "Venus in Scorpio", "love_style": "You love with volcanic intensity and absolute commitment. Surface romance insults you — you want soul-deep merging, unflinching honesty, and a partner who can match your emotional depth without flinching. Jealousy is your shadow; loyalty is your currency.", "attraction": "You are attracted to depth, mystery, emotional courage, and people who are unafraid of the darker dimensions of intimacy.", "gift": "Transformative love that deepens over time, unwavering loyalty once trust is established, emotional and physical intensity that creates unforgettable bonds."},
    "Sagittarius": {"title": "Venus in Sagittarius", "love_style": "You approach love as an adventure — you want a partner who expands your world rather than contracting it. You are generous, optimistic, and honest in relationships, sometimes to a fault. Freedom within partnership is your requirement, not your preference.", "attraction": "You are attracted to intelligence, humor, adventurous spirit, and people who have their own rich life independent of the relationship.", "gift": "Joy, growth, honesty, and the rare ability to keep long-term love feeling like a choice rather than an obligation."},
    "Capricorn": {"title": "Venus in Capricorn", "love_style": "You take love seriously — perhaps more seriously than any other Venus placement. You are cautious in early stages, assessing long-term potential before investing emotionally. Once committed, you are rock-solid. You show love by building security and showing up consistently.", "attraction": "You are attracted to ambition, maturity, financial responsibility, and people who have a clear direction in life.", "gift": "Lasting commitment, practical support, ability to build a partnership that grows stronger and more valuable over decades."},
    "Aquarius": {"title": "Venus in Aquarius", "love_style": "You need friendship as the foundation of romance. Conventional relationship scripts bore you — you prefer partnerships that respect individuality and challenge norms. You are loyal but need significant personal space to maintain your sense of self.", "attraction": "You are attracted to originality, intellectual depth, social consciousness, and people who do not try to change or possess you.", "gift": "Accepting love that respects your partner's autonomy, intellectual companionship, commitment to growth rather than stagnation."},
    "Pisces": {"title": "Venus in Pisces", "love_style": "Venus is exalted in Pisces, making this one of the most romantic and compassionate placements possible. You love unconditionally, see the best in people, and express affection through empathy, creativity, and spiritual connection. You may idealize partners early on.", "attraction": "You are attracted to sensitivity, creativity, spiritual depth, and people who need your compassion without exploiting it.", "gift": "Unconditional acceptance, artistic and spiritual romance, the ability to love someone for who they truly are beneath all defenses."}
}

# ═══════════════════════════════════════════════════════════════
# MARS SIGN INTERPRETATIONS (drive, anger, sexuality)
# ═══════════════════════════════════════════════════════════════

MARS_INTERPRETATIONS = {
    "Aries": {"title": "Mars in Aries", "drive": "Mars rules Aries — this is its most powerful and natural placement. Your energy is explosive, direct, and competitive. You act on impulse, confront problems head-on, and recover from setbacks almost immediately. Physical activity is not optional for your wellbeing.", "anger": "Fast to ignite, fast to burn out. You say what you mean in the moment and move on — but others may not recover as quickly as you do.", "passion": "Direct, physical, and initiating. You pursue desire with confidence and prefer partners who match your intensity."},
    "Taurus": {"title": "Mars in Taurus", "drive": "Slow to start, impossible to stop. Your energy builds gradually and sustains indefinitely. You are not reactive — you are determined. Physical stamina is your asset, and you apply force through persistence rather than speed.", "anger": "You tolerate a great deal before reacting, but when pushed past your limit, your anger is seismic and slow to fade. You hold grudges as investments.", "passion": "Sensual, physical, and enduring. You prioritize touch, comfort, and sustained physical connection over novelty."},
    "Gemini": {"title": "Mars in Gemini", "drive": "Your energy is mental and scattered across multiple interests simultaneously. You fight with words before fists and can outargue almost anyone. Multitasking is your natural state — focused, singular effort requires conscious discipline.", "anger": "Sharp, verbal, and cutting. You weaponize intelligence when provoked and can dismantle someone's argument — or ego — with surgical precision.", "passion": "Stimulated by conversation, variety, and mental connection. You need verbal engagement as part of physical intimacy."},
    "Cancer": {"title": "Mars in Cancer", "drive": "Your energy is driven by emotional motivation. You fight hardest when protecting people you love — personal ambition alone may not sustain your effort, but defending family or home releases formidable force. Your moods significantly affect your energy levels.", "anger": "Indirect and defensive. You withdraw, sulk, or use emotional pressure rather than direct confrontation. Your anger often manifests as hurt feelings.", "passion": "Emotionally driven and deeply connected to feelings of safety. You need emotional trust before physical vulnerability."},
    "Leo": {"title": "Mars in Leo", "drive": "Your energy is powered by pride and creative ambition. You work hard when the work allows self-expression and recognition. You lead through inspiration and perform best when an audience — literal or figurative — is watching.", "anger": "Dramatic and authoritative. You do not lose your temper quietly — offended dignity produces roaring confrontation. You fight for respect above all else.", "passion": "Generous, warm, and performative. You want to be the best your partner has ever had, and you put genuine effort into ensuring it."},
    "Virgo": {"title": "Mars in Virgo", "drive": "Your energy is precise, methodical, and detail-oriented. You accomplish through careful planning and persistent incremental effort rather than bursts of intensity. You work harder than almost any other Mars placement — the issue is knowing when to stop.", "anger": "Critical, sharp, and targeted. You do not explode — you dissect. Your anger manifests as nitpicking, silent criticism, or withdrawal of assistance.", "passion": "Attentive, service-oriented, and focused on your partner's physical experience. You pay attention to what works and refine your approach continuously."},
    "Libra": {"title": "Mars in Libra", "drive": "Mars is in its detriment in Libra, meaning your assertive energy is filtered through diplomacy. You fight for fairness rather than personal gain and may struggle with direct confrontation. Your greatest strength is strategic partnership.", "anger": "Passive-aggressive and indirect. You avoid open conflict but accumulate resentment that eventually surfaces in unexpected ways.", "passion": "Romantic, balanced, and focused on mutual pleasure. You need aesthetic beauty and emotional harmony as part of physical intimacy."},
    "Scorpio": {"title": "Mars in Scorpio", "drive": "Mars co-rules Scorpio, giving you intense, focused, and relentless energy. You commit fully to your goals and pursue them with strategic patience that outlasts everyone else's enthusiasm. You do not scatter your energy — you concentrate it.", "anger": "Cold, strategic, and unforgettable. You rarely lose your composure — instead, you plan. Your revenge is patient and precise when you choose to pursue it.", "passion": "Intense, transformative, and all-consuming. Physical intimacy is a form of emotional merging for you — surface encounters leave you hollow."},
    "Sagittarius": {"title": "Mars in Sagittarius", "drive": "Your energy is expansive, optimistic, and adventure-seeking. You are motivated by growth, freedom, and the pursuit of meaning. Routine drains you — variety and big-picture goals fuel your considerable drive.", "anger": "Honest and direct — you say exactly what you think, then move on. You do not hold grudges because you genuinely forget what made you angry.", "passion": "Adventurous, playful, and freedom-loving. You need spontaneity and humor in physical intimacy and resist anything that feels routine."},
    "Capricorn": {"title": "Mars in Capricorn", "drive": "Mars is exalted in Capricorn — this is one of the most powerful and effective Mars placements. Your energy is disciplined, strategic, and goal-oriented. You climb steadily and do not waste effort on anything that does not serve your long-term plan.", "anger": "Controlled and authoritative. You do not lose your temper — you remove your support. Your disappointment is more devastating than most people's rage.", "passion": "Controlled, enduring, and quietly intense. You take physical intimacy seriously and improve with trust over time."},
    "Aquarius": {"title": "Mars in Aquarius", "drive": "Your energy is driven by intellectual conviction and social ideals. You fight for causes and principles more readily than personal gain. Your approach to action is unconventional — you instinctively look for the solution nobody else has tried.", "anger": "Detached and ideological. You argue from principle rather than emotion, which can make your opposition feel cold and impersonal.", "passion": "Experimental, open-minded, and intellectually engaged. You need mental connection and unconventional expression in physical intimacy."},
    "Pisces": {"title": "Mars in Pisces", "drive": "Your energy flows like water — it finds the path of least resistance and achieves goals through adaptability rather than force. You are motivated by compassion, creativity, and spiritual purpose. Direct competition drains you.", "anger": "Passive, indirect, and self-directed. You are more likely to absorb anger than express it, which can lead to resentment, depression, or self-sabotage.", "passion": "Gentle, imaginative, and emotionally immersive. Physical intimacy is a spiritual experience for you — disconnected encounters feel empty."}
}

# ═══════════════════════════════════════════════════════════════
# MERCURY SIGN INTERPRETATIONS (communication, thinking)
# ═══════════════════════════════════════════════════════════════

MERCURY_INTERPRETATIONS = {
    "Aries": {"title": "Mercury in Aries", "thinking": "Fast, direct, and competitive. You think in headlines, not paragraphs. Your mind works quickly and you form opinions instantly — revision comes only when new information forces it.", "communication": "Blunt, assertive, and impatient with lengthy explanations. You say what you mean and expect others to do the same."},
    "Taurus": {"title": "Mercury in Taurus", "thinking": "Slow, methodical, and deeply practical. You think in terms of tangible outcomes and real-world applications. Abstract theory without practical use bores you.", "communication": "Deliberate and measured. You speak when you have something worth saying and rarely waste words. Your voice often has a calming, grounding quality."},
    "Gemini": {"title": "Mercury in Gemini", "thinking": "Mercury rules Gemini — this is the sharpest, quickest mental placement. You process information at remarkable speed, juggle multiple topics effortlessly, and connect ideas that others see as unrelated.", "communication": "Articulate, witty, and versatile. You adapt your communication style to your audience instinctively and excel at making complex ideas accessible."},
    "Cancer": {"title": "Mercury in Cancer", "thinking": "Your thinking is shaped by emotion and memory. You remember how things felt more vividly than what was said. Your mind processes information through an emotional filter that prioritizes security and belonging.", "communication": "Gentle, indirect, and emotionally attuned. You communicate with sensitivity to your listener's feelings, sometimes at the expense of directness."},
    "Leo": {"title": "Mercury in Leo", "thinking": "Your mind gravitates toward big-picture vision, creative solutions, and ideas that inspire. You think with confidence and are not easily swayed by criticism or doubt.", "communication": "Warm, dramatic, and persuasive. You speak with authority and conviction, and people tend to listen because your delivery commands attention."},
    "Virgo": {"title": "Mercury in Virgo", "thinking": "Mercury rules Virgo — this is the most analytical and precise mental placement. You notice details that others overlook entirely, and your mind naturally categorizes, organizes, and improves whatever it encounters.", "communication": "Precise, helpful, and occasionally critical. You communicate with accuracy and may unintentionally focus on flaws rather than strengths."},
    "Libra": {"title": "Mercury in Libra", "thinking": "Your mind naturally considers all perspectives before forming an opinion. You think diplomatically and seek intellectual balance. This makes you fair-minded but can slow your decision-making significantly.", "communication": "Charming, diplomatic, and considerate. You frame ideas in ways that minimize conflict and maximize agreement."},
    "Scorpio": {"title": "Mercury in Scorpio", "thinking": "Your mind is investigative, penetrating, and psychologically perceptive. You see through surface explanations to the underlying motivations. You are naturally suspicious of easy answers.", "communication": "Intense, strategic, and selective. You reveal information deliberately and use silence as effectively as words."},
    "Sagittarius": {"title": "Mercury in Sagittarius", "thinking": "Your mind is expansive, philosophical, and big-picture oriented. You connect ideas across disciplines and cultures. Details bore you — you care about meaning, not minutiae.", "communication": "Honest, enthusiastic, and sometimes tactless. You say what you believe and assume others want the same directness you prefer."},
    "Capricorn": {"title": "Mercury in Capricorn", "thinking": "Your mind is structured, strategic, and focused on practical outcomes. You think in terms of timelines, hierarchies, and measurable results. Theoretical knowledge without application feels wasteful.", "communication": "Authoritative, concise, and goal-oriented. You communicate to achieve specific outcomes rather than to process or socialize."},
    "Aquarius": {"title": "Mercury in Aquarius", "thinking": "Your mind is innovative, systematic, and pattern-oriented. You think in frameworks and models rather than individual cases. Original ideas come naturally — conventional thinking feels intellectually stifling.", "communication": "Objective, unconventional, and intellectually stimulating. You communicate ideas that challenge assumptions and provoke thought."},
    "Pisces": {"title": "Mercury in Pisces", "thinking": "Your mind processes information intuitively and holistically. You absorb impressions, images, and feelings rather than discrete facts. Linear logic is not your strongest mode — pattern recognition and creative synthesis are.", "communication": "Poetic, empathetic, and sometimes vague. You communicate through metaphor, story, and emotional resonance rather than precise data."}
}

# ═══════════════════════════════════════════════════════════════
# CHIRON SIGN INTERPRETATIONS (wound and healing)
# ═══════════════════════════════════════════════════════════════

CHIRON_INTERPRETATIONS = {
    "Aries": {"title": "Chiron in Aries", "wound": "A deep wound around your right to exist, take up space, and assert yourself. You may struggle with self-doubt about your identity and whether your needs matter.", "healing": "You heal by learning to put yourself first without guilt and by helping others find their own courage and self-assertion."},
    "Taurus": {"title": "Chiron in Taurus", "wound": "A wound connected to self-worth, material security, and the body. You may feel fundamentally unsafe in the physical world or struggle with believing you deserve abundance.", "healing": "You heal by developing an unshakeable sense of inner value that does not depend on external possessions or validation."},
    "Gemini": {"title": "Chiron in Gemini", "wound": "A wound around communication, learning, and being heard. You may feel that your voice does not matter or that you were misunderstood during formative years.", "healing": "You heal by finding your authentic voice and helping others articulate what they cannot express on their own."},
    "Cancer": {"title": "Chiron in Cancer", "wound": "A wound connected to home, family, and emotional belonging. You may carry a feeling of not being fully nurtured or of home never feeling safe enough.", "healing": "You heal by creating the emotional safety for others that you lacked, and by learning to parent your own inner child."},
    "Leo": {"title": "Chiron in Leo", "wound": "A wound around self-expression, creativity, and recognition. You may feel invisible or fear that expressing your true self will lead to rejection or ridicule.", "healing": "You heal by expressing yourself authentically despite the fear and by helping others find the courage to be seen."},
    "Virgo": {"title": "Chiron in Virgo", "wound": "A wound connected to competence, health, and feeling useful. You may carry a persistent fear of not being good enough or of your contributions being insufficient.", "healing": "You heal by accepting imperfection as human and by helping others find practical solutions to their struggles without judging them."},
    "Libra": {"title": "Chiron in Libra", "wound": "A wound around relationships, fairness, and partnership. You may feel that balance in relationships is impossible or that you always give more than you receive.", "healing": "You heal by learning healthy interdependence and by helping others create more equitable and honest partnerships."},
    "Scorpio": {"title": "Chiron in Scorpio", "wound": "A wound connected to trust, power, and emotional vulnerability. You may have experienced betrayal or violation that made deep trust feel dangerous.", "healing": "You heal through courageously opening yourself to vulnerability again and by helping others transform their pain into power."},
    "Sagittarius": {"title": "Chiron in Sagittarius", "wound": "A wound around meaning, belief, and belonging to something larger than yourself. You may struggle with feeling that life lacks purpose or that your beliefs have been shattered.", "healing": "You heal by building your own authentic philosophy from lived experience rather than inherited doctrine, and by helping others find meaning."},
    "Capricorn": {"title": "Chiron in Capricorn", "wound": "A wound connected to authority, achievement, and societal belonging. You may feel that no amount of accomplishment is enough or that the system is rigged against you.", "healing": "You heal by redefining success on your own terms and by mentoring others who face similar structural barriers."},
    "Aquarius": {"title": "Chiron in Aquarius", "wound": "A wound around belonging, individuality, and social acceptance. You may feel like a permanent outsider — too different to fit in, but deeply wanting community.", "healing": "You heal by embracing your uniqueness as your contribution and by creating inclusive communities where others feel they belong."},
    "Pisces": {"title": "Chiron in Pisces", "wound": "A wound connected to spiritual disconnection, escapism, and the feeling of being lost in the world. You may struggle with boundaries and feel overwhelmed by collective suffering.", "healing": "You heal through spiritual practice, creative expression, and by channeling your sensitivity into compassionate service without losing yourself."}
}

# ═══════════════════════════════════════════════════════════════
# LILITH SIGN INTERPRETATIONS (shadow, repressed power)
# ═══════════════════════════════════════════════════════════════

LILITH_INTERPRETATIONS = {
    "Aries": {"title": "Lilith in Aries", "shadow": "Your suppressed rage and desire for independence. You may have been punished for being assertive, angry, or self-centered.", "power": "When integrated, you become fearlessly authentic and teach others that anger is not inherently destructive — it is information."},
    "Taurus": {"title": "Lilith in Taurus", "shadow": "Your relationship with pleasure, the body, and material desire. You may feel shame around physical needs, money, or sensuality.", "power": "When integrated, you embody unapologetic enjoyment of the physical world and teach others that desire is not sinful."},
    "Gemini": {"title": "Lilith in Gemini", "shadow": "Your forbidden thoughts, taboo knowledge, and unconventional ideas. You may have been silenced for asking questions that made people uncomfortable.", "power": "When integrated, you become a voice for uncomfortable truths and help others think beyond socially acceptable narratives."},
    "Cancer": {"title": "Lilith in Cancer", "shadow": "Your complicated relationship with mothering, home, and emotional dependency. You may have experienced nurturing as conditional or manipulative.", "power": "When integrated, you redefine family on your own terms and model emotional honesty rather than performative caregiving."},
    "Leo": {"title": "Lilith in Leo", "shadow": "Your suppressed need for recognition, creative expression, and admiration. You may have been shamed for wanting attention or standing out.", "power": "When integrated, you become magnetically authentic and inspire others to stop dimming their light for other people's comfort."},
    "Virgo": {"title": "Lilith in Virgo", "shadow": "Your relationship with control, perfection, and the body's natural functions. You may carry shame about health, sexuality, or the messy reality of being human.", "power": "When integrated, you embrace imperfection as power and help others release the tyranny of impossible standards."},
    "Libra": {"title": "Lilith in Libra", "shadow": "Your suppressed anger about unfairness and your tendency to sacrifice authenticity for harmony. You may have been conditioned to keep the peace at any cost.", "power": "When integrated, you become an advocate for genuine justice rather than superficial peace and model honest relationship dynamics."},
    "Scorpio": {"title": "Lilith in Scorpio", "shadow": "Your relationship with power, control, sexuality, and death. This is Lilith's most intense placement. You may have experienced or witnessed the abuse of power.", "power": "When integrated, you become a force of regeneration — transforming taboo, shame, and trauma into wisdom and strength."},
    "Sagittarius": {"title": "Lilith in Sagittarius", "shadow": "Your suppressed wildness, unorthodox beliefs, and refusal to be domesticated. You may have been punished for questioning authority or rejecting conventional morality.", "power": "When integrated, you live by your own moral code and inspire others to seek truth beyond institutional boundaries."},
    "Capricorn": {"title": "Lilith in Capricorn", "shadow": "Your complicated relationship with authority, ambition, and societal expectations. You may have been denied opportunities or punished for exceeding your assigned place.", "power": "When integrated, you become an authority who earned power through authenticity rather than conformity, and you change the systems from within."},
    "Aquarius": {"title": "Lilith in Aquarius", "shadow": "Your suppressed radicalism and the punishment you received for being different. You may have learned to hide your most innovative ideas to avoid rejection.", "power": "When integrated, you become a revolutionary force that normalizes what was previously considered unacceptable or impossible."},
    "Pisces": {"title": "Lilith in Pisces", "shadow": "Your relationship with escapism, victimhood, and spiritual manipulation. You may have been exploited through your empathy or punished for your sensitivity.", "power": "When integrated, you become a spiritual healer who channels compassion without losing personal boundaries or autonomy."}
}

# ═══════════════════════════════════════════════════════════════
# NORTH NODE INTERPRETATIONS (life purpose, karmic direction)
# ═══════════════════════════════════════════════════════════════

NORTH_NODE_INTERPRETATIONS = {
    "Aries": {"title": "North Node in Aries", "purpose": "Your soul's growth direction points toward independence, self-assertion, and learning to prioritize your own needs. You are moving away from over-reliance on others toward confident self-reliance.", "past_pattern": "You have spent too much energy accommodating others and avoiding conflict (South Node in Libra). This life asks you to develop courage and stand alone when necessary."},
    "Taurus": {"title": "North Node in Taurus", "purpose": "Your growth direction leads toward simplicity, stability, and cultivating your own resources. You are learning to build rather than destroy, to accumulate rather than release.", "past_pattern": "You carry a pattern of intensity, crisis, and transformation (South Node in Scorpio). This life asks you to find peace in the ordinary and trust that stability is not stagnation."},
    "Gemini": {"title": "North Node in Gemini", "purpose": "Your growth direction points toward curiosity, communication, and gathering diverse perspectives. You are learning to listen as much as you speak and to value many small truths over one grand theory.", "past_pattern": "You carry a tendency toward dogmatism and preaching (South Node in Sagittarius). This life asks you to stay curious rather than certain."},
    "Cancer": {"title": "North Node in Cancer", "purpose": "Your growth direction leads toward emotional vulnerability, nurturing, and creating a true home. You are learning that professional achievement means little without emotional fulfillment.", "past_pattern": "You carry a pattern of prioritizing career and public image over personal connection (South Node in Capricorn). This life asks you to soften and let others in."},
    "Leo": {"title": "North Node in Leo", "purpose": "Your growth direction points toward individual self-expression, creative confidence, and learning to take center stage. You are moving from collective anonymity toward personal visibility.", "past_pattern": "You carry a tendency to hide behind groups and causes (South Node in Aquarius). This life asks you to step forward as yourself, not as a representative."},
    "Virgo": {"title": "North Node in Virgo", "purpose": "Your growth direction leads toward practical service, analytical thinking, and making yourself useful in concrete ways. You are learning that small, precise actions create more change than grand spiritual gestures.", "past_pattern": "You carry a tendency toward escapism and martyrdom (South Node in Pisces). This life asks you to show up in the real world with practical skills."},
    "Libra": {"title": "North Node in Libra", "purpose": "Your growth direction points toward partnership, diplomacy, and learning to consider others' needs alongside your own. You are developing the ability to collaborate rather than dominate.", "past_pattern": "You carry a pattern of fierce independence and self-focus (South Node in Aries). This life asks you to learn the art of compromise and mutual support."},
    "Scorpio": {"title": "North Node in Scorpio", "purpose": "Your growth direction leads toward emotional depth, transformation, and the willingness to face uncomfortable truths. You are learning to release control and trust the process of deep change.", "past_pattern": "You carry a tendency toward comfort-seeking and material attachment (South Node in Taurus). This life asks you to go deeper than the surface."},
    "Sagittarius": {"title": "North Node in Sagittarius", "purpose": "Your growth direction points toward big-picture thinking, philosophical exploration, and expanding beyond your familiar environment. You are learning to seek meaning rather than just information.", "past_pattern": "You carry a tendency to stay in your intellectual comfort zone (South Node in Gemini). This life asks you to commit to beliefs and explore the unknown."},
    "Capricorn": {"title": "North Node in Capricorn", "purpose": "Your growth direction leads toward responsibility, structure, and building lasting achievements. You are learning to take your ambitions seriously and accept the discipline required to manifest them.", "past_pattern": "You carry a tendency to retreat into emotional comfort and family dependency (South Node in Cancer). This life asks you to step into public accountability."},
    "Aquarius": {"title": "North Node in Aquarius", "purpose": "Your growth direction points toward community, innovation, and serving the collective good. You are learning to contribute to something larger than your personal story.", "past_pattern": "You carry a tendency toward personal drama and ego-driven expression (South Node in Leo). This life asks you to channel your creative energy toward collective benefit."},
    "Pisces": {"title": "North Node in Pisces", "purpose": "Your growth direction leads toward compassion, spiritual surrender, and trust in forces larger than your analytical mind. You are learning to release control and flow with life rather than managing it.", "past_pattern": "You carry a tendency toward excessive analysis and criticism (South Node in Virgo). This life asks you to trust intuition alongside logic and to embrace mystery."}
}

# ═══════════════════════════════════════════════════════════════
# PART OF FORTUNE INTERPRETATIONS
# ═══════════════════════════════════════════════════════════════

PART_OF_FORTUNE_INTERPRETATIONS = {
    "Aries": {"title": "Part of Fortune in Aries", "meaning": "Your greatest luck and fulfillment come through bold action, independent ventures, and situations that require you to act on your own initiative. You thrive when you lead and take risks."},
    "Taurus": {"title": "Part of Fortune in Taurus", "meaning": "Your greatest luck comes through patience, financial investment, and building tangible things over time. Stability and sensory enjoyment are pathways to your prosperity."},
    "Gemini": {"title": "Part of Fortune in Gemini", "meaning": "Your greatest luck comes through communication, writing, teaching, networking, and intellectual variety. Connecting people and ideas is your prosperity engine."},
    "Cancer": {"title": "Part of Fortune in Cancer", "meaning": "Your greatest luck comes through nurturing, home-based ventures, family connections, and emotional intelligence. Creating safe spaces is where you prosper."},
    "Leo": {"title": "Part of Fortune in Leo", "meaning": "Your greatest luck comes through creative self-expression, performance, leadership, and situations that put you in the spotlight. Recognition fuels your prosperity."},
    "Virgo": {"title": "Part of Fortune in Virgo", "meaning": "Your greatest luck comes through service, health-related work, analytical skills, and attention to detail. Practical problem-solving is your prosperity pathway."},
    "Libra": {"title": "Part of Fortune in Libra", "meaning": "Your greatest luck comes through partnerships, diplomacy, aesthetic ventures, and collaborative projects. Working with others amplifies your natural prosperity."},
    "Scorpio": {"title": "Part of Fortune in Scorpio", "meaning": "Your greatest luck comes through transformation, research, investment, psychology, and situations that require digging beneath the surface. Managing shared resources and understanding hidden dynamics brings prosperity."},
    "Sagittarius": {"title": "Part of Fortune in Sagittarius", "meaning": "Your greatest luck comes through travel, higher education, publishing, philosophy, and cross-cultural ventures. Expanding your horizons is literally your fortune."},
    "Capricorn": {"title": "Part of Fortune in Capricorn", "meaning": "Your greatest luck comes through long-term career building, institutional achievement, and disciplined pursuit of ambitious goals. Patience is your greatest prosperity tool."},
    "Aquarius": {"title": "Part of Fortune in Aquarius", "meaning": "Your greatest luck comes through innovation, technology, community work, and unconventional approaches. Going against the grain brings you unexpected prosperity."},
    "Pisces": {"title": "Part of Fortune in Pisces", "meaning": "Your greatest luck comes through creative and spiritual pursuits, healing work, and situations that require compassion and imagination. Trusting intuition over logic leads to your prosperity."}
}

# ═══════════════════════════════════════════════════════════════
# VERTEX SIGN INTERPRETATIONS (fated encounters)
# ═══════════════════════════════════════════════════════════════

VERTEX_INTERPRETATIONS = {
    "Aries": {"title": "Vertex in Aries", "meaning": "Fated encounters push you toward independence and self-assertion. You are likely to meet significant people during moments that require courage and decisive action."},
    "Taurus": {"title": "Vertex in Taurus", "meaning": "Fated encounters connect you with themes of value, stability, and physical beauty. Significant relationships often begin in settings related to nature, finance, or art."},
    "Gemini": {"title": "Vertex in Gemini", "meaning": "Fated encounters arrive through communication — chance conversations, written connections, or intellectual exchanges that redirect your life path unexpectedly."},
    "Cancer": {"title": "Vertex in Cancer", "meaning": "Fated encounters connect you with home, family, and emotional belonging. Significant people often enter your life during times of emotional vulnerability or domestic change."},
    "Leo": {"title": "Vertex in Leo", "meaning": "Fated encounters push you toward creative expression and visibility. Significant relationships often begin in settings where performance, art, or leadership are involved."},
    "Virgo": {"title": "Vertex in Virgo", "meaning": "Fated encounters arise through work, health, and service. Significant people often enter your life in professional or healing environments where practical help is exchanged."},
    "Libra": {"title": "Vertex in Libra", "meaning": "Fated encounters revolve around partnership and justice. Significant relationships feel destined and often involve themes of balance, commitment, and aesthetic harmony."},
    "Scorpio": {"title": "Vertex in Scorpio", "meaning": "Fated encounters are intense and transformative. Significant people enter your life during periods of crisis, deep change, or emotional upheaval that reshapes your identity."},
    "Sagittarius": {"title": "Vertex in Sagittarius", "meaning": "Fated encounters expand your worldview. Significant relationships often begin during travel, education, or philosophical exploration that changes your perspective permanently."},
    "Capricorn": {"title": "Vertex in Capricorn", "meaning": "Fated encounters connect you with authority, career, and legacy. Significant people often enter your life as mentors, employers, or guides toward your long-term ambitions."},
    "Aquarius": {"title": "Vertex in Aquarius", "meaning": "Fated encounters push you toward social change and authentic individuality. Significant relationships often begin in group settings or through unexpected circumstances that defy convention."},
    "Pisces": {"title": "Vertex in Pisces", "meaning": "Fated encounters have a spiritual or dreamlike quality. Significant people may enter your life through synchronicity, creative collaboration, or moments of collective compassion."}
}

# ═══════════════════════════════════════════════════════════════
# JUPITER & SATURN (used in birth chart full interpretation)
# ═══════════════════════════════════════════════════════════════

JUPITER_INTERPRETATIONS = {
    "Aries": {"title": "Jupiter in Aries", "meaning": "Growth through bold action, leadership, and pioneering ventures. You expand by taking risks others avoid."},
    "Taurus": {"title": "Jupiter in Taurus", "meaning": "Growth through accumulation, patience, and sensory enjoyment. Financial luck often increases over your lifetime."},
    "Gemini": {"title": "Jupiter in Gemini", "meaning": "Growth through communication, learning, and social networking. Knowledge is your most valuable asset."},
    "Cancer": {"title": "Jupiter in Cancer", "meaning": "Jupiter is exalted in Cancer. Growth through nurturing, family, and emotional generosity. Home is where your luck lives."},
    "Leo": {"title": "Jupiter in Leo", "meaning": "Growth through creative self-expression, generosity, and leadership. Your optimism inspires abundance in others."},
    "Virgo": {"title": "Jupiter in Virgo", "meaning": "Growth through service, health practices, and analytical improvement. Small consistent efforts produce your biggest breakthroughs."},
    "Libra": {"title": "Jupiter in Libra", "meaning": "Growth through partnerships, diplomacy, and aesthetic ventures. Your luck multiplies when you collaborate."},
    "Scorpio": {"title": "Jupiter in Scorpio", "meaning": "Growth through transformation, research, and managing shared resources. You find abundance in what others consider too intense."},
    "Sagittarius": {"title": "Jupiter in Sagittarius", "meaning": "Jupiter rules Sagittarius — this is its most powerful placement. Growth through exploration, philosophy, and relentless expansion of horizons."},
    "Capricorn": {"title": "Jupiter in Capricorn", "meaning": "Jupiter is in fall in Capricorn. Growth comes slowly through discipline and structure rather than luck. Your expansion is earned, not given."},
    "Aquarius": {"title": "Jupiter in Aquarius", "meaning": "Growth through innovation, community service, and unconventional thinking. Your luck increases when you serve the collective."},
    "Pisces": {"title": "Jupiter in Pisces", "meaning": "Jupiter co-rules Pisces. Growth through compassion, spiritual practice, and creative imagination. Your abundance flows from trust and surrender."}
}

SATURN_INTERPRETATIONS = {
    "Aries": {"title": "Saturn in Aries", "meaning": "Your life lesson involves learning healthy self-assertion. You may struggle with initiating action or feel blocked in expressing independence until you develop mature confidence."},
    "Taurus": {"title": "Saturn in Taurus", "meaning": "Your life lesson involves building real security from the ground up. Financial stability does not come easily but becomes unshakeable once established through disciplined effort."},
    "Gemini": {"title": "Saturn in Gemini", "meaning": "Your life lesson involves disciplined communication and focused learning. You may need to overcome scattered thinking to develop deep expertise in a specific field."},
    "Cancer": {"title": "Saturn in Cancer", "meaning": "Your life lesson involves learning emotional maturity and creating genuine security. Early family life may have taught you to suppress emotions — your growth comes from opening up."},
    "Leo": {"title": "Saturn in Leo", "meaning": "Your life lesson involves authentic self-expression and earning recognition through substance rather than performance. Creative confidence develops slowly but becomes formidable."},
    "Virgo": {"title": "Saturn in Virgo", "meaning": "Your life lesson involves mastering practical skills and releasing perfectionism. You develop exceptional competence over time but must learn that good enough is often sufficient."},
    "Libra": {"title": "Saturn in Libra", "meaning": "Saturn is exalted in Libra. Your life lesson involves creating fair, lasting partnerships and balanced structures. Relationships are your area of greatest maturation and achievement."},
    "Scorpio": {"title": "Saturn in Scorpio", "meaning": "Your life lesson involves facing deep fears about power, trust, and transformation. You develop remarkable psychological strength through confronting what most people avoid."},
    "Sagittarius": {"title": "Saturn in Sagittarius", "meaning": "Your life lesson involves developing a personal philosophy grounded in experience rather than blind optimism. Your beliefs become stronger as they are tested by reality."},
    "Capricorn": {"title": "Saturn in Capricorn", "meaning": "Saturn rules Capricorn — this is its most powerful and natural placement. Your life lesson is mastery through discipline. You are built for long-term achievement and carry natural authority."},
    "Aquarius": {"title": "Saturn in Aquarius", "meaning": "Saturn co-rules Aquarius. Your life lesson involves structured innovation and responsible community engagement. You bring discipline to progressive ideas."},
    "Pisces": {"title": "Saturn in Pisces", "meaning": "Your life lesson involves grounding spiritual sensitivity in practical reality. You develop wisdom through learning to maintain boundaries while remaining compassionate."}
}
