import requests
import pandas as pd
import time
import ta
from binance.client import Client
from datetime import datetime
import telegram
import threading

# إعدادات API و TELEGRAM - أدخلها بنفسك
BINANCE_API_KEY = '8iiROrTjur4UAUBPYyUNXYM12wXSSVOVoq1UCWIUVgyOQgj9B5tRqddNS8miUYit'
BINANCE_SECRET_KEY = 'l0okX9QJa35EciHnCBEzuBr7MG4ZLApddX9byRlk4JWCOnznkNbqMvD383jAsH8b'
TELEGRAM_BOT_TOKEN = '8019466974:AAGFCJf_OibOUnI4kpAb3AK8Y-9RN9yh7IA'
TELEGRAM_CHAT_ID = '1538980920'

client = Client(BINANCE_API_KEY, BINANCE_SECRET_KEY)
bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)

SYMBOLS = ["BTCUSDT", "ETHUSDT", "APTUSDT", "XRPUSDT", "API3USDT",  "SOLUSDT", "ADAUSDT", 
    "DOGEUSDT", "TRXUSDT", "TONUSDT", "1000SATSUSDT", "AUSDT", "ACHUSDT", "ACXUSDT", "AERGOUSDT", 
    "AGLDUSDT", "AIXBTUSDT", "ALGOUSDT", "ALPINEUSDT", "ALTUSDT", "AMPUSDT", "APEUSDT", "ARUSDT", 
    "ARBUSDT", "ARDRUSDT", "ARPAUSDT", "ASTRUSDT", "ATAUSDT", "ATOMUSDT", "AVAUSDT", "AVAXUSDT", 
    "BANDUSDT", "BATUSDT", "BBUSDT", "BCHUSDT", "BEAMXUSDT", "BICOUSDT", "BIOUSDT", "BMTUSDT", 
    "BLURUSDT", "BTTCUSDT", "CELRUSDT", "CETUSUSDT", "CELOUSDT", "CFXUSDT", "CHRUSDT", "CHZUSDT", 
    "CKBUSDT", "COOKIEUSDT", "COSUSDT", "CRVUSDT", "CTCUSDT", "CTSIUSDT", "CVCUSDT", "DASHUSDT", 
    "DATAUSDT", "DCRUSDT", "DENTUSDT", "DGBUSDT", "DIAUSDT", "DOTUSDT", "DUSKUSDT", "DYDXUSDT", 
    "EDUUSDT", "EGLDUSDT", "ELFUSDT", "ENSUSDT", "ENJUSDT", "EURIUSDT", "EURUSDT", "ETCUSDT", 
    "FDUSDUSDT", "FETUSDT", "FILUSDT", "FIROUSDT", "FIOUSDT", "FLOKIUSDT", "FLOWUSDT", "FLUXUSDT", 
    "FORMUSDT", "FTMUSDT", "GALAUSDT", "GASUSDT", "GLMRUSDT", "GLMUSDT", "GMTUSDT", "GPSUSDT", 
    "GRTUSDT", "GTCUSDT", "HBARUSDT", "HIGHUSDT", "HIVEUSDT", "HOOKUSDT", "HOTUSDT", "ICPUSDT", 
    "ICXUSDT", "IDUSDT", "INJUSDT", "IOUSDT", "IOTAUSDT", "IOTXUSDT", "IQUSDT", "JASMYUSDT", 
    "KAIAUSDT", "KAITOUSDT", "KDAUSDT", "KMDUSDT", "KNCUSDT", "KSMUSDT", "LINKUSDT", "LPTUSDT", 
    "LRCUSDT", "LSKUSDT", "LTCUSDT", "LTOUSDT", "LUNAUSDT", "MANAUSDT", "MASKUSDT", "MANTAUSDT", 
    "MDTUSDT", "MEUSDT", "METISUSDT", "MINAUSDT", "MKRUSDT", "MOVEUSDT", "MOVRUSDT", "MTLUSDT", 
    "NEARUSDT", "NEOUSDT", "NEXOUSDT", "NFPUSDT", "NILUSDT", "NKNUSDT", "NOTUSDT", "NTRNUSDT", 
    "NULSUSDT", "OXTUSDT", "OGNUSDT", "OMNIUSDT", "ONEUSDT", "ONGUSDT", "OPUSDT", "ORDIUSDT", 
    "PAXGUSDT", "PDAUSDT", "PENDLEUSDT", "PHAUSDT", "PHBUSDT", "PIVXUSDT", "POLUSDT", "POLYXUSDT", 
    "PONDUSDT", "PORTALUSDT", "POWRUSDT", "PROMUSDT", "PSGUSDT", "PYTHUSDT", "QNTUSDT", "QTUMUSDT", 
    "RADUSDT", "RAREUSDT", "RDNTUSDT", "REDUSDT", "REIUSDT", "RENDERUSDT", "REQUSDT", "RIFUSDT", 
    "RLCUSDT", "ROSEUSDT", "RPLUSUSDT", "RSRUSDT", "RVNUSDT", "SAGAUSDT", "SANDUSDT", "SCUSDT", 
    "SCRUSDT", "SCRTUSDT", "SEIUSDT", "SFPUSDT", "SHELLUSDT", "SHIBUSDT", "SKLUSDT", "SLFUSDT", 
    "SLPUSDT", "SNTUSDT", "SNXUSDT", "STEEMUSDT", "STGUSDT", "STORJUSDT", "STPTUSDT", "STRAXUSDT", 
    "STXUSDT", "SUIUSDT", "SUNUSDT", "SUPERUSDT", "SUSHIUSDT", "SXPUSDT", "SYSUSDT", "TAOUSDT", 
    "TFUELUSDT", "THETAUSDT", "THEUSDT", "TIAUSDT", "TLMUSDT", "TNSRUSDT", "TSTUSDT", "TUTUSDT", 
    "TWTUSDT", "UTKUSDT", "USDPUSDT", "USUALUSDT", "VANAUSDT", "VANRYUSDT", "VETUSDT", "VIBUSDT", 
    "VICUSDT", "VIDTUSDT", "VOXELUSDT", "VTHOUSDT", "WANUSDT", "WAVESUSDT", "WAXPUSDT", "WBETHUSDT", 
    "WLDUSDT", "WOOUSDT", "XAIUSDT", "XECUSDT", "XLMUSDT", "XNOUSDT", "XTZUSDT", "XVGUSDT", 
    "XVSUSDT", "YFIUSDT", "ZECUSDT", "ZENUSDT", "ZILUSDT", "ZKUSDT", "ZROUSDT", "ZRXUSDT", 
    "MATICUSDT", "TUSDUSDT", "XMRUSDT", "BUSDUSDT", "NFTUSDT", "KLAYUSDT", "CSPRUSDT", "LOOMUSDT", 
    "XEMUSDT", "AGIXUSDT", "HNTUSDT", "ETHWUSDT", "TOMOUSDT", "IOSTUSDT", "BORAUSDT", "MOBUSDT", 
    "CELRUSDT", "PUNDIXUSDT", "KASUSDT", "UIPUSDT", "XRDUSDT", "BTTOLDUSDT", "AZEROUSDT", "EURSUSDT", 
    "XYMUSDT", "POLYUSDT", "USDXUSDT", "LYXEUSDT", "RBTCUSDT", "KEEPUSDT", "PEGUSDT", "TRACUSDT", 
    "ARKUSDT", "ORBSUSDT", "DKAUSDT", "MLKUSDT", "DESOUSDT", "MVLUSDT", "CQTUSDT", "TELUSDT", 
    "STMXUSDT", "ATORUSDT", "OMGUSDT", "BLZUSDT", "VRAUSDT", "EWTUSDT", "ARKMUSDT", "EFIUSDT", 
    "BFCUSDT", "AVINOCUSDT", "MNWUSDT", "QKCUSDT", "WXTUSDT", "CREUSDT", "AOGUSDT", "ABBCUSDT", 
    "DEXTUSDT", "TTUSDT", "XYOUSDT", "FCTUSDT", "FORTUSDT", "POKTUSDT", "METAUSDT", "RSS3USDT", 
    "GRSUSDT", "AXELUSDT", "RKNUSDT", "DAGUSDT", "LOCUSUSDT", "ARRRUSDT", "DEROUSDT", "MULTIUSDT", 
    "ZBCUSDT", "ORCUSDT", "KINUSDT", "XSGDUSDT", "LCXUSDT", "RLYUSDT", "TRIASUSDT", "KLVUSDT", 
    "ORAIUSDT", "VRSCUSDT", "RSVUSDT", "UPPUSDT", "UQCUSDT", "AHTUSDT", "USDKUSDT", "AQTUSDT", 
    "ASMUSDT", "MONAUSDT", "LITUSDT", "ROKOUSDT", "WCFGUSDT", "NESTUSDT", "PCXUSDT", "CONVUSDT", 
    "PKTUSDT", "HUMUSDT", "DMTRUSDT", "CANTOUSDT", "CUBEUSDT", "TORNUSDT", "FODLUSDT", "YLDYUSDT", 
    "ZNNUSDT", "TRTLUSDT", "MDUUSDT", "DBCUSDT", "CLVUSDT", "PERLUSDT", "BEAMUSDT", "IQNUSDT", 
    "VETHUSDT", "VEXTUSDT", "KILTUSDT", "USDNUSDT", "PIPUSDT", "HAIUSDT", "BANUSDT", "CROATUSDT", 
    "NCASHUSDT", "TIMEUSDT", "OKSUSDT", "VDLUSDT", "EQUADUSDT", "MODUSDT", "BASICUSDT", "XSRUSDT", 
    "ENGTUSDT", "DDDUSDT", "CLAMUSDT", "BEZUSDT", "SNGUSDT", "POPPYUSDT", "BERRYUSDT", "LHTUSDT", 
    "ZTXUSDT", "NASDACUSDT", "NOIAUSDT", "SPHTXUSDT", "LOCUSDT", "EKTUSDT", "SBTCUSDT", "XCPUSDT", 
    "HACUSDT", "UPIUSDT", "VEXUSDT", "EACUSDT", "CMTUSDT", "GROUSDT", "NOBTUSDT", "AACUSDT", 
    "EXCUSDT", "MOONDUSDT", "XUCUSDT", "EMUSDT", "XRTUSDT", "LEPENUSDT", "XCRUSDT", "ACOINUSDT", 
    "MTLMC3USDT", "KRWUSDT", "MEETUSDT", "IVYUSDT", "COLXUSDT", "PPYUSDT", "CBIXUSDT", "DROPUSDT", 
    "TMCUSDT", "XPMUSDT", "HBNUSDT", "PCTUSDT", "PHRUSDT", "YVSUSDT", "NORUSDT", "BRZEUSDT", 
    "VDRUSDT", "CBMUSDT", "PINUSDT", "BOLIUSDT", "JADEUSDT", "BRYUSDT", "HTZUSDT", "TELOSUSDT", 
    "FBNUSDT", "LYRAUSDT", "POLISUSDT", "ZUMUSDT", "SIGNUSDT", "SCONEXUSDT", "CREDITUSDT", "YTNUSDT", 
    "TBXUSDT", "TZCUSDT", "CURUSDT", "KUVUSDT", "KEMAUSDT", "AXEUSDT", "INNBCLUSDT", "SCHOUSDT", 
    "1MILUSDT", "BSDUSDT", "INNUSDT", "KGOUSDT", "LANDUSDT", "REWUSDT", "ISLAMIUSDT", "SPACEUSDT", 
    "TALKUSDT", "PRIUSDT", "SNCUSDT", "INTUSDT", "VICAUSDT", "OCTUSDT", "OMIUSDT", "WITUSDT", 
    "DGCUSDT", "BOXUSDT", "UMMAUSDT", "TEMCOUSDT", "CAPPUSDT", "NAVUSDT", "ENGUSDT", "ZCNUSDT", 
    "LBTCUSDT", "AIEPKUSDT", "MOBIUSDT", "NEWUSDT", "UGASUSDT", "NASUSDT", "GERAUSDT", "BNTYUSDT", 
    "REMUSDT", "DPYUSDT", "NBOTUSDT", "OPENUSDT", "HITUSDT", "COFIUSDT", "RDNUSDT", "MDSUSDT", 
    "EOSDACUSDT", "FDZUSDT", "MDAUSDT", "VIDYUSDT", "GEMUSDT", "CSUSDT", "SKMUSDT", "RIDEUSDT", 
    "XCHFUSDT", "XPXUSDT", "METUSDT", "LEOXUSDT", "MNYUSDT", "PIUSDT", "PRIXUSDT", "AUXUSDT", 
    "ENQUSDT", "FJBUSDT", "KRDUSDT", "CXOUSDT", "OWCUSDT", "KATUSDT", "EVCUSDT", "EVXUSDT", 
    "CAJUSDT", "CPCUSDT", "NUUSDT", "SRNUSDT", "CNDUSDT", "HOUSDT", "EMC2USDT", "EGEMUSDT", 
    "X8XUSDT", "BLKUSDT", "SAPPUSDT", "NXSUSDT", "MAIDUSDT", "GLFUSDT", "AIONUSDT", "CARDUSDT", 
    "BLOCKUSDT", "VEEUSDT", "SNTVTUSDT", "HEDGUSDT", "EYEUSDT", "RAVENUSDT", "BECNUSDT", "SANUSDT", 
    "PNYUSDT", "RDDUSDT", "1ECOUSDT", "EXPUSDT", "WINGSUSDT", "TMNUSDT", "XDNUSDT", "MYBUSDT", 
    "SARCOUSDT", "CHEESEUSDT", "SEELEUSDT", "BITBUSDT", "CASHUSDT", "GRCUSDT", "POTUSDT", "QCHUSDT", 
    "SUBUSDT", "TERAUSDT", "INDUSDT", "TAUUSDT", "AMNUSDT", "PUTUSDT", "VIAUSDT", "TKNUSDT", 
    "PINKUSDT", "CRWUSDT", "MOLKUSDT", "PGNUSDT", "CUREUSDT", "DGDUSDT", "ONIONUSDT", "WPRUSDT", 
    "TYPEUSDT", "EKOUSDT", "ZETUSDT", "TAGUSDT", "BITSUSDT", "XSTUSDT", "CANNUSDT", "EMCUSDT", 
    "OPALUSDT", "OKUSDT", "XPYUSDT", "KOBOUSDT", "LOGUSDT", "BTAUSDT", "SIBUSDT", "XHIUSDT", 
    "2GIVEUSDT", "GBUSDT", "CJUSDT", "KURTUSDT", "ENTUSDT", "CNTUSDT", "SWTUSDT", "NETKOUSDT", 
    "SKYUSDT", "LUNUSDT", "ADKUSDT", "GLTUSDT", "GXCUSDT", "AXLUSDT", "WUSDT", "OMUSDT", "CYBERUSDT", 
    "RUPUSDT", "POEUSDT", "BUZZUSDT", "EXRNUSDT", "ATLUSDT", "EROUSDT", "STARUSDT", "APPCUSDT", 
    "AITUSDT", "TRUEUSDT", "AXPRUSDT", "MNTPUSDT", "EDGEUSDT", "TUBEUSDT", "BANCAUSDT", "UUUUSDT", 
    "MSRUSDT", "GENUSDT", "SSPUSDT", "WABUSDT", "AROUSDT", "PASSUSDT", "ABLUSDT", "PMAUSDT", 
    "XBIUSDT", "VDGUSDT", "DAVUSDT", "KNTUSDT", "STEEPUSDT", "ESCEUSDT", "BLTGUSDT", "BTUUSDT", 
    "DCTOUSDT", "CCNUSDT", "TTNUSDT", "MERIUSDT", "SAFEUSDT", "MCPCUSDT", "LEVLUSDT", "CCXXUSDT", 
    "MUSDUSDT", "FIDAUSDT", "GTFUSDT", "YOUCUSDT", "DNTUSDT", "MITHUSDT", "CTXCUSDT", "ALICEUSDT"]

