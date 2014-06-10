Advanced Retirement Calculator
=============================

Why make this?
-------

Traditional wisdom says that if you max your 401k and manage to get 7% returns per year you should be okay in retirement.
The real world is not like this. The stock market has ups and downs, and volatility can ruin performance.
I wanted to see how my portfolio would act with some more real world scenarios. I cannot find something online that treats this with any meaningful rigor.

What does it do differently?
------

The stock market is said to follow a geometric brownian motion with a positive return and some volatility. As a result, returns will be random.
We can simulate stock market data by using random data from a N(mu,sigma) distribution. 
Any option trader worth his salt knows that asset returns are not normal, but this is a much better approximation than assuming 7% smooth returns perpetuity.
This is important, because your life and retirement plan are path dependent. There could be situations where a higher average return is actually worse for your savings plan.
 

How do I use this?
------
Right now its a work in progress. I am going to put this into a django app as soon as I find the time and figure out all the details. Currently, I am working out bugs in the logic.
The idea will be to simulate 10000 paths of the stock market over any number of years and look at the distribution of your retirement portfolio.
You will then be able to plan with a certain confidence level.
Perhaps you're in good shape, but with what probability can you assume this is true?
Realistically, this model is only as good as the assumptions. The idea is to make fewer unrealistic assumptions.

Who are you?
------
I am johnnydiabetic. I am not a financial advisor, but I have worked in finance nearly a decade. This does not in any way make me qualified to give financial advice.
I'm not sure many financial advisors have great tools to plan around uncertainty. This is a shot at making a better one.