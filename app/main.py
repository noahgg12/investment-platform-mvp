from fastapi import FastAPI, Request, Form, HTTPException # type: ignore
from fastapi.responses import HTMLResponse # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from fastapi.templating import Jinja2Templates # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
import numpy as np # type: ignore
import json
import os
import logging
import sys
from enum import Enum
from datetime import datetime, timedelta
import matplotlib.pyplot as plt # type: ignore
import io
import base64
from typing import Dict, List, Optional, Tuple, Any
from pydantic import BaseModel
import math
import traceback

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger("investment-platform")

# Add debug mode flag - set to True to enable debug features
DEBUG_MODE = False

# Custom JSON encoder to handle numpy types and other non-serializable objects
class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif hasattr(obj, 'to_dict'):
            return obj.to_dict()
        return super().default(obj)

# Safe JSON serialization function
def safe_json_dumps(obj):
    try:
        return json.dumps(obj, cls=CustomJSONEncoder)
    except Exception as e:
        logger.error(f"JSON serialization error: {str(e)}")
        # Return a simplified version that's guaranteed to serialize
        if isinstance(obj, dict):
            return json.dumps({k: str(v) for k, v in obj.items()})
        elif isinstance(obj, list):
            return json.dumps([str(x) for x in obj])
        else:
            return json.dumps(str(obj))

app = FastAPI(
    title="AI Investment Platform",
    description="An MVP for AI-driven investment allocation and prediction",
    version="0.1.0"
)

# Add CORS middleware to allow access from any domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Add exception handler for debugging
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    return HTMLResponse(
        content=f"""
        <html>
            <head>
                <title>Internal Server Error</title>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; padding: 2rem; line-height: 1.5; }}
                    code {{ background: #f4f4f4; padding: 0.2rem 0.4rem; border-radius: 3px; }}
                    pre {{ background: #f4f4f4; padding: 1rem; border-radius: 5px; overflow-x: auto; }}
                </style>
            </head>
            <body>
                <h1>Internal Server Error</h1>
                <p>The application encountered an error processing your request.</p>
                <p>Please try refreshing the page or returning to the <a href="/">home page</a>.</p>
                <p>Error details (for debugging):</p>
                <pre>{str(exc)}\n\n{traceback.format_exc()}</pre>
            </body>
        </html>
        """,
        status_code=500
    )

# Configure templates and static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Investment sectors with simulated annual growth rates
class Sector(str, Enum):
    AI = "AI Startups"
    REAL_ESTATE_TECH = "Real Estate Tech"
    AUTOMATION = "Automation"
    BIOTECH = "Biotech"
    CLEAN_ENERGY = "Clean Energy"
    FINTECH = "Fintech"

# Simulated annual growth rates per sector
SECTOR_GROWTH = {
    Sector.AI: 0.25,  # 25% annual growth
    Sector.REAL_ESTATE_TECH: 0.15,
    Sector.AUTOMATION: 0.20,
    Sector.BIOTECH: 0.18,
    Sector.CLEAN_ENERGY: 0.17,
    Sector.FINTECH: 0.16
}

