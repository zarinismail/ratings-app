from flask import Flask, render_template
app = Flask(__name__)

# For web hosting
application = app

import csv
import math

def convert_to_dict(filename):
    datafile = open(filename, newline='')
    my_reader = csv.DictReader(datafile)
    list_of_dicts = list(my_reader)
    datafile.close()

    return list_of_dicts

# Convert CSV (descending order by year) to dictionary
movies_list = convert_to_dict("movies.csv")

# Convert other CSV (in ascending order by year) to dictionary
asc_movies_list = convert_to_dict("movies_asc.csv")

# Create tuples listing ID and novel title (descending list)
trio_list = []
for p in movies_list:
    trio_list.append( (p['ID'], p['title'], p['year']) )

# Create tuples for ascending list
asc_trio_list = []
for p in asc_movies_list:
    asc_trio_list.append( (p['ID'], p['title'], p['year']) )

# Index page route (year descending)
@app.route('/')
# Route for loading 15 items per page (year descending)
@app.route('/page/<page_num>')
def load_page(page_num=1):
    page_num = int(page_num)
    # Number of items to show per page
    items = 15
    # Total items in list
    total = len(trio_list)
    # Total pages
    # Discovered math module and ceil() on Stack Overflow: https://stackoverflow.com/questions/2356501/how-do-you-round-up-a-number
    pages = math.ceil(total / items)
    if page_num <= pages:
        # Start point for slicing list
        start = (page_num - 1) * items
        # End point for slicing list
        end = start + items
        # Make sure end point does not exceed list length
        if end > total:
            end = total
    else:
        return f"<h1>This page does not exist</h1>"

    return render_template('page.html', trios=trio_list[start:end], page_num=page_num)

# Route for loading 15 items per page (year ascending)
@app.route('/page_asc/<page_num>')
def load_page_asc(page_num=1):
    page_num = int(page_num)
    # Number of items to show per page
    items = 15
    # Total items in list
    total = len(trio_list)
    # Total pages
    # Discovered math module and ceil() on Stack Overflow: https://stackoverflow.com/questions/2356501/how-do-you-round-up-a-number
    pages = math.ceil(total / items)
    if page_num <= pages:
        # Start point for slicing list
        start = (page_num - 1) * items
        # End point for slicing list
        end = start + items
        # Make sure end point does not exceed list length
        if end > total:
            end = total
    else:
        return f"<h1>This page does not exist</h1>"

    return render_template('page_asc.html', trios=asc_trio_list[start:end], page_num=page_num)

# Movie page route
@app.route('/movie/<num>')
def detail(num):
    try:
        movie_dict = movies_list[int(num) - 1]
    except:
        return f"<h1>Invalid value for movie ID: {num}</h1>"

    return render_template('movie.html', movies=movie_dict)


# Run app
if __name__ == '__main__':
    app.run(debug=True)