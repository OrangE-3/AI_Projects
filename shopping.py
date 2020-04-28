import csv
import sys
import copy
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4

done={
    'Jan':0,
    'Feb':1,
    'Mar':2,
    'Apr':3,
    'May':4,
    'June':5,
    'Jul':6,
    'Aug':7,
    'Sep':8,
    'Oct':9,
    'Nov':10,
    'Dec':11
}
def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])

    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )
    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    evidence=[]
    labels=[]
    with open(filename,'r') as file:
        reader= csv.reader(file)
        p=0
        for row in reader:
            if p==0:
                p=1
                continue
            x=copy.deepcopy(row)
            x[10]=done[x[10]]
            if x[15] == 'Returning_Visitor':
                x[15]=1
            else:
                x[15]=0
            if x[16] =='TRUE':
                x[16]=1
            else:
                x[16]=0
            if x[17] =='TRUE':
                x[17]=1
            else:
                x[17]=0

            x[0]=int(x[0])
            x[1]=float(x[1])
            x[2]=int(x[2])
            x[3]=float(x[3])
            x[4]=int(x[4])
            x[5]=float(x[5])
            x[6]=float(x[6])
            x[7]=float(x[7])
            x[8]=float(x[8])
            x[9]=float(x[9])
            for i in range(10,18):
                x[i]=int(x[i])
            evidence.append(x[0:17])
            labels.append(x[17])
    return (evidence,labels)
    #raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model=KNeighborsClassifier(n_neighbors=1)
    model.fit(evidence,labels)
    return model
    #raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    a=0
    b=0
    ta=0
    tb=0
    for i in range(len(predictions)):
        if (labels[i]==1) and (predictions[i]==1):
            a+=1
        if (labels[i]==0) and (predictions[i]==0):
            b+=1
        if labels[i]==1:
            ta+=1
        if labels[i]==0:
            tb+=1

    return (float(float(a)/float(ta)), float(float(b)/float(tb)))
    #raise NotImplementedError


if __name__ == "__main__":
    main()
