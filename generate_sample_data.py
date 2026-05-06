import csv
import random
from datetime import datetime, timedelta

random.seed(42)

DISHES = [
    {"dish_name": "Fried Noodles", "dish_category": "staple", "kitchen_section": "Hot Kitchen"},
    {"dish_name": "Steamed Dumplings", "dish_category": "pastry", "kitchen_section": "Chinese Pastry"},
    {"dish_name": "Cold Cucumber Salad", "dish_category": "cold dish", "kitchen_section": "Cold Dishes"},
    {"dish_name": "Stir-fried Vegetables", "dish_category": "vegetable", "kitchen_section": "Hot Kitchen"},
    {"dish_name": "Congee Side Toppings", "dish_category": "side dish", "kitchen_section": "Cold / Prep"},
    {"dish_name": "Roasted Chicken", "dish_category": "meat", "kitchen_section": "Hot Kitchen"},
    {"dish_name": "Steamed Fish", "dish_category": "seafood", "kitchen_section": "Hot Kitchen"},
    {"dish_name": "Fried Rice", "dish_category": "staple", "kitchen_section": "Hot Kitchen"},
    {"dish_name": "Fruit Platter", "dish_category": "dessert", "kitchen_section": "Cold Dishes"},
    {"dish_name": "Chinese Pastry Assortment", "dish_category": "pastry", "kitchen_section": "Chinese Pastry"},
    {"dish_name": "Braised Pork", "dish_category": "meat", "kitchen_section": "Hot Kitchen"},
    {"dish_name": "Mixed Seafood", "dish_category": "seafood", "kitchen_section": "Hot Kitchen"},
]

MEAL_PERIODS = ["Breakfast", "Lunch", "Dinner"]
EVENT_TYPES = ["normal", "group_tour", "banquet", "wedding"]
WEATHER_TYPES = ["sunny", "cloudy", "rainy"]


def get_waste_level(leftover_ratio: float) -> str:
    if leftover_ratio <= 0.15:
        return "Low"
    elif leftover_ratio <= 0.35:
        return "Medium"
    else:
        return "High"


def get_possible_reason(leftover_ratio: float, event_type: str, service_time_remaining: int, refill_count: int) -> str:
    if leftover_ratio > 0.35 and event_type == "normal":
        return "Low guest demand"
    if leftover_ratio > 0.35 and refill_count >= 3:
        return "Over-refilled during service"
    if leftover_ratio > 0.25 and service_time_remaining <= 30:
        return "Refilled too late in service"
    if leftover_ratio > 0.25:
        return "Overproduction"
    if leftover_ratio <= 0.15:
        return "Regular consumption"
    return "Demand slowed near the end"


def get_recommended_action(waste_level: str, service_time_remaining: int, refill_count: int) -> str:
    if waste_level == "High" and service_time_remaining <= 30:
        return "Avoid final refill and reduce next initial quantity"
    if waste_level == "High":
        return "Reduce initial quantity"
    if waste_level == "Medium" and refill_count >= 2:
        return "Use smaller refill batch"
    if waste_level == "Medium":
        return "Reduce final refill quantity"
    return "Maintain current quantity"


def generate_rows(num_rows: int = 500):
    rows = []
    start_date = datetime(2025, 10, 3)

    for _ in range(num_rows):
        current_date = start_date + timedelta(days=random.randint(0, 160))
        weekday = current_date.strftime("%A")

        dish = random.choice(DISHES)
        meal_period = random.choice(MEAL_PERIODS)

        event_type = random.choices(
            EVENT_TYPES,
            weights=[0.65, 0.2, 0.1, 0.05],
            k=1
        )[0]

        weather = random.choice(WEATHER_TYPES)
        occupancy_rate = round(random.uniform(0.45, 0.95), 2)

        estimated_guests = random.randint(60, 220)

        if event_type in ["banquet", "wedding"]:
            estimated_guests += random.randint(30, 100)

        actual_guests = max(30, int(estimated_guests * random.uniform(0.75, 1.15)))

        base_prepared_qty = actual_guests / random.uniform(18, 30)

        if dish["dish_category"] in ["staple", "meat", "seafood"]:
            prepared_qty = round(base_prepared_qty * random.uniform(1.1, 1.5), 1)
        elif dish["dish_category"] in ["cold dish", "side dish"]:
            prepared_qty = round(base_prepared_qty * random.uniform(0.7, 1.2), 1)
        else:
            prepared_qty = round(base_prepared_qty * random.uniform(0.6, 1.1), 1)

        refill_count = random.randint(0, 4)
        service_time_remaining = random.choice([15, 30, 45, 60, 90])

        waste_factor = random.uniform(0.05, 0.40)

        if service_time_remaining <= 30 and refill_count >= 2:
            waste_factor += random.uniform(0.05, 0.18)

        if event_type == "normal" and occupancy_rate < 0.6:
            waste_factor += random.uniform(0.05, 0.15)

        if dish["dish_category"] in ["cold dish", "side dish", "dessert"]:
            waste_factor += random.uniform(0.02, 0.12)

        leftover_qty = round(prepared_qty * min(waste_factor, 0.75), 1)
        leftover_ratio = round(leftover_qty / prepared_qty, 2) if prepared_qty > 0 else 0

        waste_level = get_waste_level(leftover_ratio)
        possible_reason = get_possible_reason(leftover_ratio, event_type, service_time_remaining, refill_count)
        recommended_action = get_recommended_action(waste_level, service_time_remaining, refill_count)

        rows.append({
            "date": current_date.strftime("%Y-%m-%d"),
            "weekday": weekday,
            "meal_period": meal_period,
            "dish_name": dish["dish_name"],
            "dish_category": dish["dish_category"],
            "kitchen_section": dish["kitchen_section"],
            "estimated_guests": estimated_guests,
            "actual_guests": actual_guests,
            "event_type": event_type,
            "occupancy_rate": occupancy_rate,
            "weather": weather,
            "prepared_qty": prepared_qty,
            "leftover_qty": leftover_qty,
            "leftover_ratio": leftover_ratio,
            "service_time_remaining": service_time_remaining,
            "refill_count": refill_count,
            "waste_level": waste_level,
            "possible_reason": possible_reason,
            "recommended_action": recommended_action,
        })

    return rows


def save_csv(rows, file_path: str):
    fieldnames = list(rows[0].keys())

    with open(file_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    rows = generate_rows(500)
    save_csv(rows, "data/buffet_waste_sample.csv")
    print("Created: data/buffet_waste_sample.csv")
    print(f"Rows: {len(rows)}")
