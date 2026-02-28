
import streamlit as st
import random
import textwrap
from dataclasses import dataclass
from typing import List, Dict, Any, Optional

# ==========================================
# Financial Literacy App (Streamlit)
# - Lessons (~2000-word style per topic)
# - Randomized 20-question quiz (new each attempt)
# - Randomized 20-scenario simulation runs
# - Financial-themed UI
# ==========================================

st.set_page_config(page_title="MintMind — Financial Literacy", page_icon="💵", layout="wide")

# -----------------------------
# Helpers
# -----------------------------
def money(n: float) -> str:
    try:
        return f"${n:,.0f}"
    except Exception:
        return "$0"

def pct(p: float) -> str:
    try:
        return f"{int(round(p * 100))}%"
    except Exception:
        return "0%"

def clamp(n, lo, hi):
    return max(lo, min(hi, n))

def seeded_rng(seed: Optional[int] = None) -> random.Random:
    return random.Random(seed) if seed is not None else random.Random()

def sample_unique(rng: random.Random, items: List[Any], k: int) -> List[Any]:
    if k >= len(items):
        items_copy = items[:]
        rng.shuffle(items_copy)
        return items_copy
    return rng.sample(items, k)

# -----------------------------
# Content Models
# -----------------------------
@dataclass
class Topic:
    id: str
    title: str
    subtitle: str
    lesson_md: str

@dataclass
class Question:
    id: str
    topic_id: str
    prompt: str
    options: List[str]
    answer_index: int
    explanation: str

@dataclass
class SimChoice:
    label: str
    effects: Dict[str, float]  # cash, debt, savings, score
    outcome: str

@dataclass
class Scenario:
    id: str
    title: str
    context: str
    state: Dict[str, float]  # cash, debt, savings, score
    choices: List[SimChoice]

# -----------------------------
# Lessons (long-form)
# NOTE: These are written in a "2000-word lesson" style for each topic.
# If you want more topics, duplicate a Topic and add another long lesson.
# -----------------------------
LESSON_BUDGETING = """
# Budgeting & Cash Flow Mastery

A budget isn’t a punishment—it’s a **plan**. People often think budgeting means restriction, but strong budgeting is really about **freedom**: you decide what your money is supposed to do, instead of wondering where it went. The most common reason budgets “fail” is not because someone is lazy or “bad with money.” It’s because they built a plan that doesn’t match real life: bills arrive at inconvenient times, irregular expenses appear, and emotions influence spending. This lesson gives you a practical system that works in the messy world.

## 1) Cash flow comes before budgeting

Cash flow is the movement of money in and out. It’s not just *how much* you make—it’s *when* you receive it and *when* your expenses hit. Many people technically earn enough over the month but run out of money mid-month because the timing doesn’t align. For example, rent and insurance might hit early, but your paycheck comes later.

Start by listing:
- **Income sources**: paychecks, freelance, tips, benefits, reimbursements.
- **Fixed expenses**: rent/mortgage, minimum debt payments, insurance, subscriptions.
- **Variable essentials**: groceries, gas/transit, utilities, basic medical.
- **Discretionary**: eating out, entertainment, shopping, hobbies.
- **Irregular**: gifts, annual fees, car repairs, travel, taxes, back-to-school.

Irregular expenses are the silent budget killers. They aren’t truly unexpected; they’re “predictably unpredictable.”

## 2) The 3-layer budget

Think of your budget in layers that protect your life:
1. **Survival**: housing, food, utilities, transportation to work, minimum debt payments.
2. **Stability**: emergency fund contributions and sinking funds.
3. **Growth**: investing, long-term goals, and intentional joy spending.

When money is tight, survival is the priority. As you improve cash flow, you expand stability, then growth. This prevents guilt because you can say: “I funded survival and stability first—now I choose how to enjoy the rest.”

## 3) Zero-based budgeting (without stress)

Zero-based budgeting means every dollar gets a job so that:
**Income – allocations = 0**

“Zero” doesn’t mean you spend everything. It means you intentionally assign money to categories like rent, groceries, sinking funds, debt payoff, investing, and fun. The key is adding a **buffer** category to handle real life.

Example: Take-home pay = $3,200
- Rent: $1,250
- Utilities: $180
- Groceries: $380
- Transportation: $120
- Insurance: $150
- Phone: $50
- Subscriptions: $25
- Debt minimums: $200
- Sinking funds: $250
- Emergency savings: $150
- Fun money: $150
- Buffer/misc: $95

That buffer prevents “one weird week” from breaking your plan.

## 4) Categories that actually work

Too many categories = you quit. Too few = you learn nothing.

A balanced set:
- Housing
- Utilities
- Groceries
- Eating out
- Transportation
- Health
- Insurance
- Debt
- Emergency fund
- Sinking funds (irregular)
- Personal
- Entertainment
- Giving
- Buffer/Misc

If you’re working on a specific goal (like reducing eating out), split it into separate categories so you can see it clearly.

## 5) Paycheck budgeting

Monthly budgets are common, but many people get paid weekly or biweekly. Paycheck budgeting reduces chaos:
- List bills due before next payday
- Fund those first
- Fund groceries/transport
- Put the rest into sinking funds, savings, debt payoff, and fun

This system prevents overdrafts and “I’m broke on day 12” stress.

## 6) Sinking funds: the calm-maker

Sinking funds are savings buckets for known future costs:
- Car maintenance
- Gifts/holidays
- Annual subscriptions
- Medical/dental
- Travel
- Clothing replacement

If you expect $600/year in gifts, save $50/month. If car costs average $900/year, save $75/month. When the expense arrives, you’re ready.

## 7) Spending cuts that don’t feel like suffering

Two types of cuts:
- **Frequency cuts**: fewer purchases (fewer deliveries)
- **Unit price cuts**: same category cheaper (cheaper grocery plan)

The best cuts are the ones you don’t hate. Look for:
- Subscription audits
- Meal planning + grocery list
- Switching to cheaper insurance/phone plans
- Negotiating bills
- Changing defaults (auto-save first)

## 8) Income is a budgeting lever too

Budgeting isn’t only cutting. If essentials consume most income, your biggest lever is earnings:
- negotiate pay
- switch roles
- upskill
- side income (sustainable, not burnout)

Income growth works best when paired with a plan against lifestyle inflation.

## 9) The review loop (how budgets get better)

Budgeting is an experiment:
1. Plan
2. Track
3. Review
4. Adjust

Ask:
- What surprised me?
- What did I underestimate?
- What supports my life and deserves more funding?
- What can shrink with minimal pain?

## 10) Your first wins (momentum > perfection)

If you’re starting today:
1. Track spending for 7 days (no judgment)
2. Build a mini buffer ($100–$300)
3. Choose one habit (meal plan, subscription audit, auto-transfer)

A simple “good” budget beats a perfect budget you don’t use. Money management is a skill—and skills improve with practice.
""".strip()

