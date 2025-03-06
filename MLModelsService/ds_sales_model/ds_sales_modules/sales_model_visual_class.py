import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class SalesVisualization:

    def __init__(self, y_train, y_test, y_pred, model_mse, logs, lower_bound=None, upper_bound=None, margin_of_error=None) -> None:
        self.y_train = y_train 
        self.y_test = y_test
        self.y_pred = y_pred
        self.model_mse = model_mse
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.margin_of_error = margin_of_error
        self.result_logs = logs

    def compare_with_dummy_model(self):
        test_size = len(self.y_test)
        dummy_mse = sum((self.y_test - self.y_train.mean())**2) / len(self.y_test)
        dummy_mse2 = sum((self.y_test - self.y_train[len(self.y_train)-test_size*3:-test_size].mean())**2) / test_size
        model_is_ok = True

        if dummy_mse < self.model_mse:
            print('FIRST CHECK - MODEL IS GARBAGE')
            model_is_ok = False

        if dummy_mse2 < self.model_mse:
            print('SECOND CHECK - MODEL IS GARBAGE')
            model_is_ok = False

        if np.sum(self.y_pred < 0) > 0:
            print('MODEL HAVE MINUS REVENUE PREDICTIONS')
            model_is_ok = False
        
        if model_is_ok:
            print('MODEL IS OK')


    def compare_trpred_periods(self, name, periods=[7, 14, 30, 45, 60]):
        final_accuracy_mark = 0
        pred_size = len(self.y_pred)
        periods = [days for days in periods if days <= pred_size]
        
        for days in periods:
            sales_fact = sum(self.y_test[:days+1])
            sales_pred = sum(self.y_pred[:days+1])
            
            print(f'Revenue for last {days} days was {sales_fact:.2f}')
            print(f'Predicted revenue {sales_pred:.2f}')
            print(f'Difference: {sales_fact - sales_pred:.2f} {((sales_fact - sales_pred) / sales_fact)*100:.2f}%')
            print(f'----------------------')

        final_accuracy_mark = ((np.sum(self.y_test) - abs(np.sum(self.y_test) - np.sum(self.y_pred))) / np.sum(self.y_test))*100
        mean_accuracy = np.mean(((self.y_test - (np.abs(self.y_test - self.y_pred))) / self.y_test)*100)
        print('#####')
        print('#####')
        print(f'Total fact sales = {np.sum(self.y_test)}')
        print(f'Total pred sales = {np.sum(self.y_pred)}')
        print(f'Total fact sales minus total pred sales = {(np.sum(self.y_test) - np.sum(self.y_pred)):.2f}')
        print(f'Total Accuracy score: {final_accuracy_mark:.2f}%')
        print(f'Mean accuracy (on each point) {mean_accuracy:.2f}%')
        print(f'----------------------')
        
        self.result_logs.update(index=name, param='Accuracy', result=round(final_accuracy_mark,2))
        self.result_logs.update(index=name, param='mean_accuracy', result=round(mean_accuracy,2))


    def plot_predictions(self):
        y_day_pred_series = pd.Series(self.y_pred, index=self.y_test.index)

        # Создайте график и добавьте оба DataSeries на него
        plt.figure(figsize=(10, 6))
        plt.plot(self.y_test.index, self.y_test.values, label='y_day_test', marker='o', color='b', linestyle='-')
        plt.plot(y_day_pred_series.index, y_day_pred_series.values, label='y_day_pred', marker='x', color='r', linestyle='-')
        
        if self.lower_bound is not None and self.upper_bound is not None:
            plt.fill_between(y_day_pred_series.index, self.lower_bound, self.upper_bound, color='red', alpha=0.5)

        # Добавьте легенду графика
        plt.legend()

        # Настройте заголовок и подписи осей
        plt.title('График значений y_day_test и y_day_pred')
        plt.xlabel('Индекс')
        plt.ylabel('Значение')

        # Отобразите график
        plt.show()
        if self.lower_bound is not None and self.upper_bound is not None:
            sum_lower = sum(self.lower_bound > self.y_test)
            sum_upper = sum(self.upper_bound < self.y_test)
            total_miss = sum_lower + sum_upper
            total_points = len(self.y_test)
            correct_points = total_points - total_miss
            print(f'Фактические продажи ниже lower_bound {sum_lower}, {(sum_lower / total_points)*100:.2f}%')
            print(f'Фактические продажи выше upper_bound {sum_upper}, {(sum_upper / total_points)*100:.2f}%')
            print(f'Фактические продажи в рамках границ прогнозов {correct_points}, {(correct_points / total_points)*100:.2f}%')


    def plot_differences_in_predictions(self):
        y_day_pred_series = pd.Series(self.y_pred, index=np.arange(0, len(self.y_test)))
        fig, axs = plt.subplots(2, figsize=(10,8))
        axs[0].plot(y_day_pred_series.index, (self.y_test - y_day_pred_series.values), label='difference', color='b', linestyle='-', marker='x')
        axs[1].plot(y_day_pred_series.index, ((self.y_test - y_day_pred_series.values) / self.y_test)*100, label='difference %', color='r', linestyle='-', marker='o')
        axs[1].hlines(-50, 0, len(self.y_test), linestyles='--', label='-50%')
        axs[1].hlines(50, 0, len(self.y_test), linestyles='--', label='+50%')
        axs[1].hlines(-100, 0, len(self.y_test), linestyles='--', label='-100%')
        axs[1].hlines(100, 0, len(self.y_test), linestyles='--', label='+100%')

        if self.margin_of_error is None:
            axs[0].hlines(-100000, 0, len(self.y_test), linestyles='--', label='-100k', color='g')
            axs[0].hlines(100000, 0, len(self.y_test), linestyles='--', label='+100k', color='g')
        else:
            axs[0].hlines(-self.margin_of_error, 0, len(self.y_test), linestyles='--', label=f'-{self.margin_of_error/ 1000:.0f}k moe', color='g')
            axs[0].hlines(self.margin_of_error, 0, len(self.y_test), linestyles='--', label=f'+{self.margin_of_error/ 1000:.0f}k moe', color='g')

        axs[0].hlines(-500000, 0, len(self.y_test), linestyles='--', label='-500k', color='r')
        axs[0].hlines(500000, 0, len(self.y_test), linestyles='--', label='+500k', color='r')

        axs[0].legend()
        axs[1].legend()
        plt.plot

    def count_points_diff(self, points = [5, 10, 15, 25, 50, 75, 100, 200]):
        y_day_pred_series = pd.Series(self.y_pred, index=self.y_test.index)
        diff = abs((self.y_test - y_day_pred_series.values) / self.y_test)*100
        print(f'Всего точек для прогноза {len(self.y_test)}')
        for threshold in points:
            sum_dif = sum(diff > threshold)
            print(f'В результатах прогноза {sum_dif} точек имеют разницу с фактов более {threshold}%')