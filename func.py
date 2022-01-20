import numpy as np
import pandas as pd
from core_pro import Sheet


def convert_dim_quantity(dim, quantity):
    org_dim = np.sort(dim)
    s, m, l = org_dim
    s_new = s * quantity

    n, m_new = 2, 0
    while s_new > 2 * l:
        m_new = m * n
        s_new = s * quantity / n
        if s_new <= 2 * l:
            return np.sort([s_new, m_new, l])
        else:
            n += 1
    else:
        if n == 2:
            return np.sort([s_new, m, l])
        else:
            return np.sort([s_new, m_new, l])


def convert_dim_multi(arr):
    arr = np.sort(arr)
    max_1_val = np.max(arr)
    max_2_val = np.max(arr, axis=0)[1]
    stack_3_val = np.sum(arr, axis=0)[0]
    return np.sort([max_1_val, max_2_val, stack_3_val])


def find_optimal_box(order_dim, box_name, box, box_dict):
    select = box_name[np.all(box >= order_dim, axis=1)]

    pack_cost = {i: v[3] for i, v in box_dict.items() if i in select}
    pack_vol = {i: v[4] for i, v in box_dict.items() if i in select}

    if pack_cost:
        min_cost = min(pack_cost, key=pack_cost.get)
        min_vol = min(pack_vol, key=pack_vol.get)
        return min_cost, min_vol
    else:
        return None, None


# box
sh = '1RXVHMSA9oaVWMWXCDfa5GcZMbP9USvkwMPMRwzizb8E'
box = Sheet(sh).google_sheet_into_df('box_2022_02', 'A:H')
col = ['width_m', 'height_m', 'length_m', 'price_usd', 'volume']
for i in col:
    if i in ['width_m', 'height_m', 'length_m']:
        box[i] = pd.to_numeric(box[i], downcast='integer').fillna(0).astype(int)
    else:
        box[i] = pd.to_numeric(box[i])

col = ['original_id'] + col
box_dict = {i[0]: i[1:].tolist() for i in box[col].values}
box_dim_dict = {i[0]: i[1:4].tolist() for i in box[col].values}

box_name = np.array([*box_dim_dict.keys()])
box = np.sort([*box_dim_dict.values()])
