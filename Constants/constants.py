import pygame


Info = pygame.display.Info()
width = Info.current_w
height = Info.current_h
SIZE = (width, height)
FPS = 60
duration = 60 * 15 # 30 minutes

states = ["intro", "puzzle1_intro", "puzzle1", "puzzle2_intro", "puzzle2", "puzzle3_intro", "puzzle3", "summary1", "summary2", "summary3", "retry"]



intro1_title = "The Deceptive Inbox"
intro1_txt = ("You have new emails waiting. Some are normal, but not all of them.\n\n"
            "Your task: open each email, read it carefully, and decide whether it"
            " is a real email or a phishing attempt trying to trick you into clicking something "
            "dangerous or giving up sensitive information, like passwords, bank details, etc.\n\n"
            "When you have classified all five emails, submit your answers.\n\n"
            "Tip: Take your time, attackers design their emails to look convincing at first glance."
            " Read every sender address character by character and take rational, not emotional decisions.\n"
             "\n\n" 
            "Click the ENTER button if you want to submit your answer")

intro2_title = "The Profile Problem"
intro2_txt = ("A friend has asked you to help them check whether their account is secure.\n\n"
                "You will see their public social media profile, with the kind of information "
                "millions of people share online every day. Your job is to try to guess their password "
                "using only what you can see on that profile.\n\n"
                "If you succeed, and you probably will, then you might realise how dangerous it could be to "
                "have such information publicly available. Afterwards you will chose one password you "
                "think is safe and hard, or even almost impossible, to guess.")

intro3_title = "The Café Connection"
intro3_txt = ("You are on a break at a café and need to quickly check something online.\n\n"
                "This challenge has three parts: choosing a safe Wi-Fi network, " 
                "verifying that a website is safe before entering your details, and "
                "deciding which actions are risky on a public connection.\n\n"
                "No technical knowledge needed, just think about what you already "
                "know about privacy and common sense.")

summary1_title = "SECTION 1: Phishing & Social Engineering"
summary1_txt= ("Phishing is when an attacker pretends to be someone you trust, like"
               " your bank, Microsoft, PayPal, among others, to trick you into clicking "
               "a link or giving away your password. It accounts for the majority of cybersecurity "
               "incidents worldwide because it targets human psychology, not technology.\n\n"
               "\n\n"
               "Key red flags to always check:\n\n"
               "Read sender addresses character by character, 'rnicrosoft.com' and 'paypa1.com'"
               " may seem real, but they are not.\n\n"
               "- Hover over any link before clicking to see where it actually goes.\n\n"
               "- Urgency and threats ('your account will be closed') are designed to stop you "
               "from thinking. Real companies give you time.\n\n"
               "- No legitimate service will ever ask for your password by email.")

summary2_title = "SECTION 2: Password Security"
summary2_txt = ("Passwords that use personal information, names, birthdays, pets, favourite items,"
                "are the first things attackers try. Automated tools can test million of combinations "
                "per second using publicly available information.\n\n"
                "\n\n"
                "What makes a strong password:\n\n"
                "- Length matters most, at least 12 characters, 16 is better.\n\n"
                "- Use a passphrase: three unrelated words + numbers + symbols.\n\n"
                "Example: Lamp!River93#Desk"
                "- Never reuse a password across different sites. If one site is breached, "
                "attackers will try your password everywhere else. This is called credential stuffing.\n\n"
                "- Use a free password manager (Bitwarden, KeePass) to generate "
                "and store strong unique passwords, so you only need to remember one master password.")

summary3_title = "SECTION 3: Public Networks & Encryption"
summary3_txt = ("An open Wi-Fi network sends all your data without encryption. Anyone nearby with "
                "a free app can capture and read your passwords, messages, and browsing,"
                " this is called network sniffing. It is passive and invisible.\n\n"
                "\n\n"
                "How to stay safe on any network:\n\n"
                "- Always check for https:// and the padlock icon before entering "
                "any sensitive information. The 's' means the connection is encrypted.\n\n"
                "- On public or open Wi-Fi, only browse and read. Never log into "
                "banking, email, or shopping accounts.\n\n"
                "- A VPN (Virtual Private Network) encrypts all your traffic even on open network. "
                "Many free and affordable options exist (ProtonVPN, Mullvad).\n\n"
                "- Be sceptical of unknown hotspots, an 'evil twin' network set up "
                "by an attacker looks identical to a real café network.")

