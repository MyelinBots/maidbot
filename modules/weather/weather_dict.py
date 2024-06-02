class Condition:
    text: str
    icon: str
    code: int

    def __init__(self, text: str, icon: str, code: int) -> None:
        self.text = text
        self.icon = icon
        self.code = code


class Current:
    last_updated_epoch: int
    last_updated: str
    temp_c: float
    temp_f: float
    is_day: int
    condition: Condition
    wind_mph: float
    wind_kph: float
    wind_degree: int
    wind_dir: str
    pressure_mb: float
    pressure_in: float
    precip_mm: float
    precip_in: float
    humidity: int
    cloud: int
    feelslike_c: float
    feelslike_f: float
    windchill_c: float
    windchill_f: float
    heatindex_c: float
    heatindex_f: float
    dewpoint_c: float
    dewpoint_f: float
    vis_km: float
    vis_miles: float
    uv: float
    gust_mph: float
    gust_kph: float

    def __init__(self, last_updated_epoch: int, last_updated: str, temp_c: float, temp_f: float, is_day: int, condition: Condition, wind_mph: float, wind_kph: float, wind_degree: int, wind_dir: str, pressure_mb: float, pressure_in: float, precip_mm: float, precip_in: float, humidity: int, cloud: int, feelslike_c: float, feelslike_f: float, windchill_c: float, windchill_f: float, heatindex_c: float, heatindex_f: float, dewpoint_c: float, dewpoint_f: float, vis_km: float, vis_miles: float, uv: float, gust_mph: float, gust_kph: float) -> None:
        self.last_updated_epoch = last_updated_epoch
        self.last_updated = last_updated
        self.temp_c = temp_c
        self.temp_f = temp_f
        self.is_day = is_day
        self.condition = condition
        self.wind_mph = wind_mph
        self.wind_kph = wind_kph
        self.wind_degree = wind_degree
        self.wind_dir = wind_dir
        self.pressure_mb = pressure_mb
        self.pressure_in = pressure_in
        self.precip_mm = precip_mm
        self.precip_in = precip_in
        self.humidity = humidity
        self.cloud = cloud
        self.feelslike_c = feelslike_c
        self.feelslike_f = feelslike_f
        self.windchill_c = windchill_c
        self.windchill_f = windchill_f
        self.heatindex_c = heatindex_c
        self.heatindex_f = heatindex_f
        self.dewpoint_c = dewpoint_c
        self.dewpoint_f = dewpoint_f
        self.vis_km = vis_km
        self.vis_miles = vis_miles
        self.uv = uv
        self.gust_mph = gust_mph
        self.gust_kph = gust_kph


class Location:
    name: str
    region: str
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime_epoch: int
    localtime: str

    def __init__(self, name: str, region: str, country: str, lat: float, lon: float, tz_id: str, localtime_epoch: int, localtime: str) -> None:
        self.name = name
        self.region = region
        self.country = country
        self.lat = lat
        self.lon = lon
        self.tz_id = tz_id
        self.localtime_epoch = localtime_epoch
        self.localtime = localtime


class WeatherResponse:
    location: Location
    current: Current

    def __init__(self, location: Location, current: Current) -> None:
        self.location = location
        self.current = current