# Filter invalid symbols to avoid API errors for invalid symbols
try:
    exchange_info = client.get_exchange_info()
    valid_symbols = {item['symbol'] for item in exchange_info['symbols']}
    SYMBOLS = [s for s in SYMBOLS if s in valid_symbols]
    print(f"Monitoring {len(SYMBOLS)} valid symbols.")
    try:
        bot.send_message(chat_id=int(TELEGRAM_CHAT_ID), text="🚀 اختبار عمل البوت")
        print(f"✅ Telegram sent: 🚀 اختبار عمل البوت")
    except Exception as e:
        print(f"❌ Telegram send error: {e}")
except Exception as e:
    print(f"Error fetching exchange info: {e}")

INTERVAL_15M = Client.KLINE_INTERVAL_15MINUTE
INTERVAL_1H = Client.KLINE_INTERVAL_1HOUR
INTERVAL_4H = Client.KLINE_INTERVAL_4HOUR

# صفقات نشطة
open_trades = {}

def get_technical_indicators(symbol, interval):
    klines = client.get_klines(symbol=symbol, interval=interval, limit=100)
    df = pd.DataFrame(klines, columns=[
        'timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base', 'taker_buy_quote', 'ignore'
    ])
    df['close'] = pd.to_numeric(df['close'])
    df['open'] = pd.to_numeric(df['open'])

    # حساب المؤشرات الفنية
    df['rsi'] = ta.momentum.RSIIndicator(df['close'], window=14).rsi()
    macd = ta.trend.MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    df['ema20'] = ta.trend.EMAIndicator(df['close'], window=20).ema_indicator()
    df['ema50'] = ta.trend.EMAIndicator(df['close'], window=50).ema_indicator()

    # إضافة Bollinger Bands و Stochastic
    df['bollinger_upper'], df['bollinger_middle'], df['bollinger_lower'] = ta.volatility.BollingerBands(df['close'], window=20).bollinger_hband(), ta.volatility.BollingerBands(df['close'], window=20).bollinger_mavg(), ta.volatility.BollingerBands(df['close'], window=20).bollinger_lband()
    df['stochastic_k'], df['stochastic_d'] = ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'], window=14, smooth_window=3).stoch(), ta.momentum.StochasticOscillator(df['high'], df['low'], df['close'], window=14, smooth_window=3).stoch_signal()

    return df

