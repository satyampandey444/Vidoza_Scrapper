from math import sqrt
# l=[sqrt(i ** 2) for i in range(10)]
from joblib import Parallel,delayed

import datetime
start_time=datetime.datetime.now()

def x(i):
    print('Hi',i)
# l=([i for i in range(1,int(10e8))])
# for i in range(1,11):
#     x(i)

Parallel(n_jobs=2)(delayed(x)(i) for i in range(1,int(10)))
#When we change the jobs more cores are used
end_time=datetime.datetime.now()

print(end_time-start_time,'Time Consumed')



