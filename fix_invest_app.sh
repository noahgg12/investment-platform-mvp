#!/bin/bash

# Fix the investment platform app by resolving syntax errors

echo "=========================================================="
echo "FIXING INVESTMENT PLATFORM SYNTAX ERRORS"
echo "=========================================================="

# Navigate to the project directory
cd "$(dirname "$0")"

# Create a temporary Python script to fix syntax errors
cat > fix_errors.py << 'EOF'
#!/usr/bin/env python3
import re
import os

# Path to main.py
main_py_path = "app/main.py"

print(f"Reading {main_py_path}...")
with open(main_py_path, 'r') as file:
    content = file.read()

print("Fixing syntax errors...")

# Fix 1: Add 'for sector in normalized_allocation' to close the parenthesis
pattern1 = r"custom_total_return = sum\(amount \* normalized_allocation\.get\(Sector\(sector\), 0\) \* SECTOR_GROWTH\[Sector\(sector\)\]"
replacement1 = "custom_total_return = sum(amount * normalized_allocation.get(Sector(sector), 0) * SECTOR_GROWTH[Sector(sector)]\n                                 for sector in normalized_allocation)"
content = re.sub(pattern1, replacement1, content)

# Fix 2: Add the missing except block in compare_allocation if needed
if "compare_allocation" in content and "except Exception as e:" not in content:
    print("Adding missing exception handler...")
    # Find the end of the compare_allocation function
    func_start = content.find("@app.post(\"/api/compare-allocation\")")
    if func_start > 0:
        # Find where the function returns comparison
        return_idx = content.find("return comparison", func_start)
        if return_idx > 0:
            # Find the end of the line after return comparison
            end_of_func = content.find("\n", return_idx) + 1
            
            # Add the except block
            except_block = """    except Exception as e:
        logger.error(f"Error in compare_allocation: {str(e)}")
        logger.error(traceback.format_exc())
        return {"error": f"An error occurred: {str(e)}"}
"""
            content = content[:end_of_func] + except_block + content[end_of_func:]

print(f"Writing fixed content back to {main_py_path}...")
with open(main_py_path, 'w') as file:
    file.write(content)

print("✅ Syntax errors fixed!")
EOF

# Make the script executable
chmod +x fix_errors.py

# Run the fix script
echo "Running syntax error fixer..."
python fix_errors.py

# Kill any running uvicorn processes
echo "Stopping any running servers..."
pkill -f uvicorn 2>/dev/null || true

# Free up port 8000
if command -v lsof >/dev/null 2>&1; then
    lsof -i :8000 -t | xargs kill -9 2>/dev/null || true
fi

# Wait for port to be completely free
sleep 2

echo "=========================================================="
echo "STARTING SERVER WITH FIXED CODE"
echo "=========================================================="

# Start the server
python run.py

# Clean up the fix script
rm fix_errors.py 