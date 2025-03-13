import json
from rules import latest_financial_index, borrowing_to_revenue_flag, total_revenue

def probe_model(data: dict):
    """Evaluate financial flags."""
    financial_index = latest_financial_index(data)

    revenue = total_revenue(data, financial_index)
    borrowing_flag = borrowing_to_revenue_flag(data, financial_index)

    return {
        "flags": {
            "TOTAL_REVENUE": revenue,
            "BORROWING_TO_REVENUE_FLAG": borrowing_flag
        }
    }

if __name__ == "__main__":
    try:
        with open("data.json", "r") as file:
            data = json.load(file)

        if "data" in data:
            result = probe_model(data["data"])
            print(json.dumps(result, indent=4))
        else:
            print("Error: 'data' key not found in JSON file.")
    except FileNotFoundError:
        print("Error: data.json file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in data.json.")
