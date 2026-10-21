#!/usr/bin/env python3
"""Builds the Livewell Passport site into dist/ (deployable) and dist-artifact/ (claude.ai preview).
Run: python3 build.py
"""
import os, re, shutil, html

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
ART = os.path.join(ROOT, "dist-artifact")
SRC = os.path.join(ROOT, "src")

SITE = "Livewell Passport"
TAGLINE = "Your healthcare journey, reimagined."
EMAIL = "info@livewellpassport.com"
PORTAL_URL = "https://8042-1.portal.athenahealth.com/"
FB = "https://www.facebook.com/livewellpassport/"
IG = "https://www.instagram.com/livewellpassport"
FONTS = "https://fonts.googleapis.com/css2?family=Archivo:ital,wdth,wght@0,62..125,400..800;1,62..125,400..800&family=Figtree:wght@400;500;600&display=swap"

LOCATIONS = [
    dict(slug="midlothian", city="Midlothian", state="Virginia", st="VA",
         address="13553 Midlothian Tpke", city_line="Midlothian, VA 23113", phone="(804) 404-7902", tel="+18044047902"),
    dict(slug="inlet-beach", city="Inlet Beach", state="Florida", st="FL",
         address="22606 Panama City Beach Pkwy", city_line="Inlet Beach, FL 32413", phone="(850) 608-0200", tel="+18506080200"),
]

JOURNEYS = [
    dict(slug="weight-optimization", name="Weight Optimization", short="Weight", img="weight.jpg", icon="scale",
         blurb="Find the why behind the weight, then a plan that lasts.",
         h1="Weight optimization that starts with why",
         lede="We treat weight as one stop on a bigger journey. Instead of quick fixes, we look at what is really steering your health: hormone imbalances, inflammation and metabolic slowdowns. Then we build a plan you can actually keep.",
         points=[("Find the why behind the weight", "We go deeper than diet plans, uncovering hormonal imbalances, inflammation and metabolic blocks so your body works with you, not against you."),
                 ("Your path, not a shortcut", "No crash diets and no guesswork. A clear, personalized roadmap designed to help you lose weight in a way that lasts and feels good along the way.")],
         benefits_title="Feel lighter. Live freer. Travel farther.",
         benefits_intro="Weight optimization at Livewell Passport goes beyond shedding pounds. By addressing root causes like hormone imbalances, inflammation and metabolic slowdown, we help you gain energy, restore balance and feel confident in your own skin.",
         benefits=[("test-tube", "Discover the root", "Advanced testing reveals what is truly shaping your weight."),
                   ("route", "Mapped for you", "Your plan is built to match your body, your pace and your goals."),
                   ("heart-pulse", "Fit for real life", "No fads. Lasting habits that fit your daily rhythm."),
                   ("compass", "Guided all the way", "Stay on course with expert check-ins and consistent support.")],
         faq=[("What makes Livewell Passport’s weight optimization different from typical weight loss programs?", "We don’t just focus on the scale. We focus on why your body is holding on to weight. Through advanced lab testing and root-cause analysis, we uncover metabolic, hormonal and lifestyle factors affecting your health. The result is a personalized plan built for real, lasting change."),
              ("Will I receive a meal plan or workout routine?", "Yes, when it fits your journey. Plans are tailored to your lab results and goals. That might include nutrition guidance, movement recommendations, supplements or clinical support such as GLP-1 medications, all mapped to your current health and your destination."),
              ("How long before I see results?", "Every journey is unique. Some patients notice changes in energy, mood or digestion within the first few weeks. Physical changes often follow as your body responds to deeper balance. We focus on sustainable progress, not rushed outcomes.")]),
    dict(slug="womens-wellness", name="Women’s Wellness", short="Women’s", img="womens-2.jpg", icon="hand-heart",
         blurb="Real answers for every phase, from perimenopause on.",
         h1="Real answers for every phase of you",
         lede="Women’s health is a core focus here, not an afterthought. From perimenopause to postmenopause, we help you navigate hormonal changes with clarity. We uncover the root causes behind fatigue, weight gain, mood shifts and low libido, then build a plan that helps you feel like yourself again.",
         points=[("Understand the shift", "Hormonal changes aren’t random. They are signals. We listen, test and guide you toward balance with care that is precise, not guesswork."),
                 ("Life beyond symptoms", "From sleep and mood to weight and libido, personalized plans help you regain energy, confidence and control through every phase.")],
         benefits_title="Feel like yourself again. Or even better.",
         benefits_intro="Menopause may be natural, but suffering through it shouldn’t be. We go beyond symptom management to uncover what is really driving the shifts in your mood, sleep, energy and libido, then restore balance with personalized therapies and real support.",
         benefits=[("test-tube", "Rooted in science", "Advanced testing reveals what your body has been trying to tell you."),
                   ("route", "Tailored to you", "No generic fixes. Care crafted around your unique journey."),
                   ("heart-pulse", "Real relief, not guesswork", "From mood to metabolism, we treat causes, not just symptoms."),
                   ("compass", "With you, long-term", "Your care doesn’t end at symptom relief. It evolves with you.")],
         faq=[("How do I know if my symptoms are related to perimenopause or menopause?", "Fatigue, mood swings, hot flashes, weight gain and disrupted sleep can all be signs of hormonal shifts. We use advanced testing and one-on-one consultations to pinpoint the root cause, so you’re not left guessing."),
              ("Do you offer hormone therapy?", "Yes. We offer personalized hormone optimization plans, including bioidentical hormone therapy, tailored to your lab results, symptoms and lifestyle. It is never one-size-fits-all."),
              ("I’ve been told to “just deal with it.” How is this different?", "“Just deal with it” isn’t a plan. We take your concerns seriously and work to uncover what is really happening in your body, so you get the care and validation you deserve.")]),
    dict(slug="mens-wellness", name="Men’s Wellness", short="Men’s", img="mens.jpg", icon="bolt",
         blurb="Energy, performance and hormone balance for the long haul.",
         h1="Navigate strength at every stage",
         lede="Our Men’s Wellness program supports energy, performance, hormone balance and long-term vitality. Whether you are optimizing for peak health or addressing age-related changes, we take a whole-body approach backed by primary care and advanced therapies.",
         points=[("Personalized health mapping", "From testosterone to metabolism, we chart a custom path based on your health markers, lifestyle and goals. You’re not guessing, you’re guided."),
                 ("Vitality for the long haul", "More than a quick fix. Our therapies support stamina, focus and resilience so you stay sharp, strong and ready for what’s next.")],
         benefits_title="Feel like yourself again. Or even better.",
         benefits_intro="Aging is inevitable, but losing your edge doesn’t have to be. We go beyond band-aid solutions to address what is really affecting your strength, stamina, mood and drive, and help you rebalance your hormones and reclaim your confidence.",
         benefits=[("bolt", "Smooth departures", "Say goodbye to fatigue, stress and the symptoms holding you back."),
                   ("route", "Chart your course", "Personalized care plans that put your health goals on the map."),
                   ("compass", "Explore peak potential", "Boost energy, focus and performance wherever life takes you."),
                   ("scale", "Travel light", "Shed what is weighing you down with therapies built for long-term balance.")],
         faq=[("What does Men’s Wellness include at Livewell Passport?", "A full-spectrum approach, from hormone optimization and energy support to mental clarity and sexual wellness. Each care plan is personalized and grounded in both traditional primary care and therapies like peptides."),
              ("Is this covered by insurance, or is it all out-of-pocket?", "Many of our primary care services are covered by insurance, which makes Livewell Passport a convenient entry point to explore more specialized treatments. We’ll help you understand what is included and guide you through your options."),
              ("How is this different from seeing a regular doctor?", "Most traditional care stops at symptom relief. We dig deeper, mapping your root causes and offering proactive, long-term strategies. It is healthcare that travels further with you.")]),
    dict(slug="longevity-and-recovery", name="Longevity & Recovery", short="Longevity", img="recovery.jpg", icon="compass",
         blurb="Preserve vitality, strength and clarity as you age.",
         h1="Stay strong for the road ahead",
         lede="Longevity isn’t about chasing youth. It is about preserving vitality, strength and clarity as you age. We take a deep look at what is slowing you down, from chronic inflammation to hormonal shifts and nutrient imbalances, and build a recovery and restoration plan around it.",
         points=[("Cell-deep strength", "We go deeper than surface symptoms, targeting cellular health to support energy, recovery and longevity from the inside out."),
                 ("Bounce back, stronger", "Whether it is stress, fatigue or everyday wear and tear, we help your body recover, rebuild and restore balance.")],
         benefits_title="Extend the journey, strengthen the ride",
         benefits_intro="Your path to wellness shouldn’t slow with time. It should evolve. Our Longevity & Recovery program supports you at every mile marker, addressing inflammation, hormone shifts and cellular decline so you can keep moving forward with purpose.",
         benefits=[("bolt", "Reset your engine", "We fine-tune your body’s power source so you travel farther with energy to spare."),
                   ("compass", "Stay on course", "Guidance that brings your hormones back into balance."),
                   ("route", "Smooth the road ahead", "Clear the inflammation that slows you down."),
                   ("heart-pulse", "Rest, refuel, repeat", "Stronger recovery so you bounce back faster and keep going.")],
         faq=[("What is functional medicine?", "A patient-centered approach that looks deeper than symptoms to find the root causes of illness. It combines advanced diagnostic testing with personalized lifestyle, nutrition and medical interventions for lasting wellness, not quick fixes."),
              ("Do you offer in-person or virtual appointments?", "Both. Our locations are here for face-to-face visits, and our secure telehealth platform makes it easy to connect from anywhere."),
              ("How is this different from seeing a regular doctor?", "Most traditional care stops at symptom relief. We dig deeper, mapping your root causes and offering proactive, long-term strategies. It is healthcare that travels further with you.")]),
    dict(slug="hormonal-and-sexual-health", name="Hormonal & Sexual Health", short="Hormonal", img="hormonal.jpg", icon="heart-pulse",
         blurb="Reclaim balance. Rekindle vitality.",
         h1="Reclaim balance. Rekindle vitality.",
         lede="Your body’s signals are not detours. They are directions. We take the time to understand what your hormones are trying to tell you, then chart a personalized course that supports energy, libido, mood and overall well-being.",
         points=[("Find your inner compass", "Hormonal shifts can make you feel lost. We help you navigate back to clarity, energy and emotional balance."),
                 ("Sexual wellness and vitality", "Sexual health is more than physical. It is emotional, relational and vital. We listen, guide and support every step of the way.")],
         benefits_title="Rebalance your map. Rediscover your spark.",
         benefits_intro="Hormonal shifts and sexual health challenges can leave you feeling off-course, physically, emotionally and intimately. Through deep diagnostic testing and personalized care, we uncover the real reasons behind fatigue, low libido and mood changes, then guide you back to balance.",
         benefits=[("test-tube", "Navigate with clarity", "We decode your body’s signals through advanced testing. No guesswork, just direction."),
                   ("bolt", "Lift the fog", "Address the dips in mood, focus and stamina with care designed to restore energy and steadiness."),
                   ("heart-pulse", "Reignite the spark", "Sexual wellness is part of your journey. We help you reconnect with confidence and joy."),
                   ("route", "Charted for you", "Every step is tailored to your needs, your goals and your pace.")],
         faq=[("How do I know if my symptoms are hormone-related?", "Hormonal imbalances often show up as fatigue, mood swings, low libido, weight changes, sleep issues or irregular cycles. We don’t guess. We run advanced labs to uncover what is happening beneath the surface."),
              ("Is sexual health really a part of overall wellness?", "Absolutely. Sexual health affects confidence, relationships, emotional balance and quality of life. We approach it without shame or stigma, with honest conversations and personalized solutions."),
              ("What types of treatments are offered?", "Evidence-based options like bioidentical hormone therapy, peptide support, lifestyle and nutrition guidance and targeted supplements, aligned with your goals and long-term wellness.")]),
    dict(slug="mental-and-emotional-wellness", name="Mental & Emotional Wellness", short="Mental", img="mental.jpg", icon="brain",
         blurb="Clear the fog. Reclaim your path.",
         h1="Clear the fog. Reclaim your path.",
         lede="Mental and emotional health are vital parts of your journey, not side roads. We help you unpack what is weighing you down, reconnect with your sense of purpose and build the resilience to keep moving forward, with science-backed tools and compassionate guidance.",
         points=[("See the road ahead", "We help lift the emotional fog so you can move through life with clarity, confidence and renewed purpose."),
                 ("Lighten the load", "Stress and burnout don’t have to steer your journey. We help you reset, rebuild and restore balance for the miles ahead.")],
         benefits_title="Steady your mind. Strengthen your journey.",
         benefits_intro="Whether you are managing anxiety, depression or burnout, our providers work with you to uncover root causes and build a personalized care plan. The result: a lighter emotional load, greater peace of mind and the strength to move forward with confidence.",
         benefits=[("sun", "See the road clearly", "Identify emotional patterns and the root causes of anxiety, mood shifts and overwhelm."),
                   ("scale", "Unpack the weight", "Reclaim your energy and calm by addressing burnout with a plan built for balance."),
                   ("compass", "Stabilize the weather", "Support for stress, irritability or low mood. Emotional storms don’t have to last."),
                   ("route", "Your map to mental wellness", "Your story is unique, and your care should be too.")],
         faq=[("What kinds of mental health concerns do you treat?", "A wide range, including anxiety, depression, stress, mood swings and burnout. Whether you’re facing a recent challenge or have felt off-course for a while, we help you find clarity through personalized, whole-person care."),
              ("How do you approach mental and emotional wellness differently?", "Instead of masking symptoms, we explore root causes such as hormone imbalances, inflammation or lifestyle factors. Your plan combines medical insight with emotional support."),
              ("Will I need to take medication?", "Not necessarily. We explore all options, from lifestyle changes and supplements to stress management strategies and, when appropriate, prescriptions. The goal is a sustainable plan aligned with your values.")]),
    dict(slug="strength-and-performance", name="Strength & Performance", short="Strength", img="strength.jpg", icon="dumbbell",
         blurb="Science-driven strength, built for how you move and live.",
         h1="Strength that moves with purpose",
         lede="Performance isn’t just about reps or records. It is about resilience, stamina and strength that carries you through every leg of life’s journey. We create personalized plans that target muscle, movement and recovery with precision.",
         points=[("Built around your body", "Your strength plan is tailored to your physiology and goals. No templates, just precision for where you are and where you’re going."),
                 ("Power that lasts", "From injury prevention to post-exertion recovery, we help you build strength that endures on the field, at work and in daily life.")],
         benefits_title="Strength that goes the distance",
         benefits_intro="We go beyond reps and routines to help you build lasting strength from the inside out. Whether you are recovering, reconditioning or reaching for your peak, our plans optimize performance, mobility and energy.",
         benefits=[("bolt", "Train for real life", "Mobility and power that support everyday strength."),
                   ("route", "Gain with intention", "Targeted plans to improve strength, posture and body composition."),
                   ("heart-pulse", "Recover stronger", "Support joints, prevent injury and bounce back with balance."),
                   ("compass", "Keep going further", "Improve stamina and energy with personalized metabolic support.")],
         faq=[("Do I need to be an athlete to join the program?", "Not at all. Whether you’re just starting out, returning from an injury or looking to improve everyday function, the program is built around you."),
              ("What makes your approach different from personal training?", "Care goes beyond workouts. We start with lab testing and a full-body evaluation to understand hormone levels, inflammation and recovery markers, then create a plan rooted in science."),
              ("How soon will I see results?", "Most patients notice improvements in energy, strength and stamina within a few weeks. Plans focus on sustainable progress, so results last.")]),
]
JOURNEY_BY_SLUG = {j["slug"]: j for j in JOURNEYS}

