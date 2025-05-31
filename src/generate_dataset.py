import pandas as pd
import numpy as np
from datetime import datetime, date, timedelta


end_date = date.today()
start_date = end_date - timedelta(days=30)
days = pd.date_range(start=start_date, end=end_date, freq="D")
num_days = len(days)

rating_df = pd.DataFrame()
rating_df["customer_id"] = np.ones(num_days, dtype=int)
rating_df["date"] = days
rating_df["rating"] = np.random.randint(1400, 1700, size=num_days)

days_doubled = np.repeat(days, 2)
gram_vocab = np.tile(["grammar", "vocab"], len(days_doubled) // 2)

kpis_df = pd.DataFrame()
kpis_df["customer_id"] = np.ones(len(days_doubled), dtype=int)
kpis_df["date"] = days_doubled
kpis_df["label_1"] = gram_vocab
kpis_df["tasks_solved"] = np.random.randint(0, 20, size=len(days_doubled))
kpis_df["correct_answers"] = kpis_df["tasks_solved"].apply(
    lambda x: np.random.randint(0, x + 1) if x > 0 else 0
)
kpis_df["accuracy"] = kpis_df["correct_answers"] / kpis_df["tasks_solved"]
kpis_df["avg_time_sec"] = np.random.randint(5, 20, size=len(days_doubled))

num_tasks = 50
current_day = pd.date_range(start=start_date, freq="25s", periods=num_tasks)
last_day_stats = pd.DataFrame()
last_day_stats["customer_id"] = np.ones(num_tasks, dtype=int)
last_day_stats["date"] = current_day
last_day_stats["tasks_solved"] = np.random.randint(0, 2, size=num_tasks)
last_day_stats["label_1"] = np.random.choice(gram_vocab, size=num_tasks)
last_day_stats["rating"] = np.random.randint(1400, 1700, size=num_tasks)


rating_df.to_csv("../data/rating.csv", index=False)
kpis_df.to_csv("../data/kpis.csv", index=False)
last_day_stats.to_csv("../data/last_day_stats.csv", index=False)
