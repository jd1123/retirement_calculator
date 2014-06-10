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
We can simulate this by generating random data and having the returns be lognormally distributed.
Any option trader worth his salt knows that asset returns are not normal, but this is a much better approximation than assuming 7% smooth returns perpetuity.


How do I use this?
------
Right now its a work in progress. I am going to put this into a django app as soon as I find the time and figure out all the details. Right now I am working out bugs in the logic.


