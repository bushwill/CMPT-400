import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import numpy as np

def summarizeDFAEvaluations(DFAList):
    data = []
    for i, evaluated in enumerate(DFAList):
        data.append({
            "Index": i + 1,
            "Original States": len(evaluated.originalDFA.States),
            "Proposed States": len(evaluated.proposedDFA.States),
            "TP States": evaluated.tpDFAlen,
            "FP States": evaluated.fpDFAlen,
            "FN States": evaluated.fnDFAlen,
            "Precision": evaluated.precision,
            "Recall": evaluated.recall
        })
    df = pd.DataFrame(data)
    return df

def plot_precision_recall(DFAList):
    df = summarizeDFAEvaluations(DFAList)
    indices = np.arange(len(df))
    bar_width = 0.4

    plt.figure(figsize=(12, 6))

    for i, row in df.iterrows():
        idx = indices[i]
        precision = row["Precision"]
        recall = row["Recall"]

        if precision == 1.0 and recall == 1.0:
            precision_color = 'grey'
            recall_color = 'grey'
        else:
            precision_color = 'skyblue'
            recall_color = 'salmon'

        # Plot individual bars with conditional coloring
        plt.bar(idx - bar_width/2, precision, width=bar_width, color=precision_color)
        plt.bar(idx + bar_width/2, recall, width=bar_width, color=recall_color)

    plt.xlabel("DFA #")
    plt.ylabel("Score")
    plt.title("Precision and Recall per DFA")
    plt.xticks(indices, df["Index"])
    plt.ylim(0, 1.05)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()

    # Custom legend
    legend_elements = [
        Patch(facecolor='skyblue', label='Precision'),
        Patch(facecolor='salmon', label='Recall'),
        Patch(facecolor='grey', label='Perfect (Precision & Recall = 1.0)')
    ]
    plt.legend(handles=legend_elements)

    plt.show()