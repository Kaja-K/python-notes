# Python for Data Analytics — Theory Notes

---

## Python Basics

**Why Python for data analytics?** Python is the dominant language in data science because of its readable syntax, massive ecosystem of libraries (pandas, numpy, sklearn, matplotlib), and strong community. It sits between the ease of Excel and the power of custom software.

**Interpreted vs compiled** — Python is interpreted, meaning code runs line by line without a separate compilation step. This makes development fast but execution slower than compiled languages like C. For data work this is usually fine because heavy computation is delegated to libraries written in C under the hood (numpy, pandas).

**Mutable vs immutable** — Mutable objects can be changed after creation (lists, dicts, sets). Immutable objects cannot (strings, tuples, numbers). This matters because when you pass a mutable object to a function, the function can modify the original. Immutable objects are safe to share without risk of accidental modification.

**Dynamic typing** — Python infers the type of a variable at runtime. You don't declare types. The same variable can hold an integer, then a string, then a list. This flexibility can cause bugs — type hints are a way to add optional clarity without enforcement.

---

## Data Structures

**List** is an ordered, mutable sequence. You can add, remove, or change elements. Indexing starts at 0. Lists allow duplicates and mixed types, though mixing types is usually a sign of messy data.

**Tuple** is an ordered, immutable sequence. Once created it cannot be changed. Use tuples when the data should not change — coordinates, RGB values, database records returned from a query. Tuples are slightly faster than lists.

**Dictionary** stores key-value pairs. Keys must be unique and immutable (strings, numbers, tuples). Lookup by key is O(1) — extremely fast regardless of size. Since Python 3.7 dictionaries preserve insertion order.

**Set** is an unordered collection of unique values. Automatically removes duplicates. Very fast membership checks. Use sets when you only care about existence, not order or count.

**Comprehensions** are a Pythonic way to build lists, dicts, or sets in one line. They are faster than equivalent for loops because they avoid attribute lookups per iteration. They should stay readable — if a comprehension needs three conditions and a nested loop, a regular for loop is clearer.

---

## Functions

**First-class functions** — In Python, functions are objects. You can assign them to variables, pass them as arguments, and return them from other functions. This enables functional patterns like `map`, `filter`, and custom sorting with `key=`.

**Lambda** is an anonymous one-liner function. It is syntactic sugar for a simple function you only need once, usually as an argument to `sorted`, `map`, or `filter`. For anything with more than one expression, a named function is clearer.

