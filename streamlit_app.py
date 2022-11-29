import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

# function to select a fruit to get information about
def get_fruityvice_date(this_fruit_choice):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

# originaly the error message of line 35 is displayed, as there is no default value to the variable
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_date(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")
# function to fetch the current fruit load list
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * from fruit_load_list")
    return my_cur.fetchall()

# add a button to call the list
if streamlit.button('Get fruit load list'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.dataframe(my_data_rows)

streamlit.header('Add a new fruit to our list')

# add a function to add a new fruit to the fruit list
def insert_row_snowflake(fruit_to_add):
  with my_cnx2.cursor() as my_cur2:
    query_in = "insert into fruit_load_list values (?)"
    my_cur2.execute(query_in,fruit_to_add)

# input text to add later
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
# button to add
if streamlit.button('Add the fruit above'):
  my_cnx2 = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  insert_row_snowflake(add_my_fruit)

'''
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
streamlit.write('Thanks for adding '+ add_my_fruit)

my_cnx2 = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur2 = my_cnx2.cursor()
my_cur2.execute("insert into fruit_load_list values ('from streamlit')")
streamlit.text("ser")
'''
