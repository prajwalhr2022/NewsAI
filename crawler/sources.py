# ============================================================
# sources.py — Satyaksh News Crawler
# 85+ RSS feeds covering world + India with expanded categories
# ============================================================

SOURCES = [

    # ─────────────────────────────────────────────
    # WORLD — General / Wire services (Tier 1)
    # ─────────────────────────────────────────────
    {"name": "Reuters",            "url": "https://feeds.reuters.com/reuters/topNews",              "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "AP News",            "url": "https://rsshub.app/apnews/topics/apf-topnews",           "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "BBC World",          "url": "http://feeds.bbci.co.uk/news/world/rss.xml",             "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "BBC Top Stories",    "url": "http://feeds.bbci.co.uk/news/rss.xml",                   "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "Al Jazeera",         "url": "https://www.aljazeera.com/xml/rss/all.xml",              "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "The Guardian",       "url": "https://www.theguardian.com/world/rss",                  "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "DW News",            "url": "https://rss.dw.com/rdf/rss-en-all",                     "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "France 24",          "url": "https://www.france24.com/en/rss",                       "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "NPR",                "url": "https://feeds.npr.org/1001/rss.xml",                    "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "Euronews",           "url": "https://www.euronews.com/rss",                          "tier": 2, "region": "world", "category": "World Affairs"},
    {"name": "Sky News",           "url": "https://feeds.skynews.com/feeds/rss/world.xml",         "tier": 2, "region": "world", "category": "World Affairs"},
    {"name": "The Independent",    "url": "https://www.independent.co.uk/news/world/rss",          "tier": 2, "region": "world", "category": "World Affairs"},
    {"name": "Google News World",  "url": "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en", "tier": 2, "region": "world", "category": "World Affairs"},
    {"name": "South China Morning Post", "url": "https://www.scmp.com/rss/91/feed",               "tier": 2, "region": "world", "category": "World Affairs"},
    {"name": "The Diplomat",       "url": "https://thediplomat.com/feed/",                        "tier": 2, "region": "world", "category": "Geopolitics"},

    # ─────────────────────────────────────────────
    # WORLD — Geopolitics (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "Foreign Policy",     "url": "https://foreignpolicy.com/feed/",                      "tier": 1, "region": "world", "category": "Geopolitics"},
    {"name": "Foreign Affairs",    "url": "https://www.foreignaffairs.com/rss.xml",               "tier": 1, "region": "world", "category": "Geopolitics"},
    {"name": "BBC Politics",       "url": "http://feeds.bbci.co.uk/news/politics/rss.xml",        "tier": 1, "region": "world", "category": "Politics"},
    {"name": "Politico",           "url": "https://www.politico.com/rss/politics08.xml",          "tier": 2, "region": "world", "category": "Politics"},
    {"name": "The Hill",           "url": "https://thehill.com/news/feed/",                       "tier": 2, "region": "world", "category": "Politics"},

    # ─────────────────────────────────────────────
    # WORLD — Technology (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "TechCrunch",         "url": "https://techcrunch.com/feed/",                         "tier": 1, "region": "world", "category": "Technology"},
    {"name": "The Verge",          "url": "https://www.theverge.com/rss/index.xml",               "tier": 1, "region": "world", "category": "Technology"},
    {"name": "Wired",              "url": "https://www.wired.com/feed/rss",                       "tier": 1, "region": "world", "category": "Technology"},
    {"name": "Ars Technica",       "url": "http://feeds.arstechnica.com/arstechnica/index",       "tier": 1, "region": "world", "category": "Technology"},
    {"name": "MIT Tech Review",    "url": "https://www.technologyreview.com/feed/",               "tier": 1, "region": "world", "category": "Technology"},
    {"name": "VentureBeat",        "url": "https://feeds.feedburner.com/venturebeat/SZYF",        "tier": 2, "region": "world", "category": "Technology"},
    {"name": "ZDNet",              "url": "https://www.zdnet.com/news/rss.xml",                   "tier": 2, "region": "world", "category": "Technology"},
    {"name": "Hacker News",        "url": "https://hnrss.org/frontpage",                         "tier": 2, "region": "world", "category": "Technology"},
    {"name": "Google AI Blog",     "url": "https://blog.google/innovation-and-ai/technology/ai/rss/", "tier": 2, "region": "world", "category": "Technology"},

    # ─────────────────────────────────────────────
    # WORLD — Electronics & Gadgets (Tier 2)
    # ─────────────────────────────────────────────
    {"name": "GSMArena",           "url": "https://www.gsmarena.com/rss-news-reviews.php3",       "tier": 2, "region": "world", "category": "Electronics & Gadgets"},
    {"name": "AnandTech",          "url": "https://www.anandtech.com/rss/",                       "tier": 2, "region": "world", "category": "Electronics & Gadgets"},
    {"name": "Tom's Hardware",     "url": "https://www.tomshardware.com/feeds/all",               "tier": 2, "region": "world", "category": "Electronics & Gadgets"},
    {"name": "Engadget",           "url": "https://www.engadget.com/rss.xml",                     "tier": 2, "region": "world", "category": "Electronics & Gadgets"},

    # ─────────────────────────────────────────────
    # WORLD — Cars & Automobiles (Tier 2)
    # ─────────────────────────────────────────────
    {"name": "Motor Trend",        "url": "https://www.motortrend.com/feed/",                     "tier": 2, "region": "world", "category": "Cars & Automobiles"},
    {"name": "Car and Driver",     "url": "https://www.caranddriver.com/rss/all.xml/",            "tier": 2, "region": "world", "category": "Cars & Automobiles"},
    {"name": "Autocar",            "url": "https://www.autocar.co.uk/rss",                        "tier": 2, "region": "world", "category": "Cars & Automobiles"},
    {"name": "Electrek",           "url": "https://electrek.co/feed/",                            "tier": 2, "region": "world", "category": "Cars & Automobiles"},

    # ─────────────────────────────────────────────
    # WORLD — Business & Economy (Tier 1)
    # ─────────────────────────────────────────────
    {"name": "Bloomberg",          "url": "https://feeds.bloomberg.com/markets/news.rss",         "tier": 1, "region": "world", "category": "Business & Economy"},
    {"name": "Financial Times",    "url": "https://www.ft.com/rss/home",                         "tier": 1, "region": "world", "category": "Business & Economy"},
    {"name": "Reuters Business",   "url": "https://feeds.reuters.com/reuters/businessNews",       "tier": 1, "region": "world", "category": "Business & Economy"},
    {"name": "CNBC",               "url": "https://feeds.nbcnews.com/nbcnews/public/business",    "tier": 1, "region": "world", "category": "Business & Economy"},
    {"name": "The Economist",      "url": "https://www.economist.com/finance-and-economics/rss.xml", "tier": 1, "region": "world", "category": "Business & Economy"},
    {"name": "Forbes",             "url": "https://www.forbes.com/business/feed/",               "tier": 2, "region": "world", "category": "Business & Economy"},
    {"name": "Wall Street Journal","url": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml",       "tier": 1, "region": "world", "category": "Trade & Markets"},

    # ─────────────────────────────────────────────
    # WORLD — Science (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "NASA",               "url": "https://www.nasa.gov/rss/dyn/breaking_news.rss",      "tier": 1, "region": "world", "category": "Science & Space"},
    {"name": "Nature",             "url": "https://www.nature.com/nature.rss",                   "tier": 1, "region": "world", "category": "Science & Space"},
    {"name": "New Scientist",      "url": "https://www.newscientist.com/feed/home",              "tier": 2, "region": "world", "category": "Science & Space"},
    {"name": "Science Daily",      "url": "https://www.sciencedaily.com/rss/all.xml",            "tier": 2, "region": "world", "category": "Science & Space"},
    {"name": "Space.com",          "url": "https://www.space.com/feeds/all",                     "tier": 2, "region": "world", "category": "Science & Space"},
    {"name": "Phys.org",           "url": "https://phys.org/rss-feed/",                         "tier": 2, "region": "world", "category": "Science & Space"},

    # ─────────────────────────────────────────────
    # WORLD — Health (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "WHO",                "url": "https://www.who.int/rss-feeds/news-english.xml",      "tier": 1, "region": "world", "category": "Health & Medicine"},
    {"name": "Reuters Health",     "url": "https://feeds.reuters.com/reuters/healthNews",        "tier": 1, "region": "world", "category": "Health & Medicine"},
    {"name": "Healthline",         "url": "https://www.healthline.com/rss/health-news",          "tier": 2, "region": "world", "category": "Health & Medicine"},

    # ─────────────────────────────────────────────
    # WORLD — Environment (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "Guardian Environment","url": "https://www.theguardian.com/environment/rss",        "tier": 1, "region": "world", "category": "Environment & Climate"},
    {"name": "Reuters Environment", "url": "https://feeds.reuters.com/reuters/environment",      "tier": 1, "region": "world", "category": "Environment & Climate"},
    {"name": "Carbon Brief",        "url": "https://www.carbonbrief.org/feed",                   "tier": 2, "region": "world", "category": "Environment & Climate"},

    # ─────────────────────────────────────────────
    # WORLD — Agriculture (Tier 2)
    # ─────────────────────────────────────────────
    {"name": "Agri News (FAO)",    "url": "https://www.fao.org/news/rss-feed/en/",               "tier": 1, "region": "world", "category": "Agriculture"},
    {"name": "Successful Farming", "url": "https://www.agriculture.com/rss/news",                "tier": 2, "region": "world", "category": "Agriculture"},
    {"name": "Agweb",              "url": "https://www.agweb.com/rss/news",                      "tier": 2, "region": "world", "category": "Agriculture"},

    # ─────────────────────────────────────────────
    # WORLD — Sports (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "ESPN",               "url": "https://www.espn.com/espn/rss/news",                  "tier": 1, "region": "world", "category": "Sports"},
    {"name": "BBC Sport",          "url": "http://feeds.bbci.co.uk/sport/rss.xml",              "tier": 1, "region": "world", "category": "Sports"},
    {"name": "Sky Sports",         "url": "https://www.skysports.com/rss/12040",                "tier": 2, "region": "world", "category": "Sports"},

    # ─────────────────────────────────────────────
    # WORLD — Entertainment (Tier 2)
    # ─────────────────────────────────────────────
    {"name": "Variety",            "url": "https://variety.com/feed/",                           "tier": 2, "region": "world", "category": "Entertainment"},
    {"name": "Hollywood Reporter", "url": "https://www.hollywoodreporter.com/feed/",             "tier": 2, "region": "world", "category": "Entertainment"},
    {"name": "Deadline",           "url": "https://deadline.com/feed/",                          "tier": 2, "region": "world", "category": "Entertainment"},

    # ─────────────────────────────────────────────
    # WORLD — Defence (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "Defense News",       "url": "https://www.defensenews.com/arc/outboundfeeds/rss/", "tier": 2, "region": "world", "category": "Defence & Security"},
    {"name": "Jane's Defence",     "url": "https://www.janes.com/feeds/news",                   "tier": 1, "region": "world", "category": "Defence & Security"},

    # ─────────────────────────────────────────────
    # WORLD — Fact Check (Tier 1)
    # ─────────────────────────────────────────────
    {"name": "Reuters Fact Check", "url": "https://feeds.reuters.com/reuters/factcheck",         "tier": 1, "region": "world", "category": "World Affairs"},
    {"name": "Snopes",             "url": "https://www.snopes.com/feed/",                       "tier": 2, "region": "world", "category": "World Affairs"},

    # ─────────────────────────────────────────────
    # WORLD — Social Signals (Tier 3)
    # ─────────────────────────────────────────────
    {"name": "Reddit WorldNews",   "url": "https://www.reddit.com/r/worldnews/.rss",            "tier": 3, "region": "world", "category": "World Affairs"},
    {"name": "Reddit Technology",  "url": "https://www.reddit.com/r/technology/.rss",           "tier": 3, "region": "world", "category": "Technology"},
    {"name": "Reddit Science",     "url": "https://www.reddit.com/r/science/.rss",              "tier": 3, "region": "world", "category": "Science & Space"},

    # ─────────────────────────────────────────────
    # INDIA — General (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "NDTV",               "url": "https://feeds.feedburner.com/ndtvnews-top-stories",   "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "Times of India",     "url": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms", "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "The Hindu",          "url": "https://www.thehindu.com/feeder/default.rss",        "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "Hindustan Times",    "url": "https://www.hindustantimes.com/rss/topnews/rssfeed.xml", "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "India Today",        "url": "https://www.indiatoday.in/rss/home",                 "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "Indian Express",     "url": "https://indianexpress.com/feed/",                    "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "News18 India",       "url": "https://www.news18.com/rss/india.xml",              "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "Scroll.in",          "url": "https://scroll.in/feed",                            "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "The Wire",           "url": "https://thewire.in/feed",                           "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "The Print",          "url": "https://theprint.in/feed",                          "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "Google News India",  "url": "https://news.google.com/rss?hl=en-IN&gl=IN&ceid=IN:en", "tier": 2, "region": "india", "category": "World Affairs"},
    {"name": "Firstpost",          "url": "https://www.firstpost.com/commonfeeds/v1/mfp/rss/india.xml", "tier": 2, "region": "india", "category": "World Affairs"},

    # ─────────────────────────────────────────────
    # INDIA — Politics (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "NDTV Politics",      "url": "https://feeds.feedburner.com/ndtvnews-politics-news", "tier": 1, "region": "india", "category": "Politics"},
    {"name": "The Hindu Politics", "url": "https://www.thehindu.com/news/national/rss",         "tier": 1, "region": "india", "category": "Politics"},
    {"name": "Times Politics",     "url": "https://timesofindia.indiatimes.com/rssfeeds/4719148.cms", "tier": 1, "region": "india", "category": "Politics"},

    # ─────────────────────────────────────────────
    # INDIA — Regional Politics (Tier 1 & 2)
    # All major Indian states covered
    # ─────────────────────────────────────────────
    {"name": "Google News Karnataka",   "url": "https://news.google.com/rss?hl=kn&gl=IN&ceid=IN:kn",  "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Google News Tamil Nadu",  "url": "https://news.google.com/rss?hl=ta&gl=IN&ceid=IN:ta",  "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Google News Kerala",      "url": "https://news.google.com/rss?hl=ml&gl=IN&ceid=IN:ml",  "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Google News Maharashtra", "url": "https://news.google.com/rss?hl=mr&gl=IN&ceid=IN:mr",  "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Google News UP",          "url": "https://news.google.com/rss?hl=hi&gl=IN&ceid=IN:hi&topic=CAAqIQgKIhtDQkFTRGdvSUwyMHZNRE53ZGpRU0FtVnVLQUFQAQ", "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Google News Bengal",      "url": "https://news.google.com/rss?hl=bn&gl=IN&ceid=IN:bn",  "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Google News Punjab",      "url": "https://news.google.com/rss?hl=pa&gl=IN&ceid=IN:pa",  "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Google News Gujarat",     "url": "https://news.google.com/rss?hl=gu&gl=IN&ceid=IN:gu",  "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Google News Rajasthan",   "url": "https://news.google.com/rss?hl=hi&gl=IN&ceid=IN:hi",  "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Deccan Herald",           "url": "https://www.deccanherald.com/rss-feed/feeds",          "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Deccan Chronicle",        "url": "https://www.deccanchronicle.com/rss_feed/",           "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Mathrubhumi",             "url": "https://english.mathrubhumi.com/news/rss",             "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Tribune India",           "url": "https://www.tribuneindia.com/rss/feed",               "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "Telangana Today",         "url": "https://telanganatoday.com/feed",                      "tier": 2, "region": "india", "category": "Regional Politics"},
    {"name": "New Indian Express",      "url": "https://www.newindianexpress.com/rss/state",          "tier": 2, "region": "india", "category": "Regional Politics"},

    # ─────────────────────────────────────────────
    # INDIA — Business (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "Economic Times",     "url": "https://economictimes.indiatimes.com/rssfeedstopstories.cms", "tier": 1, "region": "india", "category": "Business & Economy"},
    {"name": "Mint",               "url": "https://www.livemint.com/rss/news",                  "tier": 1, "region": "india", "category": "Business & Economy"},
    {"name": "Business Standard",  "url": "https://www.business-standard.com/rss/home_page_top_stories.rss", "tier": 1, "region": "india", "category": "Business & Economy"},
    {"name": "Moneycontrol",       "url": "https://www.moneycontrol.com/rss/MCtopnews.xml",    "tier": 2, "region": "india", "category": "Business & Economy"},
    {"name": "ET Markets",         "url": "https://economictimes.indiatimes.com/markets/rssfeeds/1977021501.cms", "tier": 1, "region": "india", "category": "Trade & Markets"},

    # ─────────────────────────────────────────────
    # INDIA — Agriculture (Tier 2)
    # ─────────────────────────────────────────────
    {"name": "Krishi Jagran",      "url": "https://www.krishijagran.com/feed",                   "tier": 2, "region": "india", "category": "Agriculture"},
    {"name": "AgriMoney India",    "url": "https://www.agrimoney.com/feed",                      "tier": 2, "region": "india", "category": "Agriculture"},
    {"name": "ET Agri",            "url": "https://economictimes.indiatimes.com/news/economy/agriculture/rssfeeds/1368389.cms", "tier": 2, "region": "india", "category": "Agriculture"},

    # ─────────────────────────────────────────────
    # INDIA — Technology (Tier 2)
    # ─────────────────────────────────────────────
    {"name": "YourStory",          "url": "https://yourstory.com/feed",                         "tier": 2, "region": "india", "category": "Technology"},
    {"name": "Inc42",              "url": "https://inc42.com/feed/",                            "tier": 2, "region": "india", "category": "Technology"},
    {"name": "ET Tech",            "url": "https://economictimes.indiatimes.com/tech/rssfeeds/13357270.cms", "tier": 2, "region": "india", "category": "Technology"},
    {"name": "MediaNama",          "url": "https://www.medianama.com/feed/",                   "tier": 2, "region": "india", "category": "Technology"},

    # ─────────────────────────────────────────────
    # INDIA — Cars (Tier 2)
    # ─────────────────────────────────────────────
    {"name": "CarDekho News",      "url": "https://www.cardekho.com/news/rss",                  "tier": 2, "region": "india", "category": "Cars & Automobiles"},
    {"name": "Autocar India",      "url": "https://www.autocarindia.com/rss/news",              "tier": 2, "region": "india", "category": "Cars & Automobiles"},
    {"name": "ZigWheels",          "url": "https://www.zigwheels.com/news-cars/rss",            "tier": 2, "region": "india", "category": "Cars & Automobiles"},

    # ─────────────────────────────────────────────
    # INDIA — Sports / Cricket (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "ESPN Cricinfo",      "url": "https://static.espncricinfo.com/rss/content/story/feeds/0.xml", "tier": 1, "region": "india", "category": "Cricket"},
    {"name": "NDTV Sports",        "url": "https://feeds.feedburner.com/NdtvNews-Sports",       "tier": 2, "region": "india", "category": "Sports"},
    {"name": "The Bridge",         "url": "https://thebridge.in/feed/",                        "tier": 2, "region": "india", "category": "Sports"},
    {"name": "Sportskeeda",        "url": "https://www.sportskeeda.com/feed",                  "tier": 2, "region": "india", "category": "Sports"},

    # ─────────────────────────────────────────────
    # INDIA — Entertainment (Tier 2)
    # ─────────────────────────────────────────────
    {"name": "Bollywood Hungama",  "url": "https://www.bollywoodhungama.com/rss/news.xml",      "tier": 2, "region": "india", "category": "Entertainment"},
    {"name": "Pinkvilla",          "url": "https://www.pinkvilla.com/feed",                     "tier": 2, "region": "india", "category": "Entertainment"},
    {"name": "FilmiBeat",          "url": "https://www.filmibeat.com/rss.xml",                 "tier": 2, "region": "india", "category": "Entertainment"},

    # ─────────────────────────────────────────────
    # INDIA — Fact Check (Tier 1 & 2)
    # ─────────────────────────────────────────────
    {"name": "BOOM Live",          "url": "https://www.boomlive.in/feed",                      "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "Alt News",           "url": "https://www.altnews.in/feed/",                      "tier": 1, "region": "india", "category": "World Affairs"},
    {"name": "Factly",             "url": "https://factly.in/feed/",                           "tier": 2, "region": "india", "category": "World Affairs"},

    # ─────────────────────────────────────────────
    # INDIA — Defence (Tier 2)
    # ─────────────────────────────────────────────
    {"name": "Indian Defence Review", "url": "https://www.indiandefencereview.com/feed/",      "tier": 2, "region": "india", "category": "Defence & Security"},
    {"name": "Swarajya Mag",       "url": "https://swarajyamag.com/feed",                      "tier": 2, "region": "india", "category": "Defence & Security"},

    # ─────────────────────────────────────────────
    # INDIA — Social Signals (Tier 3)
    # ─────────────────────────────────────────────
    {"name": "Reddit India",       "url": "https://www.reddit.com/r/india/.rss",               "tier": 3, "region": "india", "category": "World Affairs"},
    {"name": "Reddit IndiaPolitics","url": "https://www.reddit.com/r/IndiaSpeaks/.rss",        "tier": 3, "region": "india", "category": "Regional Politics"},
]

# Helper lookups
TIER_1_SOURCES = [s for s in SOURCES if s["tier"] == 1]
TIER_2_SOURCES = [s for s in SOURCES if s["tier"] == 2]
TIER_3_SOURCES = [s for s in SOURCES if s["tier"] == 3]
WORLD_SOURCES  = [s for s in SOURCES if s["region"] == "world"]
INDIA_SOURCES  = [s for s in SOURCES if s["region"] == "india"]
SOURCE_NAME_TO_TIER = {s["name"]: s["tier"] for s in SOURCES}
