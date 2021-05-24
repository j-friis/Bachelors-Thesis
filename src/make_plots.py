import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns


def plot_estimates_hh_degree(number_of_queries, N, model, epsilon, degree, dates, counts, range_qurey, plot_name):
    
    test_dates, test_counts = dates[:N].copy(), counts[:N].copy()
    answers = np.zeros(number_of_queries)
    

    for i in range(0,number_of_queries):
        current_model = model(epsilon, degree, test_dates, test_counts)
        answer = current_model.answer(range_qurey)
        answers[i] = answer
    print(answers)
    correct_answer = current_model.real_answer(range_qurey)
    
    x = np.arange(0,number_of_queries)
    answers.sort()

    plt.scatter(x,answers, marker = '+', label="Esitmates")
    plt.axhline(np.mean(answers),linewidth=0.5, color='r', linestyle = '-', label="Mean of esitmates ")
    plt.axhline(correct_answer,linewidth=.4, color='b', linestyle = '--', label="Correct answer")
    #plt.hlines(np.mean(answears128),line_range[0],line_range[1])
    #plt.hlines(np.mean(correct_answear),line_range[0],line_range[1])
    plt.legend()
    plt.title(f'Local HH OLH with N = {N}, B = {degree} and \u03B5 = {epsilon}')
    plt.savefig(plot_name)
    plt.show()
    return answers


def plot_estimates_flat(number_of_queries, N, model, epsilon, dates, counts, range_qurey, plot_name):
    
    test_dates, test_counts = dates[:N].copy(), counts[:N].copy()
    answers = np.zeros(number_of_queries)
    

    for i in range(0,number_of_queries):
        current_model = model(epsilon, test_dates, test_counts)
        answer = current_model.answer(range_qurey)
        answers[i] = answer
    #print(answers)
    correct_answer = current_model.real_answer(range_qurey)
    
    x = np.arange(0,number_of_queries)
    answers.sort()

    plt.scatter(x,answers, marker = '+', label="Mean of esitmates")
    plt.axhline(np.mean(answers),linewidth=0.5, color='r', linestyle = '-', label="Mean of esitmates ")
    plt.axhline(correct_answer,linewidth=.4, color='b', linestyle = '--', label="Correct answer")
    plt.axhline(current_model.var,linewidth=.4, color='g', linestyle = '--', label="Correct answer")
    #plt.hlines(np.mean(answears128),line_range[0],line_range[1])
    #plt.hlines(np.mean(correct_answear),line_range[0],line_range[1])
    plt.legend()
    plt.title(f'Flat OLH with N = {N} and \u03B5 = {epsilon}')
    plt.savefig(plot_name,dpi=300,bbox_inches='tight')
    plt.show()
    
    return answers

#Getting all error values from dict
def dict_error_plot_epsilons(dic, plotname, epsilons):
    n = len(dic)
    mse_errors = np.zeros(n)
    max_errors = np.zeros(n)
    abs_errors = np.zeros(n)

    for num, item in enumerate(dic.items()):
        mse_errors[num] = item[1]['mse']
        max_errors[num] = item[1]['max']
        abs_errors[num] = item[1]['abs']

    error_stack = np.vstack((mse_errors,max_errors,abs_errors)).flatten()
    mse_labels = np.full(mse_errors.size, 'mse errors')
    max_labels = np.full(max_errors.size, 'max errors')
    abs_labels = np.full(abs_errors.size, 'abs errors')


    labels_stack = np.vstack((mse_labels,max_labels,abs_labels)).flatten()
    epsilons_stack = np.tile(epsilons,3)
    
    seaborn_df = pd.DataFrame({'epsilons':epsilons_stack, 'errors':error_stack,'labels':labels_stack})
    seaborn_df.to_csv(plotname + '_olh_seaborn_plotting_data.csv',index=False)

    all_data = pd.DataFrame({'epsilons':epsilons,'max_errors':max_errors,'rmse_errors':mse_errors,'abs_errors':abs_errors})
    all_data.to_csv(plotname + '_plotting_data.csv',index=False)
    sns.set()
    sns_plot = sns.catplot(x="epsilons", y="errors", hue="labels", data=seaborn_df)
    sns_plot.set(yscale="log")
    sns_plot.savefig(plotname + "_AllErrors.png")
    
#Getting all error values from dict
def dict_error_plot_n(dic, plotname, ns):
    n = len(dic)
    mse_errors = np.zeros(n)
    max_errors = np.zeros(n)
    abs_errors = np.zeros(n)

    for num, item in enumerate(dic.items()):
        mse_errors[num] = item[1]['mse']
        max_errors[num] = item[1]['max']
        abs_errors[num] = item[1]['abs']

    error_stack = np.vstack((mse_errors,max_errors,abs_errors)).flatten()
    mse_labels = np.full(mse_errors.size, 'mse errors')
    max_labels = np.full(max_errors.size, 'max errors')
    abs_labels = np.full(abs_errors.size, 'abs errors')


    labels_stack = np.vstack((mse_labels,max_labels,abs_labels)).flatten()
    n_stack = np.tile(ns,3)
    """
    print('______________')
    print(np.tile(ns,n-1))
    print(n_stack)
    print('______________')
    print(ns)
    print(len(n_stack))
    print(len(error_stack))
    print(len(labels_stack))
    """
    
    seaborn_df = pd.DataFrame({'N':n_stack, 'errors':error_stack, 'labels':labels_stack})
    seaborn_df.to_csv(plotname + '_olh_seaborn_plotting_data.csv',index=False)

    all_data = pd.DataFrame({'N':ns,'max_errors':max_errors,'rmse_errors':mse_errors,'abs_errors':abs_errors})
    all_data.to_csv(plotname + '_plotting_data.csv',index=False)
    sns.set()
    sns_plot = sns.catplot(x="N", y="errors", hue="labels", data=seaborn_df)
    sns_plot.set(yscale="log")
    sns_plot.savefig(plotname + "_AllErrors.png")
