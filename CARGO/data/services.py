import json
import os
import random
import math
import requests
from dotenv import load_dotenv

load_dotenv()
ORDERS_FILE = os.path.join("data", "orders.json")
USERS_FILE = os.path.join("data", "users.json")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

UKRAINE_CITIES = {
    "Київ": (50.45, 30.52), "Львів": (49.83, 24.02), "Одеса": (46.48, 30.72),
    "Харків": (49.99, 36.23), "Дніпро": (48.46, 35.04), "Вінниця": (49.23, 28.46),
    "Івано-Франківськ": (48.92, 24.71), "Луцьк": (50.74, 25.32), "Ужгород": (48.62, 22.28),
    "Тернопіль": (49.55, 25.59), "Рівне": (50.61, 26.25), "Житомир": (50.25, 28.66),
    "Чернігів": (51.49, 31.28), "Чернівці": (48.29, 25.93), "Хмельницький": (49.42, 26.98),
    "Полтава": (49.58, 34.55), "Запоріжжя": (47.83, 35.13)
}

def get_usd_rate():
    try:
        url = "https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5"
        resp = requests.get(url, timeout=3).json()
        for x in resp:
            if x['ccy'] == 'USD': return float(x['sale'])
    except: return 42.0
    return 42.0

def calculate_distance_haversine(city1, city2):
    if city1 not in UKRAINE_CITIES or city2 not in UKRAINE_CITIES: return 500
    lat1, lon1 = UKRAINE_CITIES[city1]
    lat2, lon2 = UKRAINE_CITIES[city2]
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return int(R * c)

def get_route_info(city1, city2):
    if GOOGLE_API_KEY:
        try:
            c1, c2 = UKRAINE_CITIES[city1], UKRAINE_CITIES[city2]
            url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={c1[0]},{c1[1]}&destinations={c2[0]},{c2[1]}&key={GOOGLE_API_KEY}"
            resp = requests.get(url).json()
            if resp['status'] == 'OK':
                txt = resp['rows'][0]['elements'][0]['distance']['text']
                return int(''.join(filter(str.isdigit, txt))), "Google API"
        except: pass
    return calculate_distance_haversine(city1, city2), "Haversine"

def is_user_registered(uid):
    if not os.path.exists(USERS_FILE): return False
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for u in json.load(f):
                if u['user_id'] == uid: return True
    except: return False
    return False

def register_new_user(udata):
    udata['bonus_points'] = 0
    udata['total_orders'] = 0
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding="utf-8") as f: json.dump([], f)
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f: users = json.load(f)
    except: users = []
    users.append(udata)
    with open(USERS_FILE, "w", encoding="utf-8") as f: json.dump(users, f, indent=4, ensure_ascii=False)

def get_user_info(uid):
    if not os.path.exists(USERS_FILE): return None
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for u in json.load(f):
                if u['user_id'] == uid: return u
    except: return None
    return None

def update_user_bonuses(uid, spent=0):
    earned = random.randint(1, 10)
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f: users = json.load(f)
        for u in users:
            if u['user_id'] == uid:
                u['bonus_points'] = u.get('bonus_points', 0) - spent + earned
                u['total_orders'] = u.get('total_orders', 0) + 1
                break
        with open(USERS_FILE, "w", encoding="utf-8") as f: json.dump(users, f, indent=4, ensure_ascii=False)
    except: pass
    return earned

def save_order(odata):
    if not os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "w", encoding="utf-8") as f: json.dump([], f)
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f: data = json.load(f)
    except: data = []
    data.append(odata)
    with open(ORDERS_FILE, "w", encoding="utf-8") as f: json.dump(data, f, indent=4, ensure_ascii=False)

def get_global_stats():
    c, m, u = 0, 0, 0
    if os.path.exists(ORDERS_FILE):
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            o = json.load(f)
            c = len(o)
            m = sum(x.get('price', 0) for x in o)
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            u = len(json.load(f))
    return c, m, u