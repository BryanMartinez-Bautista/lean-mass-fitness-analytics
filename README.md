# Lean Mass Fitness Analytics

## Project Objective
Explore which workout, nutrition, and lifestyle factors are associated with lean
body mass, and build predictive models using an AI-assisted data science workflow
(Streamlit + LangChain + Gemini).

## Dataset
Smart Fitness & Nutrition Analytics Dataset
https://huggingface.co/datasets/Idankhen/SmartFitnessNutritionAnalyticsDataset

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/BryanMartinez-Bautista/lean-mass-fitness-analytics.git
   cd lean-mass-fitness-analytics
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the dataset:
   ```bash
   python src/load_data.py
   ```
4. Add your Gemini API key to a `.env` file (see `.env.example`):
   ```
   GOOGLE_API_KEY=your_key_here
   ```
5. Run the app:
   ```bash
   streamlit run src/app.py
   ```

## Project Structure
```
data/     - dataset
src/      - source code (app, cleaning, models, AI assistant)
figures/  - generated figures
report/   - exported PDF report
```

## Author
Bryan Martinez-Bautista