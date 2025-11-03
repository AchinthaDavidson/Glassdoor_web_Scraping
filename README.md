# Glassdoor IT Jobs Scraper for Sri Lanka

A **manual-assisted web scraping solution** to collect IT job data from Glassdoor, specifically designed for IT positions in Sri Lanka. This project uses a hybrid approach where users manually navigate past Glassdoor's protection mechanisms, then the scraper automatically extracts job details.

## 🎯 Features

- **Manual-Assisted Scraping**: Bypasses Glassdoor's anti-bot protection through user interaction
- **IT Job Filtering**: Automatically filters for IT-related positions
- **Comprehensive Data Extraction**: 
  - Job titles and descriptions
  - Company names
  - Location information
  - Salary estimates
  - Job URLs
- **Multiple Export Formats**: JSON and CSV output
- **Smart Job Detection**: Identifies IT jobs using keyword matching
- **User-Friendly Interface**: Step-by-step guidance through the scraping process

## 📊 Data Fields Collected

| Field | Description |
|-------|-------------|
| Title | Job position title |
| Company | Hiring company name |
| Location | Job location |
| Salary | Salary estimate (if available) |
| URL | Direct link to the job posting |
| Scraped At | Timestamp when data was collected |

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.7 or higher
- Google Chrome browser installed
- Internet connection
- Windows 10/11 (tested), macOS, or Linux

### Step 1: Clone or Download

Download all project files to your working directory:
- `simple_manual_scraper.py`
- `requirements.txt`
- `README.md`

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv glassdoor_env

# Activate virtual environment
# Windows:
glassdoor_env\Scripts\activate
# macOS/Linux:
source glassdoor_env/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: If you encounter pandas installation issues with Python 3.13+, try:
```bash
pip install pandas==2.1.4
```

### Step 4: Verify Installation

```bash
python simple_manual_scraper.py --help
```

## 🚀 How to Use

### Quick Start

1. **Run the scraper:**
```bash
python simple_manual_scraper.py
```

2. **Follow the on-screen instructions:**
   - Browser will open automatically
   - Navigate to Glassdoor manually
   - Complete any CAPTCHA/verification
   - Search for IT jobs
   - Let the scraper extract data

### Detailed Usage Guide

#### 1. **Initial Setup**
```bash
python simple_manual_scraper.py
```

#### 2. **Manual Navigation Process**
The scraper will guide you through these steps:

