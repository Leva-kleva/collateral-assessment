import pickle
import pandas as pd
from geopy.distance import geodesic
import math
import warnings
# warnings.filterwarnings('ignore')

with open('ml/flat/xgb_model.pkl', 'rb') as f:
    xgb_model = pickle.load(f)

with open('ml/flat/labelencoder.pkl', 'rb') as f:
    labelencoder = pickle.load(f)

q = {
    'wallsMaterial': ['panel'],
    'floorNumber': [4],
    'floorsTotal': [17],
    'totalArea': [51.2],
    'kitchenArea': [9.7],
    'latitude': [55.858817],
    'longitude': [37.638755]
}


def do_beautiful_data(data):
    key = ['wallsMaterial', 'floorNumber', 'floorsTotal', 'totalArea',
           'kitchenArea', 'latitude', 'longitude']
    ans = {}
    for el in key:
        ans[el] = data[el]
    return ans


def eco_class(df):
    if (df['wallsMaterial'].values in [0, 5]):
        return 5
    if (df['wallsMaterial'].values in [7, 6]):
        return 4
    if (df['wallsMaterial'].values in [1]):
        return 3
    if (df['wallsMaterial'].values in [2, 3, 4]):
        return 2
    if (df['wallsMaterial'].values in [8]):
        return 1


def calculate_cost(queryset=q):
    def get_azimuth(latitude, longitude):
        rad = 6372795

        llat1 = city_center_coordinates[0]
        llong1 = city_center_coordinates[1]
        llat2 = latitude
        llong2 = longitude

        lat1 = llat1 * math.pi / 180.
        lat2 = llat2 * math.pi / 180.
        long1 = llong1 * math.pi / 180.
        long2 = llong2 * math.pi / 180.

        cl1 = math.cos(lat1)
        cl2 = math.cos(lat2)
        sl1 = math.sin(lat1)
        sl2 = math.sin(lat2)
        delta = long2 - long1
        cdelta = math.cos(delta)
        sdelta = math.sin(delta)

        y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
        x = sl1 * sl2 + cl1 * cl2 * cdelta
        ad = math.atan2(y, x)

        x = (cl1 * sl2) - (sl1 * cl2 * cdelta)
        y = sdelta * cl2
        z = math.degrees(math.atan(-y / x))

        if (x < 0):
            z = z + 180.

        z2 = (z + 180.) % 360. - 180.
        z2 = - math.radians(z2)
        anglerad2 = z2 - ((2 * math.pi) * math.floor((z2 / (2 * math.pi))))
        angledeg = (anglerad2 * 180.) / math.pi

        return round(angledeg, 2)

    flat = pd.DataFrame(do_beautiful_data(queryset))

    flat['wallsMaterial'] = labelencoder.transform(flat['wallsMaterial'])
    city_center_coordinates = [55.7522, 37.6156]
    flat['distance'] = list(
        map(lambda x, y: geodesic(city_center_coordinates, [x, y]).meters, flat['latitude'], flat['longitude']))
    flat['azimuth'] = list(map(lambda x, y: get_azimuth(x, y), flat['latitude'], flat['longitude']))
    flat['distance'] = flat['distance'].round(0)
    flat['azimuth'] = flat['azimuth'].round(0)

    flat = flat.drop('latitude', axis=1)
    flat = flat.drop('longitude', axis=1)

    xgb_prediction_flat = xgb_model.predict(flat).round(0)
    price = (xgb_prediction_flat) * flat['totalArea'][0]


    return {"cost": int(price[0].round(-3)), "eco": eco_class(flat)}
