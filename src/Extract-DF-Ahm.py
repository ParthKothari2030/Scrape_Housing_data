from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Reading source
f = open("Ahemdabad_source.txt","r",encoding="utf-8")
page_source = f.read()
f.close()

# parsing the soup using html parser
soup = BeautifulSoup(page_source,'html.parser')

# finds all the spc-img where we can get Title and Rera approvement
project_divs = soup.find_all('div', class_='spc-img')

# using img class extracted -> RERA and Project Name
projects_name_and_rera_registration= []
for div in project_divs:
    # get title from <img>
    img = div.find("img")
    # print(img.attrs)
    title = img["title"].strip() if img and "title" in img.attrs else None

    # get RERA status from <span>
    span = div.find("span", class_="spc-rr")
    # rera = span.get_text(strip=True) if span else "No"
    rera = "Yes" if (span and span.get_text(strip=True)) else "No"

    if title:
        projects_name_and_rera_registration.append({
            "title": title,
            "Rera registered": rera
        })


df_titleandrera = pd.DataFrame(projects_name_and_rera_registration)
# df_titleandrera

Location_and_builder = [] # Location and builder are done

for i in range(len(project_divs)):
    temp = project_divs[i].find_next_sibling("div", class_="spc-info")
    A = temp.find(class_="spc-location").get_text().strip().split(",")
    Location_and_builder.append(A)

df_locandbuild = pd.DataFrame(Location_and_builder)
df_locandbuild.drop(2, axis=1,inplace=True) # Dropping none columne inplace
df_locandbuild.rename(columns={0: "Location",1:"Builder"},inplace=True)
# df_locandbuild

price_fetch = []
for i in range(len(project_divs)):
   div_1 = project_divs[i].find_next_sibling("div", class_="spc-info")
   
   if bool(div_1.find(class_="spc-price")) == True: # finds the class where price is, If true then appends the price
      price_fetch.append(div_1.find(class_="spc-price").get_text().strip())
   else:
      price_fetch.append("None") # else appends none

df_price = pd.DataFrame(price_fetch)
df_price.rename(columns={0:"Price"},inplace=True)


def extract_project_info(info_div):
    info = {}
    
    # loop through li elements
    for li in info_div.select("ul.spc-feature li"):
        label = li.find("span", class_="spcf-lbl").get_text(strip=True)
        value = li.find("strong", class_="spcf-val sc").get_text(strip=True)
        info[label] = value
    
    # extract with defaults if missing
    return {
        "property_type": info.get("Configs"),
        "total_units": info.get("Total Units", None),
        "possession_status": info.get("Possession Status")
    }

all_projects = []

for div in project_divs:
    temp_div = div.find_next_sibling("div", class_="spc-info")
    if temp_div:  # check just in case some don't have info
        project_info = extract_project_info(temp_div)
        all_projects.append(project_info)

df_proptype_units_possesion = pd.DataFrame(all_projects)
# df_proptype_units_possesion

df_realestatedata = pd.concat([df_titleandrera, df_proptype_units_possesion, df_price, df_locandbuild],axis=1)
# len(df_realestatedata[df_realestatedata["Builder"].str.contains("By", na=False)])

df_realestatedata["Builder"] = df_realestatedata["Builder"].mask(
    ~df_realestatedata["Builder"].str.contains("By", na=False), # '~' = Bit wise Not function , returns complement
    "Not known"
) # Replaces Builders not avaiblable by None

df_realestatedata["Builder"] = (
    df_realestatedata["Builder"]
    .str.split("By", n=1)
    .str[-1]        # take the part after "By"
    .str.strip()    # remove leading/trailing spaces/newlines
) # Splits on basis of By and only lets Builder remain  
def detect_unit(val):
    val = val.strip()
    if "Cr" in val:
        return "Crore"
    elif "Lac" in val or "lac" in val or "Lacs" in val:
        return "Lac"
    else:
        return None   # explicitly return None if nothing matched

def Price_unit(val1, val2):
    unit1 = detect_unit(val1)
    unit2 = detect_unit(val2)

    # Fallbacks
    if unit1 is None and unit2 is not None:
        unit1 = unit2
    if unit1 is None:
        unit1 = "Lac"
    if unit2 is None:
        unit2 = "Lac"

    return unit1, unit2

def convert_to_lakh(value_str, unit):
    """Convert a string like '1.10' with unit into Lakhs."""
    try:
        num = float(value_str.replace("Cr.", "").replace("Cr", "").replace("Lac", "").strip())
    except:
        return np.nan
    
    if unit == "Crore":
        return num * 100  # 1 Cr = 100 Lakhs
    elif unit == "Lac":
        return num        # already in Lakhs
    else:
        return num

def parse_price(value):
    if pd.isna(value) or value.strip() == "None":
        return (np.nan, np.nan, np.nan)

    val = value.replace(",", "").strip()

    if "-" in val:
        low, high = val.split("-")
        low_s, high_s = low.strip(), high.strip()
        
        # Detect units
        unit1, unit2 = Price_unit(low_s, high_s)

        # Convert separately
        low_val = convert_to_lakh(low_s, unit1)
        high_val = convert_to_lakh(high_s, unit2)

        if np.isnan(low_val) or np.isnan(high_val):
            return (np.nan, np.nan, np.nan)
        
        avg = (low_val + high_val) / 2
        return (low_val, high_val, avg)
    else:
        unit = detect_unit(val)
        num = convert_to_lakh(val, unit)
        return (num, num, num)
    
df_realestatedata[["Min Price","Max Price","Average Price"]] = (
    df_realestatedata['Price'].apply(parse_price).apply(pd.Series)
    )
# print(df_realestatedata)
df_realestatedata.to_csv("Pyfile_ahm_data.csv",index=False)