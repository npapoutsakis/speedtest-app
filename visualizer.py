#  Visualizer

import pandas as pd
import matplotlib.pyplot as plt


SCENARIOS = [
    '5ghz-1m',
    '5ghz-10m',
    '5ghz-Moving',
]

IPERF_FILES = [
    './metrics/iperf/csv_output/iperf_5ghz_1m.csv',
    './metrics/iperf/csv_output/iperf_5ghz_10m.csv',
    './metrics/iperf/csv_output/iperf_5ghz_moving.csv',
]

SPEEDTEST_FILES = [
    './metrics/server-side/throughput_log_5ghz_1m.csv',
    './metrics/server-side/throughput_log_5ghz_10m.csv',
    './metrics/server-side/throughput_log_5ghz_moving.csv',
]


"""
    This function will evaluate the throughput of speedtest
"""
def throughput_evaluation():
    
    for file, scenario in zip(SPEEDTEST_FILES, SCENARIOS):
        df = pd.read_csv(file)
        
        interval_data = df[df['Type'] == 'INTERVAL']
        aggregated_throughput = df[df['Type'] == 'AGGREGATED'].iloc[0]
        
        plt.figure(figsize=(10, 4))
        plt.plot(interval_data['IntervalStart_s'], interval_data['Throughput_Mbps'], marker='o', label='Throughput (Mbps)')
        plt.axhline(y=aggregated_throughput['Throughput_Mbps'], color='r', linestyle='--', label=f'Avg: {aggregated_throughput["Throughput_Mbps"]:.2f} Mbps')

        plt.xticks(interval_data['IntervalStart_s'])
        plt.ylim(0, 450)
        plt.title(f'Throughput - {scenario}')
        plt.xlabel('Time (s)')
        plt.ylabel('Throughput (Mbps)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'./plots/throughput_evaluation/throughput_evaluation_{scenario}.png', dpi=300)

        # save the statistics
        f = open(f'./statistics/throughput_evaluation/throughput_evaluation_{scenario}.txt', 'w')
        f.write(f'=== Scenario: {scenario} ===\n')
        f.write(interval_data['Throughput_Mbps'].describe().to_string())
        f.close()

    return



"""
    This function will verify the throughput between SpeedTest & Iperf 
"""
def throughput_verification():

    for iperf_file, speedtest, scenario in zip(IPERF_FILES, SPEEDTEST_FILES, SCENARIOS):
        
        df_speedtest = pd.read_csv(speedtest)
        interval_data = df_speedtest[df_speedtest['Type'] == 'INTERVAL']
        aggregated_throughput = df_speedtest[df_speedtest['Type'] == 'AGGREGATED'].iloc[0]

        df_iperf = pd.read_csv(iperf_file)
        
        plt.figure(figsize=(10, 4))
        plt.plot(interval_data['IntervalStart_s'], interval_data['Throughput_Mbps'], marker='o', label='Throughput (Mbps)')
        plt.plot(df_iperf['start_time'], df_iperf['bitrate_mbps'], marker='o', label='Iperf Throughput (Mbps)')
        plt.axhline(y=aggregated_throughput['Throughput_Mbps'], color='r', linestyle='--', label=f'Avg: {aggregated_throughput["Throughput_Mbps"]:.2f} Mbps')
        plt.axhline(y=df_iperf['bitrate_mbps'].mean(), color='g', linestyle='--', label=f'Iperf Avg: {df_iperf["bitrate_mbps"].mean():.2f} Mbps')
        plt.xticks(interval_data['IntervalStart_s'])
        plt.ylim(0, 450)
        plt.title(f'Throughput - {scenario}')
        plt.xlabel('Time (s)')
        plt.ylabel('Throughput (Mbps)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'./plots/throughput_verification/throughput_verification_{scenario}.png', dpi=300)

    return


def throughput_estimation():
    """
        TODO
    """
    return




def main():
    throughput_evaluation()
    throughput_verification()
    return




if __name__ == "__main__":
    main()