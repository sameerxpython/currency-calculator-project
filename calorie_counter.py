import streamlit as st

# Title
st.title("🍎 Calorie Counter App")

# Description
st.write("Enter the quantity of each food item you've eaten today:")

# Food items and their calorie values per unit
calorie_chart = {
    "Apple (1 piece)": 95,
    "Banana (1 piece)": 105,
    "Boiled Egg (1 piece)": 78,
    "Rice (1 cup)": 200,
    "Chapati (1 piece)": 70,
    "Chicken Breast (100g)": 165,
    "Milk (1 cup)": 120
}

# Initialize total calories
total_calories = 0

# Dictionary to hold user inputs
user_inputs = {}

# Loop through items and create number input fields
for item, calories_per_unit in calorie_chart.items():
    quantity = st.number_input(label=f"{item}", min_value=0, step=1, key=item)
    user_inputs[item] = quantity
    total_calories += quantity * calories_per_unit

# Show total calories
st.markdown("---")
st.subheader(f"🔢 Total Calories Consumed: {total_calories} kcal")

# Optional breakdown
with st.expander("See Calorie Breakdown"):
    for item, quantity in user_inputs.items():
        if quantity > 0:
            item_calories = quantity * calorie_chart[item]
            st.write(f"{item}: {quantity} × {calorie_chart[item]} kcal = {item_calories} kcal")
