## A Fast Fault Localization Approach Based on Block-Level Uncertainty Inference for Software Product Lines

Fault localization for software product lines (SPLs) is complex and difficult. 
Developing an algorithm that is both high-performing and efficient is challenging. 
In this paper, we propose an approach named FCFLA, which addresses the above challenge better than existing approaches.
For efficiency, a block-level buggy statement examination is being applied for the first time to the fault localization in SPLs. 
Due to the uncertainty in this examination process, uncertainty inference methods, i.e., Bayesian decision theory and Dempster-Shafer (D-S) evidence theory, are used to detect suspicious blocks. 
Further, to improve the performance of the algorithm, the suspicious statement ranking is comprehensively determined based on the suspiciousness of the block it belongs to and its suspiciousness based on the program spectrum.
Four state-of-the-art approaches (STOAs) are compared with FCFLA on six publicly available SPL systems. 
Experimental results indicate that our approach has a significant performance advantage. 
In the single-bug cases, FCFLA can rank the buggy statements to the top-1 positions in 41\% of the cases and to the top-4 position in 83\% of the cases. 
For efficiency, FCFLA runs 10-17 times faster than its competitors for small systems (with 8-13 features) and 661 times faster for a relatively large system with 27 features. 
In the multiple bugs, the buggy statements of the 12\% cases can be ranked to the top-1 positions by FCFLA, comparable to SOTAs.
In a nutshell, our approach is high-performing and efficient, providing a promising alternative for fault localization in SPLs.  

### Empirical results
1. Performance Comparison
    1. VarCop's performance compared to the state-of-the-art approaches 
        1. [By Rank and EXAM](https://github.com/ttrangnguyen/VARCOP/blob/gh-pages/experiment_results/Analysis/SINGLE_BUG/PERFORMANCE%20COMPARISON/performance_comparsion.xlsx)
        2. [By Hit@X](https://github.com/ttrangnguyen/VARCOP/blob/gh-pages/experiment_results/Analysis/SINGLE_BUG/PERFORMANCE%20COMPARISON/Hit%40X.xlsx)
    1. [VarCop's performance by Mutation Operators causing bugs](https://github.com/ttrangnguyen/VARCOP/blob/gh-pages/experiment_results/Analysis/SINGLE_BUG/PERFORMANCE%20COMPARISON/performance_mutation_operators.xlsx)
    1. [VarCop's performance by bugs' code elements](https://github.com/ttrangnguyen/VARCOP/blob/gh-pages/experiment_results/Analysis/SINGLE_BUG/PERFORMANCE%20COMPARISON/performance_code_elements.xlsx)
    1. [VarCop's performance by the number of involving features](https://github.com/ttrangnguyen/VARCOP/blob/gh-pages/experiment_results/Analysis/SINGLE_BUG/PERFORMANCE%20COMPARISON/performance_num_of_involving_features.xlsx)
1. Intrinsic Analysis
    1. [Impact of Suspicious Statement Isolation on performance](https://github.com/ttrangnguyen/VARCOP/blob/gh-pages/experiment_results/Analysis/SINGLE_BUG/INTRINSIC%20ANALYSIS/Suspicious_statements_isolation_impact.xlsx)
    1. [Impact of choosing Metric of Local Suspiciousness Measurement on performance](https://github.com/ttrangnguyen/VARCOP/blob/gh-pages/experiment_results/Analysis/SINGLE_BUG/PERFORMANCE%20COMPARISON/performance_comparsion.xlsx)
    1. [Impact of Normalization on performance](https://github.com/ttrangnguyen/VARCOP/blob/gh-pages/experiment_results/Analysis/SINGLE_BUG/INTRINSIC%20ANALYSIS/Normalization%20Impact.xlsx)
    1. [Impact of choosing Aggreation Function of Global Suspiciousness Measurement on performance](https://github.com/ttrangnguyen/VARCOP/blob/gh-pages/experiment_results/Analysis/SINGLE_BUG/INTRINSIC%20ANALYSIS/Aggreation_function_impact.xlsx)
    2. [Impact of choosing Combination Weight when combining Suspiciousness scores](https://github.com/ttrangnguyen/VARCOP/blob/gh-pages/experiment_results/Analysis/SINGLE_BUG/INTRINSIC%20ANALYSIS/Combination_weight_impact.xlsx)
1. Sensitivity Analysis
    1. [Impact of Sample Size on performance](https://github.com/ttrangnguyen/VARCOP/blob/gh-pages/experiment_results/Analysis/SINGLE_BUG/SENSITIVITY%20ANALYSIS/sample_size_impact.xlsx)
    1. [Impact of Test Suite's Size on performance](https://github.com/ttrangnguyen/VARCOP/blob/gh-pages/experiment_results/Analysis/SINGLE_BUG/SENSITIVITY%20ANALYSIS/test_suite_size_impact.xlsx)
1. [Performance In Localizing Multiple Bugs](https://github.com/ttrangnguyen/VARCOP/tree/gh-pages/experiment_results/Analysis/MULTIPLE_BUG)
1. [Time Complexity](https://github.com/ttrangnguyen/VARCOP/tree/gh-pages/experiment_results/Analysis/RUNTIME)

#### VarCop's source code [Link](https://github.com/ttrangnguyen/VARCOP)
#### Dataset [Link](https://tuanngokien.github.io/splc2021/)
#### Slicing tool [Link](https://github.com/ttrangnguyen/Static_Slicing)

