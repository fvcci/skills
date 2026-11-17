---
name: office-meals
description: Pick and order Felix's office lunches and dinners from the Greptile DoorDash Meal Manager calendar using his food preferences and past picks. Use when Felix asks to order office meals, pick meals for the week, or asks what he should eat from Meal Manager.
---

# Office meals

Felix eats from the **Greptile - Meals** Meal Manager team (SF Office) on DoorDash. Each weekday has three or four lunch carts (checkout 9:30am PT) and three dinner carts (checkout 4:00pm PT). The tool returns the same carts under both the Lunch and Dinner calendars; split them by checkout time instead. Each cart has a per-person spend limit (`spend_limit_cents`, usually $30).

## Preferences

- **Likes:** Asian food, sandwiches, noodles, rice, Italian, tacos.
- **Loves** tomatoes and vegetables. Favor dishes that include them.
- **Sandwiches need acidity.** When there's an option, pick or customize sandwiches to include something acidic, in this order of preference: pickled peppers, then pickled onions, then pickles.
- **Never** order vegan or vegetarian dishes. Every meal has meat or fish.
- **No repeats within a day:** lunch and dinner on the same day must be different kinds of food (no two sandwiches, no sushi twice). The same cuisine/culture twice in a day is fine (e.g. Korean BBQ bowl + Japanese ramen, or ramen + sushi). Repeating a kind of food on back-to-back days is fine; don't skip a better option just to spread things out across days.
- **Override:** ignore the preferences above when one option is clearly worth it, based on restaurant reviews or reviews of a specific dish. Say why when you do.

## What his past picks show

Derived from ~50 meals he picked himself (Aug–Nov 2026). Per-restaurant pick/skip counts are in [restaurants.md](restaurants.md); check it before choosing.

- **Rank cuisines in this order:** Japanese (sushi rolls, bento combos, sashimi, poke), Cantonese/Chinese (BBQ rice plates, Peking duck, wok dishes, beef noodle soup), Korean (bibimbap, galbitang), Southeast Asian (Singaporean, Thai, Vietnamese, Burmese), then Western.
- **Fish is a favorite, salmon above all.** He picks salmon often: grilled salmon plates, smoked salmon tartine/bagel, salmon curry, salmon with black bean sauce, sashimi.
- **Avoid these, he has never picked them when offered:** Indian, Sweetgreen, goop kitchen, Chipotle, fast-casual Mediterranean wrap/bowl shops (Sajj, Locali, Sababa, Fanoos, Hummus Mediterranean, Alora), Jewish/American delis (Wise Sons, Mendocino Farms), burgers, and generic taquerias. Only pick from these when every cart in the slot is on this list.
- **Mexican and pizza only when it's the standout:** he picked a prawn burrito, carnitas tacos, and Che Fico pizza, but skipped most taquerias and pizza shops.
- **Turkish/Mediterranean sit-down entrées are fine** (Iskender kebab, karnıyarık). He skips most wrap-and-bowl Mediterranean chains, but he did pick Za'atar's Lamb & Beef Kabob Wrap with pickled onions, so a well-built meat wrap with pickles can still win.
- **Salads only when they're hearty and the alternatives are weak.** He has picked MIXT's Bachelor Salad and Soba Salad, Gott's Vietnamese Chicken Salad, and Tender Greens protein plates (steak, short rib). Treat MIXT as a fallback, not a first choice.
- **Lunch can be brunch-style:** omelets at Son & Garden, a soft-scramble tartine with tomato bisque at Tartine.
- **Sandwich style:** banh mi and tartines beat deli sandwiches. He disliked the focaccia sandwiches (Golden Focaccia) even though he ordered them twice; don't pick focaccia sandwiches.
- **Combos beat single items:** he picks two-item BBQ plates, multi-item bentos and box lunches.
- **Spend leftover budget on a side** when the main leaves room under the limit. He usually adds miso soup, chicken corn soup, spring rolls, curry puffs, or guacamole. Chinese entrées usually don't include rice; add steamed rice.
- **Noodle soups are fine for delivery**; don't skip them because of the broth.
- **Every lunch and dinner slot gets a meal.** Never leave a slot empty. When every cart is weak, pick the best of them and say why.

## Before adding anything

- **Check every cart in the slot for items Felix already added.** He sometimes pre-picks meals himself. Don't add a second meal for that slot or replace his pick; mention it in the summary instead, and flag it if it breaks a rule.
- **Check order history** with `doordash_get_order_history` (`include_group_order=true`) for the last week. Avoid ordering the exact same dish again unless it's the clearly-worth-it pick.
- **Look up menus at the delivery time.** Pass `scheduled_delivery_time` (lunch about 12:30pm PT, dinner about 6pm PT, in UTC) to `doordash_get_restaurant_menu` and `doordash_get_food_item`. Dinner-only items don't show up otherwise, and `menu_id` can differ between lunch and dinner.
- **An `ITEM_UNAVAILABLE` / `item_hours` error** means that menu isn't live yet. Retry after the store opens or closer to the meal; if it still fails, pick a backup and say so.

## New restaurants: Felix picks the dish

A restaurant is new when it appears nowhere in [restaurants.md](restaurants.md). For every slot with a new restaurant:

1. Fill the slot with your best pick from the other carts, so it has a meal at checkout.
2. Open the summary with a **New restaurants** section. For each one, give the slot (day, lunch or dinner, checkout time), cuisine, a review summary with sources, and 3 to 5 dishes that fit his preferences, each with its price, photo, and one line on why.
3. Ask him to pick a dish there or keep your pick. Use `AskUserQuestion` when it's available, one question per new restaurant, with your pick as the last option.
4. When he picks a dish, swap it in for your pick and add its side the usual way. Then record the restaurant in [restaurants.md](restaurants.md): under "Picked once" with his dish, or under "Offered once and skipped".

## Research and report

- Look up each pick on review sites (The Infatuation, Yelp, Google reviews, Eater, SF Chronicle) for both the restaurant and the specific dish before choosing. Cite the sources you used.
- In the final summary, include a picture of every dish you picked. Use the item's `image_url` from the DoorDash menu or cart; if it has none, use a photo from a review site, or say no photo was found.

## Refreshing restaurants.md

To refresh the pick history, pull his group orders from order history. Then call `doordash_get_meal_manager_calendars` with `target_date` set to each past date to see which carts he passed on. Past dates still return their carts. Update the counts and the "last updated" date in [restaurants.md](restaurants.md).