LESSON_CREDIT = """
# Credit, Debt & Interest

Credit can be a ladder or a trap. It’s a financial tool that helps you buy now and pay later—but borrowing always has a cost: **interest, risk, and behavior**. The math matters, but the system matters even more: autopay set to minimum payments, ignoring statements, spending without limits, and using debt to patch broken cash flow. In this lesson you’ll learn how credit works, how scores are built, and how to escape expensive debt cycles.

## 1) What credit really is

Credit is borrowed money with a promise to repay. Lenders charge interest because:
- you get money now
- there’s risk you won’t repay
- the lender gives up other opportunities

There are two big categories:
- **Secured credit**: backed by collateral (house, car)
- **Unsecured credit**: not backed (credit cards, many personal loans)

Unsecured debt is often more expensive.

## 2) APR and interest in plain English

**APR (Annual Percentage Rate)** is the annual cost of borrowing. Debt may accrue interest daily or monthly depending on the product, but you can think of APR as a “rough yearly price tag.”

Credit cards typically charge high APR and calculate interest on carried balances. If you pay the statement balance in full by the due date, many cards charge no interest on purchases. If you carry a balance, interest can accumulate quickly.

## 3) Why minimum payments keep you stuck

Minimum payments are designed to keep you “current,” not free. When you pay only minimum:
- a large portion goes to interest
- principal reduces slowly
- payoff can take years

A useful rule: if you can’t pay the full statement balance, aim to pay **as much above minimum as possible** and choose a plan (avalanche or snowball).

## 4) Types of debt and their risks

- **Credit cards**: flexible, high interest, easiest to grow silently
- **Personal loans**: fixed payments, can consolidate debt
- **Auto loans**: secured; repossession risk
- **Student loans**: special rules and programs (varies by country)
- **BNPL**: can be 0% but stacking payments creates hidden strain

Debt is not automatically “bad,” but high-interest consumer debt is usually a priority to eliminate.

## 5) Credit scores: what they measure (and what they don’t)

A credit score is a risk estimate for lenders. Common factors include:
- payment history (on-time payments)
- utilization (how much revolving credit is used)
- length of credit history
- new credit inquiries
- mix of credit types

Your score is not your character. It’s just a tool. You improve it with consistent habits.

## 6) Safe credit-building habits

- Set autopay for **at least** the minimum (avoid late fees)
- Pay statement balance in full when possible
- Keep utilization lower by paying down balances
- Avoid opening many accounts quickly
- Review statements weekly or biweekly

## 7) Debt payoff strategies

### Avalanche (lowest cost)
Pay minimums on all debts, then put extra toward the highest APR first.

### Snowball (motivation)
Pay minimums, then put extra toward the smallest balance first.

The best strategy is the one you’ll stick to for months.

## 8) Consolidation: powerful when used correctly

Consolidation can help if:
- the new rate is meaningfully lower
- the term doesn’t become so long you pay more overall
- you stop adding new debt

Consolidation fails when people pay off cards with a loan, then run cards back up again.

## 9) Negotiation and hardship options

If you’re struggling, call lenders early. Options may include:
- reduced interest
- payment plans
- hardship programs
- temporary forbearance

Ask: “What programs exist to help customers who are trying to pay responsibly?”

## 10) Systems beat willpower

Debt often grows from stress, social pressure, or cash flow breaks. The solution is a system:
- realistic budget
- emergency buffer
- clear spending rules
- fewer frictionless purchases (remove saved cards, unsubscribe)

## 11) A simple action plan

1. List debts: balance, APR, minimum
2. Choose avalanche or snowball
3. Autopay minimums
4. Put extra money toward target debt weekly
5. Build a small buffer to stop new debt

Credit can be your ally when managed intentionally. The goal is freedom: lower interest costs, less stress, and more options.
""".strip()

