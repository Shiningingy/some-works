def lstm_fit_regression(features, labels, start_date, end_date, window, batch_size, n_epochs):
    result_true = pd.DataFrame()
    result_prediction = pd.DataFrame()
    result_prediction_classes = pd.DataFrame()

    n = len(features[features.index.date == dt.date(2019, 7, 1)])

    features = features[(features.index.date > start_date) & (features.index.date < end_date)]
    labels = labels[(labels.index.date > start_date) & (labels.index.date < end_date)]

    N = len(features)
    iter_num = N - (window * n) + 1

    for i in np.arange(0, iter_num, n):
        # Preparation
        X = features.iloc[i:i + window * n, ]
        y = labels.iloc[i:i + window * n, ]

        num_features = 6
        num_per_feature = int(X.shape[1] / num_features)

        X = X.apply(lambda x: (x - np.median(x)) / (np.quantile(x, 0.75) - np.quantile(x, 0.25)))

        X_Train = X.iloc[0:(window - 1) * n, ].values
        train_num = X_Train.shape[0]
        X_Train = X_Train.reshape(train_num, num_per_feature, num_features)

        X_Test = X.iloc[(window - 1) * n: window * n, ].values
        test_num = X_Test.shape[0]
        X_Test = X_Test.reshape(test_num, num_per_feature, num_features)

        y_Train = y.iloc[0:(window - 1) * n, ].values
        y_Test = y.iloc[(window - 1) * n: window * n, ].values

        num_classes = 3
        dim_input_vector = num_features
        nb_time_steps = num_per_feature

        input_shape = (nb_time_steps, dim_input_vector)
        # lstm fitting
        print('Start ' + str(i / n + 1) + ' LSTM ' + 'Fitting !')
        model = Sequential()
        model.add(LSTM(128, input_shape=input_shape, return_sequences=False))
        model.add(Dropout(0.1))
        model.add(Dense(units=64, activation='linear'))
        model.add(Dropout(0.1))
        model.add(Dense(units=32, activation='linear'))
        model.add(Dropout(0.1))
        model.add(Dense(units=1, activation='linear'))

        # plot_model(model, to_file='lstm_model.png')
        # weights = [1, 1, 1]
        # classes_num = [1.5, 1, 1.2]
        # categorical_focal_loss(alpha=.25, gamma=2)
        # multi_category_focal_loss1(alpha, gamma=2.0)
        model.compile(loss='mean_squared_error',
                      optimizer=Adam(lr=0.01),
                      metrics=['mae'])

        timer = mytimer()
        timer.start()
        model.fit(X_Train, y_Train,
                  batch_size=batch_size,
                  epochs=n_epochs,
                  verbose=1)

        # accuracy
        scores = model.evaluate(X_Test, y_Test, verbose=0)
        print("%s: %.2f%%" % (model.metrics_names[1], scores[1] * 100))

        # prediction
        y_pred = model.predict(X_Test)

        y_pred = pd.DataFrame(y_pred, index=X.iloc[(window - 1) * n: window * n, ].index)
        y_Test = pd.DataFrame(y_Test, index=X.iloc[(window - 1) * n: window * n, ].index)

        result_true = result_true.append(y_Test, ignore_index=False)
        result_prediction = result_prediction.append(y_pred, ignore_index=False)

        timer.stop()

    result_true.columns = ['true']
    result_prediction.columns = ['pred']

    return result_prediction, result_true
