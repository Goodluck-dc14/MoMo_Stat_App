import sqlite3
import json
from collections import defaultdict
from datetime import datetime, timedelta
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('momo_analytics.log'),
        logging.StreamHandler()
    ]
)

def get_db_connection():
    """
    Establish database connection with proper error handling
    """
    try:
        conn = sqlite3.connect('momo_data.db')
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        logging.error(f"Database connection error: {e}")
        raise

def get_table_summary(table_name):
    """
    Get comprehensive summary statistics for a transaction table
    """
    try:
        conn = get_db_connection()
        
        # Basic counts and sums
        query = f"""
        SELECT 
            COUNT(*) as total_transactions,
            COALESCE(SUM(amount), 0) as total_amount,
            COALESCE(AVG(amount), 0) as average_amount,
            COALESCE(MIN(amount), 0) as min_amount,
            COALESCE(MAX(amount), 0) as max_amount,
            MIN(date) as earliest_date,
            MAX(date) as latest_date
        FROM {table_name}
        """
        
        cursor = conn.execute(query)
        result = cursor.fetchone()
        
        if result:
            summary = {
                'table_name': table_name,
                'total_transactions': result['total_transactions'],
                'total_amount': result['total_amount'],
                'average_amount': round(result['average_amount'], 2),
                'min_amount': result['min_amount'],
                'max_amount': result['max_amount'],
                'earliest_date': result['earliest_date'],
                'latest_date': result['latest_date']
            }
            
            # Add fee information if applicable
            if 'fee' in [desc[0] for desc in cursor.description]:
                fee_query = f"SELECT COALESCE(SUM(fee), 0) as total_fees FROM {table_name}"
                fee_result = conn.execute(fee_query).fetchone()
                summary['total_fees'] = fee_result['total_fees'] if fee_result else 0
            
            conn.close()
            logging.info(f"Generated summary for table: {table_name}")
            return summary
        
        conn.close()
        return None
        
    except sqlite3.Error as e:
        logging.error(f"Error getting table summary for {table_name}: {e}")
        return None

def analyze_incoming_money_transactions(data):
    """
    Comprehensive analysis of incoming money transactions
    """
    if not data:
        return {'error': 'No data provided'}
    
    try:
        total_transactions = len(data)
        total_amount_received = sum(item.get('amount_received', item.get('amount', 0)) for item in data)
        final_balance = data[-1].get('new_balance') if data else None

        # Convert date strings to datetime objects
        dates = []
        for item in data:
            try:
                date_str = item.get('date', '')
                if 'T' in date_str:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                else:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                dates.append(date_obj)
            except ValueError:
                logging.warning(f"Invalid date format: {item.get('date')}")
                continue

        earliest_date = min(dates).strftime("%Y-%m-%d %H:%M:%S") if dates else None
        latest_date = max(dates).strftime("%Y-%m-%d %H:%M:%S") if dates else None

        # Sender analysis
        senders = {}
        for item in data:
            sender = item.get('sender', item.get('sender_name', 'Unknown'))
            senders[sender] = senders.get(sender, 0) + 1

        # Top transactions
        amount_key = 'amount_received' if 'amount_received' in data[0] else 'amount'
        largest_transactions = sorted(
            data, 
            key=lambda x: x.get(amount_key, 0), 
            reverse=True
        )[:5]

        # Monthly breakdown
        monthly_transactions = defaultdict(lambda: {'count': 0, 'amount': 0})
        for item in data:
            if item.get('date'):
                try:
                    date_str = item['date']
                    if 'T' in date_str:
                        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                    else:
                        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    month_year = date.strftime("%Y-%m")
                    monthly_transactions[month_year]['count'] += 1
                    monthly_transactions[month_year]['amount'] += item.get(amount_key, 0)
                except ValueError:
                    continue

        # Daily patterns
        daily_patterns = defaultdict(lambda: {'count': 0, 'amount': 0})
        for item in data:
            if item.get('date'):
                try:
                    date_str = item['date']
                    if 'T' in date_str:
                        date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
                    else:
                        date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                    day_name = date.strftime("%A")
                    daily_patterns[day_name]['count'] += 1
                    daily_patterns[day_name]['amount'] += item.get(amount_key, 0)
                except ValueError:
                    continue

        results = {
            'total_transactions': total_transactions,
            'total_amount_received': total_amount_received,
            'average_amount': round(total_amount_received / total_transactions, 2) if total_transactions > 0 else 0,
            'final_balance': final_balance,
            'earliest_transaction_date': earliest_date,
            'latest_transaction_date': latest_date,
            'unique_senders': len(senders),
            'transactions_per_sender': dict(sorted(senders.items(), key=lambda x: x[1], reverse=True)[:10]),
            'largest_transactions': largest_transactions,
            'monthly_breakdown': dict(monthly_transactions),
            'daily_patterns': dict(daily_patterns),
            'analysis_timestamp': datetime.now().isoformat()
        }

        logging.info(f"Analyzed {total_transactions} incoming money transactions")
        return results
        
    except Exception as e:
        logging.error(f"Error analyzing incoming money transactions: {e}")
        return {'error': str(e)}