STORIES = [  # real patient video stories from the current site
    ("Dawn", "story-dawn.jpg", "6oOIo74N_ao"),
    ("Callie", "story-callie.jpg", "Nd_iQ8ZcuhY"),
    ("Tera", "story-tera.jpg", "o8AD7LXE3AU"),
    ("John", "story-john.jpg", "pVt1yzuHILo"),
]
INTRO_VIDEO = "https://www.youtube.com/watch?v=XHOmBV4js_E"

GENERAL_FAQ = [
    ("Are you primary care, and can I use you for all my healthcare needs?", "Yes. Livewell Passport blends primary care with wellness. We can serve as your primary care provider while also offering advanced therapies, hormone optimization, weight management and more."),
    ("Do you take insurance, and what costs are involved?", "Yes. Many of our primary care services are covered by insurance. Some wellness services, advanced therapies or specialized programs may be self-pay. We review pricing upfront, so there are no surprises."),
    ("Do you offer in-person or virtual appointments?", "Both. Our locations are here for face-to-face visits, and our secure telehealth platform makes it easy to connect from anywhere, which suits frequent travelers and busy schedules."),
    ("Where are you located, and do you see sick patients?", "We have locations in Midlothian, Virginia and Inlet Beach, Florida, with new destinations opening soon. We see sick patients for many common concerns, but we are not an urgent care center. If you’re unsure whether to visit us or an ER, our team can help you decide."),
    ("What is functional medicine?", "A patient-centered approach that looks deeper than symptoms to find the root causes of illness. It combines advanced diagnostic testing with personalized lifestyle, nutrition and medical interventions for lasting wellness, not quick fixes."),
    ("What is a health coach, and how can they help me?", "A health coach is your personal guide toward better health. They help you set goals, stay motivated and make sustainable changes to nutrition, stress and routines. Our health coaches work closely with your medical provider to keep your plan on course."),
    ("Do you handle men’s health and women’s health, including hormones?", "Yes. We offer comprehensive care for both, including hormone optimization, support for perimenopause and menopause, and treatment plans for low testosterone or energy imbalances."),
    ("Do you offer physicals, including sports physicals?", "Absolutely. Annual physicals, sports physicals and other required exams for work, school and travel. Same-day appointments may be available, especially if you’re traveling and need quick clearance."),
    ("What are peptides and GLP-1s, and do they have side effects?", "Peptides are short chains of amino acids that can support healing, muscle recovery, fat loss and more. GLP-1 medications help regulate blood sugar and support weight loss. Like any therapy, they may have side effects, which your provider reviews in detail before treatment begins."),
    ("Do you have special programs like wedding wellness or weight loss?", "We do. Whether you want to look and feel your best for a big event or embark on a long-term health transformation, we create customized programs to fit your timeline and goals."),
]