# Risk levels
class RiskProfile(str, Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with the investment form"""
    try:
        logger.info("Rendering home page")
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        logger.error(f"Error rendering home page: {str(e)}")
        logger.error(traceback.format_exc())
        raise

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Render the dashboard with investment overview"""
    try:
        logger.info("Rendering dashboard")
        
        # Sample data for the dashboard
        # In a real application, this would come from a database
        investment_summary = {
            "total_invested": 125000.00,
            "current_value": 143750.00,
            "total_return": 15.0,
            "annual_return": 8.5,
            "risk_level": "Moderate",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        
        # Sample portfolio allocation
        portfolio = {
            Sector.AI.value: 25,
            Sector.REAL_ESTATE_TECH.value: 20,
            Sector.AUTOMATION.value: 20,
            Sector.BIOTECH.value: 15,
            Sector.CLEAN_ENERGY.value: 10,
            Sector.FINTECH.value: 10
        }
        
        # Sample historical data (monthly returns for the past year)
        historical_data = {
            "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
            "values": [1.2, 0.8, -0.3, 1.5, 2.1, 0.5, -0.2, 1.1, 1.8, 0.7, 1.2, 0.9],
            "cumulative": [1.2, 2.0, 1.7, 3.2, 5.3, 5.8, 5.6, 6.7, 8.5, 9.2, 10.4, 11.3]
        }
        
        # Sample market news
        market_news = [
            {
                "title": "AI Sector Sees Unprecedented Growth",
                "summary": "The AI sector has seen remarkable growth in Q3, with leading companies reporting higher-than-expected earnings.",
                "date": "2023-11-10",
                "sentiment": "positive"
            },
            {
                "title": "Real Estate Tech Innovations Disrupting Traditional Markets",
                "summary": "New property technology solutions are changing how real estate is bought, sold, and managed.",
                "date": "2023-11-08",
                "sentiment": "positive"
            },
            {
                "title": "Biotech Stocks Face Regulatory Headwinds",
                "summary": "Recent regulatory changes have introduced uncertainty in the biotech sector, affecting short-term performance.",
                "date": "2023-11-05",
                "sentiment": "negative"
            }
        ]
        
        # Sample recent activities
        recent_activities = [
            {
                "action": "Portfolio Rebalanced",
                "details": "Automatic rebalancing adjusted your allocation to maintain target risk profile",
                "date": "2023-11-11"
            },
            {
                "action": "Dividend Received",
                "details": "Dividend payment of $320.15 received from technology sector holdings",
                "date": "2023-11-01"
            },
            {
                "action": "New Investment",
                "details": "Added $5,000 to your investment portfolio",
                "date": "2023-10-15"
            }
        ]
        
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "investment_summary": investment_summary,
            "portfolio": portfolio,
            "historical_data": historical_data,
            "market_news": market_news,
            "recent_activities": recent_activities
        })
    except Exception as e:
        logger.error(f"Error rendering dashboard: {str(e)}")
        logger.error(traceback.format_exc())
        raise

@app.post("/invest", response_class=HTMLResponse)
async def invest(
    request: Request,
    amount: float = Form(...),
    risk_profile: str = Form(...)
):
    """Process the investment and return allocation and projections"""
    try:
        logger.info(f"Processing investment: amount={amount}, risk_profile={risk_profile}")
        
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Investment amount must be positive")
        
        # Convert risk profile to enum
        try:
            risk = RiskProfile(risk_profile.lower())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid risk profile")
        
        # AI allocation logic (simplified for MVP)
        allocation = allocate_investment(amount, risk)
        
        # Format sector names for display
        formatted_allocation = {}
        for sector, value in allocation.items():
            # Convert enum to string, replace underscores with spaces, and apply title case
            formatted_name = sector.value
            formatted_allocation[formatted_name] = value
        
        logger.info("Generating projection data")
        # Generate growth projection with safety measures
        projection_data, chart_data, sector_contributions, simulation_meta = safe_generate_projection(amount, allocation)
        
        # Calculate expected returns
        total_expected_return = sum(amount * allocation[sector] * SECTOR_GROWTH[Sector(sector)] 
                                for sector in allocation)
        expected_return_percent = (total_expected_return / amount) * 100
        
        # Generate investment insights
        insights = generate_investment_insights(amount, allocation, risk)
        
        # Add risk score for visualization (1-10 scale)
        risk_score = 3 if risk == RiskProfile.CONSERVATIVE else 6 if risk == RiskProfile.MODERATE else 9
        
        # Log information about the data we're trying to serialize
        logger.info(f"Projection data length: {len(projection_data)}")
        logger.info(f"Chart data has {len(chart_data['datasets'])} datasets")
        
        # Safely serialize JSON data
        try:
            chart_data_json = safe_json_dumps(chart_data)
            sector_contributions_json = safe_json_dumps(sector_contributions)
            simulation_meta_json = safe_json_dumps(simulation_meta)
            
            logger.info("Successfully serialized all JSON data")
        except Exception as json_err:
            logger.error(f"Error serializing JSON: {str(json_err)}")
            # Create simplified versions guaranteed to work
            chart_data_json = json.dumps({
                "labels": [f"Year {i}" for i in range(6)],
                "datasets": [{
                    "label": "Expected Growth",
                    "data": [round(projection_data[i*12], 2) for i in range(6)],
                    "borderColor": "#007AFF",
                    "backgroundColor": "rgba(0, 122, 255, 0.1)",
                }]
            })
            sector_contributions_json = json.dumps({k: float(v) for k, v in sector_contributions.items()})
            simulation_meta_json = json.dumps({
                "initial_investment": float(amount),
                "simulated_scenarios": {
                    "monte_carlo": {"simulations": 1},
                },
                "risk_metrics": {"volatility": 10.0}
            })
        
        # Prepare template context with safe serialization
        template_context = {
            "request": request,
            "amount": amount,
            "allocation": formatted_allocation,
            "expected_return": expected_return_percent,
            "chart_data": chart_data_json,
            "sector_contributions": sector_contributions_json,
            "five_year_value": projection_data[-1],
            "insights": insights,
            "risk_score": risk_score,
            "risk_profile": risk.value,
            "simulation_meta": simulation_meta,
            "simulation_meta_json": simulation_meta_json
        }
        
        logger.info("Successfully generated investment plan")
        
        # Use debug template in debug mode
        if DEBUG_MODE:
            logger.info("Using debug template")
            return templates.TemplateResponse("result_debug.html", template_context)
        else:
            return templates.TemplateResponse("result.html", template_context)
    
    except HTTPException as http_ex:
        # Re-raise HTTP exceptions as they are handled by FastAPI
        logger.warning(f"HTTP exception in invest endpoint: {str(http_ex)}")
        raise
    except Exception as e:
        # Log the error and return a user-friendly error page
        logger.error(f"Error in invest endpoint: {str(e)}")
        logger.error(traceback.format_exc())
        return templates.TemplateResponse(
            "error.html", 
            {
                "request": request,
                "error_message": f"An error occurred processing your investment: {str(e)}",
                "back_url": "/"
            },
            status_code=500
        )

