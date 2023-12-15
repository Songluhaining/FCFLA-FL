import math
import numpy as np

from methods.mutual_information import su_calculation


def mul_evd_fusion(a, b):
    m1 = np.array(a)
    m2 = np.array(b)
    k = 0
    for i in range(len(a)):
        for j in range(len(a)):
            k = k + m1[i] * m2[j]

    res = 0
    for q in range(len(a)):
        res = res + m1[q] * m2[q]
    k = k - res
    list = []
    for s in range(len(a)):
        A = m1[s] * m2[s] / (1 - k)
        list.append(A)

    list2 = []
    for t in range(len(a)):
        P = list[t] / np.sum(list)
        list2.append(P)
    return list2


def evd_fusion_with_SBFL_and_FCFLA(a, b):
    m1 = np.array(a)
    m2 = np.array(b)
    k = 0
    for i in range(len(a)):
        for j in range(len(a)):
            k = k + m1[i] * m2[j]

    res = 0
    dis = 0
    for q in range(len(a)):
        res = res + m1[q] * m2[q]
        dis += abs(m1[q] - m2[q])
    k = k - res
    if dis < 1.8:
        return a
    list = []
    for s in range(len(a)):
        A = m1[s] * m2[s] / (1 - k)
        list.append(A)

    list2 = []
    for t in range(len(a)):
        P = list[t] / np.sum(list)
        list2.append(P)
    return list2


def fusion(a, b, c):
    m1 = np.array(a)
    m2 = np.array(b)
    m3 = np.array(c)
    k = 0
    dis = 0

    for i in range(len(a)):
        for j in range(len(a)):
            k = k + m1[i] * m2[j]

    res = 0
    for q in range(len(a)):
        res = res + m1[q] * m2[q]
        dis += abs(m1[q] - m2[q])
    k = k - res

    if k >= 0.98:
        k2 = 0
        dis2 = 0
        for i in range(len(a)):
            for j in range(len(a)):
                k2 = k2 + m1[i] * m3[j]

        res_c = 0
        for q in range(len(a)):
            res_c = res_c + m1[q] * m3[q]
            dis2 += abs(m1[q] - m3[q])

        k2 = k2 - res_c
        list = []
        for s in range(len(a)):
            A = m1[s] * m3[s] / (1 - k2)
            list.append(A)

        list2 = []
        for t in range(len(a)):
            P = list[t] / np.sum(list)
            list2.append(P)
        return 1, list2

    list = []
    for s in range(len(a)):
        A = m1[s] * m2[s] / (1 - k)
        list.append(A)

    list2 = []
    for t in range(len(a)):
        P = list[t] / np.sum(list)
        list2.append(P)
    return 0, mul_evd_fusion(list2, c)


def softmax(x):
    c = np.max(x)
    exp_a = np.exp(x - c)  # 溢出对策
    sum_exp_a = np.sum(exp_a)
    y = exp_a / sum_exp_a

    return y


def calculate_C_Relevance(f, C):
    return su_calculation(f, C)
