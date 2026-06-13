"""
محرك توليد IP لجميع دول العالم (250 دولة)
World-wide IP Generation Engine
"""

import json
import random
import ipaddress
from pathlib import Path
from dataclasses import dataclass, asdict
from countries_data import COUNTRIES_META

# تحميل قاعدة بيانات نطاقات IP الرسمية
_DATA_PATH = Path(__file__).parent / "ip_ranges_compact.json"
with open(_DATA_PATH, "r") as f:
    IP_RANGES = json.load(f)


@dataclass
class IPLocation:
    ip_address: str
    country_code: str
    country_en: str
    country_ar: str
    city: str
    city_ar: str
    latitude: float
    longitude: float
    timezone: str
    isp: str
    language: str
    currency: str
    proxy_type: str


def _random_ip_in_range(start_ip: str, end_ip: str) -> str:
    start = int(ipaddress.IPv4Address(start_ip))
    end = int(ipaddress.IPv4Address(end_ip))
    return str(ipaddress.IPv4Address(random.randint(start, end)))


def generate_ip_for_country(country_code: str, proxy_type: str = "Residential") -> IPLocation:
    """توليد IP حقيقي وموقع جغرافي لأي دولة في العالم"""
    country_code = country_code.upper()

    if country_code not in IP_RANGES:
        raise ValueError(f"رمز الدولة '{country_code}' غير موجود في قاعدة بيانات IP")
    if country_code not in COUNTRIES_META:
        raise ValueError(f"رمز الدولة '{country_code}' غير موجود في قاعدة بيانات المعلومات")

    ranges = IP_RANGES[country_code]
    meta = COUNTRIES_META[country_code]

    # اختيار نطاق IP عشوائي ثم IP عشوائي ضمنه
    ip_range = random.choice(ranges)
    ip = _random_ip_in_range(ip_range[0], ip_range[1])

    # تشويش بسيط على الإحداثيات لتبدو طبيعية (±0.08)
    lat_jitter = random.uniform(-0.08, 0.08)
    lon_jitter = random.uniform(-0.08, 0.08)

    return IPLocation(
        ip_address=ip,
        country_code=country_code,
        country_en=meta["en"],
        country_ar=meta["ar"],
        city=meta["capital"],
        city_ar=meta["capital_ar"],
        latitude=round(meta["lat"] + lat_jitter, 6),
        longitude=round(meta["lon"] + lon_jitter, 6),
        timezone=meta["tz"],
        isp=random.choice(meta["isp"]),
        language=meta["lang"],
        currency=meta["currency"],
        proxy_type=proxy_type,
    )


def get_available_countries() -> list:
    """قائمة كل الدول المتاحة (موجودة في كلتا القاعدتين)"""
    available = []
    for cc in sorted(COUNTRIES_META.keys()):
        if cc in IP_RANGES:
            available.append({
                "code": cc,
                "en": COUNTRIES_META[cc]["en"],
                "ar": COUNTRIES_META[cc]["ar"],
            })
    return available


def to_dict(loc: IPLocation) -> dict:
    return asdict(loc)


def get_stats() -> dict:
    """إحصائيات قاعدة البيانات"""
    total_countries = len(get_available_countries())
    total_ranges = sum(len(IP_RANGES.get(cc, [])) for cc in COUNTRIES_META.keys())
    return {"countries": total_countries, "ip_ranges": total_ranges}
