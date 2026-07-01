# ShelfLife

Built at BeanHacks.

Coffee shops and grocers throw out a lot of food that was fine to sell an hour earlier. The problem is timing: nobody wants to manually re-tag the price on a carton of milk every few hours as it creeps toward its expiry date, so it either sells at full price or ends up in the bin.

ShelfLife handles that re-tagging for you. Scan a product, tell it when the item expires, and it decides how much to discount as the clock runs down. The markdown gets deeper as an item gets closer to expiry, has more stock sitting around, or the shop gets closer to closing time. The goal is to sell the thing before it's binned without slashing the price more than you have to.

## How it works

You scan a barcode with your phone or webcam. ShelfLife looks the product up in Open Food Facts to pre-fill the name and category, then you add the price, expiry date, and how much stock you have.

On the dashboard, every product shows up as a shelf ticket colour-coded by urgency: green if you've got more than five days, amber inside five days, red at two days or fewer. Hit "Reprice" and the app sends the product's details to Claude, which returns a new price and a one-line explanation of why. There's a hard floor at 30% of the original price and a ceiling at the original price, so the model can't do anything silly. Every price change gets logged so you can see the history.

## Tech stack

- Python + Flask for the backend
- SQLite for storage (two tables: `products` and `price_updates`)
- Anthropic's Claude (Sonnet) for the pricing decisions
- Open Food Facts API for barcode lookups
- html5-qrcode for in-browser scanning
- Plain HTML, CSS, and vanilla JS on the front end

## Running it locally

You'll need Python 3.9+ and an Anthropic API key.

```bash
# from inside the ShelfLife folder
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install flask requests anthropic python-dotenv
```

Add your API key to a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your-key-here
```

Set up the database and drop in a few sample products:

```bash
python -c "from db import init_db; init_db()"
python seed.py
```

Then start the server:

```bash
flask run
# or: python app.py
```

Open http://localhost:5000 and you'll see the seeded products on the dashboard. Head to `/add` to scan something new.

## Project layout

```
ShelfLife/
├── app.py            # Flask routes
├── db.py             # SQLite setup and queries
├── pricing.py        # Claude pricing logic
├── off_lookup.py     # Open Food Facts barcode lookup
├── seed.py           # sample products
├── templates/        # index, add, base
└── static/           # css + js (scanner, dashboard)
```

## Routes

- `GET /` — the dashboard
- `GET /add` — the scan-and-add page
- `GET /lookup/<barcode>` — barcode lookup against Open Food Facts
- `POST /save` — save a new product
- `POST /reprice/<id>` — ask Claude for a new price and log it

## What's next

A few things we didn't get to during the hackathon: automatic repricing on a schedule instead of a button press, a proper login so different shops can keep their own stock separate, and a summary of how much waste and revenue the discounts actually saved.