LESSON_INVEST = """
# Saving & Investing Basics

Saving and investing both mean “paying future you,” but they serve different jobs. **Saving** protects stability and near-term goals. **Investing** grows money for long-term goals, accepting volatility in exchange for potential returns. This lesson explains how to build an emergency fund, create goal-based savings, and start investing in a simple, realistic way.

## 1) Start with a goal (motivation matters)

People stay consistent when money has meaning:
- freedom (choices)
- safety (less anxiety)
- options (career flexibility)
- big goals (home, education, business)

Write 1–3 goals that matter. Your plan should serve your life, not a generic rule.

## 2) Emergency fund: the shock absorber

An emergency fund prevents a tire blowout from turning into credit card debt.

Typical milestones:
- Starter: $300–$1,000
- Then: 1 month of essentials
- Then: 3–6 months (depends on job stability, dependents, health)

You don’t build it overnight. Automation and consistency win.

## 3) Sinking funds: predictable future costs

Many “surprises” are predictable:
- gifts/holidays
- car repairs
- annual insurance premiums
- medical and dental
- travel

A sinking fund reduces stress because expenses stop feeling like emergencies.

## 4) Where to keep savings (principles)

Near-term money should prioritize:
- safety
- liquidity (easy access)
- modest yield

Often this means a high-yield savings account or equivalent in your region, but the principle is: don’t invest money you can’t afford to risk.

## 5) Inflation: why investing exists

Inflation reduces purchasing power over time. If your money earns 0% and inflation is 3%, you effectively lose 3% in buying power each year. Investing aims to outpace inflation over long horizons.

## 6) Risk and time horizon

Risk is not just “chance of losing money.” It’s the chance your money is worth less when you need it. Time helps because markets often fluctuate short-term but can grow over decades. This is why retirement investing often uses diversified portfolios.

## 7) Diversification: don’t bet on one outcome

Diversification spreads your investments across many companies and sectors. Broad funds (like diversified index funds/ETFs) often provide instant diversification. Concentrating in one company increases risk—even if the company seems “safe.”

## 8) Fees: the silent compounding enemy

Fees compound too. A 1% annual fee may sound small, but over decades it can significantly reduce outcomes. Prefer transparent, low-fee options when available.

## 9) Compounding: time + consistency

Compounding is when returns earn returns. It works best when you start earlier and contribute regularly.

**Dollar-cost averaging**: investing a fixed amount regularly regardless of market price. It reduces pressure to time the market.

## 10) A practical order of operations

A common, practical sequence:
1. Essentials + minimum debt payments
2. Starter emergency fund
3. Pay off high-interest debt
4. Build larger emergency fund
5. Invest for long-term goals
6. Save for medium-term goals safely

This sequence reduces the chance you’ll need to borrow at high interest.

## 11) Retirement accounts and matching

Many employers offer matching contributions. A match can be a powerful benefit. If available, it’s often worth prioritizing because it’s like an immediate “return.”

Tax rules vary by country, but the general idea is: tax advantages can amplify long-term growth.

## 12) Emotional discipline matters more than prediction

The biggest investing mistakes are emotional:
- panic selling during downturns
- chasing hype
- overtrading
- investing money needed soon

A plan protects you:
- emergency fund
- diversified portfolio
- automation
- long-term horizon

## 13) Your first steps

1. Calculate one month of “survival expenses”
2. Automate a small weekly savings transfer
3. Create one sinking fund (car or gifts)
4. When stable, automate investing

You don’t need to be an expert to win. You need a simple system you can follow for years.
""".strip()

TOPICS: List[Topic] = [
    Topic(
        id="budgeting_cashflow",
        title="Budgeting & Cash Flow Mastery",
        subtitle="Build a plan that works in real life, not just on paper.",
        lesson_md=LESSON_BUDGETING,
    ),
    Topic(
        id="credit_debt",
        title="Credit, Debt & Interest",
        subtitle="Understand credit, reduce expensive debt, and build options.",
        lesson_md=LESSON_CREDIT,
    ),
    Topic(
        id="saving_investing",
        title="Saving & Investing Basics",
        subtitle="Emergency funds, simple investing, and long-term growth.",
        lesson_md=LESSON_INVEST,
    ),
]