EMAIL_DATA_POOL = [
    {
        "id": "legit_amazon",
        "sender": "shipment-tracking@amazon.com",
        "recipient": "you@email.com",
        "title": "Your order has been dispatched!",
        "txt": ("Good news! Your recent order has been dispatched and is on its way.\n\n"
                "Tracking number: TBA294817563\n"
                "Estimated delivery: 2-3 business days\n\n"
                "You can track your package anytime from your Amazon orders page. "
                "No action is needed from you at this time.\n\n"
                "Thank you for shopping with us."),
        "phishing": False,
    },
    {
        "id": "legit_newsletter",
        "sender": "weekly@medium-digest.com",
        "recipient": "you@email.com",
        "title": "Your weekly reading digest is ready",
        "txt": ("Here's what's trending this week:\n\n"
                "- The Future of Quantum Computing: Where Are We Really?\n"
                "- 10 Lessons From a Decade in Software Engineering\n"
                "- Why Minimalism Is Making a Comeback in Design\n\n"
                "Click through to read the full articles, or manage your "
                "subscription preferences at any time from your account settings."),
        "phishing": False,
    },
    {
        "id": "legit_calendar",
        "sender": "calendar-noreply@google.com",
        "recipient": "you@email.com",
        "title": "Reminder: Dentist appointment tomorrow at 10:30",
        "txt": ("This is a reminder for the following event:\n\n"
                "Dentist appointment\n"
                "Tomorrow, 10:30 - 11:15\n"
                "Location: Cabinet Dentaire Belval\n\n"
                "This event was added to your calendar. "
                "You can edit or remove it directly from your Google Calendar."),
        "phishing": False,
    },
    {
        "id": "legit_bank_statement",
        "sender": "statements@ing.lu",
        "recipient": "you@email.com",
        "title": "Your May account statement is available",
        "txt": ("Dear Customer,\n\n"
                "Your account statement for May is now available to view in your "
                "online banking portal under Documents > Statements.\n\n"
                "For your security, this email does not contain any links. "
                "Please log in directly through the ING app or by typing ing.lu "
                "into your browser to access your statement.\n\n"
                "ING Luxembourg"),
        "phishing": False,
    },
    {
        "id": "phish_microsoft_typo",
        "sender": "support@rnicrosoft.com",
        "recipient": "you@email.com",
        "title": "URGENT: Your Microsoft account will be suspended",
        "txt": ("Dear User,\n\n"
                "We have detected unusual activity on your Microsoft account. "
                "Your account will be SUSPENDED within 24 hours unless you verify "
                "your identity immediately.\n\n"
                "Click here to verify now: http://rnicrosoft-secure-verify.com/login\n\n"
                "Failure to act will result in permanent loss of access to your "
                "files and emails.\n\n"
                "Microsoft Account Team"),
        "phishing": True,
        "red_flags": [
            "Typosquatting sender domain — 'rnicrosoft.com' uses 'rn' to mimic 'm'",
            "Artificial urgency — a 24-hour suspension threat to force quick action",
            "Suspicious link domain — does not match any real Microsoft domain",
            "Illegitimate credential request — real Microsoft never asks you to verify via an emailed link like this",
        ],
    },
    {
        "id": "phish_bank_cyrillic",
        "sender": "security@ing-lU.com",
        "recipient": "you@email.com",
        "title": "Action required: Suspicious transaction on your account",
        "txt": ("Dear Client,\n\n"
                "We detected a suspicious transaction of €1,450.00 on your account. "
                "If you do not recognize this transaction, you must verify your "
                "identity within 2 HOURS or your account will be frozen.\n\n"
                "Verify here: http://ing-lu-secure-banking.com/verify\n\n"
                "ING Security Team"),
        "phishing": True,
        "red_flags": [
            "Wrong sender domain — 'ing-lU.com' does not match the real 'ing.lu'",
            "Extreme urgency — a 2-hour threat designed to bypass careful thinking",
            "Unregistered/unofficial link domain — not ing.lu",
            "Real banks never send clickable login links in emails asking you to verify your account",
        ],
    },
]

SARAH_NAME   = "Sarah Mitchell"
SARAH_HANDLE = "@sarah_m_lux"
SARAH_BIO    = (
    "Birthday: 14 March 1990\n"
    "Location: Luxembourg City\n"
    "Dog: Biscuit\n"
    "Favourite club: Chelsea FC\n"
    "Favourite player: Ronaldo\n\n"
    "\n"
    "Recent posts:\n"
    "- Happy bday Biscuit! My dog turns 4!\n"
    "- CHELSEA FOREVER!! What a match!\n"
    "- Another year older, March 14th!\n"
    "- Ronaldo is the GOAT, no debate."
)

