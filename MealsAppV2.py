import pandas as pd
import streamlit as st
import io

# Initialize session state for navigation
if 'screen' not in st.session_state:
    st.session_state.screen = 'main'

# Load data once
df_recipes = pd.read_excel('test_meals.xlsx', sheet_name='recipes')
df_ingredients = pd.read_excel('test_meals.xlsx', sheet_name='list')
df_ingredients['TotalQuantity'] = df_ingredients['Quantity1Measures'] * df_ingredients['MeasuresNeeded']
merged_df = pd.merge(df_ingredients, df_recipes, left_on='RecipeID', right_on='RecipeID', how='left')

# Determine correct recipe column name after merge
recipe_col = 'RecipeName_x' if 'RecipeName_x' in merged_df.columns else 'RecipeName'

# Define screens
def main_menu():
    st.title("Meal Planner")
    st.write("Choose an action:")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Select Meals"):
            st.session_state.screen = 'select_meals'
        if st.button("Generate Menu"):
            st.session_state.screen = 'generate_menu'
    with col2:
        if st.button("See Categories and Recipes"):
            st.session_state.screen = 'see_categories'
        if st.button("Add/Modify Recipe"):
            st.session_state.screen = 'add_modify_recipe'

def select_meals_screen():
    st.header("Select Meals")
    selected_recipes = st.multiselect(
        'Select recipes:',
        df_recipes['RecipeName'].unique()
    )

    filtered_df = merged_df[merged_df[recipe_col].isin(selected_recipes)]

    if not filtered_df.empty:
        summaryingredientstobuy = filtered_df.groupby(['IngredientName', 'QuantityMeasure'], as_index=False)['TotalQuantity'].sum()
        st.dataframe(summaryingredientstobuy)

        # Download button
        output = io.BytesIO()
        summaryingredientstobuy.to_excel(output, index=False)
        st.download_button(
            label="Download Shopping List as Excel",
            data=output.getvalue(),
            file_name='shoppinglistfromchecklist.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    else:
        st.write("Please select at least one recipe to see the shopping list.")

    if st.button("Back to Main Menu"):
        st.session_state.screen = 'main'

def generate_menu_screen():
    st.header("Generate Menu")
    st.write("This feature is coming soon!")
    if st.button("Back to Main Menu"):
        st.session_state.screen = 'main'

def see_categories_screen():
    st.header("See Categories and Recipes")
    st.write("This feature is coming soon!")
    if st.button("Back to Main Menu"):
        st.session_state.screen = 'main'

def add_modify_recipe_screen():
    st.header("Add/Modify Recipe")
    st.write("This feature is coming soon!")
    if st.button("Back to Main Menu"):
        st.session_state.screen = 'main'

# Navigation logic
if st.session_state.screen == 'main':
    main_menu()
elif st.session_state.screen == 'select_meals':
    select_meals_screen()
elif st.session_state.screen == 'generate_menu':
    generate_menu_screen()
elif st.session_state.screen == 'see_categories':
    see_categories_screen()
elif st.session_state.screen == 'add_modify_recipe':
    add_modify_recipe_screen()


