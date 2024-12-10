# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col, when_matched
import requests
import pandas as pd

# Write directly to the app
st.title(":cup_with_straw: Custom Ordering App :cup_with_straw:")
st.write(
    "Choose the fruits you want in the following selections: "
)

name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name on your smoothie is", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
st.dataframe(data=my_dataframe, use_container_width=True)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients: ',
    my_dataframe,
    max_selections = 5
)

if ingredients_list:
   
    ingredients_string = ''

    for fruit in ingredients_list:
        ingredients_string += fruit + ' '
        st.subheader(fruit + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit)
        sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+name_on_order+"""')"""


    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered! ' + name_on_order, icon="✅")