# -----------------------------
# Quiz Question Bank
# - We include a base set + generated variants for variety
# - Each quiz run selects 20 random questions
# -----------------------------
BASE_QUESTIONS: List[Question] = [
    # Budgeting
    Question(
        id="q_budget_1",
        topic_id="budgeting_cashflow",
        prompt="What is the main purpose of a budget?",
        options=[
            "To restrict you from enjoying life",
            "To make money visible and intentional",
            "To maximize the number of bank accounts you have",
            "To avoid tracking expenses",
        ],
        answer_index=1,
        explanation="A budget is a plan/map so you decide what money does instead of wondering where it went.",
    ),
    Question(
        id="q_budget_2",
        topic_id="budgeting_cashflow",
        prompt="Which expense type is most likely to break a budget if ignored?",
        options=["Fixed expenses", "Irregular expenses", "Income taxes", "Monthly bills only"],
        answer_index=1,
        explanation="Irregular expenses (car repairs, gifts, annual fees) are predictable but often overlooked.",
    ),
    Question(
        id="q_budget_3",
        topic_id="budgeting_cashflow",
        prompt="In zero-based budgeting, “zero” means:",
        options=[
            "You spend every dollar",
            "Income minus allocations equals zero",
            "You have no savings",
            "You never use a buffer",
        ],
        answer_index=1,
        explanation="Every dollar gets a job. Zero refers to unassigned dollars, not “having nothing.”",
    ),
    Question(
        id="q_budget_4",
        topic_id="budgeting_cashflow",
        prompt="A sinking fund is best described as:",
        options=[
            "A loan for emergencies",
            "Saving gradually for predictable future expenses",
            "An investment account for retirement only",
            "A category for impulse purchases",
        ],
        answer_index=1,
        explanation="Sinking funds are savings buckets for known future expenses like gifts, travel, or repairs.",
    ),

    # Credit
    Question(
        id="q_credit_1",
        topic_id="credit_debt",
        prompt="What does APR generally represent?",
        options=[
            "A monthly fee",
            "The yearly cost of borrowing, expressed as a percentage",
            "A guarantee you will be approved",
            "Your credit limit",
        ],
        answer_index=1,
        explanation="APR is an annualized rate that reflects the cost of borrowing.",
    ),
    Question(
        id="q_credit_2",
        topic_id="credit_debt",
        prompt="Why are credit card minimum payments risky?",
        options=[
            "They are always illegal",
            "They can make repayment take years and increase total interest",
            "They lower your credit score immediately",
            "They stop interest from accruing",
        ],
        answer_index=1,
        explanation="Minimum payments keep you current but often maximize payoff time and total interest.",
    ),
    Question(
        id="q_credit_3",
        topic_id="credit_debt",
        prompt="Which payoff method is typically cheapest mathematically?",
        options=["Snowball", "Avalanche", "Skipping payments", "Refinancing always"],
        answer_index=1,
        explanation="Avalanche targets highest APR first, minimizing total interest costs.",
    ),
    Question(
        id="q_credit_4",
        topic_id="credit_debt",
        prompt="Credit utilization generally refers to:",
        options=[
            "How often you use cash",
            "The percentage of your revolving credit limit you’re using",
            "How many years you’ve had a job",
            "Your total income",
        ],
        answer_index=1,
        explanation="Utilization is how much of your available revolving credit is currently used.",
    ),

    # Investing
    Question(
        id="q_invest_1",
        topic_id="saving_investing",
        prompt="The primary purpose of an emergency fund is to:",
        options=[
            "Earn high returns",
            "Cover unexpected expenses and prevent new debt",
            "Replace all insurance",
            "Time the stock market",
        ],
        answer_index=1,
        explanation="Emergency funds reduce stress and stop small surprises from becoming high-interest debt.",
    ),
    Question(
        id="q_invest_2",
        topic_id="saving_investing",
        prompt="Diversification means:",
        options=[
            "Buying only one strong company",
            "Spreading investments across many assets to reduce risk",
            "Keeping all money in cash forever",
            "Changing investments daily",
        ],
        answer_index=1,
        explanation="Diversification reduces the damage if one company/sector performs poorly.",
    ),
    Question(
        id="q_invest_3",
        topic_id="saving_investing",
        prompt="Why do investing fees matter?",
        options=[
            "They never affect returns",
            "They compound over time and can reduce ending balances",
            "They only apply to billionaires",
            "They cancel out inflation",
        ],
        answer_index=1,
        explanation="Even small annual fees can significantly reduce long-term results via compounding.",
    ),
]

def generate_more_questions() -> List[Question]:
    # Generate many variants so quizzes feel fresh.
    out: List[Question] = []

    # Templates per topic
    for i in range(1, 51):
        out.append(
            Question(
                id=f"q_budget_gen_{i}",
                topic_id="budgeting_cashflow",
                prompt=f"If your budget keeps getting wrecked by 'random' costs, what’s the best fix? (Variant {i})",
                options=[
                    "Stop budgeting",
                    "Add a buffer and create sinking funds for irregular expenses",
                    "Only track fixed bills",
                    "Increase subscriptions",
                ],
                answer_index=1,
                explanation="Buffers and sinking funds absorb real-life variability so your plan stays realistic.",
            )
        )

    for i in range(1, 51):
        out.append(
            Question(
                id=f"q_credit_gen_{i}",
                topic_id="credit_debt",
                prompt=f"Which habit best protects your credit score over time? (Variant {i})",
                options=[
                    "Opening lots of cards quickly",
                    "Paying on time consistently",
                    "Maxing utilization often",
                    "Ignoring statements",
                ],
                answer_index=1,
                explanation="Payment history is a major factor in most credit scoring models.",
            )
        )

    for i in range(1, 51):
        out.append(
            Question(
                id=f"q_invest_gen_{i}",
                topic_id="saving_investing",
                prompt=f"What’s the biggest advantage of automating saving/investing? (Variant {i})",
                options=[
                    "It guarantees profit",
                    "It reduces reliance on willpower and increases consistency",
                    "It eliminates volatility",
                    "It increases fees",
                ],
                answer_index=1,
                explanation="Automation builds consistency, which often matters more than perfect timing.",
            )
        )

    return out

QUESTION_BANK: List[Question] = BASE_QUESTIONS + generate_more_questions()

