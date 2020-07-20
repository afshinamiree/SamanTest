import pandas as pd
import numpy as np

col_names = ['base_suit', 'other_suit', 'flag', 'value']
cache_df = pd.DataFrame(columns=col_names)


def calc_score(base_suit, other_suit, has_base):
	cache_row = cache_df[
		(cache_df.base_suit == base_suit) & (cache_df.other_suit == other_suit) & (cache_df.flag == has_base)]
	if not cache_row.empty:
		return np.array(cache_row['value'])[0]

	if not has_base:
		if base_suit == 1 or base_suit == 0:
			result = 0
		elif other_suit == 0:
			result = base_suit - 1
		else:
			result = (base_suit / (base_suit + other_suit)) * calc_score(base_suit - 1, other_suit, True) + \
					 (other_suit / (base_suit + other_suit)) * calc_score(base_suit, other_suit - 1, False)
	if has_base:
		if base_suit == 0:
			result = 0
		elif other_suit == 0:
			result = base_suit
		else:
			result = (base_suit / (base_suit + other_suit)) * (1 + calc_score(base_suit - 1, other_suit, True)) + (
					other_suit / (base_suit + other_suit)) * calc_score(base_suit, other_suit - 1, False)
	cache_df.loc[len(cache_df)] = {'base_suit': base_suit, 'other_suit': other_suit, 'flag': has_base, 'value': result}
	return result


def print_scores():
	print('the mean point for the case N=26 and M=2 is :')
	print(2 * calc_score(13, 13, False))

	print('the mean point for the case N=52 and M = 4 is :')
	print(4 * calc_score(13, 39, False))


if __name__ == "__main__":
	print_scores()
