import sys
import os
import pandas as pd
from whatsapp import send_message as whatsapp_send_message

def send_bulk_messages(excel_path: str, message: str) -> None:
    """
    Send WhatsApp message to all numbers in the Excel file.
    
    Args:
        excel_path: Path to Excel file containing phone numbers
        message: Message to send
    """
    try:
        # Get absolute path if relative path is provided
        abs_excel_path = os.path.abspath(excel_path)
        
        if not os.path.exists(abs_excel_path):
            print(f"Error: Excel file not found at: {abs_excel_path}")
            print("Make sure the Excel file exists and the path is correct.")
            return
            
        # Read the Excel file
        df = pd.read_excel(abs_excel_path)
        
        if 'phone_number' not in df.columns:
            print("Error: Column 'phone_number' not found in Excel file")
            print("Make sure your Excel file has a column named 'phone_number'")
            return
        
        total = len(df)
        success = 0
        failed = 0
        
        print(f"\nSending message to {total} numbers...")
        print("-" * 50)
        
        # Process each phone number
        for phone in df['phone_number'].dropna():
            # Clean the phone number
            clean_phone = str(phone).strip().replace("+", "").replace(" ", "").replace("-", "")
            
            # Send message
            success_status, status_message = whatsapp_send_message(clean_phone, message)
            
            # Print status
            status = "✓" if success_status else "✗"
            print(f"{status} {clean_phone}: {status_message}")
            
            if success_status:
                success += 1
            else:
                failed += 1
        
        print("-" * 50)
        print(f"Summary: Total={total}, Success={success}, Failed={failed}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nTroubleshooting tips:")
        print("1. Make sure you're in the correct directory")
        print("2. Check if the Excel file exists")
        print("3. Verify the Excel file has a 'phone_number' column")

def main():
    if len(sys.argv) != 3:
        print("Usage: python send_bulk_whatsapp.py <excel_file_path> <message>")
        print("Example: python send_bulk_whatsapp.py sample_numbers.xlsx 'Hello everyone!'")
        print("\nMake sure you're in the directory containing the Excel file.")
        sys.exit(1)
    
    excel_path = sys.argv[1]
    message = sys.argv[2]
    
    send_bulk_messages(excel_path, message)

if __name__ == "__main__":
    main() 