"""
Simple Manual-Assisted Glassdoor Scraper
User manually navigates past protection, then scraper takes over
"""

import time
import json
import logging
from datetime import datetime
from typing import List, Dict
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException


class ManualAssistedScraper:
    """Scraper that requires manual navigation past protection"""
    
    def __init__(self):
        self.driver = None
        self.jobs_data = []
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('manual_scraper.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def setup_browser(self):
        """Setup browser in visible mode for manual navigation"""
        try:
            options = uc.ChromeOptions()
            # Don't use headless - we need user interaction
            options.add_argument('--window-size=1920,1080')
            options.add_argument('--start-maximized')
            
            self.driver = uc.Chrome(options=options)
            self.driver.set_page_load_timeout(60)
            
            print("✅ Browser opened successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error setting up browser: {str(e)}")
            return False

    def manual_navigation_instructions(self):
        """Print instructions for manual navigation"""
        instructions = """
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

❗ IMPORTANT: Do NOT close the browser window!
"""
        print(instructions)

    def wait_for_user_confirmation(self):
        """Wait for user to manually navigate and confirm"""
        input("👉 Press ENTER when you've completed the manual navigation and can see job listings...")
        
        # Check if we're on a job search results page
        try:
            current_url = self.driver.current_url
            if 'glassdoor.com' in current_url and ('job' in current_url or 'search' in current_url):
                print("✅ Great! You're on a Glassdoor job search page")
                return True
            else:
                print(f"⚠️  Current URL: {current_url}")
                retry = input("Are you sure you're on the job listings page? (y/n): ")
                return retry.lower() == 'y'
        except Exception as e:
            print(f"⚠️  Could not verify page: {str(e)}")
            retry = input("Continue anyway? (y/n): ")
            return retry.lower() == 'y'

    def extract_jobs_from_current_page(self):
        """Extract job data from the current page"""
        jobs = []
        
        try:
            print("🔍 Looking for job listings on current page...")
            
            # Try multiple selectors for job titles
            title_selectors = [
                '[data-test="job-title"]',
                '[class*="jobTitle"]',
                'a[data-jl]',
                '.jobTitle',
                'h2 a'
            ]
            
            job_elements = []
            for selector in title_selectors:
                try:
                    elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        job_elements = elements
                        print(f"✅ Found {len(elements)} jobs using selector: {selector}")
                        break
                except:
                    continue
            
            if not job_elements:
                print("❌ Could not find any job listings on this page")
                return jobs
            
            # Extract data from each job
            for i, job_element in enumerate(job_elements[:10], 1):  # Limit to first 10
                try:
                    job_data = {
                        'title': 'N/A',
                        'company': 'N/A',
                        'location': 'N/A',
                        'salary': 'N/A',
                        'scraped_at': datetime.now().isoformat()
                    }
                    
                    # Get job title
                    try:
                        if job_element.tag_name == 'a':
                            job_data['title'] = job_element.text.strip()
                            job_data['url'] = job_element.get_attribute('href')
                        else:
                            job_data['title'] = job_element.text.strip()
                            # Try to find link
                            try:
                                link = job_element.find_element(By.TAG_NAME, 'a')
                                job_data['url'] = link.get_attribute('href')
                            except:
                                job_data['url'] = 'N/A'
                    except Exception as e:
                        print(f"Error getting title for job {i}: {str(e)}")
                        continue
                    
                    # Try to get company and location from nearby elements
                    try:
                        # Look for parent container
                        parent = job_element.find_element(By.XPATH, '../..')
                        
                        # Company name selectors
                        company_selectors = [
                            '[data-test="employer-name"]',
                            '.companyName',
                            '[class*="company"]',
                            '[class*="employer"]'
                        ]
                        
                        for comp_selector in company_selectors:
                            try:
                                comp_elem = parent.find_element(By.CSS_SELECTOR, comp_selector)
                                job_data['company'] = comp_elem.text.strip()
                                break
                            except:
                                continue
                        
                        # Location selectors
                        location_selectors = [
                            '[data-test="job-location"]',
                            '.location',
                            '[class*="location"]'
                        ]
                        
                        for loc_selector in location_selectors:
                            try:
                                loc_elem = parent.find_element(By.CSS_SELECTOR, loc_selector)
                                job_data['location'] = loc_elem.text.strip()
                                break
                            except:
                                continue
                        
                        # Salary selectors
                        salary_selectors = [
                            '[data-test="salary-estimate"]',
                            '.salary',
                            '[class*="salary"]'
                        ]
                        
                        for sal_selector in salary_selectors:
                            try:
                                sal_elem = parent.find_element(By.CSS_SELECTOR, sal_selector)
                                job_data['salary'] = sal_elem.text.strip()
                                break
                            except:
                                continue
                    
                    except Exception as e:
                        self.logger.debug(f"Error extracting additional data for job {i}: {str(e)}")
                    
                    # Basic IT job filtering
                    if self.is_it_job(job_data['title']):
                        jobs.append(job_data)
                        print(f"✅ {i:2d}. {job_data['title']} at {job_data['company']}")
                    else:
                        print(f"❌ {i:2d}. Skipped: {job_data['title']} (not IT)")
                    
                except Exception as e:
                    print(f"❌ Error processing job {i}: {str(e)}")
                    continue
            
        except Exception as e:
            print(f"❌ Error extracting jobs: {str(e)}")
        
        return jobs

    def is_it_job(self, title: str) -> bool:
        """Check if job title is IT-related"""
        if not title:
            return False
        
        it_keywords = [
            'developer', 'engineer', 'programmer', 'software', 'python', 'java',
            'javascript', 'data scientist', 'data analyst', 'devops', 'cloud',
            'full stack', 'frontend', 'backend', 'mobile', 'web', 'qa', 'testing',
            'architect', 'technical', 'technology', 'coding', 'programming'
        ]
        
        title_lower = title.lower()
        return any(keyword in title_lower for keyword in it_keywords)

    def scrape_jobs(self, max_pages: int = 3):
        """Main scraping method with manual assistance"""
        if not self.setup_browser():
            return False
        
        try:
            print("🚀 Starting Manual-Assisted Glassdoor Scraper")
            print("=" * 50)
            
            # Show instructions
            self.manual_navigation_instructions()
            
            # Navigate to Glassdoor
            print("🌐 Opening Glassdoor.com...")
            self.driver.get("https://www.glassdoor.com")
            
            # Wait for manual navigation
            if not self.wait_for_user_confirmation():
                print("❌ User cancelled or not ready")
                return False
            
            all_jobs = []
            
            # Extract jobs from current and subsequent pages
            for page in range(max_pages):
                print(f"\n📄 Processing page {page + 1}")
                
                page_jobs = self.extract_jobs_from_current_page()
                all_jobs.extend(page_jobs)
                
                print(f"📊 Found {len(page_jobs)} IT jobs on page {page + 1}")
                
                # Ask user to go to next page
                if page < max_pages - 1:
                    next_page = input(f"\n👉 Please navigate to page {page + 2} and press ENTER (or 'q' to quit): ")
                    if next_page.lower() == 'q':
                        print("⏹️  Stopped by user")
                        break
            
            self.jobs_data = all_jobs
            print(f"\n🎉 Scraping completed! Total IT jobs: {len(all_jobs)}")
            
            # Save results
            if all_jobs:
                self.save_results()
            
            return True
            
        except Exception as e:
            print(f"❌ Error during scraping: {str(e)}")
            return False
        
        finally:
            if self.driver:
                input("\n👉 Press ENTER to close the browser...")
                self.driver.quit()

    def save_results(self):
        """Save results to JSON file"""
        if not self.jobs_data:
            print("⚠️  No data to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"glassdoor_manual_scrape_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.jobs_data, f, indent=2, ensure_ascii=False)
            
            print(f"💾 Results saved to: {filename}")
            
            # Also save as CSV for easy viewing
            try:
                import pandas as pd
                df = pd.DataFrame(self.jobs_data)
                csv_filename = filename.replace('.json', '.csv')
                df.to_csv(csv_filename, index=False, encoding='utf-8')
                print(f"💾 CSV saved to: {csv_filename}")
            except ImportError:
                print("📝 Install pandas to also save as CSV: pip install pandas")
            
        except Exception as e:
            print(f"❌ Error saving results: {str(e)}")


def main():
    """Run the manual-assisted scraper"""
    scraper = ManualAssistedScraper()
    
    try:
        success = scraper.scrape_jobs(max_pages=3)
        
        if success and scraper.jobs_data:
            print(f"\n✅ Successfully scraped {len(scraper.jobs_data)} jobs!")
            
            # Show sample results
            print("\n📋 Sample results:")
            for i, job in enumerate(scraper.jobs_data[:5], 1):
                print(f"{i}. {job['title']} at {job['company']} - {job['location']}")
        else:
            print("❌ No jobs were scraped")
    
    except KeyboardInterrupt:
        print("\n⏹️  Scraping interrupted by user")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
