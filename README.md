# MTN MoMo Data Analysis Dashboard

## 📊 Project Overview

This is my full-stack web application built for analyzing MTN MoMo transaction data from SMS messages. The project processes over 1,600 SMS messages from an XML file, categorizes them into different transaction types, and presents the insights through an interactive dashboard with real-time charts and filtering capabilities.

The application showcases my skills in data processing, database design, backend development with Flask, and frontend development with modern web technologies.

**🎥 Video Walkthrough:** [Add your video link here]

## 🎯 What I Built

- **Data Processing Engine**: Parses XML SMS data and categorizes transactions using pattern matching
- **Database System**: Normalized SQLite database with 9 different transaction tables
- **REST API Backend**: Flask application with endpoints for each transaction type
- **Interactive Dashboard**: Responsive web interface with Chart.js visualizations
- **Search & Filter System**: Real-time filtering by transaction type, date, and amount
- **Static Sidebar Navigation**: Consistent navigation across all pages with active state highlighting

## 🏗️ System Architecture

```
Raw XML Data → Python Parser → SQLite Database → Flask API → Interactive Dashboard
    (1600+ SMS)      (Regex)        (9 Tables)      (REST)     (Charts & Filters)
```

## 🛠️ Tech Stack

**Backend**
- Python 3.9 with Flask framework
- SQLite for data storage
- xml.etree.ElementTree for XML parsing
- Regular expressions for data cleaning

**Frontend**
- HTML5, CSS3, Tailwind CSS
- Vanilla JavaScript (ES6+)
- Chart.js for data visualizations
- Font Awesome icons

**Tools**
- Git for version control
- Virtual environment for dependency management

## � Getting Started

**What you need:**
- Python 3.9+
- Git
- Any modern web browser

**Installation:**

1. **Clone and navigate to the project**
   ```bash
   git clone https://github.com/Goodluck-dc14/MoMo_Stat_App.git
   cd MoMo_Stat_App
   ```

2. **Set up virtual environment**
   ```bash
   python3 -m venv env
   source env/bin/activate  # Windows: env\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install flask lxml
   ```

4. **Parse the data and create database**
   ```bash
   python new-parser.py
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Open in browser**
   Go to `http://127.0.0.1:5000`

## 🗄️ Database Design

I designed a normalized database with separate tables for each transaction type. Here's the structure:

```sql
-- Example: Incoming money table
CREATE TABLE incoming_money (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    transaction_id TEXT UNIQUE,
    amount INTEGER,
    sender_name TEXT,
    date TEXT,
    new_balance INTEGER
);

-- Similar structure for other transaction types:
-- airtime_payments, bank_transfers, transfers_to_mobile_numbers,
-- payments_to_code_holders, cashpower_payments, third_party_transactions,
-- withdrawals_from_agents, bundle_purchases
```

Each table has:
- Primary key for unique identification
- Transaction ID to prevent duplicates
- Amount and balance information
- Date/time stamps
- Relevant metadata (sender, recipient, etc.)

## � Features

**Dashboard Overview**
- Summary cards showing total transactions and amounts for each category
- Pie chart showing transaction distribution by type  
- Monthly trend analysis with line charts
- Responsive design that works on desktop and mobile

**Transaction Categories**
The system processes 9 different types of mobile money transactions:
- Airtime payments (mobile credit)
- Incoming money transfers
- Transfers to mobile numbers  
- Payments to code holders
- Bank transfers
- Internet/voice bundle purchases
- CashPower (electricity) payments
- Third-party service payments
- Agent withdrawals

**Navigation & Filtering**
- Static sidebar with all transaction categories
- Active page highlighting so you know where you are
- Search and filter by transaction type, date range, and amount
- Individual detail pages for each transaction type

**Data Processing**
- Parses 1,600+ SMS messages from XML format
- Uses regex patterns to extract transaction details
- Handles data cleaning and validation
- Stores processed data in normalized SQLite database

## � API Endpoints

The Flask backend provides these REST API endpoints:

```
GET /                                   # Main dashboard
GET /airtime                           # Airtime payments page
GET /incoming-money                    # Incoming money page
GET /transfers-to-mobile               # Mobile transfers page
GET /code-holders                      # Code payments page
GET /bank-transfers                    # Bank transfers page
GET /internet-voice                    # Bundle purchases page
GET /cash-power                        # CashPower payments page
GET /third-parties                     # Third party transactions page
GET /agent-withdrawals                 # Agent withdrawals page

# JSON data endpoints for dashboard
GET /get-airtime-payments              # Returns airtime data as JSON
GET /get-incoming-money                # Returns incoming money data as JSON
# ... similar endpoints for all transaction types
```

## 📋 Project Files

**Core Files:**
- `app.py` - Main Flask application with routes and API endpoints
- `new-parser.py` - XML parser that processes SMS data and populates database
- `db.py` - Database connection and helper functions
- `sms.xml` - Raw SMS data (1600+ messages)
- `momo_data.db` - SQLite database with processed transactions

**Templates:**
- `templates/index.html` - Main dashboard with charts and summary cards
- `templates/airtime.html` - Airtime payments detail page
- `templates/incoming-money.html` - Incoming money transactions page
- And 7 other transaction-specific pages

**Data:**
- `data/` folder contains JSON files with sample data for each transaction type

## 💡 Technical Challenges Solved

**Data Extraction**: Created regex patterns to extract transaction details from unstructured SMS text

**Database Design**: Normalized the data into separate tables while maintaining relationships

**Frontend Interactivity**: Built dynamic charts that update based on user filters without page refresh

**Responsive Navigation**: Implemented a static sidebar that works on both desktop and mobile

**Error Handling**: Added comprehensive logging for SMS messages that couldn't be parsed
## 🎯 Assignment Requirements Met

**Data Processing** - Parsed 1600+ SMS messages from XML, categorized into 9 transaction types

**Database Design** - Created normalized SQLite database with proper relationships and constraints  

**Frontend Development** - Built responsive dashboard with Chart.js visualizations and real-time filtering

**Backend API** - Flask application with REST endpoints serving JSON data

**Code Quality** - Clean, documented code with proper error handling and modular structure

## 📊 Project Report

**Detailed PDF Report:** [https://docs.google.com/document/d/1YEfro8m5rG1ucElmZfMwy1WBBKJe0qwB0crW33eVB_4/edit?usp=sharing](https://docs.google.com/document/d/1YEfro8m5rG1ucElmZfMwy1WBBKJe0qwB0crW33eVB_4/edit?usp=sharing)

## 🔮 Future Improvements

- Add user authentication and role-based access
- Implement real-time data updates with WebSockets  
- Create PDF export functionality for reports
- Add machine learning for fraud detection
- Build mobile app version with React Native

## �‍💻 About Me

**Goodluck DC** - Full Stack Developer  
- GitHub: [@Goodluck-dc14](https://github.com/Goodluck-dc14)
- Email: [your.email@example.com]

This project demonstrates my skills in data processing, database design, backend development with Python/Flask, and frontend development with modern web technologies.

## 📄 License

This project was developed for academic purposes as part of a summative assignment.

## 🙏 Acknowledgments

Thanks to MTN Rwanda for providing the context and inspiration for this mobile money analytics project.
