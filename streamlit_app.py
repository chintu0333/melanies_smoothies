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

st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

# Customer Name
name_on_order = st.text_input("Name on Smoothie:")

st.write("The name on your Smoothie will be:", name_on_order)

# Snowflake Connection
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options and search values
my_dataframe = (
    session.table("smoothies.public.fruit_options")
    .select(
        col("FRUIT_NAME"),
        col("SEARCH_ON")
    )
)

fruit_df = my_dataframe.to_pandas()

# List shown to user
fruit_options = fruit_df["FRUIT_NAME"].tolist()

# Dictionary used for API lookups
search_lookup = dict(
    zip(
        fruit_df["FRUIT_NAME"],
        fruit_df["SEARCH_ON"]
    )
)

# Multiselect
ingredient_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

if ingredient_list:

    ingredients_string = ''

    for fruit_chosen in ingredient_list:

        ingredients_string += fruit_chosen + ' '

        st.subheader(fruit_chosen + ' Nutrition Information')

        search_on = search_lookup[fruit_chosen]

        try:

            smoothiefroot_response = requests.get(
                "https://my.smoothiefroot.com/api/fruit/" + search_on
            )

            st.dataframe(
                data=smoothiefroot_response.json(),
                use_container_width=True
            )

        except Exception as e:

            st.error(
                f"Error retrieving nutrition information for {fruit_chosen}: {e}"
            )

    my_insert_stmt = f"""
        INSERT INTO smoothies.public.orders
        (ingredients, name_on_order)
        VALUES
        ('{ingredients_string}',
         '{name_on_order}')
    """

    time_to_insert = st.button("Submit Order")

    if time_to_insert:

        session.sql(my_insert_stmt).collect()

        st.success(
            f"Your Smoothie is ordered! {name_on_order}",
            icon="✅"
        )
