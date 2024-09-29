from datetime import datetime
from dateutil.relativedelta import relativedelta


today = datetime.today()
next_year = today + relativedelta(years=1)
print(next_year)

