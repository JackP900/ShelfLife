from datetime import datetime, timedelta
from db import add_product


def days_from_now(n):
    return (datetime.now() + timedelta(days=n)).strftime("%Y-%m-%d")

add_product("0001", "Fresh Milk", "Dairy", 1.20, days_from_now(1), 8)    
add_product("0002", "Croissant", "Bakery", 1.50, days_from_now(4), 12)     
add_product("0003", "Cheddar", "Dairy", 3.00, days_from_now(10), 5)   

