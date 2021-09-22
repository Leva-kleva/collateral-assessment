from objects.db import *

engine = ['gasoline', 'diesel', 'SYG', 'hybrid', 'electro']
drive = ['full', 'front', 'rear']
box = ['automatic', 'variator', 'robot', 'mechanics']

params = {
    'mark': get_mark(),
    'Model': (get_model, ['mark']),
    'Generation': (get_generation, ['mark', 'Model']),
    'Engine': engine,
    'Drive': drive,
    'Box': box,
    'Mileage': [0],
    'Year': [0],
    'Engine_volume': [0],
    'Torque': [0],
}
