from sklearn.ensemble import RandomForestRegressor

def main(input_data, var_names):
    var_names = var_names[:-1]

    regr = RandomForestRegressor(
        n_estimators=200, random_state=0, oob_score=True, max_depth=3)
    regr.fit(input_data[:, :-1], input_data[:, -1])

    var_imp = (regr.feature_importances_) / max(regr.feature_importances_)
    print(var_imp)

    return var_imp
