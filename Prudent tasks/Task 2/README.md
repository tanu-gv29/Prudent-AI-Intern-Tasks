Task 2 – Price Gap + Movies API 

This project has two small APIs made using FastAPI:

1. POST /api/price-gap-pair – finds a pair of numbers whose difference is `k`.  
2. GET /api/movies – shows a list of movies and their directors using the OMDb movie API.

What You Need

- Python 3.9 or newer  
- Internet connection  
- A free API key from [omdbapi.com/apikey.aspx](https://www.omdbapi.com/apikey.aspx)

Then install the 3 Python packages we use:

pip install fastapi uvicorn requests

Start Your Movie API Key

You get the key by signing up at OMDb.
When you receive the key, open your terminal and set it like this:

On Windows

set MOVIE_API_KEY=your_api_key_here

How to Run

1. Open the Task2 folder in your terminal.
2. Start the server:

   uvicorn main:app --reload

3. Wait until it says:

   Uvicorn running on http://127.0.0.1:8000

4. Open that link in your browser → click /docs to test easily.

Try the First API – POST /api/price-gap-pair

In the docs screen click POST /api/price-gap-pair → Try it out
and paste this example:

json
{
  "nums": [4, 1, 6, 3, 8],
  "k": 2
}


Click Execute and you should see:

{
  "pair": [0, 2],
  "values": [4, 6]
}

If no matching pair exists, you’ll get:

json
{
  "pair": null,
  "values": null
}

Try the Second API – GET /api/movies

In the docs screen click GET /api/movies → Try it out
Type a movie name, for example `batman`, and run it.
You’ll see something like this:

json
{
  "page": 1,
  "total_pages": 10,
  "total_results": 100,
  "movies": [
    {"title": "Batman Begins", "director": "Christopher Nolan"},
    {"title": "The Batman", "director": "Matt Reeves"}
  ]
}

If you leave the search box empty, it will show:

json
{
  "page": 1,
  "total_pages": 0,
  "total_results": 0,
  "movies": []
}