def analyze_transaction_trends(table_name, days=30):
    """
    Analyze transaction trends over specified period
    """
    try:
        conn = get_db_connection()
        
        # Get transactions from last N days
        query = f"""
        SELECT date, amount, transaction_id
        FROM {table_name}
        WHERE date >= date('now', '-{days} days')
        ORDER BY date
        """
        
        cursor = conn.execute(query)
        transactions = cursor.fetchall()
        conn.close()
        
        if not transactions:
            return {'error': 'No recent transactions found'}
        
        # Group by date
        daily_data = defaultdict(lambda: {'count': 0, 'total_amount': 0, 'transactions': []})
        
        for txn in transactions:
            date_key = txn['date'][:10]  # Extract date part (YYYY-MM-DD)
            daily_data[date_key]['count'] += 1
            daily_data[date_key]['total_amount'] += txn['amount']
            daily_data[date_key]['transactions'].append(dict(txn))
        
        # Calculate trends
        dates = sorted(daily_data.keys())
        if len(dates) >= 2:
            recent_avg = sum(daily_data[date]['total_amount'] for date in dates[-7:]) / min(7, len(dates))
            older_avg = sum(daily_data[date]['total_amount'] for date in dates[:-7]) / max(1, len(dates) - 7)
            trend_direction = "increasing" if recent_avg > older_avg else "decreasing"
            trend_percentage = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
        else:
            trend_direction = "stable"
            trend_percentage = 0
        
        results = {
            'table_name': table_name,
            'period_days': days,
            'daily_data': dict(daily_data),
            'total_transactions': sum(data['count'] for data in daily_data.values()),
            'total_amount': sum(data['total_amount'] for data in daily_data.values()),
            'trend_direction': trend_direction,
            'trend_percentage': round(trend_percentage, 2),
            'analysis_date': datetime.now().isoformat()
        }
        
        logging.info(f"Analyzed trends for {table_name} over {days} days")
        return results
        
    except Exception as e:
        logging.error(f"Error analyzing trends for {table_name}: {e}")
        return {'error': str(e)}

