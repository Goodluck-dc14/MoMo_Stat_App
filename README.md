# MoMo Data Analysis App

## About

This is my project for the MoMo Data Analysis assignment. It’s a full-stack app that processes SMS data from MTN MoMo, a mobile payment service in Rwanda. The app reads an XML file with about 1600 SMS messages, cleans and organizes the data, stores it in a SQLite database, and shows it on a dashboard with charts and filters.

## Goals

- Read and process SMS data from an XML file.
- Clean the data and sort it into categories like payments, transfers, and withdrawals.
- Save the data in a SQLite database for easy access.
- Build a dashboard with HTML, CSS, and JavaScript to show data insights.

## Tools Used

- **Backend**: Python, Flask, SQLite, xml.etree.ElementTree (for XML parsing)
- **Frontend**: HTML, CSS, JavaScript, Chart.js (for charts)
- **Other**: Git for version control

## How to Run

1. **Set Up Your Environment**:

   - Make sure Python 3 is installed (`python3 --version`).
   - Install Git (`git --version`).
   - Clone this repo: `git clone <(https://github.com/Goodluck-dc14/MoMo_Stat_App.git)>` (replace with your GitHub repo URL after creating it).
   - Go to the project folder: `cd MoMo_Stat_App`.

2. **Create a Virtual Environment**:
   ```bash
   python3 -m venv env
   source env/bin/activate
   ```