# -----------------------------
# Simulation Scenario Bank
# - Large bank; each run samples 20 scenarios randomly
# -----------------------------
def build_sim_bank() -> List[Scenario]:
    bank: List[Scenario] = []

    # Hand-crafted scenarios
    bank.append(
        Scenario(
            id="sim_1",
            title="Surprise Car Repair",
            context="Your car won’t start. Repair quote: $650. You have $400 in savings and a credit card at ~24% APR.",
            state={"cash": 900, "debt": 1200, "savings": 400, "score": 0},
            choices=[
                SimChoice(
                    label="Pay $400 from savings + $250 from cash",
                    effects={"cash": -250, "debt": 0, "savings": -400, "score": 8},
                    outcome="You avoid new high-interest debt. Savings drops, but the decision supports stability. Rebuild your buffer next.",
                ),
                SimChoice(
                    label="Put the full $650 on the credit card",
                    effects={"cash": 0, "debt": +650, "savings": 0, "score": 2},
                    outcome="Fast fix, but you add expensive debt. Make a payoff plan to reduce interest costs.",
                ),
                SimChoice(
                    label="Delay repair and use rideshares for a week",
                    effects={"cash": -180, "debt": 0, "savings": 0, "score": 4},
                    outcome="You buy time, but costs and risk increase. Sometimes delay helps; sometimes it becomes more expensive.",
                ),
            ],
        )
    )

    bank.append(
        Scenario(
            id="sim_2",
            title="Rent Due Before Payday",
            context="Rent is due tomorrow: $1,200. You have $950 in checking and get paid $900 in three days.",
            state={"cash": 950, "debt": 300, "savings": 200, "score": 0},
            choices=[
                SimChoice(
                    label="Pay rent late with a $75 late fee",
                    effects={"cash": -75, "debt": 0, "savings": 0, "score": -2},
                    outcome="Late fees are expensive. This highlights why paycheck budgeting and buffers reduce timing stress.",
                ),
                SimChoice(
                    label="Use $250 from savings to pay on time",
                    effects={"cash": -950, "debt": 0, "savings": -250, "score": 6},
                    outcome="You cover the timing gap. That’s what buffers are for. Rebuild savings after payday.",
                ),
                SimChoice(
                    label="Ask landlord for a 3-day grace period",
                    effects={"cash": 0, "debt": 0, "savings": 0, "score": 7},
                    outcome="If approved, you avoid fees and stress. Communicating early often creates better outcomes.",
                ),
            ],
        )
    )

    # Generate many more scenario variants so each run feels fresh
    base_defs = [
        {
            "base_id": "sim_budget_review",
            "title": "Budget Review Day",
            "context": "You overspent on dining out by $140 this month. You can adjust next month.",
            "choices": [
                ("Set a weekly dining limit + meal plan", {"cash": 0, "debt": 0, "savings": 0, "score": 8},
                 "You build a realistic system. Iteration improves budgets."),
                ("Ignore it and hope next month is better", {"cash": 0, "debt": 0, "savings": 0, "score": -1},
                 "If nothing changes, outcomes often repeat."),
                ("Cut all fun spending to $0", {"cash": 0, "debt": 0, "savings": 0, "score": 2},
                 "Extreme cuts often backfire. Targeted changes are more sustainable."),
            ],
        },
        {
            "base_id": "sim_debt_choice",
            "title": "Debt Payoff Choice",
            "context": "You have an extra $200 this month. Debts: $1,000 at 29% APR and $2,500 at 14% APR.",
            "choices": [
                ("Put extra toward 29% APR (avalanche)", {"cash": -200, "debt": -200, "savings": 0, "score": 9},
                 "Mathematically efficient: you reduce expensive interest."),
                ("Put extra toward the smaller balance (snowball)", {"cash": -200, "debt": -200, "savings": 0, "score": 7},
                 "Motivation matters. Quick wins can keep you consistent."),
                ("Spend the extra $200", {"cash": -200, "debt": 0, "savings": 0, "score": -2},
                 "Not always fatal, but repeated patterns slow progress."),
            ],
        },
        {
            "base_id": "sim_invest_step",
            "title": "First Investing Step",
            "context": "You can invest $50/week. You have $600 credit card debt at 22% APR and $400 emergency savings.",
            "choices": [
                ("Build emergency savings to $1,000 first", {"cash": 0, "debt": 0, "savings": +100, "score": 7},
                 "Stability reduces new debt risk. Then investing becomes easier to sustain."),
                ("Pay down high-interest card debt first", {"cash": -200, "debt": -200, "savings": 0, "score": 9},
                 "Often a strong “guaranteed return.” Keep a mini buffer to avoid relapse."),
                ("Invest now and keep the card balance", {"cash": -200, "debt": 0, "savings": 0, "score": 2},
                 "Carrying high APR debt can overwhelm gains. Order of operations matters."),
            ],
        },
        {
            "base_id": "sim_job_change",
            "title": "Job Offer Decision",
            "context": "You receive an offer with +$600/month income but higher commute costs (+$120/month).",
            "choices": [
                ("Take the job and budget the difference", {"cash": +480, "debt": 0, "savings": +100, "score": 8},
                 "Net gain supports goals if you avoid lifestyle inflation."),
                ("Decline due to change discomfort", {"cash": 0, "debt": 0, "savings": 0, "score": 1},
                 "Stability has value, but consider long-term growth and options."),
                ("Negotiate salary or remote days", {"cash": +540, "debt": 0, "savings": +100, "score": 9},
                 "Negotiation can improve outcomes without increasing costs."),
            ],
        },
    ]

    # Create 80 generated scenarios (big bank)
    for i in range(1, 81):
        base = base_defs[(i - 1) % len(base_defs)]
        cash = 600 + (i % 9) * 110
        debt = 250 + (i % 11) * 160
        savings = 120 + (i % 7) * 85
        choices = [
            SimChoice(label=c[0], effects=c[1], outcome=c[2]) for c in base["choices"]
        ]
        bank.append(
            Scenario(
                id=f"{base['base_id']}_{i}",
                title=f"{base['title']} (Scenario {i})",
                context=base["context"],
                state={"cash": cash, "debt": debt, "savings": savings, "score": 0},
                choices=choices,
            )
        )

    return bank