def check_buy_signal(df):
    latest = df.iloc[-1]
    return (
        latest['rsi'] < 30 and
        latest['macd'] > latest['macd_signal'] and
        latest['ema20'] > latest['ema50'] and
        latest['close'] > latest['bollinger_middle'] and
        latest['stochastic_k'] > latest['stochastic_d']
    )

def check_timeframe_confirmation(symbol):
    df_15m = get_technical_indicators(symbol, INTERVAL_15M)
    df_1h = get_technical_indicators(symbol, INTERVAL_1H)
    df_4h = get_technical_indicators(symbol, INTERVAL_4H)

    # التحقق من توافق الإشارات عبر الثلاثة إطارات الزمنية
    return (check_buy_signal(df_15m) and
            check_buy_signal(df_1h) and
            check_buy_signal(df_4h))

def send_telegram_message(message):
    try:
        bot.send_message(chat_id=int(TELEGRAM_CHAT_ID), text=message)
        print(f"✅ Telegram sent: {message}")
    except Exception as e:
        print(f"❌ Telegram send error: {e}")

def monitor_trade(symbol, entry_price, targets, sl_price, entry_time):
    print(f"Monitoring {symbol}...")
    hit_targets = [False, False, False]
    trailing_sl = sl_price

    while True:
        df = get_technical_indicators(symbol, INTERVAL_15M)
        current_price = df['close'].iloc[-1]

        # تحقق من الأهداف
        for i in range(3):
            if not hit_targets[i] and current_price >= targets[i]:
                hit_targets[i] = True
                duration = (datetime.utcnow() - entry_time).seconds // 60
                try:
                    bot.send_message(chat_id=int(TELEGRAM_CHAT_ID), text=f"""تحقق الهدف TP{i+1} لـ {symbol}!
السعر: {current_price:.2f}
المدة: {duration} دقيقة""")
                    print(f"✅ Telegram sent: تحقق الهدف TP{i+1} لـ {symbol}!")
                except Exception as e:
                    print(f"❌ Telegram send error: {e}")

                
                # بعد TP1، رفع وقف الخسارة إلى نقطة الدخول
                if i == 0:
                    trailing_sl = entry_price

        # تحقق من وقف الخسارة (متحرك بعد TP1)
        if current_price <= trailing_sl:
            duration = (datetime.utcnow() - entry_time).seconds // 60
            try:
                bot.send_message(chat_id=int(TELEGRAM_CHAT_ID), text=f"""ضرب وقف الخسارة لـ {symbol}!
السعر: {current_price:.2f}
المدة: {duration} دقيقة""")
                print(f"✅ Telegram sent: ضرب وقف الخسارة لـ {symbol}!")
            except Exception as e:
                print(f"❌ Telegram send error: {e}")
            del open_trades[symbol]
            break

        # إذا تحققت كل الأهداف
        if all(hit_targets):
            try:
                bot.send_message(chat_id=int(TELEGRAM_CHAT_ID), text=f"""كل الأهداف تحققت لـ {symbol}!""")
                print(f"✅ Telegram sent: كل الأهداف تحققت لـ {symbol}!")
            except Exception as e:
                print(f"❌ Telegram send error: {e}")
            del open_trades[symbol]
            break

        time.sleep(60)

