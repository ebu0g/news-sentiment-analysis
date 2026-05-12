# Step-by-Step Workflow for News Sentiment Analysis Project

## Current Status

✅ **Completed:**
- Project scaffold created with all directories and configurations
- CI/CD pipeline set up (.github/workflows/unittests.yml)
- Task 1 EDA notebook fully structured with analysis templates
- Initial commits on main and task-1 branches

**Current Branch:** `task-1`

---

## Task 1: Exploratory Data Analysis (You are here!)

### What to Do Now

#### Step 1: Prepare Your Data
1. Obtain the financial news CSV file (fields: `headline`, `url`, `publisher`, `date`, `stock`)
2. Obtain historical stock price data (fields: `Date`, `Open`, `High`, `Low`, `Close`, `Adj Close`, `Volume`)
3. Place both files in `data/raw/` folder
   - Example: `data/raw/financial_news.csv`
   - Example: `data/raw/stock_prices.csv`

#### Step 2: Open and Run the Notebook
1. Navigate to `notebooks/task1_eda.ipynb`
2. Open it in Jupyter (VS Code or `jupyter notebook`)
3. Update the file path in **Cell 1** to match your actual data file names
4. Run cells sequentially—each section builds on the previous one

#### Step 3: Execute Each Analysis Section

**Cell 1: Data Loading**
- Loads the CSV and displays schema, shape, and missing values
- **Action:** Replace `'../data/raw/financial_news.csv'` with your actual file path

**Cells 2–4: Descriptive Statistics**
- Headline length distribution (histogram + boxplot)
- Top 20 publishers by article count (bar chart)
- Publication frequency over time (line plot)
- **Expected Output:** 3 visualizations showing data patterns

**Cells 5–6: Text Analysis**
- Extracts top 20 keywords using TF-IDF
- Identifies top 15 common bigrams (2-word phrases)
- **Expected Output:** 2 bar charts showing frequent topics like "earnings beat", "price target", "FDA approval"

**Cell 7: Publisher Analysis**
- Lists all unique publishers
- If email addresses are present, extracts and ranks domains
- Shows stock coverage (which stocks get most coverage)
- **Expected Output:** 2 bar charts (domains and stock symbols)

**Cell 8: Time-of-Day Analysis**
- Extracts hour from timestamp
- Shows which hours have most publications
- Identifies peak and slowest publishing hours
- **Expected Output:** 1 bar chart showing hourly distribution

**Cell 9: Summary**
- Fill in the template with your key findings
- Document dataset overview, headline characteristics, keywords, publisher patterns, temporal trends

#### Step 4: Document and Commit
After running the entire notebook:

1. **Document findings** in Cell 9 (Summary section)
2. **Commit your changes** with a descriptive message:
   ```bash
   git add notebooks/task1_eda.ipynb
   git commit -m "feat(eda): complete Task 1 analysis with findings

   - Analyzed 5000 articles spanning Q1 2025
   - Identified 'earnings' and 'FDA approval' as top keywords
   - Reuters is top publisher with 1200 articles
   - Peak publishing hours: 9-11 AM UTC-4"
   ```
3. **Target:** Commit at least 3 times per day with meaningful messages

---

## Git Workflow for Multi-Day Work

### Daily Workflow

Each day, follow this pattern:

```bash
# Start each work session
git checkout task-1
git pull origin task-1  # In case you're working on multiple machines

# Make changes to notebooks/task1_eda.ipynb
# Test your code by running cells

# Commit your work frequently (aim for 3+ commits/day)
git add notebooks/task1_eda.ipynb
git commit -m "feat(eda): add [specific analysis or fix]"

# Push to remote
git push origin task-1
```

### Commit Message Guidelines (Conventional Commits)

Use this format for clear, searchable commit history:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat` – New feature or analysis
- `fix` – Bug fix or correction
- `docs` – Documentation or comments
- `refactor` – Code reorganization
- `test` – Testing additions

**Examples:**
```
feat(eda): add TF-IDF keyword extraction

- Extract top 20 keywords from headlines
- Generate bar chart visualization
- Identify recurring themes (earnings, M&A, FDA)

Relates to: Task 1 requirement 3
```

```
fix(eda): handle missing dates in publication frequency plot

