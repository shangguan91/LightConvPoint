import numpy as np

# ==============================================
# ==============================================
# STATS
# ==============================================
# ==============================================


def stats_overall_accuracy(cm):
    """Compute the overall accuracy.
    """
    return np.trace(cm) / cm.sum()


def stats_pfa_per_class(cm):
    """Compute the probability of false alarms.
    """
    sums = np.sum(cm, axis=0)
    mask = sums > 0
    sums[sums == 0] = 1
    pfa_per_class = (cm.sum(axis=0) - np.diag(cm)) / sums
    pfa_per_class[np.logical_not(mask)] = -1
    average_pfa = pfa_per_class[mask].mean()
    return average_pfa, pfa_per_class


def stats_accuracy_per_class(cm):
    """Compute the accuracy per class and average
        puts -1 for invalid values (division per 0)
        returns average accuracy, accuracy per class
    """
    # equvalent to for class i to
    # number or true positive of class i
    # (data[target==i]==i).sum()/ number of elements of i (target==i).sum()
    sums = np.sum(cm, axis=1)
    mask = sums > 0
    sums[sums == 0] = 1
    accuracy_per_class = np.diag(cm) / sums  # sum over lines
    accuracy_per_class[np.logical_not(mask)] = -1
    average_accuracy = accuracy_per_class[mask].mean()
    return average_accuracy, accuracy_per_class


def stats_iou_per_class(cm, replace_missing_categories_by_one=False):
    """Compute the iou per class and average iou
        Puts -1 for invalid values
        returns average iou, iou per class

        REplace missing category by one => some paper do that (Not a good idea)
    """

    # compute TP, FN et FP
    TP = np.diagonal(cm, axis1=-2, axis2=-1)
    TP_plus_FN = np.sum(cm, axis=-1)
    TP_plus_FP = np.sum(cm, axis=-2)

    # compute IoU
    mask = TP_plus_FN == 0
    IoU = TP / (TP_plus_FN + TP_plus_FP - TP + mask)

    # replace IoU with 0 by the average IoU
    if replace_missing_categories_by_one:
        aIoU = 1
    else:
        aIoU = IoU[np.logical_not(mask)].mean(axis=-1, keepdims=True)
    IoU += mask * aIoU

    return IoU.mean(axis=-1), IoU

    # sums = (np.sum(cm, axis=1) + np.sum(cm, axis=0) - np.diag(cm))
    # mask  = (sums>0)
    # sums[sums==0] = 1
    # iou_per_class = np.diag(cm) / sums

    # if replace_missing_categories_by_one:
    #     iou_per_class[np.logical_not(np.sum(cm, axis=1)>0)] = 1
    #     average_iou = iou_per_class.mean()
    # else:
    #     iou_per_class[np.logical_not(mask)] = -1
    #     if mask.sum()>0:
    #         average_iou = iou_per_class[mask].mean()
    #     else:
    #         average_iou = 0

    # return average_iou, iou_per_class


def stats_f1score_per_class(cm):
    """Compute f1 scores per class and mean f1.
        puts -1 for invalid classes
        returns average f1 score, f1 score per class
    """
    # defined as 2 * recall * prec / recall + prec
    sums = np.sum(cm, axis=1) + np.sum(cm, axis=0)
    mask = sums > 0
    sums[sums == 0] = 1
    f1score_per_class = 2 * np.diag(cm) / sums
    f1score_per_class[np.logical_not(mask)] = -1
    average_f1_score = f1score_per_class[mask].mean()
    return average_f1_score, f1score_per_class
