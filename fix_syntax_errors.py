#!/usr/bin/env python3
"""
Script to fix syntax errors in the investment platform's main.py file
"""

import os
import re
import sys

def fix_main_py():
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app", "main.py")
    
    if not os.path.exists(file_path):
        print(f"Error: Cannot find {file_path}")
        return False
    
    # Read the file content
    with open(file_path, 'r') as f:
        content = f.read()
    
    # Fix 1: The unclosed parenthesis in custom_total_return
    pattern1 = r"custom_total_return = sum\(amount \* normalized_allocation\.get\(Sector\(sector\), 0\) \* SECTOR_GROWTH\[Sector\(sector\)\]"
    replacement1 = "custom_total_return = sum(amount * normalized_allocation.get(Sector(sector), 0) * SECTOR_GROWTH[Sector(sector)]\n                                 for sector in normalized_allocation)"
    content = re.sub(pattern1, replacement1, content)
    
    # Fix 2: Complete the except block if it's incomplete
    try_pattern = r"try:(?:.*?)\n\s+logger\.info\(\"Successfully generated allocation comparison\"\)\n\s+return comparison\n\s+(?:except Exception as e:)?\s*$"
    
    if re.search(try_pattern, content, re.DOTALL) and "except Exception as e:" not in content:
        # Find the end of the function
        return_idx = content.find("return comparison", content.find("comparison = {"))
        if return_idx > 0:
            end_of_func = content.find("\n", return_idx) + 1
            
            # Add the except block
            except_block = """    except Exception as e:
        logger.error(f"Error in compare_allocation: {str(e)}")
        logger.error(traceback.format_exc())
        return {"error": f"An error occurred: {str(e)}"}
"""
            content = content[:end_of_func] + except_block + content[end_of_func:]
    
    # Write the fixed content back to the file
    with open(file_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Successfully fixed syntax errors in {file_path}")
    return True

def main():
    print("Fixing syntax errors in main.py...")
    if fix_main_py():
        print("\nErrors fixed! Now try running the server again with:")
        print("python run.py")
    else:
        print("\nFailed to fix errors. Please check the file manually.")

if __name__ == "__main__":
    main() 