from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

app = FastAPI()

executor = ThreadPoolExecutor(max_workers=5)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobRequest(BaseModel):
    keyword: str

@app.post("/scrape-jobs/")
async def scrape_jobs(request: JobRequest):
    keyword = request.keyword.lower()
    data = await run_in_threadpool(lamda:scraper_func(leyword))
    return data

def scraper_func(keyword:str):
    google_search_url = f"https://www.google.com/search?q={keyword}+site:wellfound.com"

    chrome_options = Options()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(google_search_url)
        links = driver.find_elements(By.XPATH, "//a[@href]")
        loaded = False

        for link in links:
            if "Wellfound" in link.get_attribute("innerHTML"):
                link.click()
                loaded = True
                break

        if not loaded:
            return JSONResponse(
                content={"error": "No Wellfound links found in the search results."},
                status_code=404,
            )

        wait = WebDriverWait(driver, 10)
        elements = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/div[4]/div[2]/div"))
        )
        page_content = elements[0].get_attribute("innerHTML")

        company_names = page_content.split("h2")
        job_titles = page_content.split("mr-2 text-sm font-semibold text-brand-burgandy hover:underline")

        job_data = {
            company_names[i].split(">")[-1].replace("</", ""): 
            job_titles[i].split(">")[1].replace("</a", "").strip()
            for i in range(1, min(len(company_names), len(job_titles)), 2)
        }

        return {"jobs": job_data}

    except Exception as e:
        return JSONResponse(
            content={"error": f"An error occurred: {str(e)}"},
            status_code=500,
        )
    finally:
        driver.quit()

