import json


class SkillResponse:
    def __init__(self, response_type):
        self.type = response_type
        self.contents = {"type": self.type}
        self.quickReplies = []

    def repr_json(self):
        return dict(contents=self.contents, quickReplies=self.quickReplies)

    def add(self, param):
        if self.type == "text":
            self.contents["text"] = param.text

        elif self.type == "image":
            self.contents["image"] = param

        elif self.type == "card.text":
            self.contents["cards"] = param

        elif self.type == "card.image":
            self.contents["cards"] = param

        elif self.type == "card.commerce":
            self.contents["cards"] = param

        elif self.type == "quickReplies":
            self.quickReplies.append(param)

        else:
            print("I don't know this type -> " + param)


class QuickReplies:
    def __init__(self):
        self.type = "type"


class Text:
    def __init__(self, s):
        self.text = s


class Image:
    def __init__(self, s):
        self.text = s


class CardDeck:
    def __init__(self, cards=None):
        if cards is None:
            cards = []
        self.cards = cards

    def add(self, card):
        self.cards.append(card)

    def repr_json(self):
        a_list = []
        for card in self.cards:
            a_list.append(card.repr_json())

        return a_list


class CardImage:
    def __init__(self, image_url, title, description, link_url="", buttons=None):
        self.imageUrl = image_url
        self.title = title
        self.description = description
        self.linkUrl = link_url
        if buttons is None:
            buttons = []
        self.buttons = buttons

    def repr_json(self):
        return dict(imageUrl=self.imageUrl, title=self.title, description=self.description, linkUrl=self.linkUrl, buttons=self.buttons)


class CardText:
    def __init__(self, title, description, link_url, buttons):
        self.title = title
        self.description = description
        self.linkUrl = link_url
        self.buttons = buttons

    def repr_json(self):
        return dict(title=self.title, description=self.description, linkUrl=self.linkUrl, buttons=self.buttons)


class CardCommerce:
    def __init__(self, image_url, title, price, link_url, description="", buttons=None):
        self.imageUrl = image_url
        self.title = title
        self.price = price
        self.linkUrl = link_url
        self.description = description

        if buttons is None:
            buttons = []
        self.buttons = buttons

    def repr_json(self):
        return dict(imageUrl=self.imageUrl,
                    title=self.title,
                    description=self.description,
                    price=self.price,
                    linkUrl=self.linkUrl,
                    buttons=self.buttons)


class Button:
    def __init__(self, button_type, label, data):
        self.type = button_type
        self.label = label
        self.data = data

    def repr_json(self):
        return dict(name=self.type, label=self.label, data=self.data)


class Price:
    def __init__(self,
                 regular_price,
                 discount_price,
                 discount_type,
                 is_discount=False,
                 discount_rate=0,
                 fixed_discount_price=0,
                 currency_unit="원"):
        self.regularPrice = regular_price
        self.isDiscount = is_discount
        self.discountPrice = discount_price
        self.discountType = discount_type
        self.discountRate = discount_rate
        self.fixedDiscountPrice = fixed_discount_price
        self.currencyUnit = currency_unit

    def repr_json(self):
        return dict(regularPrice=self.regularPrice,
                    isDiscount=self.isDiscount,
                    discountPrice=self.discountPrice,
                    discountType=self.discountType,
                    discountRate=self.discountRate,
                    fixedDiscountPrice=self.fixedDiscountPrice,
                    currencyUnit=self.currencyUnit)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if hasattr(obj, 'repr_json'):
            return obj.repr_json()
        else:
            return json.JSONEncoder.default(self, obj)


skill = SkillResponse("text")
skill.add(Text("hi"))

print(skill.repr_json())
print(json.dumps(skill.repr_json(), cls=ComplexEncoder))

cd = CardDeck()
cd.add(CardImage(image_url="hell.jpg", title="title", description="desc", buttons=[Button("url", "label", {"url": "url_loc"})]))
cd.add(CardImage(image_url="hell.jpg", title="title", description="desc", buttons=[Button("url", "label", {"url": "url_loc"})]))

skill2 = SkillResponse("card.image")
skill2.add(cd)

print(json.dumps(skill2.repr_json(), cls=ComplexEncoder, sort_keys=True, indent=2))

price = Price(regular_price=4950,
              is_discount=True,
              discount_price=2970,
              discount_type="rate",
              discount_rate=40)

cd2 = CardDeck()
cd2.add(CardCommerce(image_url="i", title="dd", price=price, link_url="", buttons=[Button("url", "label", {"url": "url_loc"})]))

skill3 = SkillResponse("card.commerce")
skill3.add(cd2)

print(json.dumps(skill3.repr_json(), cls=ComplexEncoder, sort_keys=True, indent=2))
