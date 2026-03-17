# ============================================================
# sources.py — All 65+ RSS feeds, tiered by trust level
# Tier 1 = wire services / top outlets (highest trust)
# Tier 2 = reliable niche / regional outlets
# Tier 3 = social signals only (trend boost, never primary)
# ============================================================

SOURCES = [

    # ─────────────────────────────────────────────
    # WORLD — General News (Tier 1)
    # ─────────────────────────────────────────────
    {"name": "Reuters",           "url": "https://feeds.reuters.com/reuters/topNews",              "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "AP News",           "url": "https://rsshub.app/apnews/topics/apf-topnews",           "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "BBC World",         "url": "http://feeds.bbci.co.uk/news/world/rss.xml",             "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "BBC Top Stories",   "url": "http://feeds.bbci.co.uk/news/rss.xml",                   "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "Al Jazeera",        "url": "https://www.aljazeera.com/xml/rss/all.xml",              "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "The Guardian",      "url": "https://www.theguardian.com/world/rss",                  "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "DW News",           "url": "https://rss.dw.com/rdf/rss-en-all",                     "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "France 24",         "url": "https://www.france24.com/en/rss",                       "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "NPR",               "url": "https://feeds.npr.org/1001/rss.xml",                    "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "Euronews",          "url": "https://www.euronews.com/rss",                          "tier": 2, "region": "world", "category": "World Affairs"},
    {"name": "Sky News",          "url": "https://feeds.skynews.com/feeds/rss/world.xml",         "tier": 2, "region": "world", "category": "World Affairs"},
    {"name": "The Independent",   "url": "https://www.independent.co.uk/news/world/rss",          "tier": 2, "region": "world", "category": "World Affairs"},
    {"name": "Google News World", "url": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", "tier": 2, "region": "world", "category": "World Affairs"},

    # ─────────────────────────────────────────────
    # WORLD — Technology (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "TechCrunch",        "url": "https://techcrunch.com/feed/",                          "tier": 1, "region": "world", "category": "Technology"},
    {"name": "The Verge",         "url": "https://www.theverge.com/rss/index.xml",                "tier": 1, "region": "world", "category": "Technology"},
    {"name": "Wired",             "url": "https://www.wired.com/feed/rss",                        "tier": 1, "region": "world", "category": "Technology"},
    {"name": "Ars Technica",      "url": "http://feeds.arstechnica.com/arstechnica/index",        "tier": 1, "region": "world", "category": "Technology"},
    {"name": "MIT Tech Review",   "url": "https://www.technologyreview.com/feed/",                "tier": 1, "region": "world", "category": "Technology"},
    {"name": "VentureBeat",       "url": "https://feeds.feedburner.com/venturebeat/SZYF",         "tier": 2, "region": "world", "category": "Technology"},
    {"name": "ZDNet",             "url": "https://www.zdnet.com/news/rss.xml",                    "tier": 2, "region": "world", "category": "Technology"},
    {"name": "Hacker News",       "url": "https://hnrss.org/frontpage",                          "tier": 2, "region": "world", "category": "Technology"},
    {"name": "Google AI Blog",    "url": "https://blog.google/technology/ai/rss/",               "tier": 2, "region": "world", "category": "Technology"},
    {"name": "Google News Tech",  "url": "https://news.google.com/rss/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB", "tier": 2, "region": "world", "category": "Technology"},

    # ─────────────────────────────────────────────
    # WORLD — Business (Tier 1)
    # ─────────────────────────────────────────────
    {"name": "Bloomberg",         "url": "https://feeds.bloomberg.com/markets/news.rss",          "tier": 1, "region": "world", "category": "Business & Economy"},
    {"name": "Financial Times",   "url": "https://www.ft.com/rss/home",                          "tier": 1, "region": "world", "category": "Business & Economy"},
    {"name": "Reuters Business",  "url": "https://feeds.reuters.com/reuters/businessNews",        "tier": 1, "region": "world", "category": "Business & Economy"},
    {"name": "CNBC",              "url": "https://feeds.nbcnews.com/nbcnews/public/business",     "tier": 1, "region": "world", "category": "Business & Economy"},
    {"name": "The Economist",     "url": "https://www.economist.com/finance-and-economics/rss.xml","tier": 1, "region": "world", "category": "Business & Economy"},
    {"name": "Forbes",            "url": "https://www.forbes.com/business/feed/",                "tier": 2, "region": "world", "category": "Business & Economy"},

    # ─────────────────────────────────────────────
    # WORLD — Science (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "NASA",              "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss",       "tier": 1, "region": "world", "category": "Science & Space"},
    {"name": "Nature",            "url": "https://www.nature.com/nature.rss",                    "tier": 1, "region": "world", "category": "Science & Space"},
    {"name": "New Scientist",     "url": "https://www.newscientist.com/feed/home",               "tier": 2, "region": "world", "category": "Science & Space"},
    {"name": "Science Daily",     "url": "https://www.sciencedaily.com/rss/all.xml",             "tier": 2, "region": "world", "category": "Science & Space"},
    {"name": "Space.com",         "url": "https://www.space.com/feeds/all",                      "tier": 2, "region": "world", "category": "Science & Space"},
    {"name": "Phys.org",          "url": "https://phys.org/rss-feed/",                          "tier": 2, "region": "world", "category": "Science & Space"},

    # ─────────────────────────────────────────────
    # WORLD — Health (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "WHO",               "url": "https://www.who.int/rss-feeds/news-english.xml",       "tier": 1, "region": "world", "category": "Health & Medicine"},
    {"name": "Reuters Health",    "url": "https://feeds.reuters.com/reuters/healthNews",         "tier": 1, "region": "world", "category": "Health & Medicine"},
    {"name": "Medical News Today","url": "https://www.medicalnewstoday.com/rss",                 "tier": 2, "region": "world", "category": "Health & Medicine"},
    {"name": "WebMD",             "url": "https://rssfeeds.webmd.com/rss/rss.aspx?RSSSource=RSS_PUBLIC", "tier": 2, "region": "world", "category": "Health & Medicine"},

    # ─────────────────────────────────────────────
    # WORLD — Environment (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "Guardian Environment","url": "https://www.theguardian.com/environment/rss",        "tier": 1, "region": "world", "category": "Environment & Climate"},
    {"name": "Reuters Environment","url": "https://feeds.reuters.com/reuters/environment",       "tier": 1, "region": "world", "category": "Environment & Climate"},
    {"name": "Carbon Brief",      "url": "https://www.carbonbrief.org/feed",                    "tier": 2, "region": "world", "category": "Environment & Climate"},
    {"name": "Yale E360",         "url": "https://e360.yale.edu/feed",                          "tier": 2, "region": "world", "category": "Environment & Climate"},

    # ─────────────────────────────────────────────
    # WORLD — Sports (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "ESPN",              "url": "https://www.espn.com/espn/rss/news",                   "tier": 1, "region": "world", "category": "Sports"},
    {"name": "BBC Sport",         "url": "http://feeds.bbci.co.uk/sport/rss.xml",               "tier": 1, "region": "world", "category": "Sports"},
    {"name": "Reuters Sports",    "url": "https://feeds.reuters.com/reuters/sportsNews",         "tier": 1, "region": "world", "category": "Sports"},
    {"name": "Sky Sports",        "url": "https://www.skysports.com/rss/12040",                 "tier": 2, "region": "world", "category": "Sports"},

    # ─────────────────────────────────────────────
    # WORLD — Fact Check (Tier 1)
    # ─────────────────────────────────────────────
    {"name": "Reuters Fact Check","url": "https://feeds.reuters.com/reuters/factcheck",          "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "AFP Fact Check",    "url": "https://factcheck.afp.com/list/rss",                  "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "PolitiFact",        "url": "https://www.politifact.com/feeds/statements/truth-o-meter/", "tier": 2, "region": "world", "category": "Politics"},
    {"name": "Snopes",            "url": "https://www.snopes.com/feed/",                        "tier": 2, "region": "world", "category": "World Affairs"},

    # ─────────────────────────────────────────────
    # WORLD — Social Signals (Tier 3)
    # ─────────────────────────────────────────────
    {"name": "Reddit WorldNews",  "url": "https://www.reddit.com/r/worldnews/.rss",             "tier": 3, "region": "world", "category": "World Affairs"},
    {"name": "Reddit Technology", "url": "https://www.reddit.com/r/technology/.rss",            "tier": 3, "region": "world", "category": "Technology"},
    {"name": "Reddit Science",    "url": "https://www.reddit.com/r/science/.rss",               "tier": 3, "region": "world", "category": "Science & Space"},

    # ─────────────────────────────────────────────
    # INDIA — General News (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "NDTV",              "url": "https://feeds.feedburner.com/ndtvnews-top-stories",    "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "Times of India",    "url": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "The Hindu",         "url": "https://www.thehindu.com/feeder/default.rss",         "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "Hindustan Times",   "url": "https://www.hindustantimes.com/rss/topnews/rssfeed.xml","tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "India Today",       "url": "https://www.indiatoday.in/rss/home",                  "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "Indian Express",    "url": "https://indianexpress.com/feed/",                     "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "ANI",               "url": "https://www.aninews.in/rss/",                        "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "News18 India",      "url": "https://www.news18.com/rss/india.xml",               "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "Scroll.in",         "url": "https://scroll.in/feed",                             "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "The Wire",          "url": "https://thewire.in/feed",                            "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "The Print",         "url": "https://theprint.in/feed",                           "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "Google News India", "url": "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en","tier": 2, "region": "india", "category": "World Affairs"},

    # ─────────────────────────────────────────────
    # INDIA — Business (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "Economic Times",    "url": "https://economictimes.indiatimes.com/rssfeedstopstories.cms", "tier": 1, "region": "india", "category": "Business & Economy"},
    {"name": "Mint",              "url": "https://www.livemint.com/rss/news",                   "tier": 1, "region": "india", "category": "Business & Economy"},
    {"name": "Business Standard", "url": "https://www.business-standard.com/rss/home_page_top_stories.rss", "tier": 1, "region": "india", "category": "Business & Economy"},
    {"name": "Financial Express", "url": "https://www.financialexpress.com/feed/",             "tier": 2, "region": "india", "category": "Business & Economy"},
    {"name": "Moneycontrol",      "url": "https://www.moneycontrol.com/rss/MCtopnews.xml",    "tier": 2, "region": "india", "category": "Business & Economy"},
    {"name": "CNBC TV18",         "url": "https://www.cnbctv18.com/commonfeeds/v1/eng/rss/economy.xml", "tier": 2, "region": "india", "category": "Business & Economy"},

    # ─────────────────────────────────────────────
    # INDIA — Technology (Tier 2)
    # ─────────────────────────────────────────────
    {"name": "YourStory",         "url": "https://yourstory.com/feed",                         "tier": 2, "region": "india", "category": "Technology"},
    {"name": "Inc42",             "url": "https://inc42.com/feed/",                            "tier": 2, "region": "india", "category": "Technology"},
    {"name": "NDTV Tech",         "url": "https://feeds.feedburner.com/NdtvNews-Tech",         "tier": 2, "region": "india", "category": "Technology"},
    {"name": "ET Tech",           "url": "https://economictimes.indiatimes.com/tech/rssfeeds/13357270.cms", "tier": 2, "region": "india", "category": "Technology"},
    {"name": "MediaNama",         "url": "https://www.medianama.com/feed/",                   "tier": 2, "region": "india", "category": "Technology"},
    {"name": "Entrackr",          "url": "https://entrackr.com/feed/",                        "tier": 2, "region": "india", "category": "Technology"},

    # ─────────────────────────────────────────────
    # INDIA — Sports (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "Cricbuzz",          "url": "https://www.cricbuzz.com/rss-feeds/cricket-news",    "tier": 1, "region": "india", "category": "Sports"},
    {"name": "ESPN Cricinfo",     "url": "https://static.espncricinfo.com/rss/content/story/feeds/0.xml", "tier": 1, "region": "india", "category": "Sports"},
    {"name": "NDTV Sports",       "url": "https://feeds.feedburner.com/NdtvNews-Sports",      "tier": 2, "region": "india", "category": "Sports"},
    {"name": "The Bridge",        "url": "https://thebridge.in/feed/",                        "tier": 2, "region": "india", "category": "Sports"},
    {"name": "Sportskeeda",       "url": "https://www.sportskeeda.com/feed",                  "tier": 2, "region": "india", "category": "Sports"},

    # ─────────────────────────────────────────────
    # INDIA — Fact Check (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "BOOM Live",         "url": "https://www.boomlive.in/feed",                      "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "Alt News",          "url": "https://www.altnews.in/feed/",                      "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "Factly",            "url": "https://factly.in/feed/",                           "tier": 2, "region": "india", "category": "World Affairs"},

    # ─────────────────────────────────────────────
    # INDIA — Regional Google News (Tier 2)
    # ─────────────────────────────────────────────
    {"name": "Google News Hindi",       "url": "https://news.google.com/rss?hl=hi&gl=IN&ceid=IN:hi",  "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "Google News Tamil Nadu",  "url": "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en&topic=CAAqIQgKIhtDQkFTRGdvSUwyMHZNRE53ZGpRU0FtVnVLQUFQAQ", "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "Google News Karnataka",   "url": "https://news.google.com/rss?hl=kn&gl=IN&ceid=IN:kn",  "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "Google News Maharashtra", "url": "https://news.google.com/rss?hl=mr&gl=IN&ceid=IN:mr",  "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "Google News Kerala",      "url": "https://news.google.com/rss?hl=ml&gl=IN&ceid=IN:ml",  "tier": 2, "region": "india", "category": "World Affairs"},

    # ─────────────────────────────────────────────
    # INDIA — Social Signals (Tier 3)
    # ─────────────────────────────────────────────
    {"name": "Reddit India",      "url": "https://www.reddit.com/r/india/.rss",               "tier": 3, "region": "india", "category": "World Affairs"},
]

# ─────────────────────────────────────────────
# Helper lookups
# ─────────────────────────────────────────────
TIER_1_SOURCES = [s for s in SOURCES if s["tier"] == 1]
TIER_2_SOURCES = [s for s in SOURCES if s["tier"] == 2]
TIER_3_SOURCES = [s for s in SOURCES if s["tier"] == 3]

WORLD_SOURCES = [s for s in SOURCES if s["region"] == "world"]
INDIA_SOURCES = [s for s in SOURCES if s["region"] == "india"]

SOURCE_NAME_TO_TIER = {s["name"]: s["tier"] for s in SOURCES}