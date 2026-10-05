import pandas as pd

def read_key(key_path="KEY2006.txt"):
    """Read a key file of lines like '15 18 DOB_YY' (1-based, inclusive positions)."""
    starts, ends, names = [], [], []
    with open(key_path) as f:
        for line in f:
            if line.strip():
                s, e, name = line.split()
                starts.append(int(s)); ends.append(int(e)); names.append(name)
    # pandas wants 0-based, end-exclusive (start, end) pairs
    colspecs = [(s - 1, e) for s, e in zip(starts, ends)]
    return colspecs, names

def load_natality(dat_path="Nat2006us.dat", key_path="KEY2006.txt",
                  usecols=None, nrows=None):
    colspecs, names = read_key(key_path)
    if usecols is not None:                      # keep only the columns you need
        keep = [i for i, n in enumerate(names) if n in usecols]
        colspecs = [colspecs[i] for i in keep]
        names = [names[i] for i in keep]
    return pd.read_fwf(dat_path, colspecs=colspecs, names=names,
                       dtype=str, nrows=nrows)    # str keeps leading zeros/blanks

if __name__ == "__main__":
    df = load_natality(nrows=1000)               # drop nrows to load everything
    print(df.shape)
    print(df.head())