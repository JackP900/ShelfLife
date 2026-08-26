import anthropic
import os
import json

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_price(name, category, original_price, days_left, stock, time_of_day):

    prompt = f"""You are a pricing assistant for a coffee shop, helping reduce waste by discounting products before they expire. Your goal is to set a price low enough to sell the item before its expiry date, but high enough to protect margin — don't discount more than necessary.

    Product details:
    - Name: {name}
    - Category: {category}
    - Original price: £{original_price}
    - Days until expiry: {days_left}
    - Stock remaining: {stock}
    - Time of day: {time_of_day}

    Consider all factors: items closer to expiry or with high stock need deeper discounts; time of day matters (near closing, push harder to sell).

    Rules:
    - Never price above the original price of £{original_price}.
    - Never discount below 30% of the original price.

    Respond with ONLY a JSON object in exactly this format, with no other text:
    {{"price": <number>, "reasoning": "<one short sentence explaining the decision>"}}
    """

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=300,
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = message.content[0].text

    # Strip any code fences the model might wrap around the JSON
    response_text = response_text.strip()
    if response_text.startswith("```"):
        response_text = response_text.strip("`")
        if response_text.startswith("json"):
            response_text = response_text[4:]
        response_text = response_text.strip()

    result = json.loads(response_text)
    price = result["price"]
    reasoning = result["reasoning"]

    floor = original_price * 0.3
    if price < floor:
        price = floor
    if price > original_price:
        price = original_price

    return {"price": price, "reasoning": reasoning}

