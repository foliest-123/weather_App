from flask import Flask, jsonify, render_template,request
import requests
import mysql.connector

app = Flask(__name__)

# Creating connection object
mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'username',
    password = '1234',
    db='weather_app'
)
 
cursor=mydb.cursor()

  


@app.route('/')
def index():
   return render_template("home.html")
@app.route('/weather',methods=["GET","POST"])
def weather():
    api_key = "863242cfb2b1d357e6093d9a4df19a4b"
    search_data = request.form.get('search_data')
    print(search_data)
    if request.method == "POST":
         data = request.form.get('country')
         print(data)
         if data is not None:
          query = "SELECT countryname FROM country WHERE countryname LIKE %s"
        
          try:
            cursor.execute(query, (data + '%',))
            limited_cities = cursor.fetchall()
            return data
          except mysql.connector.Error as err:
            print("Error:", err)
            
         else:
           return "Invalid input"  
    
# API endpoint URL
    country="japan"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={search_data}&visiblity&appid={api_key}&units=celcius&pressure=units"
    response = requests.get(url)
# Check if the request was successful
    if response.status_code == 200:
     weather_data = response.json()
     weathers=weather_data['weather'][0]['main']
     desc=weather_data['weather'][0]['description']
     windspeed=weather_data['wind']['speed']
     pressure=weather_data['main']['pressure']
     humidity=weather_data['main']['humidity']
     deg=weather_data['wind']['deg']
     title=weather_data['name']
     con=weather_data['sys']['country']
     return render_template('weather.html',desc=desc,windspeed=windspeed,humidity=humidity,pressure=pressure,weathers=weathers,deg=deg,title=title,con=con)    
    else:
     print("Failed to retrieve weather data",response.status_code)
     return render_template('weather.html')

@app.route('/filter')
def filter():
    country = request.args.get('country', default='', type=str)
    query = "SELECT * FROM country WHERE countryname LIKE %s limit 10"
    try:
        cursor.execute(query, (country + '%',))
        filtered_cities = cursor.fetchall()
        return jsonify(filtered_cities)
    except mysql.connector.Error as err:
        print("Error:", err)
        return jsonify([])

if __name__ == "__main__":
    app.run(debug=True)