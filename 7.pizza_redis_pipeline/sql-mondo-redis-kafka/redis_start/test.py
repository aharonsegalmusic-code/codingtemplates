dic = {
  "common_allergens": [
    "milk",
    "dairy",
    "wheat",
    "gluten",
    "eggs",
    "soy",
    "fish",
    "shellfish",
    "shrimp",
    "clams",
    "tree nuts",
    "peanuts",
    "pine nuts",
    "walnuts",
    "sesame",
    "mustard",
    "celery",
    "sulfites"
  ],
  "forbidden_non_kosher": [
    "pork",
    "ham",
    "bacon",
    "pepperoni",
    "prosciutto",
    "salami",
    "shrimp",
    "clams",
    "lobster",
    "seafood",
    "shellfish",
    "pancetta",
    "lard"
  ],
  "meat_ingredients": [
    "chicken",
    "beef",
    "steak",
    "meatball",
    "sausage",
    "pepperoni",
    "ham",
    "bacon",
    "prosciutto",
    "salami",
    "pork",
    "meat",
    "pancetta",
    "sirloin",
    "ribeye"
  ],
  "dairy_ingredients": [
    "cheese",
    "mozzarella",
    "parmesan",
    "ricotta",
    "feta",
    "gorgonzola",
    "provolone",
    "cheddar",
    "butter",
    "cream",
    "alfredo",
    "milk",
    "dairy",
    "goat cheese"
  ]
}

pizza_type = "cheese"

pizza = {"pizza_type" : pizza_type,
         "hit" : False,
         "is_meat" : False,
         "is_dairy" : True,
         "is_kosher" : True
         }

# step 1 -> NOT KOSHER
if any(pizza_type in dic[key] for key in ["forbidden_non_kosher"]):
    pizza["hit"] = True
    pizza["is_kosher"] = False

# step 1 
if any(pizza_type in dic[key] for key in ["dairy_ingredients"]):
    pizza["hit"] = True

# step 1 
if any(pizza_type in dic[key] for key in ["meat_ingredients"]):
    pizza["hit"] = True
    pizza["is_meat"] = True

if pizza["is_dairy"] and pizza["is_meat"]:
    pizza["is_kosher"] = False  

burn = not pizza["is_kosher"]