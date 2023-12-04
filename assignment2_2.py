import requests
import json
import sqlite3
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm, ttest_ind

# Is the number of selling providers different on public holidays compared to normal days?

r = requests.get("https://date.nager.at/api/v3/PublicHolidays/2023/FI")
public_holidays_json = json.loads(r.content)
public_holidays = [pbl['date'] for pbl in public_holidays_json if "Public" in pbl['types']]

r = requests.get("https://date.nager.at/api/v3/PublicHolidays/2022/FI")
public_holidays_json = json.loads(r.content)
public_holidays.extend([pbl['date'] for pbl in public_holidays_json if "Public" in pbl['types']])

print(public_holidays)

with sqlite3.connect("./database/mock_resq.db") as conn:
    c = conn.cursor()
    c.execute(f" select COUNT(DISTINCT providerid) from orders group by strftime('%Y-%m-%d',createdat) having strftime('%Y-%m-%d',createdat) in {str(tuple(public_holidays))}")

    records = c.fetchall()
    holiday_providers = [record[0] for record in records]
    #for record in records:
        #print(record)

    c = conn.cursor()
    c.execute(f" select COUNT(DISTINCT providerid) from orders group by strftime('%Y-%m-%d',createdat) having strftime('%Y-%m-%d',createdat) NOT in {str(tuple(public_holidays))}")

    records = c.fetchall()
    non_holiday_providers = [record[0] for record in records]


res = ttest_ind(holiday_providers, non_holiday_providers, equal_var=False)

x1 = np.sort(holiday_providers)
y1 = np.arange(len(x1))/float(len(x1))
m = np.mean(holiday_providers)
s = np.std(holiday_providers)
y1n = np.array([norm.cdf(x,m,s) for x in x1])
x2 = np.sort(non_holiday_providers)
y2 = np.arange(len(x2))/float(len(x2))
m = np.mean(non_holiday_providers)
s = np.std(non_holiday_providers)
y2n = np.array([norm.cdf(x,m,s) for x in x2])
plt.plot(x1, y1, label="Holiday Providers CDF")
plt.plot(x1, y1n, label="Holiday Providers Normal Fit CDF")
plt.plot(x2,y2, label="Regular Day Providers CDF")
plt.plot(x2,y2n, label="Regular Day Providers Normal Fit CDF")
plt.title("Providers comparison between holidays and regular days")
plt.xlabel(f"Providers \n The distributions as well as the means are significantly different, the statistical test rejects equal means with p-value={res.pvalue}")
plt.legend(loc='best')
figManager = plt.get_current_fig_manager()
figManager.window.state('zoomed')
plt.show()

# As expected from visual inspection the p_value for the null hypothesis of equal means is extremely small, therefore we can say with great certainty that the means are different.