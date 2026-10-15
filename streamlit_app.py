# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col


# Write directly to the app
st.title(":cup_with_straw: Customise Your Smoothie :cup_with_straw:")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)


name_on_order = st.text_input('Name of Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)


session = get_active_session()


fruit_df = (
    session.table("FRUIT_OPTIONS")
    .sort("FRUIT_NAME")
    .to_pandas()
)

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_df["FRUIT_NAME"].tolist()
)


if ingredients_list:

    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    my_insert_stmt = f"""
    INSERT INTO smoothies.public.orders
    (name_on_order, ingredients)
    VALUES
    ('{name_on_order}', '{ingredients_string}')
"""

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(
        f"Your smoothie has been ordered, {name_on_order}!",
        icon="✅"
    )


        

#if ingredients_list:
    #ingredients_string = ''

   # for fruit_chosen in ingredients_list:
        #ingredients_string += fruit_chosen + ' ' 

   # my_insert_stmt = f"""
        #INSERT INTO smoothies.public.orders(ingredients)
       # VALUES ('{ingredients_string}')
  #  """

  #  time_to_insert = st.button("Submit Order")

    #if time_to_insert:
       # session.sql(my_insert_stmt).collect()

      #  st.success(
          #  "Your Smoothie is ordered!",
          #  icon="✅"
        #)