1. **Browser Opens**: Chrome browser opens automatically
2. **Navigate to Glassdoor**: Go to [glassdoor.com](https://www.glassdoor.com)
3. **Complete Verification**: 
   - Click "I'm not a robot" checkbox
   - Complete any image verification
   - Click "Continue" or "Verify"
4. **Search for Jobs**:
   - Type job keywords (e.g., "Python Developer", "Software Engineer")
   - Select location (Sri Lanka)
   - Click "Search"
5. **Confirm Ready**: Press ENTER in console when job listings appear

#### 3. **Automatic Data Extraction**
Once you confirm, the scraper will:
- Extract job information from the current page
- Filter for IT-related positions
- Display progress in real-time
- Ask you to navigate to the next page

#### 4. **Multi-Page Scraping**
For each additional page:
- Navigate to the next page manually
- Press ENTER in console
- Scraper extracts data automatically
- Repeat until desired number of pages

### Example Session

```
🚀 Starting Manual-Assisted Glassdoor Scraper
==================================================

🤝 MANUAL NAVIGATION REQUIRED

📋 Please follow these steps:

1. 🌐 I will open Glassdoor.com in a browser window
2. 🛡️  If you see "Help Us Protect Glassdoor" or CAPTCHA:
   • ✅ Click the "I'm not a robot" checkbox
   • ✅ Complete any image verification
   • ✅ Click "Continue" or "Verify"
3. 🔍 Navigate to the job search you want:
   • Type "Python Developer" (or your preferred search) in the search box
   • Select your location
   • Click "Search" button
4. ⏳ Wait until you see the job listings page
5. ⌨️  Press ENTER in this console when ready

👉 Press ENTER when you've completed the manual navigation and can see job listings...

✅ Great! You're on a Glassdoor job search page

🔍 Looking for job listings on current page...
✅ Found 15 jobs using selector: [data-test="job-title"]

✅  1. Senior Python Developer at TechCorp - Colombo
✅  2. Full Stack Developer at DataCorp - Remote
❌  3. Marketing Manager at SalesCorp - Colombo (not IT)
✅  4. DevOps Engineer at CloudCorp - Kandy
...
```

## 📁 Output Files

### Generated Files
- **JSON Format**: `glassdoor_manual_scrape_YYYYMMDD_HHMMSS.json`
- **CSV Format**: `glassdoor_manual_scrape_YYYYMMDD_HHMMSS.csv` (if pandas is installed)

### Sample Output Structure

```json
[
  {
    "title": "Senior Python Developer",
    "company": "TechCorp",
    "location": "Colombo, Sri Lanka",
    "salary": "$2,000 - $3,500",
    "url": "https://www.glassdoor.com/job-listing/...",
    "scraped_at": "2024-01-15T10:30:00"
  },
  {
    "title": "Full Stack Developer",
    "company": "DataCorp",
    "location": "Remote",
    "salary": "N/A",
    "url": "https://www.glassdoor.com/job-listing/...",
    "scraped_at": "2024-01-15T10:30:00"
  }
]
```

## ⚙️ Configuration Options

### Customizing Job Search

You can modify the scraper to search for different types of jobs:

1. **Edit the scraper file**:
```python
# In simple_manual_scraper.py, modify the IT keywords:
it_keywords = [
    'developer', 'engineer', 'programmer', 'software', 'python', 'java',
    'javascript', 'data scientist', 'data analyst', 'devops', 'cloud',
    'full stack', 'frontend', 'backend', 'mobile', 'web', 'qa', 'testing',
    'architect', 'technical', 'technology', 'coding', 'programming'
]
```

2. **Add your own keywords**:
```python
it_keywords = [
    'your_keyword_1', 'your_keyword_2',
    # ... existing keywords
]
```

### Adjusting Scraping Parameters

```python
# Change number of pages to scrape
success = scraper.scrape_jobs(max_pages=5)  # Scrape 5 pages instead of 3

# Modify job filtering logic
def is_it_job(self, title: str) -> bool:
    # Your custom logic here
    pass
```

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. **"Chrome driver not found"**
```bash
# Solution: Install webdriver-manager
pip install webdriver-manager
```

#### 2. **"No module named 'selenium'"**
```bash
# Solution: Install selenium
pip install selenium
```

#### 3. **Browser opens but no data extracted**
- **Check**: Are you on a job listings page?
- **Solution**: Navigate to actual job search results, not the homepage
- **Verify**: Look for job titles, company names on the page

#### 4. **"Access denied" or CAPTCHA loops**
- **Solution**: Complete the CAPTCHA manually
- **Wait**: Give it a few minutes between attempts
- **Check**: Ensure you're not being rate-limited

#### 5. **No IT jobs found**
- **Check**: Are you searching in the right location?
- **Verify**: Use IT-related search terms
- **Solution**: Try different search keywords

### Debug Mode

Enable detailed logging by modifying the scraper:

```python
# In simple_manual_scraper.py
logging.basicConfig(
    level=logging.DEBUG,  # Change from INFO to DEBUG
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('manual_scraper.log'),
        logging.StreamHandler()
    ]
)
```

## 📊 Understanding Your Data

### Job Filtering Logic

The scraper automatically filters for IT jobs using these criteria:

- **Programming Languages**: Python, Java, JavaScript, etc.
- **Job Roles**: Developer, Engineer, Programmer, etc.
- **Technology Areas**: Software, Data Science, DevOps, Cloud, etc.
- **Skills**: Full Stack, Frontend, Backend, Mobile, Web, etc.

### Data Quality

- **Automatic Filtering**: Only IT-related jobs are included
- **Real-time Validation**: Jobs are checked as they're processed
- **Error Handling**: Failed extractions are logged and skipped
- **Duplicate Prevention**: Each job is processed only once per session

## 🎯 Best Practices

### For Best Results

1. **Use Specific Search Terms**:
   - "Python Developer" instead of "Developer"
   - "Software Engineer" instead of "Engineer"
   - "Data Scientist" instead of "Scientist"

2. **Location Selection**:
   - Start with "Sri Lanka" as country
   - Try specific cities: "Colombo", "Kandy", "Galle"
   - Include "Remote" for work-from-home positions

3. **Timing**:
   - Run during business hours for more active listings
   - Avoid running multiple times in short succession
   - Give 15-30 minutes between scraping sessions

### Ethical Scraping

- **Respect Rate Limits**: Don't overwhelm the server
- **Manual Verification**: Complete CAPTCHAs manually
- **Reasonable Use**: Scrape only what you need
- **Terms of Service**: Review Glassdoor's terms

## 🔄 Maintenance & Updates

### Updating the Scraper

1. **Check for Updates**: Monitor Glassdoor's website changes
2. **Update Selectors**: If scraping fails, update CSS selectors
3. **Test Regularly**: Run small tests before major scraping

### Handling Website Changes

If Glassdoor changes their structure:

1. **Identify New Selectors**: Use browser developer tools
2. **Update the Code**: Modify selector arrays in the scraper
3. **Test Changes**: Verify with small data sets

## 📞 Support & Help

### Getting Help

1. **Check Logs**: Review `manual_scraper.log` for errors
2. **Verify Setup**: Ensure all dependencies are installed
3. **Test with Small Data**: Start with 1-2 pages
4. **Check Console Output**: Look for error messages

### Common Error Messages

| Error | Solution |
|-------|----------|
| "No jobs found" | Check if you're on job listings page |
| "Selector not found" | Glassdoor may have changed structure |
| "Browser timeout" | Increase timeout values or check internet |
| "CAPTCHA required" | Complete verification manually |

## 🚨 Important Notes

### Legal & Ethical Considerations

- **Educational Use**: This tool is for educational and research purposes
- **Terms of Service**: Review Glassdoor's terms before use
- **Rate Limiting**: Use reasonable delays between requests
- **Data Usage**: Respect privacy and use data responsibly

### Limitations

- **Manual Intervention Required**: Cannot run completely automatically
- **CAPTCHA Handling**: Requires human verification
- **Website Changes**: May break if Glassdoor updates their site
- **Rate Limits**: Subject to Glassdoor's anti-bot measures

## 🎉 Success Tips

1. **Start Small**: Test with 1-2 pages first
2. **Be Patient**: Manual navigation takes time but is more reliable
3. **Use Specific Terms**: Narrow search for better results
4. **Check Results**: Verify data quality before large-scale scraping
5. **Save Regularly**: Export data after each successful session

---

**Disclaimer**: This tool is provided as-is for educational and research purposes. Users are responsible for ensuring compliance with Glassdoor's terms of service and applicable laws. The authors are not responsible for any misuse of this tool.

**Happy Scraping! 🎉**
