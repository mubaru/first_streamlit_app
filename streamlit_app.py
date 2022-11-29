import streamlit
import pandas
import requests
import snowflake.connector

streamlit.title('My parents new healthy diner')

streamlit.header('menu🍞')
streamlit.text('🥑 fish')
streamlit.text('🥣 fish with rice')
streamlit.text('🥗 fish in water')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")

fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
streamlit.write('The user entered ', fruit_choice)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# normalizing json file
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# adding normalized data to a table
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list:")
streamlit.dataframe(my_data_rows)

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding '+ add_my_fruit)

my_cnx2 = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur2 = my_cnx2.cursor()
my_cur2.execute("insert into fruit_load_list values ('from streamlit')")
streamlit.text("ser")
