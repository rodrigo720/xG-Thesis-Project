import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
from pathlib import Path

INPUT_PATH = Path("data/processed/shots_model_ready_wc2022.csv")
FIGURES_PATH = Path("report/figures")

def main():
    FIGURES_PATH.mkdir(parents=True,exist_ok=True)

    df = pd.read_csv(INPUT_PATH)

    print("Dataset shape:", df.shape)
    print(df["goal"].value_counts())

    sns.set_theme(style="whitegrid")

    #distribuzione goal/no goal
    plt.figure(figsize=(6,4))
    sns.countplot(x="goal",data=df)
    plt.title("Distribution of Goals vs Non Goals")
    plt.xlabel("Goal")
    plt.ylabel("Number of shots")
    plt.savefig(FIGURES_PATH/"goal_distribution_wc2022.png")
    plt.close()

    #distribuzione distanza tiro
    plt.figure(figsize=(8,5))
    sns.histplot(df["distance"],bins=30, kde=True)
    plt.title("Distribution of shot distance")
    plt.xlabel("distance from goal")
    plt.ylabel("frequency")
    plt.savefig(FIGURES_PATH/"distance_distribution_wc_2022.png")
    plt.close()

    #Goal rate per distanza
    bins=[0,10,20,30,40,50,100] #raggruppamento
    labels=["0-10","10-20","20-30","30-40","40-50","40+"]

    df["distance_bin"] = pd.cut(df["distance"],bins=bins,labels=labels)

    goal_rate = df.groupby("distance_bin")["goal"].mean().reset_index()

    plt.figure(figsize=(8,5))
    sns.barplot(x="distance_bin", y="goal", data=goal_rate)
    plt.title("Goal Rate by Distance")
    plt.xlabel("Distance from Goal (m)")
    plt.ylabel("Goal probability")
    plt.tight_layout()
    plt.savefig(FIGURES_PATH / "goal_rate_by_distance_wc2022.png")
    plt.close

    #Distribuzione body part
    plt.figure(figsize=(8,5))
    sns.countplot(y="shot.body_part.name", data=df)
    plt.title("Shot Distribution by Body Part")
    plt.xlabel("Number of Shots")
    plt.ylabel("Body Part")
    plt.savefig(FIGURES_PATH / "body_part_distribution_wc2022.png")
    plt.close()

    #Distribuzione shot type
    plt.figure(figsize=(8,5))
    sns.countplot(y="shot.type.name", data=df)
    plt.title("Shot Distribution by Shot Type")
    plt.xlabel("Number of Shots")
    plt.ylabel("Shot Type")
    plt.savefig(FIGURES_PATH / "shot_type_distribution_wc2022.png")
    plt.close()

    #Under pressure vs goal rate
    pressure_goal = df.groupby("under_pressure")["goal"].mean().reset_index()

    plt.figure(figsize=(6,4))
    sns.barplot(x="under_pressure", y="goal", data=pressure_goal)
    plt.title("Goal Rate Under Pressure")
    plt.xlabel("Under Pressure")
    plt.ylabel("Goal Probability")
    plt.savefig(FIGURES_PATH / "goal_rate_under_pressure_wc2022.png")
    plt.close()

    #Play pattern distribution
    plt.figure(figsize=(8,5))
    sns.countplot(y="play_pattern.name", data=df)
    plt.title("Shot Distribution by Play Pattern")
    plt.xlabel("Number of Shots")
    plt.ylabel("Play Pattern")
    plt.savefig(FIGURES_PATH / "play_pattern_distribution_wc2022.png")
    plt.close()

    print("EDA completed. Figures saved in reports/figures/")


if __name__ == "__main__":
    main()