PASSWORD_POOL = [
    {"pwd": "Biscuit2022",       "personal": True,
     "why": "Her dog's name + a year. Visible in her posts."},
    {"pwd": "Chelsea1990",       "personal": True,
     "why": "Favourite club + birth year. Both on her profile."},
    {"pwd": "Sarah_14March",     "personal": True,
     "why": "Her first name + birthday. Right there in her bio."},
    {"pwd": "Ronaldo7star",      "personal": True,
     "why": "Her favourite player. She posted about it publicly."},
    {"pwd": "qX9mL42vPk",        "personal": False,
     "why": "Random string. Impossible to guess from her profile."},
    {"pwd": "sunshine",          "personal": False,
     "why": "Common word. Easy to crack, but not personal to her."},
    {"pwd": "password123",       "personal": False,
     "why": "Most common password in the world. Not from her profile."},
    {"pwd": "Biscuit_Chelsea07", "personal": True,
     "why": "Dog name + club combined. Both obvious from her profile."},
]

STRONG_OPTIONS = [
    {"pwd": "Biscuit2022",         "strong": False,
     "why": "Contains her dog's name. Easy to guess from her profile."},
    {"pwd": "Chelsea1990",         "strong": False,
     "why": "Club + birth year. An attacker who knows her could guess this instantly."},
    {"pwd": "sunshine",            "strong": False,
     "why": "A common dictionary word. Cracked in under a second."},
    {"pwd": "Lamp!River93Desk",    "strong": True,
     "why": "Three unrelated words + numbers + symbol. Long and unpredictable."},
    {"pwd": "password123",         "strong": False,
     "why": "The most common password in the world. Never use this."},
    {"pwd": "March14Biscuit",      "strong": False,
     "why": "Combines her birthday and dog name. Completely guessable."},
]

NETWORKS_BASE = [
    {
        "name":   "CafeLux_FreeWiFi",
        "detail": "Open - no password required",
        "secure": False,
        "reason": (
            "Open networks send your data without any encryption. "
            "Think of it like talking loudly in a crowded room - anyone nearby "
            "can listen in. An attacker with a free app can read everything "
            "you send or receive, including passwords. This is called network sniffing."
        ),
    },
    {
        "name":   "CafeLux_Secured_5G",
        "detail": "Password protected (WPA2)",
        "secure": True,
        "reason": "",
    },
    {
        "name":   "Free_Internet_Guest",
        "detail": "Open - no password required",
        "secure": False,
        "reason": (
            "The word Guest sounds official but means nothing about security. "
            "This is still an open, unencrypted network. "
            "Anyone nearby can capture everything you send and receive."
        ),
    },
    {
        "name":   "iPhone_hotspot_8821",
        "detail": "Personal hotspot - unknown owner",
        "secure": False,
        "reason": (
            "A stranger's hotspot can be a deliberate trap. "
            "The person who owns that device can see all your internet traffic. "
            "Only ever use a hotspot from a device you personally own or trust."
        ),
    },
]

URLS_BASE = [
    {
        "bar":     "[LOCK]  https://mybank.lu/login",
        "detail":  "Secure - encrypted connection (https)",
        "secure":  True,
        "bar_col": (0, 130, 0),
        "feedback": (
            "Correct. The s in https stands for secure. "
            "The lock symbol confirms the connection is encrypted, meaning your "
            "login details cannot be read by anyone intercepting the traffic. "
            "Always look for https and the lock before entering any sensitive information."
        ),
    },
    {
        "bar":     "[!]  http://mybank.lu/login",
        "detail":  "Not secure - unencrypted (http only)",
        "secure":  False,
        "bar_col": (180, 0, 0),
        "feedback": (
            "This address uses http without the s and has no lock symbol. "
            "Your username and password travel as plain readable text "
            "and could be captured by anyone on the same network. "
            "Never enter sensitive details on a page without https."
        ),
    },
]

ACTIONS_BASE = [
    {"text": "Check the weather forecast",              "safe": True},
    {"text": "Log in to your online banking",           "safe": False},
    {"text": "Read a news article",                     "safe": True},
    {"text": "Enter your credit card details",          "safe": False},
    {"text": "Watch a video online",                    "safe": True},
    {"text": "Send a work email with private content",  "safe": False},
]

