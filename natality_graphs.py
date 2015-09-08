import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


def load_data(filename):
    """
    Load data and return a Pandas DataFrame.
    """
    data = []
    print "Opening file"
    with open(filename, "r") as f:
        for row in f:
            new_data = json.loads(row)
            if new_data.get("gestation_weeks") is None:
                continue
            data.append(new_data)
    df = pd.DataFrame(data)
    return df


def add_kg_to_df(df):
    """
    Recalculate weight in pounds to kg.
    """
    df["weight_kg"] = df["weight_pounds"] * 0.454


def convert_fields(df):
    df.gestation_weeks = df.gestation_weeks.astype(int)
    df.mother_age = df.mother_age.astype(int)
    df.year = df.year.astype(int)


def plot_hist(df, param, title="", x_label="", approx=False, save=False, savename="1", bw_arg="silverman"):
    sns.set(style="darkgrid", palette="muted", color_codes=True)
    sns.despine(left=True)
    if approx:
        sns.kdeplot(df[df["is_male"] == True][param].dropna(), shade=True, kernel="gau", bw=bw_arg, color="b")
        sns.kdeplot(df[df["is_male"] == False][param].dropna(), shade=True, kernel="gau", bw=bw_arg, color="r")
    else:
        sns.distplot(df[df["is_male"] == True][param].dropna(), hist=True, kde=False, color="b")
        sns.distplot(df[df["is_male"] == False][param].dropna(), hist=True, kde=False, color="r")
    plt.legend(["Male", "Female"])
    plt.xlabel(x_label)
    plt.title(title)
    plt.tight_layout()
    if save:
        if approx:
            plt.savefig("out/{}_approx.png".format(savename), dpi=300, pad_inches=0.1)
        else:
            plt.savefig("out/{}_dist.png".format(savename), dpi=300, pad_inches=0.1)
    plt.clf()


def plot_scatter(df, paramx, paramy, save=False, savename="1", title="", x_label="", y_label=""):
    sns.set(style="darkgrid", palette="muted", color_codes=True)
    sns.despine(left=True)


    # Use JointGrid directly to draw a custom plot
    x = df[df["is_male"] == True][paramx].dropna()
    y = df[df["is_male"] == True][paramy].dropna()

    grid = sns.JointGrid(x, y, space=0.2, ratio=4, size=10, ylim=(0, 6), xlim=(0, 60))
    grid.plot_joint(plt.scatter, marker=".")
    grid.plot_marginals(sns.distplot)
    grid.ax_marg_x.hist(x, color="b", alpha=.5, bins=np.arange(0, 70, 1))
    grid.set_axis_labels(x_label, y_label)

    plt.tight_layout()
    if save:
        plt.savefig("out/{}.png".format(savename), dpi=300, pad_inches=0.1)


if __name__ == "__main__":
    datafr = load_data("data/natality_small.json")
    add_kg_to_df(datafr)
    convert_fields(datafr)

    print datafr.dtypes
    print "Overall stats"
    print datafr.describe()
    print 80 * "-"
    print "Male children"
    print datafr[datafr["is_male"] == True].describe()
    print 80 * "-"
    print "Female children"
    print datafr[datafr["is_male"] == False].describe()
    print 80 * "-"

    print "Creating graphs"
    plot_hist(datafr, "weight_kg", approx=True, x_label="Weight [kg]",
              title="Weight distribution of newborns \n US Natality data, 2003 - 2008", save=True, savename="weight")
    plot_hist(datafr, "weight_kg", approx=False, x_label="Weight [kg]",
              title="Weight distribution of newborns \n US Natality data, 2003 - 2008", save=True, savename="weight")

    plot_hist(datafr, "gestation_weeks", approx=True, x_label="Weeks",
              title="Gestation Length distribution of newborns \n US Natality data, 2003 - 2008", save=True,
              savename="gest", bw_arg=2)
    plot_hist(datafr, "gestation_weeks", approx=False, x_label="Weeks",
              title="Gestation Length distribution of newborns \n US Natality data, 2003 - 2008", save=True,
              savename="gest")

    plot_scatter(datafr, "mother_age", "weight_kg", x_label="Mother Age", y_label="Weight [kg]", save=True,
                 savename="scatter")