def allocate_investment(amount: float, risk: RiskProfile) -> Dict[str, float]:
    """AI-driven allocation of investment across sectors based on risk profile"""
    try:
        # Simplified AI allocation logic for MVP
        if risk == RiskProfile.CONSERVATIVE:
            # Lower-risk allocation with focus on stable sectors
            return {
                Sector.AI: 0.15,
                Sector.REAL_ESTATE_TECH: 0.25,
                Sector.AUTOMATION: 0.15,
                Sector.BIOTECH: 0.10,
                Sector.CLEAN_ENERGY: 0.20,
                Sector.FINTECH: 0.15
            }
        elif risk == RiskProfile.MODERATE:
            # Balanced allocation
            return {
                Sector.AI: 0.25,
                Sector.REAL_ESTATE_TECH: 0.20,
                Sector.AUTOMATION: 0.20,
                Sector.BIOTECH: 0.15,
                Sector.CLEAN_ENERGY: 0.10,
                Sector.FINTECH: 0.10
            }
        else:  # AGGRESSIVE
            # Higher-risk allocation with focus on high-growth sectors
            return {
                Sector.AI: 0.40,
                Sector.REAL_ESTATE_TECH: 0.10,
                Sector.AUTOMATION: 0.25,
                Sector.BIOTECH: 0.15,
                Sector.CLEAN_ENERGY: 0.05,
                Sector.FINTECH: 0.05
            }
    except Exception as e:
        logger.error(f"Error in allocate_investment: {str(e)}")
        # Provide a safe default allocation if something fails
        return {
            Sector.AI: 0.20,
            Sector.REAL_ESTATE_TECH: 0.20,
            Sector.AUTOMATION: 0.15,
            Sector.BIOTECH: 0.15,
            Sector.CLEAN_ENERGY: 0.15,
            Sector.FINTECH: 0.15
        }

