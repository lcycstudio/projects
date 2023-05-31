import random


def additionFunc(grade):
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list4a = []
    list4b = []
    list5 = []
    list_a = []
    list_b = []
    if grade == 'Grade 1':
        for i in range(10):
            list1.append(random.randint(0, 9))
    elif grade == 'Grade 2':
        list1 = random.sample(range(0, 99), 10)
    elif grade == 'Grade 3':
        list1 = random.sample(range(0, 999), 10)
    elif grade == 'Grade 4':
        list1 = random.sample(range(0, 999), 10)
    # decimals
    elif grade == 'Grade 3 Decimals':
        for i in range(10):
            list1.append(round(random.uniform(0, 9), 1))
    elif grade == 'Grade 4 Decimals':
        for i in range(10):
            list1.append(round(random.uniform(0, 99), 2))
    elif grade == 'Grade 5 Decimals':
        for i in range(10):
            list1.append(round(random.uniform(0, 99), 2))
    # fractions
    elif grade == 'Grade 3 Fractions':
        for i in range(10):
            list3.append(random.randint(2, 10))
        for item in list3:
            list4.append(random.randint(1, item - 1))
        for j in range(10):
            list_a.append('{0}/{1}'.format(list4[j], list3[j]))
            list1.append(
                '\\frac{' + str(list4[j]) + '}' + '{' + str(list3[j]) + '}')
    elif grade == 'Grade 4 Fractions':
        for i in range(10):
            list3.append(random.randint(2, 100))
        for item in list3:
            list4.append(random.randint(1, item - 1))
        for j in range(10):
            list_a.append('{0}/{1}'.format(list4[j], list3[j]))
            list1.append(
                '\\frac{' + str(list4[j]) + '}' + '{' + str(list3[j]) + '}')
    elif grade == 'Grade 5 Fractions':
        for i in range(10):
            list3.append(random.randint(1, 9) * random.randint(1, 9))
        for item in list3:
            factor_list = []
            for k in range(2, item):
                if item % k == 0:
                    factor_list.append(k)
            if factor_list == []:
                list4.append(item)
                list4a.append(random.randint(1, item))
            else:
                factor = random.choice(factor_list)
                list4.append(random.choice(factor_list))
                list4a.append(random.randint(1, item - factor))
        for j in range(10):
            list_a.append('{0}/{1}'.format(list4a[j], list3[j]))
            list1.append(
                '\\frac{' + str(list4a[j]) + '}' + '{' + str(list3[j]) + '}')
    # list2
    for item in list1:
        if grade == 'Grade 1':
            list2.append(random.randint(1, 10 - item))
        elif grade == 'Grade 2':
            list2.append(random.randint(1, 100 - item))
        elif grade == 'Grade 3':
            list2.append(random.randint(1, 1000 - item))
        elif grade == 'Grade 4':
            num2 = random.randint(1, 1000 - item)
            num3 = random.randint(1, 1000 - num2 - item)
            list2.append(num2)
            list3.append(num3)
        elif grade == 'Grade 3 Decimals':
            list2.append(round(random.uniform(0, 10 - item), 1))
        elif grade == 'Grade 4 Decimals':
            list2.append(round(random.uniform(0, 100 - item), 2))
        elif grade == 'Grade 5 Decimals':
            list2.append(round(random.uniform(0, 100 - item), 2))
    if 'Fractions' in grade:
        if 'Grade 5' in grade:
            for i in range(10):
                factor_list = []
                for j in range(list4a[i], list3[i]):
                    if j % list4[i] == 0:
                        factor_list.append(j)
                if factor_list == []:
                    list5.append(random.randint(0, (list3[i] - list4a[i])))
                else:
                    factor = random.choice(factor_list)
                    list5.append(factor - list4a[i])
            for j in range(10):
                list_b.append('{0}/{1}'.format(list5[j], list3[j]))
                list2.append(
                    '\\frac{' + str(list5[j]) + '}' + '{' + str(list3[j]) + '}')
        else:
            for i in range(10):
                list5.append(random.randint(1, list3[i] - list4[i]))
            for j in range(10):
                list_b.append('{0}/{1}'.format(list5[j], list3[j]))
                list2.append(
                    '\\frac{' + str(list5[j]) + '}' + '{' + str(list3[j]) + '}')
        return list1, list2, list_a, list_b
    else:
        return list1, list2, list3


