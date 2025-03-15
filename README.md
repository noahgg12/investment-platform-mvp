# Rain Investment Platform

A modern AI-powered investment platform that provides personalized investment strategies based on your risk profile.

## Features

### Core Features
- AI-driven investment allocation across different sectors
- Risk profile assessment (Conservative, Moderate, Aggressive)
- Detailed investment projections and visualizations
- Interactive data visualization with Chart.js
- Responsive design with Apple-inspired UI

### New Features
- **Dark Mode** - Switch between light and dark themes for comfortable viewing
- **Portfolio Simulator** - Create and compare your own allocations with AI recommendations
- **Interactive Charts** - Multiple chart types with real-time toggling
- **Enhanced Homepage** - Animated statistics, testimonials, and comparison tools
- **Improved Performance** - Optimized server handling and smart restart
- **Accessibility Improvements** - Better contrast and keyboard navigation
- **Public Sharing** - Make your investment platform accessible to others on the internet

## Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/rain-investment-platform.git
cd rain-investment-platform
```

2. Install the required packages:
```
pip install -r requirements.txt
```

3. Run the application:
```
python run.py
```

4. Open your browser and navigate to:
```
http://localhost:8000
```

## Making the Application Publicly Accessible

To share your investment platform with others over the internet, you can use the included script:

```
chmod +x public_access.sh
./public_access.sh
```

This will:
1. Install ngrok if it's not already installed
2. Start the Rain Investment Platform in the background
3. Create a secure tunnel using ngrok
4. Provide you with a public URL to share with others

The URL will look something like `https://abc123.ngrok.io` and will be valid as long as the script is running.

Note: You'll need to sign up for a free ngrok account at https://ngrok.com/ and configure your authtoken the first time you run this.

## Usage

1. **Enter Investment Amount**: Specify how much you want to invest
2. **Select Risk Profile**: Choose between Conservative, Moderate, or Aggressive
3. **View Results**: See optimized allocation, projections, and insights
4. **Simulate Alternatives**: Use the Portfolio Simulator to try different allocations
5. **Toggle Views**: Switch between different chart types and visualization modes
6. **Compare Results**: See how your custom allocations compare to AI recommendations

## Technology Stack

- **Backend**: FastAPI, Python, Pydantic
- **Frontend**: HTML5, CSS3, JavaScript, Chart.js
- **UI Framework**: Bootstrap 5
- **Data Visualization**: Chart.js
- **Design System**: Apple-inspired design language

## Development

### Project Structure

```
investment-platform-mvp/
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI application
├── static/
│   └── styles.css       # CSS styles
├── templates/
│   ├── index.html       # Homepage template
│   └── result.html      # Results page template
├── requirements.txt     # Python dependencies
├── run.py               # Application launcher
├── public_access.sh     # Script for making the app publicly accessible
└── README.md            # This file
```

### Key Components

- **Investment Allocation**: AI-driven strategy based on risk profile
- **Growth Projection**: 5-year forecast with multiple scenarios
- **Interactive Visualization**: Real-time data exploration
- **Portfolio Simulator**: Compare custom allocations with AI recommendations

## Troubleshooting

### Common Issues

- **Port conflicts**: The application automatically finds an available port if 8000 is in use
- **Dark mode not working**: Check if your browser supports localStorage
- **Charts not rendering**: Ensure you have a stable internet connection for Chart.js CDN
- **Public URL not working**: Make sure you've configured your ngrok authtoken correctly

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Chart.js for powerful data visualization
- Bootstrap for responsive UI components
- FastAPI for high-performance API framework
- ngrok for secure tunneling # investment-platform-mvp