def safe_generate_projection(amount: float, allocation: Dict[str, float]) -> Tuple[List[float], Dict[str, Any], Dict[str, float], Dict[str, Any]]:
    """Wrapper around generate_projection with guaranteed safe return values"""
    try:
        logger.info("Generating investment projection")
        return generate_projection(amount, allocation)
    except Exception as e:
        logger.error(f"Error in generate_projection, falling back to simplified projection: {str(e)}")
        logger.error(traceback.format_exc())
        
        # Create a guaranteed safe fallback projection
        years = 5
        months = years * 12
        
        # Simple linear growth projection
        simple_projection = [amount]
        for month in range(1, months + 1):
            avg_growth_rate = sum(SECTOR_GROWTH[Sector(sector)] * allocation[sector] for sector in allocation)
            monthly_growth = simple_projection[-1] * (avg_growth_rate / 12)
            simple_projection.append(simple_projection[-1] + monthly_growth)
        
        # Simple chart data with just one dataset
        labels = [f"Month {i}" for i in range(months + 1)]
        for i in range(0, months + 1, 12):
            year = i // 12
            labels[i] = f"Year {year}"
            
        chart_data = {
            "labels": labels,
            "datasets": [
                {
                    "label": "Expected Growth",
                    "data": [round(val, 2) for val in simple_projection],
                    "borderColor": "#007AFF",
                    "backgroundColor": "rgba(0, 122, 255, 0.1)",
                    "borderWidth": 3,
                    "fill": True,
                    "tension": 0.4
                }
            ]
        }
        
        # Simple sector contributions
        sector_contributions = {}
        for sector in allocation:
            sector_name = Sector(sector).value
            growth_rate = SECTOR_GROWTH[Sector(sector)]
            initial_investment = amount * allocation[sector]
            final_value = initial_investment * (1 + growth_rate) ** years
            contribution = final_value - initial_investment
            sector_contributions[sector_name] = round(contribution, 2)
        
        # Simple simulation metadata
        simulation_meta = {
            "initial_investment": amount,
            "simulated_scenarios": {
                "monte_carlo": {
                    "simulations": 1,
                    "percentiles": {
                        "10": round(simple_projection[-1] * 0.9, 2),
                        "90": round(simple_projection[-1] * 1.1, 2)
                    }
                },
                "economic_scenarios": {
                    "bull_market": round(simple_projection[-1] * 1.2, 2),
                    "recession": round(simple_projection[-1] * 0.8, 2)
                }
            },
            "risk_metrics": {
                "volatility": 10.0,  # Default value
                "downside_risk": 15.0,  # Default value
                "upside_potential": 25.0  # Default value
            },
            "simulation_parameters": {
                "years": years,
                "inflation_rate": 2.5
            }
        }
        
        return simple_projection, chart_data, sector_contributions, simulation_meta

