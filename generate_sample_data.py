#!/usr/bin/env python3
"""
Sample data generator for MoMo Analytics Dashboard
This script adds sample transaction data for demonstration purposes
"""

import sqlite3
import random
from datetime import datetime, timedelta

def create_sample_data():
    """Generate sample transaction data for dashboard demonstration"""
    
    conn = sqlite3.connect('momo_data.db')
    cursor = conn.cursor()
    
    # Clear existing data
    tables = [
        'airtime_payments', 'incoming_money', 'transfers_to_mobile_numbers',
        'payments_to_code_holders', 'bank_transfers', 'bundle_purchases',
        'cashpower_payments', 'third_party_transactions', 'withdrawals_from_agents'
    ]
    
    for table in tables:
        try:
            cursor.execute(f"DELETE FROM {table}")
        except sqlite3.Error:
            pass
    
    # Sample names and data
    senders = ['John Doe', 'Jane Smith', 'Bob Johnson', 'Alice Brown', 'Charlie Wilson']
    recipients = ['Mary Johnson', 'David Wilson', 'Sarah Connor', 'Michael Scott', 'Emma Watson']
    banks = ['Bank of Kigali', 'Equity Bank', 'KCB Bank Rwanda', 'Cogebanque', 'BNR']
    agents = ['Agent A', 'Agent B', 'Agent C', 'Agent D', 'Agent E']
    agent_numbers = ['250123456789', '250987654321', '250111222333', '250444555666', '250777888999']
    bundle_types = ['1GB Internet', '2GB Internet', '500MB Internet', 'Voice Bundle', 'Social Media']
    
    # Generate sample data for each table
    
    # 1. Airtime Payments
    for i in range(50):
        amount = random.randint(500, 10000)
        fee = int(amount * 0.02)  # 2% fee
        date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S')
        balance = random.randint(10000, 100000)
        
        cursor.execute("""
            INSERT INTO airtime_payments (transaction_id, amount, fee, date, new_balance)
            VALUES (?, ?, ?, ?, ?)
        """, (f"AT{1000000 + i}", amount, fee, date, balance))
    
    # 2. Incoming Money
    for i in range(75):
        amount = random.randint(1000, 50000)
        sender = random.choice(senders)
        date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S')
        balance = random.randint(10000, 100000)
        
        cursor.execute("""
            INSERT INTO incoming_money (transaction_id, amount, sender_name, date, new_balance)
            VALUES (?, ?, ?, ?, ?)
        """, (f"IM{2000000 + i}", amount, sender, date, balance))
    
    # 3. Transfers to Mobile Numbers
    for i in range(60):
        amount = random.randint(1000, 30000)
        recipient = f"25078{random.randint(1000000, 9999999)}"
        date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S')
        balance = random.randint(10000, 100000)
        
        cursor.execute("""
            INSERT INTO transfers_to_mobile_numbers (transaction_id, amount, recipient_number, date, new_balance)
            VALUES (?, ?, ?, ?, ?)
        """, (f"TM{3000000 + i}", amount, recipient, date, balance))
    
    # 4. Payments to Code Holders
    for i in range(40):
        amount = random.randint(500, 25000)
        recipient = random.choice(recipients)
        date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S')
        balance = random.randint(10000, 100000)
        
        cursor.execute("""
            INSERT INTO payments_to_code_holders (transaction_id, amount, recipient_name, date, new_balance)
            VALUES (?, ?, ?, ?, ?)
        """, (f"PC{4000000 + i}", amount, recipient, date, balance))
    
    # 5. Bank Transfers
    for i in range(35):
        amount = random.randint(5000, 100000)
        bank = random.choice(banks)
        date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S')
        balance = random.randint(10000, 100000)
        
        cursor.execute("""
            INSERT INTO bank_transfers (transaction_id, amount, bank_name, date, new_balance)
            VALUES (?, ?, ?, ?, ?)
        """, (f"BT{5000000 + i}", amount, bank, date, balance))
    
    # 6. Bundle Purchases
    for i in range(45):
        amount = random.randint(1000, 5000)
        bundle = random.choice(bundle_types)
        validity = f"{random.choice([7, 30, 90])} days"
        date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S')
        balance = random.randint(10000, 100000)
        
        cursor.execute("""
            INSERT INTO bundle_purchases (transaction_id, amount, bundle_type, validity, date, new_balance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (f"BP{6000000 + i}", amount, bundle, validity, date, balance))
    
    # 7. CashPower Payments
    for i in range(30):
        amount = random.randint(2000, 20000)
        fee = int(amount * 0.01)  # 1% fee
        date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S')
        balance = random.randint(10000, 100000)
        
        cursor.execute("""
            INSERT INTO cashpower_payments (transaction_id, amount, fee, date, new_balance)
            VALUES (?, ?, ?, ?, ?)
        """, (f"CP{7000000 + i}", amount, fee, date, balance))
    
    # 8. Third Party Transactions
    for i in range(25):
        amount = random.randint(1000, 15000)
        party = f"Service Provider {random.choice(['A', 'B', 'C', 'D', 'E'])}"
        date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S')
        balance = random.randint(10000, 100000)
        
        cursor.execute("""
            INSERT INTO third_party_transactions (transaction_id, amount, party_name, date, new_balance)
            VALUES (?, ?, ?, ?, ?)
        """, (f"TP{8000000 + i}", amount, party, date, balance))
    
    # 9. Withdrawals from Agents
    for i in range(55):
        amount = random.randint(5000, 50000)
        agent = random.choice(agents)
        agent_number = random.choice(agent_numbers)
        date = (datetime.now() - timedelta(days=random.randint(1, 365))).strftime('%Y-%m-%d %H:%M:%S')
        balance = random.randint(10000, 100000)
        
        cursor.execute("""
            INSERT INTO withdrawals_from_agents (transaction_id, amount, agent_name, agent_number, date, new_balance)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (f"WA{9000000 + i}", amount, agent, agent_number, date, balance))
    
    conn.commit()
    conn.close()
    
    print("✅ Sample data generated successfully!")
    print("📊 Transaction counts:")
    print("   - Airtime Payments: 50")
    print("   - Incoming Money: 75") 
    print("   - Mobile Transfers: 60")
    print("   - Code Payments: 40")
    print("   - Bank Transfers: 35")
    print("   - Bundle Purchases: 45")
    print("   - CashPower Payments: 30")
    print("   - Third Party: 25")
    print("   - Agent Withdrawals: 55")
    print(f"📈 Total: {50+75+60+40+35+45+30+25+55} transactions")

if __name__ == "__main__":
    create_sample_data()
