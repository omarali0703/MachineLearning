def main():
    x = [1, 2, 3, 4, 5]
    y = [3, 4, 2, 4, 5]

    mx = 0
    my = 0
    mean_x = 0
    mean_y = 0

    for i in x :
        mx = i + mx

    for i in y :
        my = i + my

    mean_x = mx / len(x)
    mean_y = my / len(y)

    #y = mx + c

    x_minus_bar = []
    y_minus_bar = []
    x_minus_bar_square = []

    for i in range(len(x)) :
        x_minus_bar.append(x[i] - mean_x)

    for i in range(len(y)) :
        y_minus_bar.append(round(y[i] - mean_y, 1))

    for i in range(len(x_minus_bar)) :
        x_minus_bar_square.append(x_minus_bar[i] ** 2)

    m_sum_numer = []
    m_sum_denom = []

    for i in range(len(x_minus_bar)) :
        m_sum_denom.append(x_minus_bar[i] * y_minus_bar[i])

        m_sum_numer = x_minus_bar_square

    numer = sum(m_sum_denom)
    denom = sum(m_sum_numer)

    m = numer / denom

    fun_mx = mean_x * m
    fun_y = mean_y
    fun_c = fun_y - fun_mx

    # How should i go about defining the seasons?
    # Where should i start in terms of submissions and work?
    # determine the value for x equals [1, 2, 3, 4, 5] --> this is the regression line
    print(fun_c)

main()