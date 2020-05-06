from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect
import copy
import ast

app = Flask(__name__)

pizzas_data = {
    '1': {
        'name': 'Pizza Protono',
        'price': '14.99',
        'description': 'Dessert cotton candy apple pie topping. Sugar plum tart sugar plum. Cheesecake marzipan soufflé pie muffin chocolate cake.',
        'image': 'https://media-cdn.tripadvisor.com/media/photo-s/15/c5/a4/14/pepperoni-lovers.jpg'
    },
    '2': {
        'name': 'Pizza Indori',
        'price': '10.99',
        'description': 'Dessert cotton candy apple pie topping. Sugar plum tart sugar plum. Cheesecake marzipan soufflé pie muffin chocolate cake.',
        'image': 'https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/delish-homemade-pizza-horizontal-1542312378.png'
    },
    '3': {
        'name': 'Pizza Jadoogar',
        'price': '10.59',
        'description': 'Dessert cotton candy apple pie topping. Sugar plum tart sugar plum. Cheesecake marzipan soufflé pie muffin chocolate cake.',
        'image': 'https://images.dominos.co.in/new_margherita_2502.jpg'
    },
    '4': {
        'name': 'Pizza Lajawab',
        'price': '7.99',
        'description': 'Dessert cotton candy apple pie topping. Sugar plum tart sugar plum. Cheesecake marzipan soufflé pie muffin chocolate cake.',
        'image': 'https://enrilemoine.com/wp-content/uploads/2015/10/1-Mini-pizzas-para-Halloween-Halloween-mini-pizzas-SAVOIR-FAIRE-by-enrilemoine.jpg'
    },
    '5': {
        'name': 'Pizza Ghamandi',
        'price': '99.99',
        'description': 'Dessert cotton candy apple pie topping. Sugar plum tart sugar plum. Cheesecake marzipan soufflé pie muffin chocolate cake.',
        'image': 'https://img.kidspot.com.au/E0V7ORBz/w643-h428-cfill-q90/kk/2015/03/5532-500361-1.jpg'
    },
    '6': {
        'name': 'Pizza Jalebi',
        'price': '18.99',
        'description': 'Dessert cotton candy apple pie topping. Sugar plum tart sugar plum. Cheesecake marzipan soufflé pie muffin chocolate cake.',
        'image': 'https://www.askideas.com/wp-content/uploads/2016/11/Mickey-Mouse-Face-Shaped-Funny-Pizza.jpg'
    },
    '7': {
        'name': 'Pizza Aloobada',
        'price': '20.21',
        'description': 'Dessert cotton candy apple pie topping. Sugar plum tart sugar plum. Cheesecake marzipan soufflé pie muffin chocolate cake.',
        'image': 'https://i.pinimg.com/originals/22/f2/6f/22f26fd4e1451f36fec91660843d05de.jpg'
    },
    '8': {
        'name': 'Fufaji Special Pizza',
        'price': '8.91',
        'description': 'Dessert cotton candy apple pie topping. Sugar plum tart sugar plum. Cheesecake marzipan soufflé pie muffin chocolate cake.',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcQMC_B0buY4enATnQfetRtXmXrSLP8MD1gH7K8K9TUxtrIM-EwW&usqp=CAU'
    },
    '9': {
        'name': 'Pizza Valentino',
        'price': '88.68',
        'description': 'Dessert cotton candy apple pie topping. Sugar plum tart sugar plum. Cheesecake marzipan soufflé pie muffin chocolate cake.',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTWm6xKLRc4jlpT2JXY7SkmvCB5a4tI0r5_o7LQ0KLtknI7FKFF&usqp=CAU'
    },    
}

def cookie_add_to_cart(pizza_id, remove=False):
    if 'cart' in request.cookies:
        cart = request.cookies['cart']
        cart_data = ast.literal_eval(cart)

        if pizza_id in cart_data:
            if remove == False:
                cart_data[pizza_id] = cart_data[pizza_id] + 1
            else:
                cart_data[pizza_id] = cart_data[pizza_id] - 1
                if cart_data[pizza_id] == 0:
                    del cart_data[pizza_id]
        else:
            cart_data[pizza_id] = 1

        return repr(cart_data)
    else:
        return repr(
            {
                pizza_id: 1
            }
        )

def cart_total():
    currency_adjusted_pizzas = currency_adjusted_pizza_data()
    if 'cart' in request.cookies:
        total = 0
        data = ast.literal_eval(request.cookies['cart'])
        for pizza in data:
            total = total + data[pizza] * float(currency_adjusted_pizzas[pizza]['price'])
        return round(total, 2)
    else:
        return -1

def checkout_pizzas_sidebar_data():
    currency_adjusted_pizzas = currency_adjusted_pizza_data()
    data = ast.literal_eval(request.cookies['cart'])
    pizzas = []

    for pizza in data:
        pizzas.append(
            [
                currency_adjusted_pizzas[pizza]['name'],
                data[pizza] * float(currency_adjusted_pizzas[pizza]['price']),
                data[pizza]
            ]
        )
    return pizzas

def currency_adjusted_pizza_data():
    adjusted_pizza_data = copy.deepcopy(pizzas_data)
    if 'currency' in request.cookies:
        if request.cookies['currency'] == 'eur':
            for index in adjusted_pizza_data:
                cur_price = adjusted_pizza_data[index]['price']
                adjusted_pizza_data[index]['price'] = '{0:.2f}'.format(float(cur_price) * 0.93)
    return adjusted_pizza_data

@app.route('/')
def pizzas():
    currency_adjusted_pizzas = currency_adjusted_pizza_data()
    cart = ast.literal_eval(request.cookies['cart'])
    return render_template('pizzas.html', pizzas_data = currency_adjusted_pizzas, cart_total = cart_total(), cart = cart)

@app.route('/addtocart')
def add():
    pizza_id = request.args.get('pizza')
    new_cookie = cookie_add_to_cart(pizza_id)

    resp = make_response(redirect('/'))
    resp.set_cookie('cart', new_cookie)
    return resp 

@app.route('/removefromcart')
def remove():
    pizza_id = request.args.get('pizza')
    new_cookie = cookie_add_to_cart(pizza_id, True)

    resp = make_response(redirect('/'))
    resp.set_cookie('cart', new_cookie)
    return resp 

@app.route('/checkout')
def checkout():
    pdata = checkout_pizzas_sidebar_data()
    total = cart_total()
    return render_template('checkout.html', pdata = pdata, total = total)

@app.route('/continuecheckout')
def continuecheckout():
    resp = make_response(render_template('ontheway.html'))
    resp.set_cookie('cart', expires=0)
    return resp

@app.route('/changecurrency')
def changecurrency():
    currency = request.args.get('currency')

    resp = make_response(redirect('/'))
    resp.set_cookie('currency', currency)
    return resp