def subtractionFunc(grade):
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list_a = []
    list_b = []
    if grade == 'Grade 1':
        for i in range(10):
            list1.append(random.randint(1, 10))
    elif grade == 'Grade 2':
        list1 = random.sample(range(1, 100), 10)
    elif grade == 'Grade 3':
        list1 = random.sample(range(1, 1000), 10)
    elif grade == 'Grade 4':
        list1 = random.sample(range(1, 1000), 10)
    elif grade == 'Grade 3 Decimals':
        for i in range(10):
            list1.append(round(random.uniform(0, 10), 1))
    elif grade == 'Grade 3 Fractions':
        for i in range(10):
            list3.append(random.randint(2, 10))
        for item in list3:
            list4.append(random.randint(1, item - 1))
        for j in range(10):
            list_a.append('{0}/{1}'.format(list4[j], list3[j]))
            list1.append(
                '\\frac{' + str(list4[j]) + '}' + '{' + str(list3[j]) + '}')
    elif grade == 'Grade 4 Decimals':
        for i in range(10):
            list1.append(round(random.uniform(0, 100), 2))
    elif grade == 'Grade 4 Fractions':
        for i in range(10):
            list3.append(random.randint(2, 100))
        for item in list3:
            list4.append(random.randint(1, item - 1))
        for j in range(10):
            list_a.append('{0}/{1}'.format(list4[j], list3[j]))
            list1.append(
                '\\frac{' + str(list4[j]) + '}' + '{' + str(list3[j]) + '}')
    elif grade == 'Grade 5 Decimals':
        for i in range(10):
            list1.append(round(random.uniform(0, 99), 2))
    elif grade == 'Grade 5 Fractions':
        for i in range(10):
            list1.append(round(random.uniform(0, 99), 2))
    # list2
    for item in list1:
        if grade == 'Grade 1':
            list2.append(random.randint(0, item - 1))
        elif grade == 'Grade 2':
            list2.append(random.randint(0, item - 1))
        elif grade == 'Grade 3':
            list2.append(random.randint(0, item - 1))
        elif grade == 'Grade 4':
            num2 = random.randint(0, item - 1)
            num3 = random.randint(0, item - num2 - 1)
            list2.append(num2)
            list3.append(num3)
        elif grade == 'Grade 3 Decimals':
            list2.append(round(random.uniform(0, item), 1))
        elif grade == 'Grade 4 Decimals':
            list2.append(round(random.uniform(0, item), 2))
        elif grade == 'Grade 5 Decimals':
            list2.append(round(random.uniform(0, item), 3))
    if 'Fractions' in grade:
        for i in range(10):
            list5.append(random.randint(0, list4[i]))
        for j in range(10):
            list_b.append('{0}/{1}'.format(list5[j], list3[j]))
            list2.append(
                '\\frac{' + str(list5[j]) + '}' + '{' + str(list3[j]) + '}')
        return list1, list2, list_a, list_b
    else:
        return list1, list2, list3


def multiplicationFunc(grade):
    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    list_a = []
    list_b = []
    if grade == 'Grade 3 1x1':
        for i in range(10):
            list1.append(random.randint(1, 9))
            list2.append(random.randint(1, 9))
    elif grade == 'Grade 3 2x1':
        list1 = random.sample(range(10, 99), 10)
        for i in range(10):
            list2.append(random.randint(1, 9))
    elif grade == 'Grade 4 2x2':
        list1 = random.sample(range(10, 99), 10)
        list2 = random.sample(range(10, 99), 10)
    elif grade == 'Grade 4 3x1':
        list1 = random.sample(range(100, 999), 10)
        for i in range(10):
            list2.append(random.randint(1, 9))
    elif grade == 'Grade 4 3x2':
        list1 = random.sample(range(100, 999), 10)
        list2 = random.sample(range(10, 99), 10)
    elif grade == 'Grade 4 3x3':
        list1 = random.sample(range(100, 999), 10)
        list2 = random.sample(range(100, 999), 10)
    return list1, list2


def divisionFunc(grade):
    list1 = []
    list2 = []
    list3 = []
    if grade == 'Grade 3':
        for i in range(10):
            list3.append(random.randint(1, 9))
            list2.append(random.randint(1, 9))
            list1.append(list3[i] * list2[i])
    elif grade == 'Grade 3 Remainder':
        for i in range(10):
            item = random.randint(1, 99)
            list1.append(item)
            list2.append(random.randint(1, item))
    return list1, list2
