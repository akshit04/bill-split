import math

def getMin(arr, N):
    minInd = 0
    for i in range(1, N):
        if (arr[i] < arr[minInd]):
            minInd = i
    return minInd


# A utility function that returns
# index of maximum value in arr[]

def getMax(arr, N):
    maxInd = 0
    for i in range(1, N):
        if (arr[i] > arr[maxInd]):
            maxInd = i
    return maxInd


# A utility function to
# return minimum of 2 values

def minOf2(x, y):
    return x if x < y else y


# amount[p] indicates the net amount to
# be credited/debited to/from person 'p'
# If amount[p] is positive, then i'th
# person will amount[i]
# If amount[p] is negative, then i'th
# person will give -amount[i]
def minCashFlowRec(amount, log_string, N, person_dictionary):
    # Find the indexes of minimum
    # and maximum values in amount[]
    # amount[mxCredit] indicates the maximum
    # amount to be given(or credited) to any person.
    # And amount[mxDebit] indicates the maximum amount
    # to be taken (or debited) from any person.
    # So if there is a positive value in amount[],
    # then there must be a negative value

    mxCredit = getMax(amount, N)
    mxDebit = getMin(amount, N)
    # If both amounts are 0,
    # then all amounts are settled
    if ((math.floor(abs(amount[mxCredit])) == 0) and (math.floor(abs(amount[mxDebit]) == 0))):
        return log_string
    # Find the minimum of two amounts
    min = minOf2(-amount[mxDebit], amount[mxCredit])
    amount[mxCredit] -= min
    amount[mxDebit] += min
    # If minimum is the maximum amount to be
    for x in person_dictionary:
        if person_dictionary[x] == mxDebit:
            alpha = x
        elif person_dictionary[x] == mxCredit:
            beta = x
    min = round(min, 2)
    min = str(min)


    if min=="0.0":      # this condition is to exit the infintie recursion in case where rounding off might cause inconsistency
        return log_string

    log_string += alpha + " owes " + beta + " " + min + "\n"
    # ambrogio.send_text(alpha,"owes",beta,min) #use abroglio.send_text()
    # Recur for the amount array. Note that
    # it is guaranteed that the recursion
    # would terminate as either amount[mxCredit]
    # or amount[mxDebit] becomes 0
    return minCashFlowRec(amount, log_string, N, person_dictionary)


def minCashFlow(graph, N, person_dictionary):
    # Create an array amount[],
    # initialize all value in it as 0.
    amount = [0 for i in range(N)]
    # Calculate the net amount to be paid
    # to person 'p', and stores it in amount[p].
    # The value of amount[p] can be calculated by
    # subtracting debts of 'p' from credits of 'p'
    for p in range(N):
        for i in range(N):
            amount[p] += (graph[i][p] - graph[p][i])
            amount[p] = round(amount[p],2)
    return minCashFlowRec(amount, "", N, person_dictionary)


# Given a set of persons as graph[] where
# graph[i][j] indicates the amount that
# person i needs to pay person j, this
# function finds and prints the minimum
# cash flow to settle all debts.

class Balance():
    def balance(ambrogio, message, log_string=""):
        temporary_storage = ambrogio.store
        if not temporary_storage:
            ambrogio.send_text("Done")
        else:
            person_set = set()
            for x in temporary_storage:
                person1 = x[0:2]
                person2 = x[2:4]
                person_set.add(person1)
                person_set.add(person2)
            person_dictionary = {}
            i = 0
            for x in person_set:
                person_dictionary[x] = i
                i = i + 1
            N = len(person_set)  # total number of persons involved.


            graph = [[]]
            for i in range(0,N):
                graph.append([])
                for j in range(0,N):
                    graph[i].append(0)


            for x in temporary_storage:
                m = x[2:4]
                n = x[0:2]
                graph[person_dictionary[m]][person_dictionary[n]] = float(temporary_storage[x])

            log_string = ""
            log_string = minCashFlow(graph, N, person_dictionary)
            log_string = log_string[:-1]
            ambrogio.send_text(log_string)