# # Import python packages
# import streamlit as st
# import os
# # from snowflake.snowpark.context import get_active_session
# from snowflake.snowpark.functions import col

# # Write directly to the app
# st.title(f":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
# st.write(
#   """Choose the fruits you want in your custom Smoothie!
#   """)

# name_on_order = st.text_input('Name on Smoothie: ')
# st.write('The name on your Smoothie will be :',name_on_order)

# cnx = st.connection("snowflake")
# session = cnx.session()
# my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# # st.dataframe(data=my_dataframe, use_container_width=True)

# ingredient_list = st.multiselect(
#     'Choose upto 5 ingredient: ',my_dataframe,max_selections=5
# )

# if ingredient_list:
#     ingredients_string = ' '

#     for fruit_choosen in ingredient_list:
#         ingredients_string = " ".join(ingredient_list)

#     # st.write(ingredients_string)

#     my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
#                         values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    
#     # st.write(my_insert_stmt)
#     time_to_insert = st.button('Submit Order')

#     if time_to_insert:
#         session.sql(my_insert_stmt).collect()
#         st.success(f'Your Smoothie is ordered! {name_on_order} ', icon="✅")

# import requests  
# smoothiefroot_response = requests.get("[https://my.smoothiefroot.com/api/fruit/watermelon](https://my.smoothiefroot.com/api/fruit/watermelon)")  
# st.text(smoothiefroot_response)











# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

# Page Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write("""
Choose the fruits you want in your custom Smoothie!
""")

# Customer Name
name_on_order = st.text_input("Name on Smoothie:")

st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake Connection
cnx = st.connection("snowflake")
session = cnx.session()

# Get Fruit List
my_dataframe = (
    session.table("smoothies.public.fruit_options")
    .select(col("FRUIT_NAME"))
)

fruit_list = my_dataframe.to_pandas()["FRUIT_NAME"].tolist()

# Fruit Selection
ingredient_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)

# Display Nutrition Information
if ingredient_list:
    st.subheader("Fruit Nutrition Information")

    for fruit in ingredient_list:
        try:
            smoothiefroot_response = requests.get(
                f"https://my.smoothiefroot.com/api/fruit/{fruit.lower()}"
            )

            if smoothiefroot_response.status_code == 200:
                st.write(f"### {fruit}")
                st.json(smoothiefroot_response.json())
            else:
                st.warning(f"Could not retrieve information for {fruit}")

        except Exception as e:
            st.error(f"Error retrieving data for {fruit}: {e}")

# Submit Order
if ingredient_list:

    ingredients_string = ", ".join(ingredient_list)

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders
        (ingredients, name_on_order)
        VALUES
        ('{ingredients_string}', '{name_on_order}')
    """

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success(
            f"Your Smoothie is ordered! {name_on_order}",
            icon="✅"
        )
