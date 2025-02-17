# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests



cnx = st.connection("snowflake")

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie! :cup_with_straw:")
st.write(
    """choose the fruits you want  in the cutsom smoothie
    """
)





session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)



ingredients_list = st.multiselect('choose upto 5 ingredients', my_dataframe,max_selections=5)
order_name = st.text_input('Name of the Smoothie');
st.write('The name of your smoothie is ' + order_name)
time_to_insert = st.button('Submit',)

# if(ingredients_list):
#    st.write(ingredients_list)
#    st.text(ingredients_list)

ingredients_string = ''

for fruits_chosen in ingredients_list:
    ingredients_string += ' ' +  fruits_chosen
    st.subheader(fruits_chosen + "Nutrition Information")
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/"+fruits_chosen)
    sf_df = st.dataframe(data = smoothiefroot_response.json(),use_container_width = True)

st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','""" + order_name + """')"""

# st.write(my_insert_stmt)

if time_to_insert and ingredients_string:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!', icon="✅")

