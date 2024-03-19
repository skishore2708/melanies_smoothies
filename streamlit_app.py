# Import python packages
import streamlit as st
import requests
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """ Choose the fruits you want in your custom Smoothie!
    """
)

name_on_Order = st.text_input('Name on Smoothie: ')
st.write('The name on your Smoothie will be ', name_on_Order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('search_on'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

#Convert the Snowpark dataframe into pandas dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
st.dataframe(pd_df)
st.stop()

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:' , my_dataframe , max_selections = 5
)

if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)

    ingredients_string =''

    for each_fruit in ingredients_list:
        ingredients_string += each_fruit + ' '
        st.subheader(each_fruit + '  Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + each_fruit)
        fv_dv=st.dataframe(data=fruityvice_response.json(), use_container_width=True)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order,Order_Filled)
            values ('""" + ingredients_string + """','""" + name_on_Order+ """',0)""" 

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')
    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_Order +"!" , icon="✅")


