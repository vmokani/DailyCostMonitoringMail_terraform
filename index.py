import boto3
import datetime

# Vriables for email source and destination and region
source_email = 'cloudopsjeavio@gmail.com'
destination_emails = ['vishal.mokani@jeavio.com']
region_name = 'us-east-1'

ce = boto3.client('ce', region_name)
ses = boto3.client('ses', region_name)

def send_email(to_email, subject, body):
    try:
        # Send email
        response = ses.send_email(
            Source= source_email,
            Destination={'ToAddresses': destination_emails},
            Message={
                'Subject': {'Data': subject},
                'Body': {
                    'Html': {
                        'Data': body
                    }
                }
            }
        )
        print("Email sent. Message ID:", response['MessageId'])
        return True
    except Exception as e:
        print("Error:", str(e))
        return False

def get_service_costs(start_date, end_date):
    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['BlendedCost'],
            GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
        )
        # Extract service costs
        service_costs = []
        for result in response['ResultsByTime']:
            date = result['TimePeriod']['Start']
            for group in result['Groups']:
                service = group['Keys'][0]
                amount = float(group['Metrics']['BlendedCost']['Amount'])
                if amount > 0:  # Exclude services with zero cost
                    service_costs.append((date, service, amount))
        return service_costs
    except Exception as e:
        print("Error fetching service costs:", str(e))
        return None

def get_daily_costs(start_date, end_date):
    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='DAILY',
            Metrics=['BlendedCost']
        )
        # Extract daily costs
        daily_costs = []
        for result in response['ResultsByTime']:
            date = result['TimePeriod']['Start']
            amount = float(result['Total']['BlendedCost']['Amount'])
            if amount > 0:  # Exclude days with zero cost
                daily_costs.append((date, amount))
        return daily_costs
    except Exception as e:
        print("Error fetching daily costs:", str(e))
        return None

def generate_service_table(service_costs, header):
    if not service_costs:
        return f"<p><b>{header}</b>: No data available</p>"

    table_html = f"<p><b>{header}</b></p>"
    table_html += "<table border='1' style='border-collapse: collapse;'>"
    table_html += "<tr><th><b>Date</b></th><th><b>Service</b></th><th><b>Cost ($)</b></th></tr>"
    
    for date, service, cost in service_costs:
        table_html += f"<tr><td>{date}</td><td>{service}</td><td style='font-size:13px;'>{cost:.2f}</td></tr>"
    
    table_html += "</table>"
    return table_html

def generate_daily_cost_table_in_rows(daily_costs):
    if not daily_costs:
        return "<p><b>Daily Costs (Current Month)</b>: No data available</p>"

    table_html = "<p><b>Daily Costs (Current Month)</b></p>"  # Heading will only be added once
    chunk_size = 15
    chunks = [daily_costs[i:i + chunk_size] for i in range(0, len(daily_costs), chunk_size)]

    for chunk_index, chunk in enumerate(chunks):
        if chunk_index > 0:
            # Remove the <br> tag to avoid extra space between tables
            table_html += "<table border='1' style='border-collapse: collapse; margin-top: 0;'>"
        else:
            table_html += "<table border='1' style='border-collapse: collapse;'>"

        # First row for dates
        table_html += "<tr><th><b>Date</b></th>"
        for date, _ in chunk:
            table_html += f"<td><b>{date}</b></td>"
        table_html += "</tr>"

        # Second row for amounts
        table_html += "<tr><th><b>Amount ($)</b></th>"
        for _, amount in chunk:
            table_html += f"<td style='font-size:13px;'>{amount:.2f}</td>"
        table_html += "</tr>"

        table_html += "</table>"

    return table_html


def get_total_cost_for_current_month(start_date, end_date):
    try:
        response = ce.get_cost_and_usage(
            TimePeriod={
                'Start': start_date,
                'End': end_date
            },
            Granularity='MONTHLY',
            Metrics=['BlendedCost']
        )
        total_cost = float(response['ResultsByTime'][0]['Total']['BlendedCost']['Amount'])
        return total_cost
    except Exception as e:
        print("Error fetching total monthly cost:", str(e))
        return None

def lambda_handler(event, context):
    try:
        # Get today's date and calculate yesterday's and last week's dates
        today = datetime.datetime.now()
        yesterday = (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        seven_days_ago = (today - datetime.timedelta(days=7)).strftime('%Y-%m-%d')
        current_month_start = today.strftime('%Y-%m-01')
        current_month_end = today.strftime('%Y-%m-%d')

        # Get service costs for yesterday and last week
        yesterday_service_costs = get_service_costs(yesterday, today.strftime('%Y-%m-%d'))
        last_week_service_costs = get_service_costs(seven_days_ago, today.strftime('%Y-%m-%d'))

        if yesterday_service_costs is None or last_week_service_costs is None:
            return {
                'statusCode': 500,
                'body': 'Error fetching service costs'
            }

        # Get daily costs for the current month (for the table)
        daily_costs = get_daily_costs(current_month_start, current_month_end)

        # Get total cost for the current month
        current_month_total_cost = get_total_cost_for_current_month(current_month_start, current_month_end)

        if current_month_total_cost is None:
            return {
                'statusCode': 500,
                'body': 'Error fetching total monthly cost'
            }

        # Generate HTML table for daily costs in rows (month-wide breakdown)
        daily_cost_table_html = generate_daily_cost_table_in_rows(daily_costs)

        # Generate service-level cost tables for yesterday and last week
        yesterday_service_html = generate_service_table(yesterday_service_costs, "Yesterday's Service-wise Cost")
        last_week_service_html = generate_service_table(last_week_service_costs, "Last 7 days's Service-wise Cost")

        # Calculate the total amount for yesterday and the last week
        total_yesterday = sum(cost for date, service, cost in yesterday_service_costs)
        total_last_week = sum(cost for date, service, cost in last_week_service_costs)

        # Compose email subject and body with the current month's total cost
        subject = f"AWS Billing Details - {today.strftime('%Y-%m-%d')} (Total Monthly Cost: ${current_month_total_cost:.2f})"
        body = (
            f"<p><b>Total cost for the current month so far:</b> <span style='font-size:17px;'>${current_month_total_cost:.2f}</span></p>"
            f"<p><b>Total cost for yesterday:</b> <span style='font-size:17px;'>${total_yesterday:.2f}</span></p>"
            f"<p><b>Total cost for last 7 days:</b> <span style='font-size:17px;'>${total_last_week:.2f}</span></p>"
            f"{daily_cost_table_html}"  # Monthly cost breakdown in rows with a limit of 15 per table
            f"<p><b>Service wise cost breakdown for yesterday and last 7 days is provided below:</b></p>"
            f"{yesterday_service_html}"
            f"{last_week_service_html}"
        )

        # Send email
        if send_email(source_email, subject, body):
            return {
                'statusCode': 200,
                'body': 'Email sent successfully!'
            }
        else:
            return {
                'statusCode': 500,
                'body': 'Failed to send email!'
            }

    except Exception as e:
        print("Error:", str(e))
        return {
            'statusCode': 500,
            'body': 'An error occurred.'
        }