**`*args` and `**kwargs`** let a function accept a variable number of arguments. `*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dictionary. They are useful for wrapper functions and flexible APIs.

**Default arguments** are evaluated once when the function is defined, not each time it is called. The classic bug: using a mutable default like an empty list. Every call shares the same list object. Use `None` as the default and create the list inside the function.

**Scope and closures** — Python looks up names in the order: local → enclosing → global → built-in (LEGB). A closure is a function that captures variables from its enclosing scope even after that scope has finished executing.

**Decorators** are functions that wrap another function to add behaviour before or after it runs. `@timer` adds timing, `@retry` adds retry logic. They are applied with `@` syntax which is shorthand for `func = decorator(func)`.

---

## OOP

**Class** is a blueprint for creating objects. It bundles data (attributes) and behaviour (methods) together. `__init__` is the constructor — it runs when you create an instance.

**`__str__` vs `__repr__`** — `__str__` is the human-readable description, shown when you print an object. `__repr__` is the unambiguous developer-friendly representation, shown in the interpreter. If only one is defined, Python falls back to `__repr__`.

**Inheritance** lets a child class inherit attributes and methods from a parent. The child can override parent methods or extend them using `super()`. This avoids duplicating code across similar classes.

**Encapsulation** — convention in Python is to prefix private attributes with `_` (one underscore = "don't touch unless you know what you're doing") or `__` (two underscores = name mangling, harder to access accidentally). Python does not enforce access control the way Java does.

**`@property`** lets you define a method that behaves like an attribute. You access it without parentheses. It is used to add validation or computation when getting or setting a value, without changing the public interface.

**`@classmethod`** receives the class itself as the first argument (by convention `cls`). Used for alternative constructors — for example, `Station.from_dict(data)`.

**`@staticmethod`** receives no implicit first argument. A utility function that logically belongs to the class but doesn't need access to instance or class state.

**Dataclass** (`@dataclass` decorator) automatically generates `__init__`, `__repr__`, and `__eq__` from the class attributes. Less boilerplate for classes whose main purpose is to hold data.

---

## NumPy

**Why NumPy over Python lists?** NumPy arrays store data in contiguous memory blocks of a single type, which allows vectorized operations — the same operation applied to all elements simultaneously in C-speed loops. Python lists store pointers to objects scattered in memory, which is slow to iterate.

**Vectorization** means applying operations to entire arrays without writing Python loops. `arr * 2` doubles every element. This is not just syntactic convenience — it is genuinely faster because the loop runs in compiled C, not interpreted Python.

**Broadcasting** is NumPy's mechanism for performing operations between arrays of different shapes. A 1D array of shape (3,) can be added to a 2D array of shape (4, 3) because NumPy stretches the smaller array along the missing dimension. The rule: dimensions are compatible if they are equal or one of them is 1.

**Array vs matrix** — NumPy's ndarray is the general purpose array. `*` is element-wise multiplication. `@` or `np.dot` is matrix multiplication. This distinction is important — many bugs come from accidentally using `*` when matrix multiplication was intended.

**Fancy indexing** — NumPy arrays can be indexed with boolean arrays or integer arrays, not just slices. `arr[arr > 5]` returns all elements greater than 5. This is used constantly in data filtering.

**Axis** — operations like `sum`, `mean`, `max` take an `axis` argument. `axis=0` collapses rows (operates column-wise). `axis=1` collapses columns (operates row-wise). A common source of confusion — think of axis as "the dimension that disappears after the operation".

---

## Pandas

**DataFrame vs Series** — A DataFrame is a 2D table with labelled rows and columns. A Series is a 1D labelled array — essentially one column of a DataFrame. Most DataFrame operations return a new DataFrame or Series, leaving the original unchanged unless `inplace=True` is used.

**`loc` vs `iloc`** — `loc` uses label-based indexing — you refer to rows and columns by name. `iloc` uses integer position-based indexing — you refer by position (0, 1, 2). The key difference is that `loc` is inclusive on both ends of a slice, while `iloc` is exclusive on the end like regular Python slices.

**Index** — The index is the row label of a DataFrame. By default it is 0, 1, 2... but it can be set to any column. Operations like `join` and `merge` use the index. A well-chosen index speeds up lookups. After filtering or sorting, always consider `reset_index(drop=True)` to get a clean sequential index.

**`groupby` — Split-Apply-Combine** — The groupby operation has three conceptual phases. First it splits the data into groups based on one or more columns. Then it applies an aggregation function (sum, mean, count, custom) to each group independently. Finally it combines the group results back into a single output. This pattern is the core of most analytical aggregations.

**`merge` vs `join` vs `concat`** — `merge` is the most flexible — it does SQL-style joins on columns. `join` is a shorthand for merging on the index. `concat` stacks DataFrames vertically (more rows) or horizontally (more columns), no key matching.

**`apply`** runs a function on each row or column. It is flexible but slow — it calls Python for every row. For numeric operations, prefer built-in vectorized methods like `sum()`, `mean()`, or numpy ufuncs. Use `apply` when you need custom logic that can't be vectorized.

**`transform`** is like `apply` but returns a result with the same shape as the input. Used inside groupby to add a group-level statistic as a new column without collapsing rows — for example, adding the group mean next to each individual value.

**`pivot_table`** is the DataFrame equivalent of an Excel pivot table. It reshapes data by grouping on row and column dimensions and applying an aggregation. It is essentially a grouped aggregation presented as a 2D matrix.

**Copy vs view** — When you slice a DataFrame, pandas may return a view (same memory) or a copy (new memory). Modifying a view modifies the original. The `SettingWithCopyWarning` is pandas warning you that you might be modifying a copy when you expected to modify the original. The safe solution is `df.copy()` or using `.loc` for assignment.

**`inplace=True`** modifies the object directly and returns None. Without it, most operations return a new object. The general advice is to avoid `inplace=True` in complex pipelines because it makes code harder to chain and debug.

---

## Data Cleaning

**Missing values** — NaN (Not a Number) is pandas' representation of missing data. Always check `df.isnull().sum()` early to understand the scale of the problem before deciding how to handle it.

The decision of how to handle missing values depends on the context. Dropping rows makes sense when very few rows have NaN and the data is not time-ordered. Imputing with mean or median works when the missing values are random and the distribution is stable. Forward fill or backward fill is appropriate for time series where the previous value is the best estimate of the missing one. Imputing with a constant ('Unknown', 0) makes sense for categorical columns where NaN has a specific meaning.

Always check what percentage of a column is missing before choosing a method. A column that is 80% missing is rarely worth keeping.

**Outliers** — Values far from the rest of the distribution. Common detection methods are the z-score (flag values more than 3 standard deviations from the mean) and the IQR method (flag values below Q1 − 1.5×IQR or above Q3 + 1.5×IQR). The IQR method is more robust because it is not affected by the outliers themselves.

What to do with outliers depends on context. Sometimes they are data errors (cap or remove them). Sometimes they are the most interesting data points (keep them, investigate them).

**Data types** — Wrong data types waste memory and cause incorrect calculations. A column of numbers stored as strings cannot be summed. Dates stored as strings cannot be compared. Categories stored as plain strings use far more memory than the pandas `category` dtype. Always check `df.dtypes` early.

**Duplicates** — Exact duplicate rows almost always indicate a data pipeline error. Use `df.duplicated().sum()` to detect them and `df.drop_duplicates()` to remove them. Be specific about which columns define a duplicate — sometimes you want to deduplicate on a subset of columns.

---

## Statistics for Data Analysis

**Mean** is the arithmetic average. Sensitive to outliers — one extreme value pulls it significantly. Best used when the distribution is roughly symmetric.

**Median** is the middle value when data is sorted. Robust to outliers. Better than mean for skewed distributions like income or house prices.

**Mode** is the most frequent value. Most useful for categorical data.

**Standard deviation** measures the average spread of values around the mean. Low std = values are clustered close to the mean. High std = values are spread out. It is in the same units as the original data.

**Variance** is standard deviation squared. Used more in mathematical formulas than in interpretation.

**Skewness** measures asymmetry of a distribution. Positive skew = long right tail (most values are low, a few are very high — typical for income). Negative skew = long left tail. A roughly symmetric distribution has skewness near zero.

**Kurtosis** measures the heaviness of the tails. High kurtosis means more extreme outliers than a normal distribution would produce.

**Correlation** measures the linear relationship between two variables. Ranges from -1 (perfect negative) to 0 (no linear relationship) to +1 (perfect positive). Correlation does not imply causation. Two variables can be correlated because they are both caused by a third variable.

**Pearson correlation** assumes a linear relationship and normally distributed data. **Spearman correlation** works on ranks and captures monotonic (not just linear) relationships — more robust for non-normal data.

**p-value** is the probability of observing data at least as extreme as the actual data, assuming the null hypothesis is true. A p-value below 0.05 is the conventional threshold for calling a result statistically significant. It does not measure the size or importance of an effect — only whether it is unlikely to be due to chance.

**Confidence interval** gives a range of plausible values for a population parameter. A 95% confidence interval means that if you repeated the study 100 times, about 95 of the resulting intervals would contain the true value.

---

## Machine Learning Concepts

**Supervised vs unsupervised learning** — In supervised learning, the model learns from labelled examples — each input has a known correct output (classification, regression). In unsupervised learning, there are no labels — the model finds structure in the data on its own (clustering, dimensionality reduction).

**Classification vs regression** — Classification predicts a category (spam or not spam, which species). Regression predicts a continuous number (price, temperature, sales).

**Overfitting** means the model has memorised the training data, including its noise, and performs poorly on new data. Signs: very high training accuracy, much lower test accuracy. Solutions: more data, regularisation, simpler model, cross-validation.

**Underfitting** means the model is too simple to capture the patterns in the data. Signs: poor performance on both training and test data. Solutions: more complex model, more features, more training.

**Bias-variance tradeoff** — Bias is the error from wrong assumptions (underfitting — model too simple). Variance is the error from sensitivity to small fluctuations in training data (overfitting — model too complex). Reducing one tends to increase the other. The goal is to find the right balance.

**Train / validation / test split** — Training data is used to fit the model. Validation data is used to tune hyperparameters and select the best model. Test data is held out until the very end to give an unbiased estimate of final performance. The test set must never influence any modelling decision — it simulates unseen real-world data.

**Cross-validation** — Instead of a single train/test split, the data is split into k folds. The model is trained k times, each time using a different fold as the test set. The average performance across folds is a more reliable estimate than a single split. Standard choice is k=5 or k=10.

**Feature engineering** is creating new input features from raw data to help the model learn better. Examples: extracting the hour from a datetime, creating a ratio of two columns, one-hot encoding a categorical variable. Often more impactful than choosing a better algorithm.

**Regularisation** penalises model complexity to prevent overfitting. Ridge (L2) shrinks coefficients toward zero. Lasso (L1) can shrink some coefficients to exactly zero, performing implicit feature selection. ElasticNet combines both.

**Scaling** — Many algorithms (SVM, KNN, neural networks, gradient descent) are sensitive to the scale of features. A column ranging from 0 to 1 and a column ranging from 0 to 1,000,000 give the second column disproportionate influence. StandardScaler (mean=0, std=1) and MinMaxScaler (0 to 1) are the most common solutions. Tree-based models (Random Forest, Gradient Boosting) are scale-invariant.

---

## Model Evaluation

**Accuracy** is the fraction of correct predictions. Misleading on imbalanced datasets — a model that always predicts the majority class can have 95% accuracy on a 95/5 split while being completely useless.

**Precision** is the fraction of positive predictions that were actually positive. Optimise precision when false positives are costly — for example, flagging innocent transactions as fraud.

**Recall (Sensitivity)** is the fraction of actual positives that were correctly predicted. Optimise recall when false negatives are costly — for example, missing a cancer diagnosis.

**F1 score** is the harmonic mean of precision and recall. A balanced metric when both false positives and false negatives matter.

**ROC-AUC** measures how well a classifier separates the two classes across all possible thresholds. 1.0 is perfect, 0.5 is no better than random. Useful for comparing models regardless of threshold.

**MAE (Mean Absolute Error)** is the average absolute difference between predicted and actual values. In the same units as the target. Robust to outliers.

**RMSE (Root Mean Squared Error)** penalises large errors more than MAE because it squares them first. More sensitive to outliers. Also in the same units as the target.

**R² (R-squared)** measures what fraction of the variance in the target is explained by the model. 1.0 is perfect, 0 is no better than predicting the mean, negative means worse than predicting the mean.

---

## Handling Large Datasets

Loading the entire dataset into memory is sometimes not possible. The main strategies are:

Loading in chunks with `read_csv(chunksize=...)` processes the file in pieces, applying operations to each chunk separately. Useful for aggregations that can be accumulated incrementally.

Converting data types before loading reduces memory. Reading floats as float32 instead of float64 halves their memory footprint. Converting repeated string columns to the `category` dtype can reduce memory by 10x or more.

Using `dask` provides a pandas-like API that operates on data larger than RAM by splitting operations into a task graph executed lazily. `modin` is another drop-in pandas replacement with parallel execution.

Parquet format is far more efficient than CSV for large datasets — it is columnar (reads only the columns you need), compressed, and preserves data types exactly.

---

## Common Topics

**loc vs iloc** — `loc` is label-based, `iloc` is position-based. `loc` is inclusive on both ends of a slice. `iloc` is exclusive on the end.

**groupby mechanics** — Split-Apply-Combine. Split the data into groups, apply an aggregation or transformation to each group independently, combine the results. Transform keeps the original shape (useful for adding group statistics as columns).

**merge types** — inner (only matches), left (all left), right (all right), outer (all rows from both). These are identical to SQL join types.

**handling missing values** — check percentage first, then decide: drop if few, impute with mean/median/mode for numeric, forward/backward fill for time series, constant fill for categorical.

**scaling when and why** — needed for distance-based algorithms (KNN, SVM, k-means) and gradient descent. Not needed for tree-based models.

**NumPy advantages over lists** — contiguous memory, single data type per array, vectorized C-speed operations, broadcasting, less memory per element.

**copy vs view in pandas** — a view shares memory with the original, a copy is independent. Modifying a view modifies the original. Use `.copy()` or `.loc` assignment to be safe.

**what is broadcasting** — NumPy's ability to perform arithmetic between arrays of different but compatible shapes, by implicitly expanding the smaller array along the matching dimensions without copying data.

**overfitting vs underfitting** — overfitting is too complex (memorises noise), underfitting is too simple (misses patterns). The bias-variance tradeoff is the fundamental tension between the two.
