import numpy as np
import pandas as pd
from loadnat2006 import load_natality
import matplotlib.pyplot as plt

df = load_natality("Nat2006us.dat", "KEY2006.txt",
                   usecols=["MEDUC_REC", "MRACEREC", "MAGER"])

df = df.apply(pd.to_numeric, errors="coerce")

print(df.shape)
print(df.describe())

# For plots 1-2: only need race and age (keeps all births)
clean = df.dropna(subset=["MRACEREC", "MAGER"])

# For plot 3: also need a valid education code (1-5).
# MEDUC_REC is blank for states using the 2003 revised certificate.
edu = df[df["MEDUC_REC"].between(1, 5) & df["MRACEREC"].between(1, 4)]

fig, axs = plt.subplots(1, 3, figsize=(22, 7))

# 1. Mother's age histogram
axs[0].hist(df["MAGER"], bins=np.arange(12, 52), alpha=0.7, edgecolor="white")
axs[0].set_xlabel("Age")
axs[0].set_ylabel("Number of mothers")
axs[0].set_title("Age distribution of mothers in 2006")

# 2. Mother's average age by race
race_labels = {
    1: "White",
    2: "Black",
    3: "American Indian /\nAlaska Native",
    4: "Asian /\nPacific Islander",
    0: "Other",   # only used for Puerto Rico records
}

avg_age = clean.groupby("MRACEREC")["MAGER"].mean()
avg_age.index = avg_age.index.map(race_labels)

axs[1].bar(avg_age.index, avg_age.values, edgecolor="white")
axs[1].set_xlabel("Race of mother")
axs[1].set_ylabel("Average age of mother (years)")
axs[1].set_title("Average age of mothers by race, 2006")

for i, v in enumerate(avg_age.values):
    axs[1].text(i, v + 0.3, f"{v:.1f}", ha="center")

# 3. Heatmap: average age by race and education
education_labels = {1: "0–8 years",
                    2: "9–11 years",
                    3: "12 years",
                    4: "13–15 years",
                    5: "16 years and over"}

grid = edu.pivot_table(index="MEDUC_REC", columns="MRACEREC",
                       values="MAGER", aggfunc="mean")

im = axs[2].imshow(grid.values, cmap="viridis", aspect="auto", origin="lower")
axs[2].set_xticks(range(grid.shape[1]))
axs[2].set_xticklabels([race_labels[c] for c in grid.columns])
axs[2].set_yticks(range(grid.shape[0]))
axs[2].set_yticklabels([education_labels[r] for r in grid.index])
axs[2].set_xlabel("Race of mother")
axs[2].set_ylabel("Mother's education")
axs[2].set_title("Average age of mother by race and education, 2006")

# Write the average age in each cell
for i in range(grid.shape[0]):
    for j in range(grid.shape[1]):
        v = grid.values[i, j]
        axs[2].text(j, i, f"{v:.1f}", ha="center", va="center",
                    color="white" if v < np.nanmean(grid.values) else "black")

fig.colorbar(im, ax=axs[2], label="Average age (years)")

captions = [
    "Age distribution of mothers (2006); includes both the 1989\n"
    "and 2003 revisions of birth certificates.",
    "Bar chart of average age of mothers by race (2006); includes race\n"
    "recode and both the 1989 and 2003 revisions of birth certificates.",
    "Average age by race and education (2006); education recode\n"
    "is used and excludes states using the 2003 revised certificate.",
]
for ax, cap in zip(axs, captions):
    ax.text(0.5, -0.2, cap, transform=ax.transAxes,
            ha="center", fontsize=10, style="italic")

fig.tight_layout()
fig.savefig("mother_distribution_2006.png", bbox_inches="tight")