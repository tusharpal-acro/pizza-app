from flask import Flask
from flask import render_template
from flask import request
from flask import make_response
from flask import redirect
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
        'image': 'https://lh3.googleusercontent.com/proxy/3zPagFGhmmaLfcihvVeErq9tuCfo_cy__-EaFAPlObnAf7viLSnCO0QDiKoaSsnEoS1KtYefXyjTwemnWjHUgKf1RkIEo3aCTua01NjeC5whNNGlNwXU42-_'
    },
    '9': {
        'name': 'Pizza Valentino',
        'price': '88.68',
        'description': 'Dessert cotton candy apple pie topping. Sugar plum tart sugar plum. Cheesecake marzipan soufflé pie muffin chocolate cake.',
        'image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcTWm6xKLRc4jlpT2JXY7SkmvCB5a4tI0r5_o7LQ0KLtknI7FKFF&usqp=CAU'
    },    
}

def cookie_add_to_cart(pizza_id):
    if 'cart' in request.cookies:
        cart = request.cookies['cart']
        cart_data = ast.literal_eval(cart)

        if pizza_id in cart_data:
            cart_data[pizza_id] = cart_data[pizza_id] + 1
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
    if 'cart' in request.cookies:
        total = 0
        data = ast.literal_eval(request.cookies['cart'])
        for pizza in data:
            total = total + data[pizza] * float(pizzas_data[pizza]['price'])
        return round(total, 2)
    else:
        return -1

def checkout_pizzas_sidebar_data():
    data = ast.literal_eval(request.cookies['cart'])
    pizzas = []

    for pizza in data:
        pizzas.append(
            [
                pizzas_data[pizza]['name'],
                data[pizza] * float(pizzas_data[pizza]['price']),
                data[pizza]
            ]
        )
    return pizzas

@app.route('/')
def pizzas():
    return render_template('pizzas.html', pizzas_data = pizzas_data, cart_total = cart_total())

@app.route('/addtocart')
def add():
    pizza_id = request.args.get('pizza')
    new_cookie = cookie_add_to_cart(pizza_id)

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