PLANS = [
    dict(name="Maximum Strength", tag="For the road ahead", img="plan-strength.jpg",
         items=["Optimize muscle growth and recovery", "Improve energy, endurance and focus", "Personalized support for peak performance"]),
    dict(name="The Longevity Route", tag="Stay well, go far", img="plan-longevity.jpg",
         items=["Ongoing support designed to prevent illness and protect long-term vitality", "Regular deep-dive diagnostics that guide your evolving plan", "Nutrition, movement and stress support, tailored to you"]),
]

# ---------------------------------------------------------------- icons (one stroke weight, drawn)
ICONS = {
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
    "chev": '<path d="M6 9l6 6 6-6"/>',
    "plus": '<path d="M12 5v14M5 12h14"/>',
    "play": '<path d="M7 5v14l11-7z" fill="currentColor" stroke="none"/>',
    "pin": '<path d="M12 21s7-6.2 7-11.5A7 7 0 0 0 5 9.5C5 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3 7l9 6 9-6"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "flask": '<path d="M9 3h6M10 3v6L4.5 18.5A2 2 0 0 0 6.2 21h11.6a2 2 0 0 0 1.7-2.5L14 9V3"/><path d="M7 15h10"/>',
    "route": '<circle cx="6" cy="18" r="2.5"/><circle cx="18" cy="6" r="2.5"/><path d="M8.5 18H14a3 3 0 0 0 0-6h-4a3 3 0 0 1 0-6h5.5"/>',
    "heart": '<path d="M12 20s-7-4.6-7-10a4 4 0 0 1 7-2.6A4 4 0 0 1 19 10c0 5.4-7 10-7 10z"/><path d="M8 11h2l1.5-2.5L13 13l1.2-2H16"/>',
    "shield": '<path d="M12 3l7 3v5c0 5-3.5 8-7 10-3.5-2-7-5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "video": '<rect x="3" y="6" width="13" height="12" rx="2"/><path d="M16 10l5-3v10l-5-3"/>',
    "scale": '<path d="M12 3v18M5 7h14"/><path d="M5 7l-3 7a3 3 0 0 0 6 0zM19 7l-3 7a3 3 0 0 0 6 0z"/>',
    "bolt": '<path d="M13 3L5 14h6l-1 7 9-12h-6z"/>',
    "sun": '<circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M2 12h2M20 12h2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "check": '<path d="M5 12l4 4L19 7"/>',
    "close": '<path d="M6 6l12 12M18 6L6 18"/>',
    "arrow-left": '<path d="M19 12H5M11 6l-6 6 6 6"/>',
    "spark": '<path d="M12 3l1.8 5.2L19 10l-5.2 1.8L12 17l-1.8-5.2L5 10l5.2-1.8z" fill="currentColor" stroke="none"/>',
    "facebook": '<path d="M14 8h3V4h-3a4 4 0 0 0-4 4v3H7v4h3v6h4v-6h3l1-4h-4V8z"/>',
    "instagram": '<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor" stroke="none"/>',
}
_SOL = {}
def sol(name):
    """Inline a Solar line-duotone icon from src/icons (fetched with better-icons)."""
    if name not in _SOL:
        svg = open(os.path.join(SRC, "icons", name + ".svg"), encoding="utf-8").read()
        _SOL[name] = svg.replace('width="1em" height="1em"', 'aria-hidden="true" focusable="false"')
    return _SOL[name]
_HUES = ["blue", "green", "teal", "sky"]
_hue_i = [0]
def tile(name, cls="", hue=None):
    if hue is None:
        hue = _HUES[_hue_i[0] % len(_HUES)]; _hue_i[0] += 1
    return f'<span class="ico {cls}" data-ico data-hue="{hue}">{sol(name)}</span>'