while True:
    print(f"\n===== New scan at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC =====")
    for symbol in SYMBOLS:
        if symbol in open_trades:
            print(f"➡️ Skipping {symbol} (active trade)")
            continue

        print(f"🔍 Checking {symbol}...", end="")
        if check_timeframe_confirmation(symbol):
            print(" ✅ Signal!")
            df = get_technical_indicators(symbol, INTERVAL_15M)
            entry_price = df['close'].iloc[-1]
            tp1 = entry_price * 1.015
            tp2 = entry_price * 1.03
            tp3 = entry_price * 1.05
            sl_price = entry_price * 0.985
            entry_time = datetime.utcnow()

            open_trades[symbol] = {
                'entry': entry_price,
                'tp1': tp1,
                'tp2': tp2,
                'tp3': tp3,
                'sl': sl_price,
                'time': entry_time
            }

            msg = (
                f"إشارة شراء: {symbol}\n"
                f"الدخول: {entry_price:.2f}\n"
                f"TP1: {tp1:.2f} | TP2: {tp2:.2f} | TP3: {tp3:.2f}\n"
                f"وقف الخسارة: {sl_price:.2f}\n"
                f"الوقت: {entry_time.strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )
            try:
                bot.send_message(chat_id=int(TELEGRAM_CHAT_ID), text=msg)
                print(f"✅ Telegram sent: إشارة شراء: {symbol}")
            except Exception as e:
                print(f"❌ Telegram send error: {e}")

            thread = threading.Thread(target=monitor_trade, args=(symbol, entry_price, [tp1, tp2, tp3], sl_price, entry_time))
            thread.start()
        else:
            print(" ❌ No signal")
    print("🌙 Scan complete. Sleeping 5 minutes.")
    time.sleep(60 * 5)