- Add null check before datetime conversion
- Filter out articles without date field
- Re-run time series analysis
```

---

## When Task 1 Is Complete: Merging to Main

### Prerequisites
- All EDA analyses complete
- At least 3 insights documented
- Notebook runs without errors
- 3+ commits with descriptive messages

### Steps to Merge

1. **Push final changes:**
   ```bash
   git push origin task-1
   ```

2. **Create a Pull Request (PR)** on GitHub:
   - Go to your repository on GitHub
   - Click "Pull requests" → "New pull request"
   - Base: `main` ← Compare: `task-1`
   - Title: `Merge task-1: Complete EDA analysis`
   - Description: Summarize key findings (3-5 bullet points)
   - Click "Create pull request"

3. **Request review** (if working in team) or self-review

4. **Merge to main:**
   - Click "Merge pull request"
   - Select "Squash and merge" or "Create a merge commit"
   - Delete the branch after merging

5. **Pull main locally:**
   ```bash
   git checkout main
   git pull origin main
   ```

---

## Next Tasks Preview (After Task 1)

### Task 2: Technical Indicators (After Task 1 merges)

```bash
git checkout main
git pull origin main
git checkout -b task-2
```

**Focus:** Load historical stock prices, compute MA, RSI, MACD using TA-Lib and PyNance
- New notebook: `notebooks/task2_technical_indicators.ipynb`
- Deliverable: Technical indicator plots overlaid on price data

### Task 3: Sentiment-to-Return Correlation (After Task 2 merges)

```bash
git checkout main
git pull origin main
git checkout -b task-3
```

**Focus:** Apply sentiment analysis (TextBlob/VADER) to headlines, compute daily returns, correlate
- New notebook: `notebooks/task3_sentiment_correlation.ipynb`
- Deliverable: Scatter plot, correlation coefficient, investment insights

---

## Helpful Commands Reference

```bash
# View current branch
git branch

# View commit history
git log --oneline -10

# View changes before committing
git status
git diff notebooks/task1_eda.ipynb

# Undo last commit (keep changes)
git reset --soft HEAD~1

# View remote branches
git branch -a

# Set up tracking (if not already tracked)
git branch --set-upstream-to=origin/task-1 task-1
```

---

## Troubleshooting

**Q: "ModuleNotFoundError: No module named 'pandas'"**
A: Reinstall dependencies:
```bash
pip install -r requirements.txt
```

**Q: "Notebook won't open in VS Code"**
A: Ensure the JSON is valid and restart VS Code. Check file path is absolute.

**Q: "I lost my changes, how do I recover?"**
A: If committed, use `git log` to find the commit hash and `git checkout <hash>`. If not committed, check `git reflog`.

**Q: "How do I switch to a different branch?"**
A: `git checkout <branch-name>` (or `git switch <branch-name>` on newer Git versions)

---

## Key Files to Know

- **Notebook:** [notebooks/task1_eda.ipynb](notebooks/task1_eda.ipynb) – Your main analysis file
- **Data:** Place raw data in [data/raw/](data/raw/) folder
- **Config:** [.vscode/settings.json](.vscode/settings.json) – IDE configuration
- **Dependencies:** [requirements.txt](requirements.txt) – Python packages
- **CI:** [.github/workflows/unittests.yml](.github/workflows/unittests.yml) – Automated tests
- **Repo Root:** [README.md](README.md) – Project overview

---

## Interim Submission (Due: Sunday, 10 May 2026, 8:00 PM UTC)

**What to Submit:**
1. GitHub repository link (public or shared with team)
2. Completed Task 1 notebook with 3+ visualizations and findings
3. Initial progress on Task 2 (at least one technical indicator calculated)

**Report Contents (Max 3 pages):**
- Summary of data loading and cleaning
- Key EDA findings with supporting visualizations
- Initial stock price analysis with one technical indicator
- Challenges and next steps

---

## Final Submission (Due: Tuesday, 12 May 2026, 8:00 PM UTC)

**What to Submit:**
1. Complete GitHub repository with all 3 tasks merged to `main`
2. Final report (blog post format, up to 10 pages)
3. All code clean, documented, and tested

---

Good luck! Start with loading your data and running the first notebook cell. Feel free to iterate, experiment, and commit frequently. You've got this! 🚀
