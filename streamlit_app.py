
import streamlit
import pandas
import snowflake.connector
import requests
from urllib.error import URLError

streamlit.title("Hello World")
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def my_func(this_fruit):  
  streamlit.write('The user entered ', this_fruit)
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+this_fruit)    
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized
  

streamlit.header('Fruityvice Advice')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
  if not fruit_choice:
    streamlit.error("Please select Fruit")
  else:
    my_norm=my_func(fruit_choice)
    streamlit.dataframe(my_norm)
except URLError as e:
  streamlit.error()
  


def get_my_all_fruit_list():  
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_cur = my_cnx.cursor()
  my_cur.execute("select * from fruit_load_list")
  return my_cur.fetchall()

if streamlit.button("Fruit List"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_my_all_fruit_list()
  streamlit.dataframe(my_data_rows)

streamlit.stop()
fruit_add = streamlit.text_input('What fruit would you like add?')
streamlit.write('Thanks for adding ', fruit_add)
my_str="insert into fruit_load_list values('"+ fruit_add + "')"
my_cur.execute(my_str)
