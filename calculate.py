import pandas as pd

mixes = {
    25069: ((41018, 41019, 41021, 41034),0.25),
    25071:((40055, 40056, 40054, 40042, 40053), 0.2),
    25072:((40056, 40054, 40042, 40053, 41018, 41019, 41021, 41034), 0.125)
}


def calc_mix(mix, weight):
    data = pd.DataFrame(columns=['code', 'weight'])
    for i in mixes[mix][0]:
        data.loc[len(data.index)] = [i, mixes[mix][1] * weight]
    return data


def decompose_mix(data):

    sum_df = pd.DataFrame()

    for i in range(len(df)):
        sum_df = pd.concat([sum_df, calc_mix(*df.loc[i].tolist())]).groupby('code', as_index=False).sum()

    return(sum_df)