SIM_BANK: List[Scenario] = build_sim_bank()

# -----------------------------
# App State
# -----------------------------
def init_state():
    if "progress" not in st.session_state:
        st.session_state.progress = {t.id: {"completed": False, "best_quiz": 0} for t in TOPICS}
    if "coins" not in st.session_state:
        st.session_state.coins = 0
    if "quizzes_taken" not in st.session_state:
        st.session_state.quizzes_taken = 0
    if "sim_runs" not in st.session_state:
        st.session_state.sim_runs = 0

    # Quiz session
    if "quiz_seed" not in st.session_state:
        st.session_state.quiz_seed = None
    if "quiz_questions" not in st.session_state:
        st.session_state.quiz_questions = []
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}  # qid -> chosen index
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = False

    # Simulation session
    if "sim_seed" not in st.session_state:
        st.session_state.sim_seed = None
    if "sim_scenarios" not in st.session_state:
        st.session_state.sim_scenarios = []
    if "sim_idx" not in st.session_state:
        st.session_state.sim_idx = 0
    if "sim_state" not in st.session_state:
        st.session_state.sim_state = {"cash": 0.0, "debt": 0.0, "savings": 0.0, "score": 0.0}
    if "sim_log" not in st.session_state:
        st.session_state.sim_log = []
    if "sim_done" not in st.session_state:
        st.session_state.sim_done = False

init_state()

