import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

def generate_mock_crm_data(num_records=1000):
    # Setup data choices
    reps = ["Alice Smith", "Bob Jones", "Charlie Brown", "Diana Prince", "Evan Wright"]
    regions = ["North America", "EMEA", "APAC", "LATAM"]
    industries = ["Technology", "Healthcare", "Finance", "Retail", "Manufacturing"]
    stages = ["Prospecting", "Qualification", "Proposal", "Negotiation", "Closed Won", "Closed Lost"]
    
    # Generate data
    data = []
    start_date = datetime(2023, 1, 1)
    
    for i in range(num_records):
        created_date = start_date + timedelta(days=random.randint(0, 365))
        # Close date is 10 to 90 days after created date
        close_date = created_date + timedelta(days=random.randint(10, 90))
        
        stage = random.choice(stages)
        # Probability based on stage
        if stage == "Prospecting": prob = 0.1
        elif stage == "Qualification": prob = 0.3
        elif stage == "Proposal": prob = 0.5
        elif stage == "Negotiation": prob = 0.8
        elif stage == "Closed Won": prob = 1.0
        else: prob = 0.0
        
        amount = round(random.uniform(5000, 150000), 2)
        
        data.append({
            "deal_id": f"DL-{10000 + i}",
            "sales_rep_name": random.choice(reps),
            "region": random.choice(regions),
            "company_name": f"Company {random.randint(1, 500)}",
            "industry": random.choice(industries),
            "amount": amount,
            "stage": stage,
            "probability": prob,
            "created_date": created_date.strftime("%Y-%m-%d"),
            "close_date": close_date.strftime("%Y-%m-%d")
        })
    
    df = pd.DataFrame(data)
    
    # Ensure data directory exists
    target_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
    os.makedirs(target_dir, exist_ok=True)
    out_path = os.path.join(target_dir, "raw_crm_data.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {num_records} mock CRM records at {out_path}!")

if __name__ == "__main__":
    generate_mock_crm_data(2000)
