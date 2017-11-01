from flask import Flask, jsonify, Response
import os
import csv
import json

from SkillHelper import SkillResponse, CardDeck, CardCommerce, Price, Button, ComplexEncoder

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))  # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')


@app.route('/')
def hello_world():
    return 'Hell'


@app.route('/sample')
def sample():
    skill = SkillResponse("card.commerce")
    cd = CardDeck()
    with open(os.path.join(APP_STATIC, "food.csv"), 'r', encoding='utf8') as f:
        data = csv.DictReader(f)
        for d in data:
            # print(d)
            if d['DP'] != d['RP'] or d['DP'] != '':  # isDiscount == True
                price = Price(discount_rate=int(d['DR']),
                              discount_type="rate",
                              discount_price=int(d['DP']),
                              fixed_discount_price=0,
                              regular_price=int(d['RP']),
                              is_discount=True) \
                    if d['DR'] != '' else \
                    Price(discount_rate=0,
                          discount_type="amount",
                          discount_price=int(d['DP']),
                          fixed_discount_price=int(d['FP']),
                          regular_price=int(d['RP']),
                          is_discount=True)
                # readability.........

                cd.add(CardCommerce(image_url=d['image'],
                                    title=d['title'],
                                    price="",
                                    link_url=d['button_url'],
                                    buttons=[Button(button_type="url", label=d['button_name'], data={"url": d['button_url']})]))
            else:  # isDiscount == False
                price = Price(discount_rate=0,
                              discount_type="",
                              discount_price=0,
                              fixed_discount_price=0,
                              regular_price=int(d['RP']),
                              is_discount=False)
                cd.add(CardCommerce(image_url=d['image'],
                                    title=d['title'],
                                    price=price,
                                    link_url=d['button_url'],
                                    buttons=[Button("url", d['button_name'], {"url", d['button_url']})]))

        skill.add(cd)

    return Response(json.dumps(skill.repr_json(), cls=ComplexEncoder, ensure_ascii=False), mimetype='application/json')


if __name__ == '__main__':
    app.run()