def get_transaction_distribution():
    """
    Get distribution of transactions across all types
    """
    try:
        conn = get_db_connection()
        
        tables = [
            'airtime_payments', 'incoming_money', 'transfers_to_mobile_numbers',
            'payments_to_code_holders', 'bank_transfers', 'bundle_purchases',
            'cashpower_payments', 'third_party_transactions', 'withdrawals_from_agents'
        ]
        
        distribution = {}
        total_transactions = 0
        total_volume = 0
        
        for table in tables:
            try:
                query = f"""
                SELECT 
                    COUNT(*) as count,
                    COALESCE(SUM(amount), 0) as volume
                FROM {table}
                """
                
                result = conn.execute(query).fetchone()
                if result:
                    count = result['count']
                    volume = result['volume']
                    
                    distribution[table] = {
                        'count': count,
                        'volume': volume,
                        'table_display_name': table.replace('_', ' ').title()
                    }
                    
                    total_transactions += count
                    total_volume += volume
                    
            except sqlite3.Error as e:
                logging.warning(f"Could not process table {table}: {e}")
                continue
        
        # Calculate percentages
        for table_data in distribution.values():
            table_data['count_percentage'] = (table_data['count'] / total_transactions * 100) if total_transactions > 0 else 0
            table_data['volume_percentage'] = (table_data['volume'] / total_volume * 100) if total_volume > 0 else 0
        
        conn.close()
        
        results = {
            'distribution': distribution,
            'totals': {
                'total_transactions': total_transactions,
                'total_volume': total_volume
            },
            'analysis_timestamp': datetime.now().isoformat()
        }
        
        logging.info("Generated transaction distribution analysis")
        return results
        
    except Exception as e:
        logging.error(f"Error getting transaction distribution: {e}")
        return {'error': str(e)}

def export_data_summary():
    """
    Export comprehensive data summary for reporting
    """
    try:
        summary = {
            'generated_at': datetime.now().isoformat(),
            'database_file': 'momo_data.db',
            'tables': {},
            'overall_stats': {}
        }
        
        # Get distribution
        distribution = get_transaction_distribution()
        if 'error' not in distribution:
            summary['overall_stats'] = distribution['totals']
            summary['transaction_distribution'] = distribution['distribution']
        
        # Get individual table summaries
        tables = [
            'airtime_payments', 'incoming_money', 'transfers_to_mobile_numbers',
            'payments_to_code_holders', 'bank_transfers', 'bundle_purchases',
            'cashpower_payments', 'third_party_transactions', 'withdrawals_from_agents'
        ]
        
        for table in tables:
            table_summary = get_table_summary(table)
            if table_summary:
                summary['tables'][table] = table_summary
        
        # Save to file
        with open('data_summary_export.json', 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        logging.info("Exported comprehensive data summary")
        return summary
        
    except Exception as e:
        logging.error(f"Error exporting data summary: {e}")
        return {'error': str(e)}


def analyze__airtime_transactions(data):
    total_transactions = len(data)
    total_payment_amounts = sum(item['payment_amount'] for item in data)
    final_balance = data[-1]['new_balance'] if data else None

    # Convert date strings to datetime objects and find the earliest and latest transaction dates
    dates = [datetime.strptime(item['date'], "%Y-%m-%d %H:%M:%S")
             for item in data]
    earliest_date = min(dates).strftime("%Y-%m-%d %H:%M:%S") if dates else None
    latest_date = max(dates).strftime("%Y-%m-%d %H:%M:%S") if dates else None

    # Prepare results
    results = {
        'Total Transactions': total_transactions,
        'Total Payment Amounts': total_payment_amounts,
        'Final Balance': final_balance,
        'Earliest Transaction Date': earliest_date,
        'Latest Transaction Date': latest_date
    }

    return results


# Connect to the database

def get_db_connection():
    conn = sqlite3.connect("momo_data.db")
    conn.row_factory = sqlite3.Row  # Enables dictionary-like row access
    return conn

# Function to get transaction summary for a table


def get_table_summary(table_name):
    query = f"""
    SELECT 
        COUNT(*) AS num_transactions, 
        SUM(amount) AS total_amount, 
        MIN(date) AS first_transaction_date, 
        MAX(date) AS last_transaction_date 
    FROM {table_name}
    """
    conn = get_db_connection()
    cursor = conn.execute(query)
    result = cursor.fetchone()
    conn.close()
    return {
        "table": table_name,
        "num_transactions": result["num_transactions"],
        "total_amount": result["total_amount"],
        "first_transaction_date": result["first_transaction_date"],
        "last_transaction_date": result["last_transaction_date"]
    }


# List of tables in your database
