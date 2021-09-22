import json
from flask import Flask, request, make_response, abort, session
import ml
import schemes
import objects
import conf

app = Flask(__name__)
app.config['SECRET_KEY'] = conf.secret_key
app.secret_key = conf.secret_key  # os.urandom(24)
models = {
    'car': ml.car.model.calculate_cost,
    'flat': ml.flat.model.calculate_cost,
}
form = {
    'car': objects.objects['car'].keys(),
    'flat': objects.objects['flat'].keys(),
}

translate = {
    "floorNumber": "этаж",
    "floorsTotal": "количество этажей в доме",
    "kitchenArea": "площадь кухни",
    "latitude": "географическую широту",
    "longitude": "географическую долготу",
    "totalArea": "общую площадь",
    "wallsMaterial": "тип дома",
    '': "неизвестно",
    'block': "блочный",
    'brick': "кирпичный",
    'monolith': "монолитный",
    'monolithBrick': "монолитно-кирпичный",
    'old': "старый",
    'panel': "панельный",
    'stalin': "сталинка",
    'wood': "деревянный",
    'gasoline': "бензин",
    'diesel': "дизель",
    'SYG': 'газ',
    'hybrid': 'гибрид',
    'electro': 'электро',
    'full': 'полный',
    'front': 'передний',
    'rear': 'задний',
    'automatic': 'автомат',
    'variator': 'вариатор',
    'robot': 'робот',
    'mechanics': 'механика',
    'mark': 'марку',
    'Model': 'модель',
    'Generation': 'поколение',
    'Engine': 'тип двигателя',
    'Drive': 'тип привода',
    'Box': 'коробку передач',
    'Mileage': 'пробег',
    'Year': 'год выпуска',
    'Engine_volume': 'объем двигателя',
    'Torque': 'крутящий момент',
}

def template_response(body, code, is_json=False):
    if not is_json:
        status = "info" if code < 400 else "error"
        tmp = f'{{"{status}": "{body}"}}'
        body = tmp
    response = make_response(body, code)
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/request', methods=['POST'])
def req():
    if not schemes.check(request, schemes.req.object):
        return template_response('Невалидный запрос', 400)

    object = request.json.pop('object')[0]

    if not schemes.check(request, schemes.req.post[object]):
        return template_response('Невалидный запрос', 400)

    queryset = request.json
    for key, value in queryset.items():
        if value[0].isdigit():
            queryset[key] = [int(value[0])]
        else:
            try: queryset[key] = [float(value[0])]
            except: pass

    if queryset.get('wallsMaterial') is not None:
        if queryset['wallsMaterial'][0] == "": queryset['wallsMaterial'] = ['panel']
        # queryset['wallsMaterial'] = [objects.id_materials[queryset['wallsMaterial'][0]]]

    ans = models[object](queryset)
    body, code = ans, 200

    return template_response(json.dumps(body), code, is_json=True)


@app.route('/get_params', methods=['POST'])
def get_params():
    print(request.json)
    object = request.json['object']
    response = {}
    for el in form[object]:
        if request.json.get(el) is None:
            if isinstance(objects.objects[object][el], list):
                response[el] = objects.objects[object][el]
            elif isinstance(objects.objects[object][el], tuple): # function
                flg = True
                data = []
                for e in objects.objects[object][el][1]:
                    if request.json.get(e) is None or request.json[e] == "":
                        flg = False
                        break
                    data.append(request.json[e])
                if flg:
                    response[el] = objects.objects[object][el][0](*data)
    response['translate'] = translate
    return response


if __name__ == '__main__':
    app.run(debug=conf.debug, port=conf.port, host=conf.host)
