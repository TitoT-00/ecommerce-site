from flask import Flask, render_template, jsonify, request, session
from dotenv import load_dotenv
import os
import stripe
import json

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Stripe configuration
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Product data
games = [
    {
        'id': 1,
        'name': 'Super Mario Bros. 3',
        'price': 49.99,
        'description': 'Classic NES game in excellent condition',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/a/a5/Super_Mario_Bros._3_coverart.png',
        'platform': 'NES'
    },
    {
        'id': 2,
        'name': 'The Legend of Zelda',
        'price': 79.99,
        'description': 'Original NES classic in working condition',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/4/41/Legend_of_zelda_cover_%28with_cartridge%29_gold.png',
        'platform': 'NES'
    },
    {
        'id': 3,
        'name': 'Sonic the Hedgehog 2',
        'price': 39.99,
        'description': 'SEGA Genesis classic, tested and working',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/0/0c/Sonic_2_US_Cover.jpg',
        'platform': 'SEGA Genesis'
    },
    {
        'id': 4,
        'name': 'Final Fantasy VII',
        'price': 89.99,
        'description': 'Complete in box, PlayStation classic RPG',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/c/c2/Final_Fantasy_VII_Box_Art.jpg',
        'platform': 'PlayStation'
    },
    {
        'id': 5,
        'name': 'Pokemon Red Version',
        'price': 69.99,
        'description': 'Original GameBoy classic, new save battery',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/a/a6/Pok%C3%A9mon_box_art_-_Red_Version.png',
        'platform': 'GameBoy'
    },
    {
        'id': 6,
        'name': 'Chrono Trigger',
        'price': 199.99,
        'description': 'Rare SNES RPG, authentic cartridge',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/a/a7/Chrono_Trigger_Box.jpg',
        'platform': 'SNES'
    },
    {
        'id': 7,
        'name': 'Street Fighter II',
        'price': 44.99,
        'description': 'SNES fighting classic, tested working',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/1/1d/Street_Fighter_II_SNES_boxart.jpg',
        'platform': 'SNES'
    },
    {
        'id': 8,
        'name': 'Mega Man X',
        'price': 59.99,
        'description': 'SNES action platformer in great condition',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/c/cd/Mega_Man_X_box_art.jpg',
        'platform': 'SNES'
    },
    {
        'id': 9,
        'name': 'Castlevania: Symphony of the Night',
        'price': 129.99,
        'description': 'PlayStation masterpiece, complete with manual',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/8/83/Castlevania_SOTN_PAL.jpg',
        'platform': 'PlayStation'
    },
    {
        'id': 10,
        'name': 'GoldenEye 007',
        'price': 69.99,
        'description': 'Legendary N64 FPS, multiplayer classic',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/3/36/GoldenEye007box.jpg',
        'platform': 'Nintendo 64'
    },
    {
        'id': 11,
        'name': 'Metal Gear Solid',
        'price': 79.99,
        'description': 'Tactical espionage action, PlayStation classic',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/3/33/Metal_Gear_Solid_cover_art.png',
        'platform': 'PlayStation'
    },
    {
        'id': 12,
        'name': 'Super Metroid',
        'price': 89.99,
        'description': 'SNES sci-fi adventure masterpiece',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/e/e4/Smetroid_boxart.jpg',
        'platform': 'SNES'
    },
    {
        'id': 13,
        'name': 'Resident Evil 2',
        'price': 69.99,
        'description': 'Survival horror classic, dual-disc complete',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/0/06/RE2_Cover_Art.jpg',
        'platform': 'PlayStation'
    },
    {
        'id': 14,
        'name': 'Pokemon Blue Version',
        'price': 69.99,
        'description': 'Original GameBoy classic, new save battery',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/a/aa/Pok%C3%A9mon_box_art_-_Blue_Version.png',
        'platform': 'GameBoy'
    },
    {
        'id': 15,
        'name': 'Banjo-Kazooie',
        'price': 49.99,
        'description': 'N64 3D platforming adventure',
        'image_url': 'https://upload.wikimedia.org/wikipedia/en/1/16/Banjo_Kazooie_Cover.png',
        'platform': 'Nintendo 64'
    }
]

consoles = [
    {
        'id': 101,
        'name': 'Nintendo 64',
        'price': 159.99,
        'description': 'N64 console with original controller and cables',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/0/02/N64-Console-Set.png',
        'condition': 'Excellent'
    },
    {
        'id': 102,
        'name': 'PlayStation 1',
        'price': 119.99,
        'description': 'Original PlayStation with two controllers',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/9/95/PSX-Console-wController.png',
        'condition': 'Good'
    },
    {
        'id': 103,
        'name': 'SEGA Genesis',
        'price': 129.99,
        'description': 'Classic SEGA Genesis with all cables',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/a/a1/Sega-Mega-Drive-JP-Mk1-Console-Set.jpg',
        'condition': 'Very Good'
    },
    {
        'id': 104,
        'name': 'Super Nintendo',
        'price': 149.99,
        'description': 'SNES console in original box',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/3/31/SNES-Mod1-Console-Set.jpg',
        'condition': 'Excellent'
    },
    {
        'id': 105,
        'name': 'GameBoy Color',
        'price': 89.99,
        'description': 'Atomic Purple, excellent condition',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/3/31/SNES-Mod1-Console-Set.jpg',
        'condition': 'Excellent'
    }
]

accessories = [
    {
        'id': 201,
        'name': 'N64 Controller',
        'price': 29.99,
        'description': 'Original Nintendo 64 controller in great condition',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/5/56/N64-Controller-Gray.jpg',
        'compatibility': 'Nintendo 64'
    },
    {
        'id': 202,
        'name': 'PlayStation Memory Card',
        'price': 19.99,
        'description': '15 blocks of storage for PlayStation games',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/d/d5/PSX-Memory-Card.jpg',
        'compatibility': 'PlayStation'
    },
    {
        'id': 203,
        'name': 'SEGA Genesis Controller',
        'price': 24.99,
        'description': '6-button controller for SEGA Genesis',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/a/a0/Sega-Genesis-6Button-Cont.jpg',
        'compatibility': 'SEGA Genesis'
    },
    {
        'id': 204,
        'name': 'Game Boy Link Cable',
        'price': 14.99,
        'description': 'Original link cable for trading Pokemon',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/e/e4/GameBoy-Link-Cable.jpg',
        'compatibility': 'Game Boy'
    },
    {
        'id': 205,
        'name': 'AC Adapter',
        'price': 12.99,
        'description': 'Universal power adapter for SEGA Genesis',
        'image_url': 'https://upload.wikimedia.org/wikipedia/commons/b/b7/SEGA-Genesis-Power-Adapter.jpg',
        'compatibility': 'SEGA Genesis'
    }
]

@app.route('/')
def home():
    featured_games = games[:3]
    featured_consoles = consoles[:2]
    featured_accessories = accessories[:2]
    return render_template('index.html', 
                         games=featured_games,
                         consoles=featured_consoles,
                         accessories=featured_accessories)

@app.route('/games')
def games_page():
    return render_template('games.html', products=games)

@app.route('/consoles')
def consoles_page():
    return render_template('consoles.html', products=consoles)

@app.route('/accessories')
def accessories_page():
    return render_template('accessories.html', products=accessories)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/order')
def order():
    return render_template('order_form.html')

@app.route('/api/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd'
        )
        return jsonify({
            'clientSecret': intent.client_secret
        })
    except Exception as e:
        return jsonify(error=str(e)), 403

def calculate_order_amount(items):
    # Replace this with your actual calculation
    return 1400

if __name__ == '__main__':
    app.run(debug=True)
