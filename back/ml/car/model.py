import pickle
import pandas as pd
from category_encoders.target_encoder import TargetEncoder
from sklearn.preprocessing import Normalizer


eco = {'electro':1,
 'hybrid':2,
  'SYG':3 ,
  'gasoline':4,
  'diesel':5}

def get_cols(df) -> list:
    '''
    function return list of name numbers and categorials columns
    '''
    categorical_feature_mask = df.dtypes == object
    number_feature_mask = df.dtypes != object
    numbers_cols = df.columns[number_feature_mask].tolist()
    categorical_cols = df.columns[categorical_feature_mask].tolist()
    return [numbers_cols, categorical_cols]


def make_prediction(row, encoder, normalizer, file_model='ml/car/cars_model.pkl',
                    file_encoder='ml/car/cars_encoder.pkl',
                    file_normalizer='ml/car/cars_normalizer.pkl'):
    model = pickle.load(open(file_model, 'rb'))
    encder = pickle.load(open(file_encoder, 'rb'))
    normalizer = pickle.load(open(file_normalizer, 'rb'))
    numeric, categorical_cols = get_cols(row)
    row[categorical_cols] = encder.transform(row[categorical_cols])
    row[numeric] = normalizer.transform(row[numeric])
    price = model.predict(row)
    return price


def do_beautiful_data(data):
    key = ['Engine', 'Mileage', 'Drive',
           'Year', 'Box', 'Engine_volume',
           'mark', 'Generation', 'Model', 'Torque']
    ans = {}
    for el in key:
        ans[el] = data[el]
    return ans


def calculate_cost(queryset):
    ta = TargetEncoder()
    norm = Normalizer()
    print(queryset)
    data = pd.DataFrame(do_beautiful_data(queryset))
    cost = make_prediction(row=data, encoder=ta, normalizer=norm)
    return {"cost": int(cost[0]), "eco": eco[queryset["Engine"][0]]}


if __name__ == "__main__":
    car = pd.DataFrame({
        'Engine': ['gasoline'],
        'Mileage': [15500],
        'Drive': ['full'],
        'Year': [2019],
        'Box': ['automatic'],
        'Engine_volume': [3982],
        'mark': ['Mercedes-Benz'],
        'Generation': ['III (W463) 2018 – now'],
        'Model': ['G-Class'],
        'Torque': [610],
    })
    q = {'Box': ['automatic'], 'Drive': ['full'], 'Engine': ['gasoline'], 'Engine_volume': [3982], 'Mileage': [15500],
         'Torque': [610], 'Year': [2019], 'mark': ['Mercedes-Benz'], 'Model': ['G-Class'],
         'Generation': ['III (W463) 2018 – now']}
    ta = TargetEncoder()
    norm = Normalizer()
    a = make_prediction(row=car, encoder=ta, normalizer=norm,
                        file_model='cars_model.pkl', file_encoder='cars_encoder.pkl',
                        file_normalizer='cars_normalizer.pkl')
    print(a)
