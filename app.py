import streamlit as st
from bs4 import BeautifulSoup
import requests
import urllib.request
import numpy as np
from PIL import Image

# Define Streamlit app
st.markdown("<h1 style='text-align: center;'>Amazon Product Scraper</h1>",unsafe_allow_html=True)
st.write("\n")
st.write("\n")
st.write("\n")

def starR(n):
    if n%1<0.5: return int(n//1)*"⭐"
    else: return (int(n//1)+1)*"⭐"

product = st.text_input("Enter the product name:")
if st.button('Search'):
    if product=="": st.error("Please Enter Something!!")
    else:
        st.write("\n")
        st.write("\n")
        HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36","Accept-Language": "en-US,en;q=0.9"}
        try:
            response = requests.get(f"https://www.amazon.in/s?k={product}",headers=HEADERS)
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            st.error(f"HTTP Error: {errh}")
        except requests.exceptions.ConnectionError as errc:
            st.error(f"Error Connecting: {errc}")
        except requests.exceptions.Timeout as errt:
            st.error(f"Timeout Error: {errt}")
        except requests.exceptions.RequestException as err:
            st.error(f"Something went wrong: {err}")

        soup = BeautifulSoup(response.content, "html.parser")
        dibba = soup.findAll("div", {"class": "a-section a-spacing-small a-spacing-top-small"})
        bigdibba = soup.findAll("div", {"class": "a-section aok-relative s-image-fixed-height"})
        if len(dibba)>0:
            dibba.pop(0)
            # Iterate through the scraped data
            for i in range(len(dibba)):
                # Scraping Name
                n = dibba[i].find("span", {"class": "a-size-medium a-color-base a-text-normal"})
                name = n.get_text() if n else "NA"

                # Scraping Price
                p = dibba[i].find("span", {"class": "a-offscreen"})
                price = p.get_text() if p else "NA"

                # Scraping Rating
                r = dibba[i].find("span", {"class": "a-icon-alt"})
                if r:
                    rn = float( r.get_text()[:3])
                    r = starR(rn)
                else: r="NA";rn=None

                # Scraping no. of reviews
                rw = dibba[i].find("span", {"class": "a-size-base s-underline-text"})
                reviews = rw.get_text() if rw else "NA"

                # Product link
                bl = dibba[i].find("a",{"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})
                if bl:
                    l = bl.get("href")
                    if l: bl = "https://www.amazon.in" +l
                        
                #Creating 2 Columns
                col1, col2 = st.columns(2)

                # Scraping image
                image = bigdibba[i].find("img", {"class": "s-image"})
                if image:
                    img_url = image.get("src")
                    try:
                        with urllib.request.urlopen(img_url) as response:
                            # Check if the response is successful
                            if response.status == 200:
                                # Read the image data
                                img_data = np.array(Image.open(response))
                                # Display the image using Streamlit
                                col1.image(img_data, caption=f"Image {i+1}")
                    except Exception as e:
                        col1.error(f"Error: {e}\nFailed to open the image URL.")
                else:
                    col1.write("Image link: NA")

                # Display product details
                col2.write(f"**{i+1}. Product Details:**")
                col2.write(f"- Name: {name}")
                col2.write(f"- Price: {price}")
                if rn:
                    if rn >= 4.0: col2.markdown(f"- Rating: {r} <span style='color:green;'>({rn})</span>", unsafe_allow_html=True)
                    elif rn <= 3.0: col2.markdown(f"- Rating: {r} <span style='color:red;'>({rn})</span>", unsafe_allow_html=True)
                    else: col2.markdown(f"- Rating: {r} <span style='color:orange;'>({rn})</span>", unsafe_allow_html=True)
                else: col2.write(f"- Rating: {r}")
                col2.write(f"- No. of Reviews: {reviews}")
                col2.write(f"- Product Link: [Amazon]({bl})")

                # Add a separator between products
                st.write("---")
            else: st.error("No Results found")
        else: st.error("No Results found")