def generate_projection(amount: float, allocation: Dict[str, float]) -> Tuple[List[float], Dict[str, Any], Dict[str, float], Dict[str, Any]]:
    """Generate advanced investment growth projections with multiple scenarios and simulation methods"""
    # Constants and parameters
    years = 5
    months = years * 12
    num_simulations = 30  # Further reduced for stability
    inflation_rate = 0.025  # 2.5% annual inflation
    market_crash_probability = 0.08  # 8% chance of significant market downturn per year
    
    # Initialize base projection
    projection = [amount]
    
    # ---------------
    # BASE PROJECTION
    # ---------------
    # Monthly compound growth with controlled randomness for stability
    for month in range(1, months + 1):
        previous_amount = projection[-1]
        
        # Calculate growth based on allocation with monthly compounding
        monthly_growth = sum(
            previous_amount * allocation[sector] * (SECTOR_GROWTH[Sector(sector)] / 12)
            for sector in allocation
        )
        
        # Add some randomness to simulate market volatility
        volatility_factors = {
            Sector.AI: 0.025,
            Sector.REAL_ESTATE_TECH: 0.015,
            Sector.AUTOMATION: 0.020,
            Sector.BIOTECH: 0.022,
            Sector.CLEAN_ENERGY: 0.020,
            Sector.FINTECH: 0.018
        }
        
        # Calculate weighted volatility based on allocation
        weighted_volatility = sum(
            allocation[sector] * volatility_factors[Sector(sector)]
            for sector in allocation
        )
        # Cap volatility for stability
        weighted_volatility = min(weighted_volatility, 0.03)
        
        # Generate random market movement with controlled volatility
        volatility = np.random.normal(0, weighted_volatility)
        # Clamp volatility to reasonable bounds
        volatility = max(min(volatility, 0.05), -0.05)
        monthly_growth = monthly_growth * (1 + volatility)
        
        # Controlled random market crash simulation (rare event)
        if np.random.random() < (market_crash_probability / 12):
            # Market crash reduces value by 10-20%
            crash_impact = np.random.uniform(0.10, 0.20)
            monthly_growth = -(previous_amount * crash_impact)
        
        # Apply inflation effect (reduces real returns)
        real_growth = monthly_growth - (previous_amount * (inflation_rate / 12))
        
        new_amount = previous_amount + real_growth
        
        # Ensure investment doesn't go below a certain percentage of original
        new_amount = max(new_amount, amount * 0.7)  # Floor at 70% of original investment
        
        projection.append(new_amount)
    
    # --------------------
    # MONTE CARLO SIMULATION (SIMPLIFIED & MEMORY EFFICIENT)
    # --------------------
    # Use reduced memory approach - only store the end values and monthly percentiles
    final_values = []
    percentile_10 = [amount]
    percentile_90 = [amount]
    
    # Create month-by-month percentiles rather than storing all simulations
    for month in range(1, months + 1):
        month_values = []
        
        for _ in range(num_simulations):
            if month == 1:
                previous_amount = amount
            else:
                # Generate a random starting point within reasonable bounds for this month
                expected_value = projection[month]
                previous_amount = np.random.normal(expected_value, expected_value * 0.03)
                previous_amount = max(previous_amount, amount * 0.6)
            
            # Calculate expected monthly return for this allocation
            expected_monthly_return = sum(
                allocation[sector] * (SECTOR_GROWTH[Sector(sector)] / 12)
                for sector in allocation
            )
            
            # Generate random return from normal distribution (with controlled variance)
            actual_return = np.random.normal(expected_monthly_return, weighted_volatility * 0.7)
            # Clamp return to reasonable bounds
            actual_return = max(min(actual_return, expected_monthly_return * 2), expected_monthly_return * -1)
            
            # Apply the return to the previous amount
            new_amount = previous_amount * (1 + actual_return)
            
            # Apply inflation effect
            new_amount = new_amount * (1 - (inflation_rate / 12))
            
            # Ensure investment doesn't go below a certain percentage of original
            new_amount = max(new_amount, amount * 0.6)
            
            month_values.append(new_amount)
            
            # If it's the final month, collect for final value statistics
            if month == months:
                final_values.append(new_amount)
        
        # Calculate percentiles just for this month
        percentile_10.append(np.percentile(month_values, 10))
        percentile_90.append(np.percentile(month_values, 90))
    
    # ----------------------
    # ECONOMIC SCENARIOS
    # ----------------------
    # Different economic scenarios to show range of possibilities
    
    # 1. Bull Market Scenario - simplified, memory-efficient version
    bull_market = [amount]
    for month in range(1, months + 1):
        previous = bull_market[-1]
        # Growth rates 25% higher than expected
        growth = sum(
            previous * allocation[sector] * (SECTOR_GROWTH[Sector(sector)] * 1.25 / 12)
            for sector in allocation
        )
        bull_market.append(previous + growth)
    
    # 2. Recession Scenario - simplified, memory-efficient version
    recession = [amount]
    recession_months = set(range(12, 18))  # Fixed recession period in months 12-18
    for month in range(1, months + 1):
        previous = recession[-1]
        
        # Calculate growth/loss based on whether we're in the recession period
        if month in recession_months:
            # Negative growth during recession
            growth = previous * -0.01  # -1% monthly during recession
        else:
            # Normal growth in non-recession periods
            growth = sum(
                previous * allocation[sector] * (SECTOR_GROWTH[Sector(sector)] / 12)
                for sector in allocation
            )
        
        # Apply the growth
        recession.append(previous + growth)
    
    # ------------------
    # PREPARE CHART DATA
    # ------------------
    # Create monthly labels for the x-axis
    labels = [f"Month {i}" for i in range(months + 1)]
    
    # Add year markers for readability
    for i in range(0, months + 1, 12):
        year = i // 12
        labels[i] = f"Year {year}"
    
    # Create datasets for Chart.js
    chart_data = {
        "labels": labels,
        "datasets": [
            {
                "label": "Expected Growth",
                "data": [round(val, 2) for val in projection],
                "borderColor": "#007AFF",
                "backgroundColor": "rgba(0, 122, 255, 0.1)",
                "borderWidth": 3,
                "fill": True,
                "tension": 0.4
            },
            {
                "label": "10th Percentile",
                "data": [round(val, 2) for val in percentile_10],
                "borderColor": "#FF3B30",
                "backgroundColor": "rgba(255, 59, 48, 0.05)",
                "borderWidth": 1,
                "fill": "+1",  # Fill to 90th percentile
                "tension": 0.4
            },
            {
                "label": "90th Percentile",
                "data": [round(val, 2) for val in percentile_90],
                "borderColor": "#34C759",
                "backgroundColor": "rgba(52, 199, 89, 0.05)",
                "borderWidth": 1,
                "fill": False,
                "tension": 0.4
            },
            {
                "label": "Recession Scenario",
                "data": [round(val, 2) for val in recession],
                "borderColor": "#FF9500",
                "backgroundColor": "rgba(255, 149, 0, 0.1)",
                "borderWidth": 2,
                "borderDash": [5, 5],
                "fill": False,
                "tension": 0.4,
                "hidden": True  # Hidden by default, can be toggled
            },
            {
                "label": "Bull Market",
                "data": [round(val, 2) for val in bull_market],
                "borderColor": "#34C759",
                "backgroundColor": "rgba(52, 199, 89, 0.1)",
                "borderWidth": 2,
                "borderDash": [5, 5],
                "fill": False,
                "tension": 0.4,
                "hidden": True  # Hidden by default, can be toggled
            }
        ]
    }
    
    # Calculate sector contributions to the expected final value - simplified approach
    sector_contributions = {}
    for sector in allocation:
        sector_name = Sector(sector).value
        growth_rate = SECTOR_GROWTH[Sector(sector)]
        initial_investment = amount * allocation[sector]
        final_value = initial_investment * (1 + growth_rate) ** years
        contribution = final_value - initial_investment
        sector_contributions[sector_name] = round(contribution, 2)
    
    # Advanced simulation metadata
    simulation_meta = {
        "initial_investment": amount,
        "simulated_scenarios": {
            "monte_carlo": {
                "simulations": num_simulations,
                "percentiles": {
                    "10": round(percentile_10[-1], 2),
                    "90": round(percentile_90[-1], 2)
                }
            },
            "economic_scenarios": {
                "bull_market": round(bull_market[-1], 2),
                "recession": round(recession[-1], 2)
            }
        },
        "risk_metrics": {
            "volatility": round(weighted_volatility * math.sqrt(12) * 100, 2),  # Annualized volatility in %
            "downside_risk": round((amount - percentile_10[-1]) / amount * 100, 2),  # Potential downside as % of initial
            "upside_potential": round((percentile_90[-1] - amount) / amount * 100, 2)  # Potential upside as % of initial
        },
        "simulation_parameters": {
            "years": years,
            "inflation_rate": inflation_rate * 100
        }
    }
    
    return projection, chart_data, sector_contributions, simulation_meta

def generate_investment_insights(amount: float, allocation: Dict[str, float], risk: RiskProfile) -> List[str]:
    """Generate AI insights about the investment allocation"""
    try:
        # Get top 3 sectors by allocation
        sorted_sectors = sorted(allocation.items(), key=lambda x: x[1], reverse=True)[:3]
        top_sectors = [Sector(s[0]).value for s in sorted_sectors]
        
        # Simplified insights
        insights = [
            f"Based on your {risk.value} risk profile, our AI has optimized your allocation for balanced growth and risk.",
            f"Your top 3 sectors for investment are: {', '.join(top_sectors)}.",
            f"The AI model predicts these sectors will outperform the market based on current trends.",
            f"We recommend a quarterly review of your allocation to adapt to market changes."
        ]
        
        return insights
    except Exception as e:
        logger.error(f"Error generating insights: {str(e)}")
        # Return default insights if something fails
        return [
            "Our AI has created an optimized investment allocation based on your risk profile.",
            "The allocation balances growth potential and risk management.",
            "We recommend reviewing your portfolio quarterly to adjust to market changes."
        ]

# New API endpoint for comparing returns
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

if __name__ == "__main__":
    import uvicorn # type: ignore
    logger.info("Starting AI Investment Platform application")
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 