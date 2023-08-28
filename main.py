import google.generativeai as palm
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

messages = []

@app.post("/chatbot/{msg}")
async def chat(msg: str):
    palm.configure(api_key="AIzaSyD8mWHk0QRvnaulCGEFFmd94XKM-6Zwn9U")
    defaults = {
        "model": "models/chat-bison-001",
        "temperature": 0,
        "candidate_count": 1,
        "top_k": 40,
        "top_p": 0.95,
    }

    if not msg:
        raise HTTPException(status_code=422, detail="Message cannot be empty")


    context = "You are a creative bot helping in providing catchy taglines, brief content to be displayed in the webpage etc.."
    examples = [
    [
        "Give me a catchy tagline on 'Muliya Jewels' which is in the business of Gold, Silver and diamond Jewelery since 1944.",
        "Muliya Jewels: Timeless beauty, passed down for generations."
    ],
    [
        "Give me a catchy tagline on the brand 'Pepsi'",
        "Here are some catchy taglines for the brand 'Pepsi':\n\n* Pepsi: The taste that refreshes.\n* Pepsi: The choice of a new generation.\n* Pepsi: Live for now.\n* Pepsi: The Pepsi challenge.\n* Pepsi: The taste is gonna move ya.\n* Pepsi: The only thing that's cooler than Pepsi is you.\n* Pepsi: The taste that beats the heat.\n* Pepsi: The taste that's always in style.\n* Pepsi: The taste that's always there for you.\n* Pepsi: The taste that's always on point.\n* Pepsi: The taste that's always up for anything.\n* Pepsi: The taste that's always worth it.\n* Pepsi: The taste that's always yours."
    ],
    [
        "Give me a catchy tagline on 'Muliya Jewels' which is in the business of Gold, Silver and diamond Jewelery since 1944. Also give me a brief content to put up in the 'About' Section",
        "Muliya Jewels: Timeless beauty, passed down for generations.\n\nMuliya Jewels is a family-owned and operated business that has been in the jewelry industry since 1944. We are committed to providing our customers with the highest quality jewelry at the best possible prices. We offer a wide variety of gold, silver, and diamond jewelry, as well as a variety of other services, such as jewelry repair and appraisal. We are proud to be a part of the community and we are committed to providing our customers with the best possible shopping experience.\n\nWe believe that jewelry is a special way to express yourself and to commemorate important moments in your life. Whether you are looking for a gift for a loved one or for yourself, we are confident that you will find the perfect piece of jewelry at Muliya Jewels.\n\nWe invite you to visit our showroom today and experience the Muliya Jewels difference. We look forward to helping you find the perfect piece of jewelry to treasure for years to come."
    ]
    ]
    messages.append(msg)
        
    response = palm.chat(
        **defaults,
        context=context,
        examples=examples,
        messages=messages,
    )
    print(messages)
    return JSONResponse(content={"message": response.last})

@app.get("/clear")
async def clear():
    messages.clear()
    return {"message":"Done"}