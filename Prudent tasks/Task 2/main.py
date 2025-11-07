from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional
from price_gap_pair import find_price_gap_pair
import os, requests, time

app = FastAPI(title="Prudent Task 2 API")

# ----------- RETRY HELPER -----------
def get_with_retry(url, retries=2, timeout=15):
    for attempt in range(retries):
        try:
            r = requests.get(url, timeout=timeout)
            if r.status_code == 200:
                return r
        except Exception:
            if attempt < retries - 1:
                time.sleep(1)
    raise HTTPException(status_code=502, detail="Upstream movie API timeout")

# ----------- ENDPOINT 1: POST /api/price-gap-pair -----------
class PairRequest(BaseModel):
    nums: List[int]
    k: int = Field(ge=0)

@app.post("/api/price-gap-pair")
def price_gap_pair(req: PairRequest):
    pair = find_price_gap_pair(req.nums, req.k)
    if pair is None:
        return {"pair": None, "values": None}
    i, j = pair
    return {"pair": [i, j], "values": [req.nums[i], req.nums[j]]}

# ----------- ENDPOINT 2: GET /api/movies -----------
@app.get("/api/movies")
def get_movies(q: Optional[str] = Query(None), page: int = Query(1, ge=1)):
    if not q:
        return {"page": page, "total_pages": 0, "total_results": 0, "movies": []}

    api_key = os.getenv("MOVIE_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing MOVIE_API_KEY environment variable")

    try:
        url = f"https://www.omdbapi.com/?apikey={api_key}&s={q}&page={page}"
        response = get_with_retry(url)
        data = response.json()

        if data.get("Response") == "False":
            return {"page": page, "total_pages": 0, "total_results": 0, "movies": []}

        movies = []
        for item in data.get("Search", []):
            details_url = f"https://www.omdbapi.com/?apikey={api_key}&t={item['Title']}"
            details = get_with_retry(details_url).json()
            movies.append({
                "title": item["Title"],
                "director": details.get("Director", "Unknown")
            })

        total_results = int(data.get("totalResults", 0))
        total_pages = (total_results // 10) + (1 if total_results % 10 else 0)

        return {
            "page": page,
            "total_pages": total_pages,
            "total_results": total_results,
            "movies": movies
        }

    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Error contacting movie API: {str(e)}")
