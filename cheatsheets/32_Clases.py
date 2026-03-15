# ── BASIC CLASS ──────────────────────────────────────────────
class Station:
    # class variable — shared by ALL instances
    company = 'TeleCorp'

    def __init__(self, station_id, city, load):
        # instance variables — unique to each object
        self.station_id = station_id
        self.city       = city
        self.load       = load

    def __str__(self):
        return f"Station({self.station_id}, {self.city}, load={self.load}%)"

    def __repr__(self):
        return f"Station('{self.station_id}', '{self.city}', {self.load})"

    def is_overloaded(self):
        return self.load > 80

    def update_load(self, new_load):
        if not 0 <= new_load <= 100:
            raise ValueError(f"Load must be 0-100, got {new_load}")
        self.load = new_load

# creating instances
s1 = Station('ST_001', 'Warsaw', 75)
s2 = Station('ST_002', 'Krakow', 92)

print(s1)                   # calls __str__
print(repr(s1))             # calls __repr__
s1.is_overloaded()          # False
s2.is_overloaded()          # True
s1.update_load(85)

Station.company             # 'TeleCorp' — access class variable
s1.company                  # 'TeleCorp' — also accessible on instance

# ── DUNDER METHODS ───────────────────────────────────────────
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):      return f"({self.x}, {self.y})"
    def __repr__(self):     return f"Vector({self.x}, {self.y})"
    def __len__(self):      return 2
    def __add__(self, other): return Vector(self.x+other.x, self.y+other.y)
    def __mul__(self, scalar): return Vector(self.x*scalar, self.y*scalar)
    def __eq__(self, other):  return self.x==other.x and self.y==other.y
    def __lt__(self, other):  return abs(self) < abs(other)
    def __abs__(self):      return (self.x**2 + self.y**2)**0.5
    def __contains__(self, val): return val in (self.x, self.y)
    def __getitem__(self, i): return (self.x, self.y)[i]

v1 = Vector(1, 2)
v2 = Vector(3, 4)
v1 + v2             # Vector(4, 6)  — calls __add__
v1 * 3              # Vector(3, 6)  — calls __mul__
v1 == v2            # False         — calls __eq__
len(v1)             # 2             — calls __len__
abs(v1)             # 2.236...      — calls __abs__
3 in v1             # False         — calls __contains__
v1[0]               # 1             — calls __getitem__

# ── CLASS METHODS & STATIC METHODS ──────────────────────────
class Station:
    def __init__(self, station_id, city, load):
        self.station_id = station_id
        self.city       = city
        self.load       = load

    @classmethod
    def from_dict(cls, data):
        # alternative constructor — receives the class itself, not instance
        return cls(data['id'], data['city'], data['load'])

    @classmethod
    def from_csv_row(cls, row):
        parts = row.split(',')
        return cls(parts[0], parts[1], float(parts[2]))

    @staticmethod
    def validate_load(load):
        # utility function — no access to instance or class
        return 0 <= load <= 100

# usage
s = Station.from_dict({'id': 'ST_001', 'city': 'Warsaw', 'load': 75})
Station.validate_load(85)   # True
Station.validate_load(150)  # False

# ── PROPERTIES ───────────────────────────────────────────────
class Station:
    def __init__(self, station_id, city, load):
        self.station_id = station_id
        self.city       = city
        self._load      = load    # _ prefix = "private by convention"

    @property
    def load(self):
        return self._load         # accessed like attribute: s.load

    @load.setter
    def load(self, value):
        if not 0 <= value <= 100:
            raise ValueError("Load must be 0-100")
        self._load = value        # s.load = 85 → calls this

    @property
    def status(self):
        # computed property — no setter needed
        if self._load > 80:   return 'Critical'
        if self._load > 50:   return 'High'
        return 'Normal'

s = Station('ST_001', 'Warsaw', 75)
s.load              # 75       — calls getter
s.load = 85         # calls setter — validates before setting
s.status            # 'High'   — computed on the fly

# ── INHERITANCE ──────────────────────────────────────────────
class NetworkDevice:
    def __init__(self, device_id, city):
        self.device_id = device_id
        self.city      = city

    def __str__(self):
        return f"{self.__class__.__name__}({self.device_id}, {self.city})"

    def ping(self):
        return f"Pinging {self.device_id}..."

class BTS(NetworkDevice):
    def __init__(self, device_id, city, frequency):
        super().__init__(device_id, city)   # call parent __init__
        self.frequency = frequency

    def broadcast(self):
        return f"BTS {self.device_id} broadcasting on {self.frequency} MHz"

class Router(NetworkDevice):
    def __init__(self, device_id, city, ip):
        super().__init__(device_id, city)
        self.ip = ip

    def ping(self):                         # override parent method
        return f"Router ping from {self.ip}"

bts = BTS('BTS_001', 'Warsaw', 2100)
r   = Router('RTR_001', 'Krakow', '192.168.1.1')

bts.ping()          # "Pinging BTS_001..." — inherited from NetworkDevice
r.ping()            # "Router ping from 192.168.1.1" — overridden
bts.broadcast()     # BTS-specific method

isinstance(bts, BTS)            # True
isinstance(bts, NetworkDevice)  # True — also passes parent check
issubclass(BTS, NetworkDevice)  # True

# ── DATACLASS — less boilerplate ─────────────────────────────
from dataclasses import dataclass, field

@dataclass
class Station:
    station_id: str
    city:       str
    load:       float = 0.0          # default value
    tags:       list  = field(default_factory=list)  # mutable default

    def is_overloaded(self):
        return self.load > 80

# __init__, __repr__, __eq__ are auto-generated
s = Station('ST_001', 'Warsaw', 75.5)
print(s)            # Station(station_id='ST_001', city='Warsaw', load=75.5, tags=[])
s == Station('ST_001', 'Warsaw', 75.5)  # True — auto __eq__