# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas

name_on_order = st.text_input('What is your name', '')
st.write('Your name is ', name_on_order)

# Write directly to the app
st.title("Customize your smoothie :cup_with_straw:")
st.write(
    "Choose the fruits you want:"
)

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.stop()
#st.text(fruityvice_response.json())

pd_df = my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()
                                                                      
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients', 
    my_dataframe,
    max_selections = 5    
)
st.write(len(ingredients_list))

if ingredients_list:
    st.write(ingredients_list)

    ingredients_string = ' '.join(ingredients_list)

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        st.subheader(fruit_chosen + ' Nutriotion information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_dt = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '""" + name_on_order + """')"""

    time_to_insert = st.button('Submit order')

    #st.write(my_insert_stmt)

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered ' + name_on_order + '!', icon="✅")