def icon(name, cls="icon"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

_stamp_id = [0]
def stamp(top, bottom, center, cls="stamp", style=""):
    """Circular inked stamp with text on the ring. Unique path ids per instance."""
    _stamp_id[0] += 1
    i = _stamp_id[0]
    return f'''<span class="{cls}" style="{style}" aria-hidden="true"><svg viewBox="0 0 120 120">
<defs><path id="st{i}a" d="M60,60 m-44,0 a44,44 0 1,1 88,0"/><path id="st{i}b" d="M60,60 m44,0 a44,44 0 1,1 -88,0"/></defs>
<circle cx="60" cy="60" r="56" fill="none" stroke="currentColor" stroke-width="3"/>
<circle cx="60" cy="60" r="32" fill="none" stroke="currentColor" stroke-width="2"/>
<text font-size="11"><textPath href="#st{i}a" startOffset="50%" text-anchor="middle">{top}</textPath></text>
<text font-size="11"><textPath href="#st{i}b" startOffset="50%" text-anchor="middle">{bottom}</textPath></text>
<text x="60" y="64" font-size="12" text-anchor="middle">{center}</text>
</svg></span>'''

# ---------------------------------------------------------------- chrome
def rel(depth):  # path prefix for pages in subfolders
    return "../" * depth

def head(title, desc, depth=0, canonical_path=""):
    r = rel(depth)
    full = f"{title} · {SITE}" if title != SITE else f"{SITE} · Primary care and functional medicine in Midlothian, VA and Inlet Beach, FL"
    return f'''<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(full)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{html.escape(desc)}">
<meta property="og:title" content="{html.escape(full)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:image" content="{r}assets/img/about.jpg">
<link rel="icon" href="{r}assets/img/stamp-logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="{r}styles.css">'''

def footer(depth=0):
    r = rel(depth)
    jl = "".join(f'<li><a href="{r}journeys/{j["slug"]}.html">{j["name"]}</a></li>' for j in JOURNEYS)
    ll = "".join(f'<li><a href="{r}locations.html#{l["slug"]}">{l["city"]}, {l["st"]}</a></li>' for l in LOCATIONS)
    return f'''</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <a class="brand" href="{r}index.html"><img src="{r}assets/img/stamp-logo.png" alt="" width="42" height="42"><span>Livewell Passport<small>Medical · Wellness · Weight loss · Nutrition</small></span></a>
        <p class="footer-tag">{TAGLINE} From primary care covered by insurance to advanced treatment protocols, this is personalized health optimization.</p>
        <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      </div>
      <div><h4>Journeys</h4><ul>{jl}</ul></div>
      <div><h4>Locations</h4><ul>{ll}<li><a href="{r}contact.html">Start your journey</a></li><li><a href="{PORTAL_URL}" target="_blank" rel="noopener">Practice portal</a></li></ul></div>
      <div><h4>More</h4><ul>
        <li><a href="{r}faqs.html">FAQs</a></li>
        <li><a href="{r}policies.html">Cancellation &amp; billing policy</a></li>
        <li><a href="{r}privacy.html">Privacy &amp; HIPAA notice</a></li>
        <li><a href="{r}terms.html">Terms &amp; conditions</a></li>
        <li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li>
        <li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li>
      </ul></div>
    </div>
    <div class="footer-bottom">
      <p class="policy">Memberships and recurring services require 30 days’ notice to cancel, and charges are non-refundable once processed. <a href="{r}policies.html">Read the full policy</a>.</p>
      <p>© 2026 Livewell Passport of VA LLC. All rights reserved.</p>
    </div>
  </div>
</footer>
<script src="{r}site.js" defer></script>'''

def page(body, title, desc, depth=0, current=""):
    inner = head(title, desc, depth) + "\n" + header(depth, current) + body + footer(depth)
    full = "<!doctype html>\n<html lang=\"en\">\n<head>\n" + head(title, desc, depth) + "\n</head>\n<body>\n" + header(depth, current) + body + footer(depth) + "\n</body>\n</html>\n"
    return full, inner

def header(depth=0, current=""):
    r = rel(depth)
    strip_items = ["Primary care covered by insurance", "Midlothian, VA", "Inlet Beach, FL", "Telehealth", "Peptide therapy", "Bioidentical hormone replacement", "Weight optimization", "Hormone optimization"]
    strip = "".join(f'<span>{t}{icon("spark")}</span>' for t in strip_items)
    on_hero = ' on-hero' if current == 'home' else ''
    def cur(key): return ' aria-current="page"' if current == key else ""
    jitems = "".join(f'<li data-i style="--i:{i+1}"><a href="{r}journeys/{j["slug"]}.html" data-img="{r}assets/img/{j["img"]}" data-cap="{j["name"]}"{cur(j["slug"])}>{tile(j["icon"])}<span>{j["name"]}<small>{j["blurb"]}</small></span>{icon("arrow", "icon arr")}</a></li>' for i, j in enumerate(JOURNEYS))
    locs = "".join(f'<div class="mega-loc"><strong>{l["city"]}, {l["st"]}</strong><address>{l["address"]}<br>{l["city_line"]}</address><a href="tel:{l["tel"]}">{l["phone"]}</a></div>' for l in LOCATIONS)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="ticker" aria-hidden="true"><div class="ticker-track">{strip}{strip}</div></div>
<header class="header{on_hero}">
  <div class="wrap">
    <nav class="nav" aria-label="Main">
      <a class="brand" href="{r}index.html"><img src="{r}assets/img/stamp-logo.png" alt="" width="44" height="44"><span>Livewell Passport<small>Medical · Wellness · Weight loss · Nutrition</small></span></a>
      <ul class="nav-links">
        <li><button type="button" data-menu aria-expanded="false" aria-controls="mega">Journeys {icon("chev")}</button></li>
        <li><a href="{r}locations.html"{cur("locations")}>Locations</a></li>
        <li><a href="{r}faqs.html"{cur("faqs")}>FAQs</a></li>
        <li><a href="{r}portal.html"{cur("portal")}>Patient portal</a></li>
      </ul>
      <div class="nav-right">
        <a class="btn btn-primary" href="{r}contact.html">Start your journey</a>
        <button class="burger" type="button" data-menu aria-expanded="false" aria-controls="mega" aria-label="Menu"><span></span><span></span></button>
      </div>
    </nav>
  </div>
</header>
<div class="mega" id="mega" aria-label="Site menu" tabindex="-1">
  <div class="wrap mega-inner">
    <button class="mega-close" type="button" data-menu aria-label="Close menu">{icon("close")}</button>
    <div>
      <p class="label" data-i style="--i:0">Wellness journeys</p>
      <ul class="mega-list">{jitems}</ul>
      <div class="mega-cta" data-i style="--i:9"><a class="btn btn-light" href="{r}contact.html">Start your journey {icon("arrow")}</a></div>
    </div>
    <div class="mega-preview" data-i style="--i:2">
      <img src="{r}assets/img/weight.jpg" alt="" class="show"><img src="{r}assets/img/womens-2.jpg" alt="">
      <div class="cap">Weight Optimization</div>
      {stamp("LIVEWELL · PASSPORT", "MEDICAL · WELLNESS", "", cls="spin")}
    </div>
    <div class="mega-side">
      <div data-i style="--i:3"><p class="label">Locations</p>{locs}</div>
      <div data-i style="--i:5"><p class="label">More</p><ul class="mega-links">
        <li><a href="{r}portal.html">Patient portal</a></li><li><a href="{r}index.html#technology">Body composition analysis</a></li><li><a href="{r}faqs.html">FAQs</a></li><li><a href="{r}contact.html">Contact us</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul></div>
      <div class="mega-social" data-i style="--i:7"><a href="{FB}" target="_blank" rel="noopener" aria-label="Facebook">{icon("facebook")}</a><a href="{IG}" target="_blank" rel="noopener" aria-label="Instagram">{icon("instagram")}</a></div>
    </div>
  </div>
</div>
<main id="main">'''

def machine_svg():
    """A body composition analyzer, drawn and animated. No manufacturer marks."""
    keys = "".join(f'<circle cx="{118 + (i % 4) * 16}" cy="{196 + (i // 4) * 12}" r="3.2" fill="#D7DDE3"/>' for i in range(12))
    return f'''<div class="machine" aria-hidden="true"><svg viewBox="0 0 300 640">
<defs>
  <linearGradient id="col" x1="0" x2="1"><stop offset="0" stop-color="#F7F9FA"/><stop offset=".55" stop-color="#FFFFFF"/><stop offset="1" stop-color="#D9DFE5"/></linearGradient>
  <linearGradient id="base" x1="0" x2="1"><stop offset="0" stop-color="#2E343A"/><stop offset="1" stop-color="#15191D"/></linearGradient>
  <linearGradient id="scr" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1B2A3A"/><stop offset="1" stop-color="#0E1620"/></linearGradient>
  <clipPath id="scrclip"><rect x="92" y="96" width="116" height="78" rx="6"/></clipPath>
</defs>
<!-- base -->
<path d="M40 540 h220 a14 14 0 0 1 14 14 v30 a14 14 0 0 1 -14 14 h-220 a14 14 0 0 1 -14 -14 v-30 a14 14 0 0 1 14 -14z" fill="url(#base)"/>
<path d="M52 536 h196 a10 10 0 0 1 10 10 v8 h-216 v-8 a10 10 0 0 1 10 -10z" fill="#3A4148"/>
<ellipse cx="64" cy="602" rx="14" ry="5" fill="#8E99A4"/><ellipse cx="236" cy="602" rx="14" ry="5" fill="#8E99A4"/>
<rect class="pad" x="62" y="548" width="40" height="22" rx="8" fill="#E6EAEE"/><rect class="pad" x="198" y="548" width="40" height="22" rx="8" fill="#E6EAEE"/>
<rect class="pad" x="70" y="574" width="32" height="14" rx="6" fill="#E6EAEE"/><rect class="pad" x="198" y="574" width="32" height="14" rx="6" fill="#E6EAEE"/>
<rect x="128" y="552" width="44" height="30" rx="6" fill="#0F1316"/>
<!-- hinge + column -->
<rect x="118" y="496" width="64" height="44" rx="10" fill="#2A3036"/><circle cx="150" cy="516" r="9" fill="#55606B"/>
<rect x="116" y="150" width="68" height="356" rx="22" fill="url(#col)" stroke="#D4D9DF"/>
<text x="150" y="330" text-anchor="middle" transform="rotate(90 150 330)" font-family="Archivo, sans-serif" font-weight="700" font-size="11" letter-spacing="3" fill="#B4BDC6">BODY COMPOSITION</text>
<!-- head unit -->
<path d="M78 70 a20 20 0 0 1 20 -20 h104 a20 20 0 0 1 20 20 v160 a16 16 0 0 1 -16 16 h-112 a16 16 0 0 1 -16 -16z" fill="#FDFDFE" stroke="#D4D9DF"/>
<rect x="92" y="96" width="116" height="78" rx="6" fill="url(#scr)"/>
<g clip-path="url(#scrclip)">
  <g fill="none" stroke="#7FB7E6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" opacity=".9">
    <circle cx="112" cy="110" r="5"/><path d="M112 116 v18 M104 122 l8 -4 l8 4 M112 134 l-6 14 M112 134 l6 14"/>
  </g>
  <rect class="scan" x="98" y="100" width="28" height="2" fill="#9CCBEF" opacity=".9"/>
  <g transform="translate(138 106)">
    <rect width="60" height="6" rx="3" fill="#24364A"/><rect class="screen-bar" width="52" height="6" rx="3" fill="#3181C0"/>
    <rect y="14" width="60" height="6" rx="3" fill="#24364A"/><rect class="screen-bar" y="14" width="34" height="6" rx="3" fill="#2F7F5F"/>
    <rect y="28" width="60" height="6" rx="3" fill="#24364A"/><rect class="screen-bar" y="28" width="46" height="6" rx="3" fill="#8FD3B4"/>
  </g>
  <circle cx="184" cy="156" r="10" fill="none" stroke="#24364A" stroke-width="3"/>
  <circle class="ring" cx="184" cy="156" r="10" fill="none" stroke="#9CCBEF" stroke-width="3" stroke-linecap="round" transform="rotate(-90 184 156)"/>
  <text x="150" y="160" font-family="Archivo, sans-serif" font-size="8" fill="#9CCBEF" text-anchor="middle">30 s</text>
  <circle class="dot" cx="100" cy="166" r="2" fill="#3181C0"/>
</g>
{keys}
<!-- handles -->
<g class="handle l"><path d="M80 190 q-34 60 -22 200" fill="none" stroke="#1C2126" stroke-width="7" stroke-linecap="round"/><rect x="42" y="378" width="30" height="92" rx="14" fill="#FDFDFE" stroke="#D4D9DF"/><rect class="grip" x="50" y="402" width="14" height="44" rx="7" fill="none" stroke="#C8CED5" stroke-width="3"/></g>
<g class="handle r"><path d="M220 190 q34 60 22 200" fill="none" stroke="#1C2126" stroke-width="7" stroke-linecap="round"/><rect x="228" y="378" width="30" height="92" rx="14" fill="#FDFDFE" stroke="#D4D9DF"/><rect class="grip" x="236" y="402" width="14" height="44" rx="7" fill="none" stroke="#C8CED5" stroke-width="3"/></g>
</svg></div>'''

def phone_mock():
    """Phone mockup showing the custom body composition report. Sample figures, labeled as such."""
    hist = [188.3, 189.2, 189.5, 188.6, 188.4, 189.6, 190.1, 191.8]
    lo, hi = min(hist), max(hist)
    pts = " ".join(f"{10 + i * (240 / 7):.0f},{38 - (v - lo) / (hi - lo) * 30:.0f}" for i, v in enumerate(hist))
    last = pts.split(" ")[-1].split(",")
    return f'''<div class="phone-wrap"><div class="phone" data-reveal aria-label="Phone showing a sample body composition report">
  <div class="phone-screen">
    <div class="island"></div>
    <div class="statusbar"><span>9:41</span><span>●●●</span></div>
    <div class="report">
      <div><h5>Your body composition report</h5><div class="meta">Livewell Passport · Sample</div></div>
      <div class="big"><span data-count="191.8">191.8</span><small>lb weight</small></div>
      <div class="row"><span>Skeletal muscle mass</span><b>105.8 lb</b><div class="bar"><i style="--w:78%;--c:#3181C0"></i></div></div>
      <div class="row"><span>Body fat mass</span><b>11.7 lb</b><div class="bar"><i style="--w:22%;--c:#2F7F5F"></i></div></div>
      <div class="row"><span>Total body water</span><b>113.6 lb</b><div class="bar"><i style="--w:66%;--c:#1F8F9A"></i></div></div>
      <div class="row"><span>Percent body fat</span><b>6.1 %</b><div class="bar"><i style="--w:18%;--c:#4F9BD9"></i></div></div>
      <div class="seg">
        <div><b>Left arm</b>11.46 lb<b>Left leg</b>27.89 lb</div>
        <svg viewBox="0 0 46 70" aria-hidden="true"><g fill="#DCE3EA" stroke="#9AA4AE" stroke-width="1"><circle cx="23" cy="8" r="6"/><rect x="15" y="16" width="16" height="24" rx="5"/><rect x="5" y="17" width="7" height="24" rx="3.5"/><rect x="34" y="17" width="7" height="24" rx="3.5"/><rect x="15" y="41" width="7" height="26" rx="3.5"/><rect x="24" y="41" width="7" height="26" rx="3.5"/></g></svg>
        <div class="r"><b>Right arm</b>11.29 lb<b>Right leg</b>27.65 lb</div>
      </div>
      <div class="hist"><div class="row" style="grid-template-columns:1fr auto"><span>Weight history</span><b>8 visits</b></div>
        <svg viewBox="0 0 260 44" aria-hidden="true"><polyline points="{pts}"/><circle cx="{last[0]}" cy="{last[1]}" r="3"/></svg></div>
      <span class="pill">Reviewed with your provider</span>
    </div>
  </div>
</div><p class="phone-caption">Sample report. Your numbers are yours alone.</p></div>'''

def tech_section():
    return f'''<section class="pad-l bg-silver textured" id="technology">
  <div class="wrap">
    <h2 style="max-width:14ch">Take advantage of technology</h2>
    <p class="lede">Your first stop includes a full body composition analysis on our InBody analyzer. Stand on the device, hold the hand electrodes, and in about 30 seconds we have precise measurements of your muscle, fat and water, segment by segment. Then we turn it into a custom report you can actually read.</p>
    <div class="tech">
      {machine_svg()}
      <div class="tech-copy" data-reveal>
        <p>Direct segmental multi-frequency bioelectrical impedance measures each arm, each leg and your torso separately. It is non-invasive and auto-calibrated, and it does not estimate your results from age, sex, ethnicity or body type. What you see is measured, not assumed.</p>
        <ul class="tech-list">
          <li><b><span data-count="30">30</span><small>sec</small></b><span>Full body composition analysis, standing on the device and holding the hand electrodes.</span></li>
          <li><b>5<small>segments</small></b><span>Lean mass and fat for each arm, each leg and your trunk, so your plan targets what is actually there.</span></li>
          <li><b>3<small>essentials</small></b><span>Percent body fat, skeletal muscle mass and whole body phase angle, tracked visit after visit.</span></li>
          <li><b>1<small>report</small></b><span>A clear, easy-to-read result sheet, reviewed with your provider and stored securely.</span></li>
        </ul>
        <div class="hero-actions" style="justify-content:flex-start;margin-top:1.5rem"><a class="btn btn-primary" href="contact.html">Start your journey {icon("arrow")}</a></div>
      </div>
      {phone_mock()}
    </div>
  </div>
</section>'''

def closing(depth=0, h="Your passport to wellness awaits."):
    r = rel(depth)
    return f'''<section class="pad-xl bg-dark closing">
  <div class="wrap" data-reveal>
    <h2>{h}</h2>
    <p class="lede">Book your first visit in Midlothian, Inlet Beach or by telehealth. We always review pricing upfront, so there are no surprises.</p>
    <div class="hero-actions"><a class="btn btn-light btn-lg" href="{r}contact.html">Start your journey {icon("arrow")}</a><a class="btn btn-secondary btn-lg" href="{r}faqs.html">Read the FAQs</a></div>
    <p class="contact-line">Questions first? Email <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</section>'''

def home():
    words = "Wellness shouldn’t feel rushed, confusing, or cold.".split(" ")
    manifesto = " ".join(f'<span class="w">{w}</span>' for w in words)
    rail = []
    for j in JOURNEYS:
        rail.append(f'<a class="rcard" href="journeys/{j["slug"]}.html"><img src="assets/img/{j["img"]}" alt="" loading="lazy">{tile(j["icon"])}{stamp("LIVEWELL · PASSPORT", "WELLNESS · JOURNEY", "VISA", cls="mini-stamp")}<h3>{j["name"]}</h3><p>{j["blurb"]}</p><span class="more">Learn more {icon("arrow")}</span></a>')
    stories = "".join(f'''<a class="story" href="https://www.youtube.com/watch?v={vid}" target="_blank" rel="noopener">
      <div class="ph"><img src="assets/img/{img}" alt="{name}, a Livewell Passport patient" loading="lazy"><span class="play">{icon("play")}</span></div>
      <div class="meta"><strong>{name}’s story</strong><span>Watch on YouTube</span></div></a>''' for name, img, vid in STORIES)
    locs = "".join(f'''<div class="loc" id="{l["slug"]}">
      {stamp("ENTRY · " + l["st"], "LIVEWELL · PASSPORT", "OPEN", cls="entry-stamp")}
      <h3>{l["city"]}<small>{l["state"]}</small></h3>
      <address>{l["address"]}<br>{l["city_line"]}</address>
      <div class="row"><a href="tel:{l["tel"]}">{icon("phone")}{l["phone"]}</a><a href="https://www.google.com/maps/search/?api=1&query={html.escape((l["address"] + ", " + l["city_line"]).replace(" ", "+"))}" target="_blank" rel="noopener">{icon("pin")}Directions</a></div>
    </div>''' for l in LOCATIONS)

    body = f'''
<section class="hero">
  <img src="assets/img/beach.jpg" alt="" fetchpriority="high">
  <div class="hero-inner">
    <h1>Your healthcare journey, <em>reimagined.</em></h1>
    <p class="lede">Primary care covered by insurance, plus advanced therapies like peptides and bioidentical hormones. Whole-person medicine with time to listen.</p>
    <div class="hero-actions"><a class="btn btn-dark" href="contact.html">Start your journey {icon("arrow")}</a><a class="btn btn-ghost" href="#journeys">Explore journeys</a></div>
  </div>
  <div class="passport" aria-label="Illustration of a Livewell wellness passport">
    <div class="passport-head"><strong>WELLNESS PASSPORT</strong><img src="assets/img/stamp-logo.png" alt=""></div>
    <dl>
      <dt>Holder</dt><dd>You</dd>
      <dt>Issued at</dt><dd>Midlothian, VA · Inlet Beach, FL</dd>
      <dt>Covers</dt><dd>Primary care · Functional medicine · Advanced therapies</dd>
    </dl>
    <div class="stamps">
      {stamp("ROOT CAUSE", "LIVEWELL · PASSPORT", "FOUND", cls="stamp stamp-in", style="--tilt:-9deg;--delay:400ms")}
      {stamp("LABS", "LIVEWELL · PASSPORT", "REVIEWED", cls="stamp stamp-in", style="--tilt:6deg;--delay:620ms")}
      {stamp("ROUTE", "LIVEWELL · PASSPORT", "ISSUED", cls="stamp stamp-in", style="--tilt:-4deg;--delay:840ms")}
    </div>
  </div>
  <span class="scroll-cue" aria-hidden="true"></span>
</section>

<section class="pad-m">
  <div class="wrap values" data-reveal>
    <div class="value">{tile("shield-check")}<div><strong>Covered by insurance</strong><span>Many of our primary care services are covered by insurance.</span></div></div>
    <div class="value">{tile("test-tube")}<div><strong>Root-cause lab work</strong><span>Deep-dive diagnostics uncover what your body truly needs.</span></div></div>
    <div class="value">{tile("videocamera")}<div><strong>In person or virtual</strong><span>Two locations plus a secure telehealth platform, from anywhere.</span></div></div>
    <div class="value">{tile("stethoscope")}<div><strong>Time to listen</strong><span>Licensed providers and health coaches walk beside you.</span></div></div>
  </div>
</section>

<section class="pad-xl manifesto">
  <div class="wrap">
    <p class="big">{manifesto}</p>
    <div class="manifesto-grid" data-reveal>
      <p>At Livewell Passport, your story comes first, because true healing begins when someone truly listens. Here, primary care and functional medicine come together to offer more than just symptom relief. We take the time to understand what others overlook, then map a path that leads to lasting change.</p>
      <p class="side">This isn’t assembly-line care. It’s thoughtful, science-backed guidance, delivered with heart, grounded in trust, and personalized for every step of your journey.</p>
    </div>
  </div>
</section>

<section class="pad-m bg-silver textured">
  <div class="wrap">
    <h2>Your route to wellness</h2>
    <p class="lede" style="margin-bottom:2.5rem">Start your wellness journey in three stops.</p>
    <div class="stack">
      <div class="stack-card"><div class="body"><span class="stop">Stop one</span><div class="no">01</div><h3>Book your first stop</h3><p>Schedule your initial visit and begin mapping your path to better health.</p></div><div class="ph"><img src="assets/img/about.jpg" alt="" loading="lazy">{tile("calendar", "", "blue")}</div></div>
      <div class="stack-card"><div class="body"><span class="stop">Stop two</span><div class="no">02</div><h3>Discover what’s beneath the surface</h3><p>We dive deep with advanced lab testing to uncover root causes.</p></div><div class="ph"><img src="assets/img/mens.jpg" alt="" loading="lazy">{tile("test-tube", "", "green")}</div></div>
      <div class="stack-card"><div class="body"><span class="stop">Stop three</span><div class="no">03</div><h3>Follow your personalized route</h3><p>Receive a tailored wellness plan designed to guide your long-term transformation.</p></div><div class="ph"><img src="assets/img/longevity.jpg" alt="" loading="lazy">{tile("route", "", "teal")}</div></div>
    </div>
  </div>
</section>

<section class="pad-l" id="journeys">
  <div class="wrap">
    <div class="rail-head" data-reveal>
      <div><h2>Popular wellness journeys</h2><p class="lede" style="margin:0">Explore a few of our most transformative health journeys.</p></div>
      <div class="rail-nav"><button type="button" data-rail="prev" aria-label="Previous">{icon("arrow-left")}</button><button type="button" data-rail="next" aria-label="Next">{icon("arrow")}</button></div>
    </div>
    <div class="rail" tabindex="0" aria-label="Wellness journeys">{"".join(rail)}</div>
    <div class="rail-progress" aria-hidden="true"><i></i></div>
  </div>
</section>

<section class="pad-l bg-dark">
  <div class="wrap">
    <h2 style="max-width:16ch">Join our growing community</h2>
    <p class="lede" style="margin-bottom:3rem">Hundreds each month choose Livewell Passport to take control of their health story.</p>
    <div class="stats">
      <div class="stat"><b><span data-count="100">100</span><small>+</small></b><strong>Passports issued monthly</strong><span>We’re issuing more wellness passports every month as patients seek care that gets to the root of their symptoms.</span></div>
      <div class="stat"><b><span data-count="80">80</span><small>+</small></b><strong>Satisfied travelers</strong><span>Choosing health, one step at a time.</span></div>
      <div class="stat"><b><span data-count="30">30</span><small>%</small></b><strong>Off price package</strong><span>Limited time offer.</span></div>
    </div>
  </div>
</section>

<section class="pad-l bg-white">
  <div class="wrap split" data-reveal>
    <div class="photo"><img src="assets/img/womens.jpg" alt="A woman outdoors at sunrise, arms crossed and smiling" loading="lazy"></div>
    <div>
      <h2>Charting a course from primary care to whole-body wellness</h2>
      <p class="measure muted">We go beyond symptom management to uncover and treat the root causes of your health concerns. Blending advanced diagnostics with personalized care plans, we guide each patient on a unique journey toward lasting wellness, with expert providers by your side every step of the way.</p>
      <ul class="facts">
        <li>{tile("compass")}<div><strong>Wellness navigator</strong><span>Our licensed providers walk beside you, offering expert care, clear guidance and steady support on your journey toward lifelong, whole-person wellness.</span></div></li>
        <li>{tile("route")}<div><strong>The first step</strong><span>Your healing begins the moment you reach out. Our trusted providers create personalized, root-cause care plans that move with you.</span></div></li>
        <li>{tile("shield-check")}<div><strong>Your privacy, protected</strong><span>We guard your health data with the same care we give your wellness, securely and confidentially.</span></div></li>
      </ul>
    </div>
  </div>
</section>

{tech_section()}

<section class="pad-xl bg-dark">
  <div class="wrap pep" data-reveal>
    <div class="photo"><img src="assets/img/hormonal.jpg" alt="" loading="lazy">{stamp("LIVEWELL · PEPTIDES", "CLINICAL · GRADE", "RX", cls="entry-stamp")}<p class="cap">Proactive, science-backed healing without the side effects of the status quo.</p></div>
    <div>
      <h2>Rewriting the map with peptide therapy</h2>
      <p class="lede">Peptide therapy is changing the direction of modern healthcare, targeting the root of chronic conditions, aging and performance issues with precision. These naturally occurring compounds act as messengers in the body, helping repair tissue, regulate hormones, reduce inflammation and optimize cellular function.</p>
      <div class="pep-grid">
        <div>{tile("route")}<strong>Root-level healing</strong><span>Peptides work with your body’s natural systems, restoring balance at the cellular level.</span></div>
        <div>{tile("compass")}<strong>Beyond medication</strong><span>Unlike drugs that mask symptoms, peptides target the cause, helping the body repair and regenerate.</span></div>
        <div>{tile("hand-heart")}<strong>Tailored to you</strong><span>Protocols customized to your goals, whether you’re optimizing energy, aging better or healing faster.</span></div>
        <div>{tile("shield-check")}<strong>Safe travels</strong><span>Certified providers. Proven methods. Safe, secure and personalized.</span></div>
        <div>{tile("test-tube")}<strong>Purposeful care</strong><span>Expert guidance designed to protect your path to better living.</span></div>
        <div>{tile("bolt")}<strong>Resilience, built in</strong><span>Powerful, protected care, tailored to your path.</span></div>
      </div>
    </div>
  </div>
</section>

<section class="pad-l bg-white">
  <div class="wrap" data-reveal>
    <h2>Journeys worth sharing</h2>
    <p class="lede" style="margin-bottom:3rem">Discover how others found healing, clarity, and lasting change.</p>
    <p class="quote">“The staff is amazing and always willing to work with my schedule. I’ve noticed such a great transformation in such a short time.”</p>
    <p class="quote-by">Evan Rodriguez</p>
    <div class="stories">{stories}</div>
    <p style="margin-top:1.5rem"><a class="link-arrow" href="{INTRO_VIDEO}" target="_blank" rel="noopener">Play video: Livewell Passport {icon("arrow")}</a></p>
  </div>
</section>

<section class="pad-xl textured">
  <div class="wrap map-wrap" data-reveal>
    <div class="usmap"><img src="assets/img/us-map.png" alt="Map of the United States" loading="lazy">
      <span class="pin" style="left:80%;top:46%"><i></i><b>Midlothian, VA</b></span>
      <span class="pin" style="left:79%;top:84%"><i></i><b>Inlet Beach, FL</b></span>
    </div>
    <div>
      <h2>Your journey begins here</h2>
      <p class="lede">Multiple locations. One mission: your lasting wellness. New destinations are opening in the near future.</p>
      <div class="locs">{locs}</div>
    </div>
  </div>
</section>

<section class="pad-l bg-white">
  <div class="wrap faq-grid" data-reveal>
    <div><h2>We are here to help</h2><p class="muted">Whether you’re new to functional medicine or just curious about what’s included in Livewell Passport care, we’re here to guide you. From how appointments work to what results to expect, our FAQ covers the essentials.</p><a class="link-arrow" href="faqs.html">All questions and answers {icon("arrow")}</a></div>
    {faq_block([GENERAL_FAQ[1], GENERAL_FAQ[2], ("How is this different from seeing a regular doctor?", "Most traditional care stops at symptom relief. We dig deeper, mapping out your root causes and offering proactive, long-term strategies. It’s healthcare that travels further with you, not just a quick stop along the way."), GENERAL_FAQ[4]])}
  </div>
</section>
{closing()}'''
    return page(body, SITE, "Primary care covered by insurance, root-cause lab work and advanced therapies like peptides and hormone optimization. Midlothian, VA and Inlet Beach, FL.", 0, "home")

def journey(j):
    others = "".join(f'<a class="chip" href="{o["slug"]}.html">{o["name"]}</a>' for o in JOURNEYS if o is not j)
    bens = "".join(f'<div class="benefit">{tile(ic)}<div><h3>{t}</h3><p>{d}</p></div></div>' for ic, t, d in j["benefits"])
    pts = "".join(f'<div><h3>{t}</h3><p>{d}</p></div>' for t, d in j["points"])
    body = f'''
<section class="page-hero">
  <div class="wrap">
    <div class="crumbs"><a href="../index.html">Home</a>{icon("chev")}<a href="../index.html#journeys">Journeys</a>{icon("chev")}<span>{j["name"]}</span></div>
    <h1>{j["h1"]}</h1>
    <div class="hero-row"><p class="lede">{j["lede"]}</p><div class="hero-actions"><a class="btn btn-primary btn-lg" href="../contact.html">Start your journey {icon("arrow")}</a></div></div>
    <div class="page-bleed parallax"><img src="../assets/img/{j["img"]}" alt="" fetchpriority="high"></div>
  </div>
</section>
<section class="pad-l"><div class="wrap points" data-reveal>{pts}</div></section>
<section class="pad-l bg-silver textured"><div class="wrap" data-reveal>
  <h2>{j["benefits_title"]}</h2><p class="lede">{j["benefits_intro"]}</p>
  <div class="benefits">{bens}</div>
</div></section>
<section class="pad-l bg-white"><div class="wrap faq-grid" data-reveal>
  <div><h2>Questions along the way</h2><a class="link-arrow" href="../faqs.html">More questions and answers {icon("arrow")}</a></div>
  {faq_block(j["faq"])}
</div></section>
<section class="pad-m textured"><div class="wrap" data-reveal><h3>Other journeys</h3><div class="chips">{others}</div></div></section>
{closing(1)}'''
    return page(body, j["name"], j["lede"][:155], 1, j["slug"])


def faq_block(items, cls=""):
    out = [f'<div class="faq {cls}">']
    for q, a in items:
        out.append(f'<details><summary>{q}{icon("plus")}</summary><div class="a"><p>{a}</p></div></details>')
    out.append("</div>")
    return "".join(out)

# ---------------------------------------------------------------- home
# ---------------------------------------------------------------- journey pages
# ---------------------------------------------------------------- other pages
def locations_page():
    locs = "".join(f'''<div class="loc" id="{l["slug"]}">
      {stamp("ENTRY · " + l["st"], "LIVEWELL · PASSPORT", "OPEN", cls="entry-stamp")}
      <h3>{l["city"]}<small>{l["state"]}</small></h3>
      <address>{l["address"]}<br>{l["city_line"]}</address>
      <div class="row"><a href="tel:{l["tel"]}">{icon("phone")}{l["phone"]}</a><a href="https://www.google.com/maps/search/?api=1&query={html.escape((l["address"] + ", " + l["city_line"]).replace(" ", "+"))}" target="_blank" rel="noopener">{icon("pin")}Directions</a><a href="mailto:{EMAIL}">{icon("mail")}Email</a></div>
      <p class="muted" style="margin:0">Primary care, hormone optimization, weight management, peptides and more. Same-day appointments may be available for physicals.</p>
    </div>''' for l in LOCATIONS)
    body = f'''
<section class="page-hero pad-m textured"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a>{icon("chev")}<span>Locations</span></div>
  <h1>Where to find us</h1>
  <p class="lede">Physical locations in Midlothian, Virginia and Inlet Beach, Florida, with new destinations opening in the near future. Our secure telehealth platform makes it easy to connect from anywhere.</p>
  <div class="locations">{locs}</div>
</div></section>
<section class="pad-l bg-white"><div class="wrap split" data-reveal>
  <div><h2>Not sure which stop is right?</h2><p class="measure muted">We see sick patients for many common concerns, but we are not an urgent care center. If you’re unsure whether to visit us or an ER or urgent care, our team can help you decide.</p>
  <div class="hero-actions" style="justify-content:flex-start"><a class="btn btn-primary" href="contact.html">Start your journey {icon("arrow")}</a></div></div>
  <div class="photo wide"><img src="assets/img/beach.jpg" alt="A couple sitting on the sand at sunset beneath a palm tree" loading="lazy"></div>
</div></section>
{closing()}'''
    return page(body, "Locations", "Livewell Passport locations in Midlothian, Virginia and Inlet Beach, Florida, plus secure telehealth.", 0, "locations")

def contact_page():
    loc_opts = "".join(f'<option value="{l["slug"]}">{l["city"]}, {l["st"]}</option>' for l in LOCATIONS) + '<option value="telehealth">Telehealth</option>'
    j_opts = "".join(f'<option value="{j["slug"]}">{j["name"]}</option>' for j in JOURNEYS)
    sides = "".join(f'''<div class="side-card"><h3>{l["city"]}, {l["st"]}</h3><address>{l["address"]}<br>{l["city_line"]}</address>
      <a href="tel:{l["tel"]}">{icon("phone")}{l["phone"]}</a></div>''' for l in LOCATIONS)
    body = f'''
<section class="page-hero pad-m textured"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a>{icon("chev")}<span>Start your journey</span></div>
  <h1>Book your first stop</h1>
  <p class="lede">Fill out the form and our team will be in touch shortly. Whether you’re ready to book your first visit or simply have questions, we’re here to help you navigate the path ahead.</p>
  <div class="contact-grid">
    <div>
      <form class="form" novalidate data-endpoint="" aria-describedby="form-help">
        <div class="form-row">
          <div class="field"><label for="f-name">Full name</label><input id="f-name" name="name" type="text" autocomplete="name" required><span class="error" aria-live="polite"></span></div>
          <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email" required><span class="error" aria-live="polite"></span></div>
        </div>
        <div class="form-row">
          <div class="field"><label for="f-phone">Phone <span class="hint">(optional)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"><span class="error" aria-live="polite"></span></div>
          <div class="field"><label for="f-location">Preferred location</label><select id="f-location" name="location" required><option value="">Choose one</option>{loc_opts}</select><span class="error" aria-live="polite"></span></div>
        </div>
        <div class="field"><label for="f-journey">What brings you in? <span class="hint">(optional)</span></label><select id="f-journey" name="journey"><option value="">Primary care or not sure yet</option>{j_opts}</select></div>
        <div class="field"><label for="f-message">Anything we should know? <span class="hint">(optional)</span></label><textarea id="f-message" name="message" placeholder="Symptoms, goals, or questions about insurance"></textarea></div>
        <div class="field check-field"><label class="check"><input id="f-consent" name="consent" type="checkbox"><span>I agree to be contacted by phone, email or text about scheduling. Message and data rates may apply. Reply STOP to opt out. Consent is not a condition of treatment.</span></label><span class="error" aria-live="polite"></span></div>
        <div><button class="btn btn-primary" type="submit">Send request {icon("arrow")}</button></div>
        <p class="form-note" id="form-help">Fill out the form and our team will be in touch shortly.</p>
      </form>
      <div class="form-success" tabindex="-1" aria-live="polite">
        <h3>Thanks, <span data-name></span>.</h3>
        <p class="delivered">Your request is in. Our team will be in touch shortly.</p>
        <p class="not-delivered">This preview isn’t connected to the clinic’s inbox yet. To book now, email <a href="mailto:{EMAIL}">{EMAIL}</a> or call {LOCATIONS[0]["phone"]} (Midlothian) or {LOCATIONS[1]["phone"]} (Inlet Beach).</p>
      </div>
    </div>
    <div style="display:grid;gap:1rem">
      {sides}
      <div class="side-card"><h3>Prefer email?</h3><a href="mailto:{EMAIL}">{icon("mail")}{EMAIL}</a><p class="muted" style="margin:0">Current patients can also message us through the <a href="portal.html">patient portal</a>.</p></div>
    </div>
  </div>
</div></section>'''
    return page(body, "Start your journey", "Book your first visit with Livewell Passport in Midlothian, VA, Inlet Beach, FL or by telehealth.", 0, "contact")

def faqs_page():
    body = f'''
<section class="page-hero pad-m textured"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a>{icon("chev")}<span>FAQs</span></div>
  <h1>Every journey starts with questions</h1>
  <p class="lede">Informed patients make empowered decisions. Here is how our process works, from insurance-covered primary care to advanced treatments like peptides, so you can feel confident before you walk through the door.</p>
  <div style="max-width:800px">{faq_block(GENERAL_FAQ)}</div>
</div></section>
{closing()}'''
    return page(body, "FAQs", "Answers about insurance, primary care, functional medicine, telehealth, hormones, peptides and GLP-1s at Livewell Passport.", 0, "faqs")

def portal_page():
    body = f'''
<section class="page-hero pad-m textured"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a>{icon("chev")}<span>Patient portal</span></div>
  <h1>Livewell Passport portal</h1>
  <p class="lede">Login to the LWP portal.</p>
  <div class="portal-grid">
    <div class="portal-card"><span class="tag">Practice / client access</span><h3>Practice portal</h3><p>Practice and client access to the Livewell portal.</p><a class="btn btn-primary" href="{PORTAL_URL}" target="_blank" rel="noopener">Open the practice portal {icon("arrow")}</a></div>
    <div class="portal-card soon"><span class="tag">Coming soon</span><h3>Patient portal</h3><p>The patient portal is coming soon. For help signing in, email <a href="mailto:{EMAIL}">{EMAIL}</a> for help signing in.</p></div>
  </div>
</div></section>
{closing(0, "New here? Your first stop is one visit away.")}'''
    return page(body, "Patient portal", "Sign in to the Livewell Passport practice portal. Patient portal coming soon.", 0, "portal")

def policies_page():
    body = f'''
<section class="page-hero pad-m textured"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a>{icon("chev")}<span>Cancellation, billing &amp; refund policy</span></div>
  <h1>Cancellation, billing and refund policy</h1>
  <div class="prose">
    <h2>Cancellation notice requirement</h2>
    <p>All Livewell Passport memberships, subscription services and recurring charges require a minimum of thirty (30) days’ written notice to cancel. It is the sole responsibility of the patient to initiate and confirm cancellation if services are no longer desired.</p>
    <h2>Ongoing billing and responsibility</h2>
    <p>Until a cancellation request has been properly submitted and the 30-day notice period has been completed, monthly billing will continue without interruption. Failure to cancel in accordance with this policy constitutes authorization for continued billing.</p>
    <h2>No refund policy</h2>
    <p>All charges are final and non-refundable once processed. This includes, but is not limited to:</p>
    <ul><li>Membership fees</li><li>Subscription or recurring charges</li><li>Services rendered or made available</li><li>Charges incurred during the 30-day cancellation notice period</li></ul>
    <p>Livewell Passport does not issue refunds, credits or prorated adjustments for unused services, partial months, missed appointments or failure to cancel.</p>
    <h2>Medical services disclaimer</h2>
    <p>Livewell Passport provides access to wellness-related medical services, consultations and membership-based programs. Membership fees cover access and administrative availability, not guaranteed treatment outcomes or specific medical results.</p>
    <h2>HIPAA and patient responsibility</h2>
    <p>All patient information is handled in compliance with the Health Insurance Portability and Accountability Act (HIPAA). Cancellation of services does not affect Livewell Passport’s obligation to retain medical records as required by law. Patients remain responsible for any outstanding balances incurred prior to or during the cancellation notice period.</p>
    <h2>Agreement and acknowledgment</h2>
    <p>By enrolling in Livewell Passport services, the patient acknowledges, understands and agrees to:</p>
    <ul><li>The 30-day cancellation requirement</li><li>Ongoing billing until cancellation is completed</li><li>The non-refundable nature of all charges once processed</li></ul>
    <p>Questions about billing: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</div></section>'''
    return page(body, "Cancellation, billing and refund policy", "Livewell Passport membership cancellation, billing and refund policy.", 0, "policies")

def legal_pages():
    """Converts the crawled privacy notice and terms into prose pages, unchanged in substance."""
    txt = open(os.path.join(SRC, "legal.txt"), encoding="utf-8").read()
    parts = re.split(r"^=+ (\S+) \| .*$", txt, flags=re.M)
    docs = {}
    for i in range(1, len(parts), 2):
        docs[parts[i]] = parts[i + 1]
    def render(raw, title):
        lines = [l.rstrip() for l in raw.split("\n")]
        # drop everything from footer tagline onward and the duplicated title lines
        cut = next((k for k, l in enumerate(lines) if l.startswith("Your Healthcare Journey Reimagined")), len(lines))
        lines = lines[:cut]
        out, ul = [], False
        for l in lines:
            if not l.strip() or l in (f"{title} - Livewell Passport", "[h2] Livewell Passport", f"[h2] {title}"): continue
            if l.startswith("•"):
                if not ul: out.append("<ul>"); ul = True
                out.append(f"<li>{html.escape(l[1:].strip())}</li>"); continue
            if ul: out.append("</ul>"); ul = False
            m = re.match(r"\[h(\d)\]\s*(.*)", l)
            if m:
                if not m.group(2).strip(): continue
                lvl = {"2": "h2", "3": "h2", "4": "h3"}[m.group(1)]
                out.append(f"<{lvl}>{html.escape(m.group(2).strip())}</{lvl}>")
            elif l.lower().startswith("last updated"):
                out.append(f'<p class="last-updated">{html.escape(l)}</p>')
            else:
                out.append(f"<p>{html.escape(l)}</p>")
        if ul: out.append("</ul>")
        return "".join(out)
    pages = {}
    for key, title, fname, desc in [("privacy.html", "Privacy Policy", "privacy", "Livewell Passport privacy policy and HIPAA notice of privacy practices."),
                                    ("terms.html", "Terms and Conditions", "terms", "Livewell Passport website terms and conditions.")]:
        body = f'''
<section class="page-hero pad-m textured"><div class="wrap">
  <div class="crumbs"><a href="index.html">Home</a>{icon("chev")}<span>{title}</span></div>
  <h1>{title}</h1>
  <div class="prose">{render(docs[key], title)}</div>
</div></section>'''
        pages[fname] = page(body, title, desc, 0, fname)
    return pages

def notfound_page():
    body = f'''
<section class="page-hero pad-m textured"><div class="wrap nf">
  <h1>404</h1>
  <h2>This stop isn’t on the map.</h2>
  <p class="lede">The page may have moved. Try one of these routes instead.</p>
  <div class="chips"><a class="chip" href="index.html">Home</a><a class="chip" href="index.html#journeys">Journeys</a><a class="chip" href="locations.html">Locations</a><a class="chip" href="faqs.html">FAQs</a><a class="chip" href="contact.html">Start your journey</a></div>
</div></section>'''
    return page(body, "Page not found", "That page isn’t on the map.", 0, "404")

# ---------------------------------------------------------------- build
def write(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f: f.write(s)

def main():
    for d in (DIST, ART):
        if os.path.isdir(d): shutil.rmtree(d)
        os.makedirs(os.path.join(d, "journeys"))
        shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(d, "assets"))
        shutil.copy(os.path.join(SRC, "styles.css"), d)
        shutil.copy(os.path.join(SRC, "site.js"), d)
    outputs = {"index.html": home(), "locations.html": locations_page(), "contact.html": contact_page(), "faqs.html": faqs_page(),
               "portal.html": portal_page(), "policies.html": policies_page(), "404.html": notfound_page()}
    for k, v in legal_pages().items(): outputs[f"{k}.html"] = v
    for j in JOURNEYS: outputs[f"journeys/{j['slug']}.html"] = journey(j)
    for name, (full, inner) in outputs.items():
        write(os.path.join(DIST, name), full)
        # artifact: the main page has no document skeleton; every other page is served raw and keeps its own
        write(os.path.join(ART, name), inner if name == "index.html" else full)
    print(f"built {len(outputs)} pages → dist/ and dist-artifact/")

if __name__ == "__main__":
    main()