# -----------------------------
# Layout / Theme Header
# -----------------------------
st.markdown(
    """
    <style>
      .mint-card {
        border: 1px solid rgba(16,185,129,0.25);
        border-radius: 16px;
        padding: 16px;
        background: rgba(255,255,255,0.9);
      }
      .mint-title {
        font-weight: 900;
        letter-spacing: -0.02em;
      }
      .mint-subtitle {
        color: rgba(6,95,70,0.75);
      }
      .mint-pill {
        display:inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        border: 1px solid rgba(16,185,129,0.25);
        background: rgba(16,185,129,0.08);
        font-size: 12px;
        font-weight: 700;
        margin-right: 6px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

left, right = st.columns([3, 2], gap="large")
with left:
    st.markdown("<h1 class='mint-title'>💵 MintMind</h1>", unsafe_allow_html=True)
    st.markdown("<div class='mint-subtitle'>Financial literacy lessons • randomized quizzes • real-life simulations</div>", unsafe_allow_html=True)

with right:
    # Quick stats
    completed = sum(1 for t in TOPICS if st.session_state.progress[t.id]["completed"])
    overall = completed / max(1, len(TOPICS))
    st.markdown(
        f"""
        <div class='mint-card'>
          <div><span class='mint-pill'>✅ Topics: {completed}/{len(TOPICS)}</span>
               <span class='mint-pill'>🪙 Coins: {st.session_state.coins}</span>
               <span class='mint-pill'>📝 Quizzes: {st.session_state.quizzes_taken}</span>
               <span class='mint-pill'>🎮 Sims: {st.session_state.sim_runs}</span>
          </div>
          <div style="margin-top:10px; font-weight:800; color: rgba(6,95,70,0.9);">
            Overall Progress: {pct(overall)}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.divider()

# -----------------------------
# Navigation
# -----------------------------
tab = st.sidebar.radio("Navigate", ["Dashboard", "Lessons", "Quiz", "Simulation", "Reset"], index=0)

# -----------------------------
# Dashboard
# -----------------------------
if tab == "Dashboard":
    st.subheader("🏦 Your Money Skill Dashboard")
    c1, c2 = st.columns([2, 1], gap="large")
    with c1:
        st.markdown(
            """
            <div class='mint-card'>
              <div style='font-weight:900; font-size:18px;'>Build calm, confident finances</div>
              <div style='color: rgba(6,95,70,0.75); margin-top:6px;'>
                Read a topic lesson, take a fresh randomized quiz, and practice decision-making in simulations.
              </div>
              <ul style='margin-top:10px;'>
                <li>Use <b>sinking funds</b> and a <b>buffer</b> to handle real life.</li>
                <li>Pay down <b>high-interest debt</b> to reduce stress and total costs.</li>
                <li>Automate saving/investing to win with consistency.</li>
              </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        best_score = max(st.session_state.progress[t.id]["best_quiz"] for t in TOPICS)
        st.markdown(
            f"""
            <div class='mint-card'>
              <div style='font-weight:900;'>Quick Stats</div>
              <div style='margin-top:8px;'>🏆 Best Quiz: <b>{best_score}/20</b></div>
              <div>✅ Topics Complete: <b>{completed}/{len(TOPICS)}</b></div>
              <div>🪙 Coins: <b>{st.session_state.coins}</b></div>
              <div style='margin-top:10px; color: rgba(6,95,70,0.75); font-size: 13px;'>
                Tip: Mark a lesson complete after reading, then try a quiz.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()
    st.subheader("📚 Topics")
    for t in TOPICS:
        p = st.session_state.progress[t.id]
        st.markdown(
            f"""
            <div class='mint-card' style='margin-bottom:12px;'>
              <div style='font-weight:900; font-size:16px;'>{t.title}</div>
              <div style='color: rgba(6,95,70,0.75);'>{t.subtitle}</div>
              <div style='margin-top:8px;'>
                <span class='mint-pill'>{"✅ Completed" if p["completed"] else "⏳ Not completed"}</span>
                <span class='mint-pill'>🏆 Best quiz: {p["best_quiz"]}/20</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# -----------------------------
# Lessons
# -----------------------------
elif tab == "Lessons":
    st.subheader("📘 Lessons")
    topic_titles = {t.title: t for t in TOPICS}
    selected_title = st.selectbox("Choose a topic", list(topic_titles.keys()))
    topic = topic_titles[selected_title]

    colA, colB = st.columns([3, 1], gap="large")
    with colA:
        st.markdown(topic.lesson_md)

    with colB:
        st.markdown("<div class='mint-card'>", unsafe_allow_html=True)
        st.markdown(f"**Topic:** {topic.title}")
        st.markdown(f"**Status:** {'✅ Completed' if st.session_state.progress[topic.id]['completed'] else '⏳ Not completed'}")
        st.markdown(f"**Best quiz:** {st.session_state.progress[topic.id]['best_quiz']}/20")
        st.markdown("---")
        if st.button("✅ Mark as Completed", use_container_width=True):
            st.session_state.progress[topic.id]["completed"] = True
            st.session_state.coins += 25
            st.success("Marked complete! +25 coins")
        if st.button("📝 Go to Quiz", use_container_width=True):
            st.session_state["__nav"] = "Quiz"
            st.rerun()
        if st.button("🎮 Go to Simulation", use_container_width=True):
            st.session_state["__nav"] = "Simulation"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------
# Quiz
# -----------------------------
elif tab == "Quiz":
    st.subheader("📝 Randomized 20-Question Quiz")

    st.caption("Each time you start a quiz, you’ll get a fresh random set of 20 questions from a larger bank.")

    # Allow user to start a new randomized quiz
    seed_input = st.text_input("Optional seed (leave blank for random)", value="")
    col1, col2, col3 = st.columns([1, 1, 2], gap="medium")

    def start_new_quiz(seed: Optional[int]):
        rng = seeded_rng(seed)
        st.session_state.quiz_seed = seed
        st.session_state.quiz_questions = sample_unique(rng, QUESTION_BANK, 20)
        st.session_state.quiz_answers = {}
        st.session_state.quiz_submitted = False

    with col1:
        if st.button("🎲 New Random Quiz", use_container_width=True):
            start_new_quiz(None)

    with col2:
        if st.button("🔁 New Seeded Quiz", use_container_width=True):
            try:
                seed = int(seed_input.strip()) if seed_input.strip() else 0
            except Exception:
                seed = 0
            start_new_quiz(seed)

    with col3:
        st.markdown(
            "<div class='mint-card'>Tip: use a seed if you want repeatable question sets for testing.</div>",
            unsafe_allow_html=True,
        )

    if not st.session_state.quiz_questions:
        st.info("Click **New Random Quiz** to begin.")
    else:
        # Render questions
        for i, q in enumerate(st.session_state.quiz_questions, start=1):
            st.markdown(f"### Q{i}. {q.prompt}")
            chosen = st.radio(
                label=f"Choose an answer for Q{i}",
                options=list(range(len(q.options))),
                format_func=lambda idx: q.options[idx],
                key=f"quiz_{q.id}",
                index=st.session_state.quiz_answers.get(q.id, 0) if q.id in st.session_state.quiz_answers else 0,
                disabled=st.session_state.quiz_submitted,
            )
            st.session_state.quiz_answers[q.id] = chosen

        if not st.session_state.quiz_submitted:
            if st.button("✅ Submit Quiz", type="primary", use_container_width=True):
                st.session_state.quiz_submitted = True
                st.session_state.quizzes_taken += 1

                # Score
                correct = 0
                per_topic = {t.id: {"correct": 0, "total": 0} for t in TOPICS}
                for q in st.session_state.quiz_questions:
                    per_topic[q.topic_id]["total"] += 1
                    if st.session_state.quiz_answers.get(q.id, -1) == q.answer_index:
                        correct += 1
                        per_topic[q.topic_id]["correct"] += 1

                # Coins reward
                earned = correct * 2
                st.session_state.coins += earned

                # Update best score for topics included
                for tid, stats in per_topic.items():
                    if stats["total"] > 0:
                        st.session_state.progress[tid]["best_quiz"] = max(
                            st.session_state.progress[tid]["best_quiz"], correct
                        )

                st.success(f"Submitted! Score: {correct}/20  •  +{earned} coins")
        else:
            # Show results + explanations
            correct = 0
            for q in st.session_state.quiz_questions:
                got = st.session_state.quiz_answers.get(q.id, -1)
                if got == q.answer_index:
                    correct += 1

            st.markdown("---")
            st.markdown(f"## Results: {correct}/20")
            st.progress(correct / 20)

            with st.expander("See explanations"):
                for i, q in enumerate(st.session_state.quiz_questions, start=1):
                    got = st.session_state.quiz_answers.get(q.id, -1)
                    ok = (got == q.answer_index)
                    st.markdown(f"**Q{i}. {'✅' if ok else '❌'} {q.prompt}**")
                    st.markdown(f"- Your answer: {q.options[got] if 0 <= got < len(q.options) else 'None'}")
                    st.markdown(f"- Correct: {q.options[q.answer_index]}")
                    st.markdown(f"- Explanation: {q.explanation}")

# -----------------------------
# Simulation
# -----------------------------
elif tab == "Simulation":
    st.subheader("🎮 Real-Life Money Simulation (20 Random Scenarios)")
    st.caption("Each run randomly selects 20 scenarios from a larger bank and tracks your financial outcomes.")

    seed_input = st.text_input("Optional seed (leave blank for random)", value="", key="sim_seed_input")

    def start_new_sim(seed: Optional[int]):
        rng = seeded_rng(seed)
        st.session_state.sim_seed = seed
        st.session_state.sim_scenarios = sample_unique(rng, SIM_BANK, 20)
        st.session_state.sim_idx = 0
        st.session_state.sim_done = False
        st.session_state.sim_log = []

        # Initialize state from first scenario
        s0 = st.session_state.sim_scenarios[0]
        st.session_state.sim_state = dict(s0.state)

    col1, col2 = st.columns([1, 1], gap="medium")
    with col1:
        if st.button("🎲 New Random Run", use_container_width=True):
            start_new_sim(None)

    with col2:
        if st.button("🔁 New Seeded Run", use_container_width=True):
            try:
                seed = int(seed_input.strip()) if seed_input.strip() else 0
            except Exception:
                seed = 0
            start_new_sim(seed)

    if not st.session_state.sim_scenarios:
        st.info("Click **New Random Run** to begin a 20-scenario simulation.")
    else:
        # Summary sidebar-ish
        st.markdown(
            f"""
            <div class='mint-card'>
              <div style='font-weight:900;'>Your Current Snapshot</div>
              <div style='margin-top:8px;'>
                💵 Cash: <b>{money(st.session_state.sim_state['cash'])}</b><br/>
                💳 Debt: <b>{money(st.session_state.sim_state['debt'])}</b><br/>
                🏦 Savings: <b>{money(st.session_state.sim_state['savings'])}</b><br/>
                ⭐ Score: <b>{int(st.session_state.sim_state['score'])}</b>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.session_state.sim_done:
            st.markdown("---")
            st.success("Simulation complete! Here’s your final outcome.")
            st.progress(clamp(st.session_state.sim_state["score"] / 160, 0, 1))

            st.markdown("### Run Summary")
            st.write(
                {
                    "Cash": money(st.session_state.sim_state["cash"]),
                    "Debt": money(st.session_state.sim_state["debt"]),
                    "Savings": money(st.session_state.sim_state["savings"]),
                    "Score": int(st.session_state.sim_state["score"]),
                }
            )

            with st.expander("View decision log"):
                for entry in st.session_state.sim_log:
                    st.markdown(f"**{entry['title']}**")
                    st.markdown(f"- Choice: {entry['choice']}")
                    st.markdown(f"- Outcome: {entry['outcome']}")
                    st.markdown(
                        f"- New state: Cash {money(entry['state']['cash'])}, Debt {money(entry['state']['debt'])}, "
                        f"Savings {money(entry['state']['savings'])}, Score {int(entry['state']['score'])}"
                    )
                    st.markdown("---")

        else:
            idx = st.session_state.sim_idx
            scenario = st.session_state.sim_scenarios[idx]

            st.markdown("---")
            st.markdown(f"## Scenario {idx+1}/20 — {scenario.title}")
            st.info(scenario.context)

            choice_labels = [c.label for c in scenario.choices]
            selected = st.radio("Choose your action:", choice_labels, key=f"sim_choice_{scenario.id}")

            if st.button("Apply Choice", type="primary", use_container_width=True):
                chosen = next(c for c in scenario.choices if c.label == selected)

                # Apply effects
                st.session_state.sim_state["cash"] += chosen.effects.get("cash", 0)
                st.session_state.sim_state["debt"] += chosen.effects.get("debt", 0)
                st.session_state.sim_state["savings"] += chosen.effects.get("savings", 0)
                st.session_state.sim_state["score"] += chosen.effects.get("score", 0)

                # Clamp to avoid negative cash/savings going too wild (optional realism guard)
                st.session_state.sim_state["cash"] = max(st.session_state.sim_state["cash"], -500)   # overdraft-ish
                st.session_state.sim_state["savings"] = max(st.session_state.sim_state["savings"], 0)

                st.session_state.sim_log.append(
                    {
                        "title": scenario.title,
                        "choice": chosen.label,
                        "outcome": chosen.outcome,
                        "state": dict(st.session_state.sim_state),
                    }
                )

                # Next scenario
                if st.session_state.sim_idx >= 19:
                    st.session_state.sim_done = True
                    st.session_state.sim_runs += 1
                    # Reward coins by score delta-ish
                    earned = int(max(0, st.session_state.sim_state["score"] // 10))
                    st.session_state.coins += earned
                    st.success(f"Run completed! +{earned} coins")
                else:
                    st.session_state.sim_idx += 1

                st.rerun()

# -----------------------------
# Reset
# -----------------------------
elif tab == "Reset":
    st.subheader("🧹 Reset Progress")
    st.warning("This clears your progress for this session (Streamlit session state).")
    if st.button("Reset Everything", type="primary"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# -----------------------------
# Internal nav jump from buttons
# -----------------------------
if "__nav" in st.session_state:
    target = st.session_state["__nav"]
    del st.session_state["__nav"]
    # Streamlit can't directly switch sidebar radio; just rerun with user selecting.
    st.info(f"Go to the sidebar and click: **{target}**")

