import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.ticker as mtick

def set_ROI_table(llambda):

    mu = 0
    ROI_table = np.empty(129)

    for d in range(129):
        multiplier = llambda**d
    
        ROI_table[d] = multiplier
        if d == 0 or d == 128: 
            mu += multiplier/256
        else: 
            mu += multiplier/128

    ROI_table /= mu
    return(ROI_table)

def compute_profits(llambda, fee, seed):

    arr_profits = []
    arr_cumul_profits = []

    np.random.seed(seed)
    ROI_table = set_ROI_table(llambda)

    for day in range(ndays):
        collected_fees =  fee * v * nbets
        if day % 1000 == 0:
            print("seed: %4d day: %5d" % (seed, day)) 
        winner = np.random.randint(0, 256, nbets)
        guess  = np.random.randint(0, 256, nbets)
        delta = abs(winner - guess)
        d = np.minimum(delta, 256 - delta)
        d_unique, d_counts = np.unique(d, return_counts=True)
        d_nvals = len(d_unique)
        if d_nvals == 129: 
            profits = np.dot(d_counts, ROI_table) # fast computation
        else: 
            profits = 0
            for index in range(d_nvals):
                d_value = d_unique[index]
                profits += d_counts[index]*ROI_table[d_value]
        today_profit = collected_fees + v*nbets - v*profits
        arr_profits.append(today_profit)
        if day == 0:
            arr_cumul_profits.append(today_profit)
        else:
            yesterday_profit = arr_cumul_profits[day - 1]
            arr_cumul_profits.append(today_profit + yesterday_profit)

    return(arr_profits, arr_cumul_profits, ROI_table) 

#--- main part

ndays = 10000     # time period = ndays
nbets = 10000     # bets per day
v     = 20        # wager
llambda  = 0.30   # strictly between 0 and 1
transaction_fee = 0.005 
seed =  26  

arr_profits, arr_cumul_profits, ROI_table = compute_profits(llambda, 
    transaction_fee, seed)


#--- plot daily profit/loss distribution, and aggregated numbers over time

x = np.arange(ndays)
y = arr_cumul_profits

# custom tick functions

def currency_ticks_k(x, pos):
    x = int(x / 1000)  # plotted values will be in thousand $
    if x >= 0:
        return '${:,.0f}k'.format(x)
    else:
        return '-${:,.0f}k'.format(abs(x))

def currency_ticks_m(x, pos):
    x = int(x / 1000000)  # plotted values will be in million $
    if x >= 0:
        return '${:,.0f}m'.format(x)
    else:
        return '-${:,.0f}m'.format(abs(x))

mpl.rcParams['axes.linewidth'] = 0.5
mpl.rc('xtick', labelsize=8) 
mpl.rc('ytick', labelsize=8) 

fig, axes = plt.subplots(nrows = 1, ncols = 2, figsize =(8, 3))
axes[0].tick_params(axis='both', which='major', labelsize=8)
axes[0].tick_params(axis='both', which='minor', labelsize=8)

# plot: y axis in millions of dollars
tick_m = mtick.FuncFormatter(currency_ticks_m)
axes[0].yaxis.set_major_formatter(tick_m)
axes[0].plot(x, y, linewidth=0.3, c='tab:green')

# histogram: x axis in thousands of dollars
tick_k = mtick.FuncFormatter(currency_ticks_k)
axes[1].xaxis.set_major_formatter(tick_k) 
plt.locator_params(axis='both', nbins=4)
axes[1].hist(arr_profits, bins = 100,  linewidth = 0.5,edgecolor = "red",
            color = 'bisque', stacked=True) 
plt.show()


#--- print ROI table

print ("ROI Table:")
for d in range(129):
    print("%3d %8.4f" %(d, ROI_table[d]))
print("Maximum multiplier: ", ROI_table[0])
