from scipy.stats import chi2_contingency
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

vt_df = pd.read_csv('VT_cleaned.csv', low_memory=False)
mt_df = pd.read_csv('MT_cleaned.csv', low_memory=False)


def male_stop_ratio_in_mt_percentage():
	# The proportion of traffic stops in MT involving male drivers
	male_driver_count = len(mt_df[mt_df.driver_gender == 'M'])
	female_driver_count = len(mt_df[mt_df.driver_gender == 'F'])
	male_proportion = male_driver_count / (male_driver_count + female_driver_count)
	return round(male_proportion * 100)


def oos_chi_square_test():
	# Factor increase in a traffic stop arrest likelihood in MT from OOS plates
	# Chi-Squared traffic stop arrest test statistic
	oos_arrested = sum((mt_df.out_of_state == True) & mt_df.is_arrested)
	oos_not_arrested = sum((mt_df.out_of_state == True) & ~mt_df.is_arrested)
	in_state_arrested = sum((mt_df.out_of_state == False) & mt_df.is_arrested)
	in_state_not_arrested = sum((mt_df.out_of_state == False) & ~mt_df.is_arrested)
	arrested = oos_arrested + in_state_arrested
	not_arrested = oos_not_arrested + in_state_not_arrested
	total = arrested + not_arrested
	p_arrest = arrested / total
	p_arrest_oos = oos_arrested / (oos_arrested + oos_not_arrested)
	p_arrest_in_state = in_state_arrested / (in_state_arrested + in_state_not_arrested)
	likelihood_increase_for_oos_percentage = (p_arrest_oos - p_arrest_in_state) * 100 / p_arrest

	obs = np.array([[oos_arrested, oos_not_arrested], [in_state_arrested, in_state_not_arrested]])
	chi_square = chi2_contingency(obs)[0]

	return round(likelihood_increase_for_oos_percentage), round(chi_square)


def speed_violation_percentage():
	# The proportion of traffic stops in MT involving speeding violations
	speed_related_stops = mt_df[mt_df.violation_raw.apply(lambda x: 'SPEED' in str(x).upper())].violation_raw.count()
	total = len(mt_df)
	return round(speed_related_stops / total, 3) * 100


def prediction_for_2020_stop_vehicle_year():
	# The average manufacture year of vehicles stopped in MT in 2020
	# P-value of linear regression:

	# cleansing and preparing regression data
	mt_df_drop_na = mt_df[mt_df.vehicle_year.notnull()]
	mt_df_drop_na['stop_year'] = pd.DatetimeIndex(mt_df_drop_na['stop_date']).year
	mt_df_cleaned = mt_df_drop_na[mt_df_drop_na.vehicle_year != 'NON-'][mt_df_drop_na.vehicle_year != 'UNK']
	mt_df_cleaned['vehicle_year_cleaned'] = mt_df_cleaned.vehicle_year.apply(lambda x: int(x))
	data = mt_df_cleaned[['stop_year', 'vehicle_year_cleaned']].groupby(['stop_year']).mean().reset_index()

	X = np.array(data['stop_year']).reshape(-1, 1)
	y = data['vehicle_year_cleaned']
	reg = LinearRegression().fit(X, y)
	reg.score(X, y)
	vehicle_year_2020 = round(reg.predict(np.array([2020]).reshape(-1, 1))[0], 2)
	X2 = sm.add_constant(X)
	est = sm.OLS(y, X2)
	p_value = est.fit().f_pvalue

	return vehicle_year_2020, p_value


def factor_increase_dui():
	# Factor increase in traffic stop DUI likelihood in MT over VT:
	total_mt = len(mt_df)
	mt_dui = mt_df[mt_df.violation_raw.apply(lambda x: 'DUI' in str(x))].violation_raw.count()
	p_mt_dui = mt_dui / mt_dui

	total_vt = len(vt_df)
	vt_dui = vt_df[vt_df.violation == 'DUI'].violation_raw.count()
	p_vt_dui = vt_dui / total_vt

	factor_increase = (p_mt_dui - p_vt_dui) / p_vt_dui
	return factor_increase


def diff_stops_between_min_max_hour():
	# The difference in the total number of stops that occurred between min and max hours in both MT and VT
	mt_stop_hour = pd.DatetimeIndex(mt_df.stop_time).hour
	vt_stop_hour = pd.DatetimeIndex(vt_df.stop_time).hour
	mt_stop_hour_count = mt_stop_hour.value_counts()
	vt_stop_hour_count = vt_stop_hour.value_counts()

	dif_between_min_and_max_mt = mt_stop_hour_count.max() - mt_stop_hour_count.min()
	dif_between_min_and_max_vt = vt_stop_hour_count.max() - vt_stop_hour_count.min()
	return dif_between_min_and_max_mt, dif_between_min_and_max_vt


def main():
	male_percentage = male_stop_ratio_in_mt_percentage()
	print("Q.1 police stop  percentage for males in MT is {}.".format(male_percentage))

	likelihood, chi_square = oos_chi_square_test()
	print("Q.2 the likelihood increase for OOS plates is around {} percent.".format(likelihood))
	print("Q.2 chi_square value for the out od states plate is around {}.".format(chi_square))

	speed_violation = speed_violation_percentage()
	print("Q.3 the percentage of speed related violations in MT is around {} percent.".format(speed_violation))

	factor_increase = factor_increase_dui()
	print("Q.4 there are {} times chances for DUI arrest in MT over VT.".format(factor_increase))

	vehicle_year_2020, p_value = prediction_for_2020_stop_vehicle_year()
	print("Q.5 the predicted mean of vehicle year in 2020 traffic stop in MT is {}.".format(vehicle_year_2020))
	print("Q.5 the p_value for the regression is {} which is considerably low.".format(p_value))

	dif_between_min_and_max_mt, dif_between_min_and_max_vt = diff_stops_between_min_max_hour()
	print(
		"Q.6 The difference in the total number of stops that occurred between min and max hours in MT {}."
			.format(dif_between_min_and_max_mt))
	print(
		"Q.6 The difference in the total number of stops that occurred between min and max hours in VT {}."
			.format(dif_between_min_and_max_vt))


if __name__ == "__main__":
	main()
