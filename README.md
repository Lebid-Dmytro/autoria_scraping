# AutoRia 

- Scrapes details of used cars from the AutoRia website.
- Extracts information such as URL, title, price in USD, odometer reading, username, car number, VIN (Vehicle Identification Number), image URL, images count, phone number, and datetime found.
- Saves the scraped data to a PostgreSQL database.

Schedule Jobs:
- The spider is scheduled to run daily at 12:00 PM to record data from the website.
- A database dump job is scheduled daily at midnight.

## Getting Started

1. Install the required dependencies:

```bash

