"""
Fixed compare_allocation function that can be used to replace the broken one in main.py
"""

# The complete fixed compare_allocation function
fixed_function = '''
@app.post("/api/compare-allocation")
async def compare_allocation(request: Request):
    """Compare a custom allocation with the AI recommendation"""
    try:
        logger.info("Processing allocation comparison request")
        data = await request.json()
        
        amount = float(data.get('amount', 0))
        risk_profile = data.get('risk_profile', 'moderate')
        custom_allocation = data.get('custom_allocation', {})
        
        # Validate the data
        if amount <= 0:
            return {"error": "Investment amount must be positive"}
            
        # Convert risk profile to enum
        try:
            risk = RiskProfile(risk_profile.lower())
        except ValueError:
            return {"error": "Invalid risk profile"}
            
        # Get AI allocation
        ai_allocation = allocate_investment(amount, risk)
        
        # Calculate expected returns for AI allocation
        ai_total_return = sum(amount * ai_allocation[sector] * SECTOR_GROWTH[Sector(sector)] 
                              for sector in ai_allocation)
        ai_return_percent = (ai_total_return / amount) * 100
        
        # Validate custom allocation
        total_percentage = sum(float(val) for val in custom_allocation.values())
        if abs(total_percentage - 100) > 0.1:  # Allow small rounding errors
            return {"error": "Custom allocation must total 100%"}
            
        # Convert custom allocation percentages to decimals
        normalized_allocation = {}
        for sector, percentage in custom_allocation.items():
            if sector in [s.value for s in Sector]:
                normalized_allocation[Sector(sector)] = float(percentage) / 100
            
        # Calculate expected returns for custom allocation
        custom_total_return = sum(amount * normalized_allocation.get(Sector(sector), 0) * SECTOR_GROWTH[Sector(sector)]
                                 for sector in normalized_allocation)
        custom_return_percent = (custom_total_return / amount) * 100
        
        # Generate comparison data
        comparison = {
            "ai_return": round(ai_return_percent, 2),
            "custom_return": round(custom_return_percent, 2),
            "difference": round(custom_return_percent - ai_return_percent, 2),
            "recommendation": "Your custom allocation is projected to " + 
                             ("outperform" if custom_return_percent > ai_return_percent else "underperform") + 
                             " our AI recommendation by " + 
                             f"{abs(round(custom_return_percent - ai_return_percent, 2))}%"
        }
        
        logger.info("Successfully generated allocation comparison")
        return comparison
        
    except Exception as e:
        logger.error(f"Error in compare_allocation: {str(e)}")
        logger.error(traceback.format_exc())
        return {"error": f"An error occurred: {str(e)}"}
'''

print("Copy the above function to replace the broken compare_allocation function in main.py") 