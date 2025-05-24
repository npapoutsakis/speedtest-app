#  Visualizer
import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

SCENARIOS = [
    '2.4ghz-1m',
    '2.4ghz-10m',
    '2.4ghz-Moving',
    '5ghz-1m',
    '5ghz-10m',
    '5ghz-Moving',
]

IPERF_FILES = [
    './metrics/iperf/data/2_4ghz_1m.csv',
    './metrics/iperf/data/2_4ghz_10m.csv',
    './metrics/iperf/data/2_4ghz_moving.csv',
    './metrics/iperf/data/5ghz_1m.csv',
    './metrics/iperf/data/5ghz_10m.csv',
    './metrics/iperf/data/5ghz_moving.csv',
]

SPEEDTEST_FILES = [
    './metrics/server-side/thr_2ghz_1m.csv',
    './metrics/server-side/thr_2ghz_10m.csv',
    './metrics/server-side/thr_2ghz_moving.csv',
    './metrics/server-side/thr_5ghz_1m.csv',
    './metrics/server-side/thr_5ghz_10m.csv',
    './metrics/server-side/thr_5ghz_moving.csv',
]

SNIFFER_FILES = [
    './metrics/sniffer/agg_2ghz_1m.csv',
    './metrics/sniffer/agg_2ghz_10m.csv',
    './metrics/sniffer/agg_2ghz_moving.csv',
    './metrics/sniffer/agg_5ghz_1m.csv',
    './metrics/sniffer/agg_5ghz_10m.csv',
    './metrics/sniffer/agg_5ghz_moving.csv',
]


"""
    This function will evaluate the throughput of speedtest
"""
def throughput_evaluation():
    
    fig_2_4 = plt.figure(figsize=(12, 6))
    fig_5 = plt.figure(figsize=(12, 6))

    scenario_mapping = {
        '2.4ghz-1m': fig_2_4,
        '2.4ghz-10m': fig_2_4,
        '2.4ghz-Moving': fig_2_4,
        '5ghz-1m': fig_5,
        '5ghz-10m': fig_5,
        '5ghz-Moving': fig_5,
    }

    color = {
        '2.4ghz-1m': 'blue',
        '2.4ghz-10m': 'green',
        '2.4ghz-Moving': 'red',
        '5ghz-1m': 'blue',
        '5ghz-10m': 'green',
        '5ghz-Moving': 'red',
    }


    for file, scenario in zip(SPEEDTEST_FILES, SCENARIOS):
        df = pd.read_csv(file)
        interval_data = df[df['Type'] == 'INTERVAL']
        aggregated_throughput = df[df['Type'] == 'AGGREGATED'].iloc[0]
        fig = scenario_mapping[scenario].gca() # nai nai, gca() kai ola kala
        fig.plot(interval_data['IntervalStart_s'], interval_data['Throughput_Mbps'], color=color[scenario], marker='o', markersize=4, label=scenario)
        fig.axhline(y=aggregated_throughput['Throughput_Mbps'], color=color[scenario], linestyle='--', linewidth=0.8)
        fig.set_ylabel('Throughput (Mbps)')
        fig.set_xlabel('Time (s)')
        fig.legend(loc='upper right')
        fig.grid(True)
        fig.set_ylim(0, 175)
        
        # save the statistics
        f = open(f'./statistics/throughput_evaluation/{scenario}.txt', 'w')
        f.write(f'=== Scenario: {scenario} ===\n')
        f.write(interval_data['Throughput_Mbps'].describe().to_string())
        f.close()
    
    fig_2_4.suptitle('2.4GHz SpeedTest Throughput Evaluation')
    fig_2_4.tight_layout()
    fig_2_4.savefig('./plots/throughput_evaluation/thr_eval_2.4ghz.png', dpi=300)
    plt.close(fig_2_4)
    
    fig_5.suptitle('5GHz SpeedTest Throughput Evaluation')
    fig_5.tight_layout()
    fig_5.savefig('./plots/throughput_evaluation/thr_eval_5ghz.png', dpi=300)
    plt.close(fig_5)
        
    return


"""
    This function will verify the throughput between SpeedTest & Iperf 
"""
def throughput_verification():

    for iperf_file, speedtest, scenario in zip(IPERF_FILES, SPEEDTEST_FILES, SCENARIOS):
            
        df_speedtest = pd.read_csv(speedtest)
        speedtest_intervals = df_speedtest[df_speedtest['Type'] == 'INTERVAL']

        # average throughput for speedtest
        speedtest_agg = df_speedtest[df_speedtest['Type'] == 'AGGREGATED'].iloc[0]

        df_iperf = pd.read_csv(iperf_file)
        iperf_intervals = df_iperf[df_iperf['Type'] == 'INTERVAL']

        # average throughput for iperf
        iperf_agg = df_iperf[df_iperf['Type'] == 'AGGREGATED'].iloc[0]

        plt.figure(figsize=(10, 4))
        plt.plot(speedtest_intervals['IntervalStart_s'], speedtest_intervals['Throughput_Mbps'], marker='o', markersize=3, label='SpeedTest (Mbps)')
        plt.plot(iperf_intervals['IntervalStart_s'], iperf_intervals['Throughput_Mbps'], marker='o', markersize=3, label='Iperf (Mbps)')
        # plt.axhline(y=speedtest_agg['Throughput_Mbps'], color='r', linestyle='--', label=f'SpeedTest Avg: {speedtest_agg["Throughput_Mbps"]:.2f} Mbps', linewidth=0.8)
        # plt.axhline(y=iperf_agg['Throughput_Mbps'], color='g', linestyle='--', label=f'Iperf Avg: {iperf_agg["Throughput_Mbps"]:.2f} Mbps', linewidth=0.8)
        plt.xticks(speedtest_intervals['IntervalStart_s'])
        plt.ylim(0, 175)
        plt.title(f'Throughput - {scenario}')
        plt.xlabel('Time (s)')
        plt.ylabel('Throughput (Mbps)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'./plots/throughput_verification/{scenario}.png', dpi=300)
        plt.close()

        # save the statistics
        f = open(f'./statistics/throughput_verification/{scenario}-mean.txt', 'w')
        f.write(f'=== Scenario: {scenario} ===\n')
        f.write(f'SpeedTest Avg: {speedtest_agg["Throughput_Mbps"]:.2f} Mbps\n')
        f.write(f'Iperf Avg: {iperf_agg["Throughput_Mbps"]:.2f} Mbps\n')

    return


"""
    Active vs. Passive Throughput (SpeedTest vs. Sniffing)
"""
def throughput_estimation():
    
    for sniff_file, speedtest_file, scenario in zip(SNIFFER_FILES, SPEEDTEST_FILES, SCENARIOS):
        df_sniff = pd.read_csv(sniff_file)
        df_speedtest = pd.read_csv(speedtest_file)
        df_speedtest_intervals = df_speedtest[df_speedtest['Type'] == 'INTERVAL']
        time = df_sniff['time_bin']

        plt.figure(figsize=(12, 5))
        plt.plot(time, df_sniff['mean_throughput'], marker='o', markersize=4, label='Wi-Fi Doctor (Mbps)')
        plt.plot(df_speedtest_intervals['IntervalStart_s'], df_speedtest_intervals['Throughput_Mbps'], marker='o', markersize=4, label='SpeedTest App')
        
        plt.title(f"Throughput Comparison - {scenario}")
        plt.xlabel("Time (s)")
        plt.ylabel("Throughput (Mbps)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'./plots/throughput_estimation/thr_{scenario}.png', dpi=300)
        plt.close()


    # Plot the wi-fi doctor metrics for all scenarios
    metrics = [
        ("mean_data_rate", "Data Rate (Mbps)"),
        ("retry_percentage", "Frame Loss Rate (%)"),
        ("most_common_rssi", "RSSI (dBm)"),
        ("mean_rate_gap", "Rate Gap"),
    ]

    for metric, title in metrics:
        plt.figure(figsize=(12, 6))
        for sniff_file, scenario in zip(SNIFFER_FILES, SCENARIOS):
            df_sniff = pd.read_csv(sniff_file)
            time = df_sniff['time_bin']
            plt.plot(time, df_sniff[metric], marker='o', markersize=4, label=scenario)
    
        plt.title(title)
        plt.ylabel(title)
        plt.xlabel("Time (s)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'./plots/throughput_estimation/{metric}.png', dpi=300)
        plt.close()

    return


"""
    This function will delete all old plots in the specified directories
"""
def delete_old_plots():
    directories = [
        './plots/throughput_evaluation/',
        './plots/throughput_verification/',
        './plots/throughput_estimation/',
        './statistics/throughput_evaluation/',
        './statistics/throughput_verification/',
    ]

    for directory in directories:
        files = glob.glob(os.path.join(directory, '*'))
        for file in files:
            os.remove(file)



def main():
    # throughput_evaluation()
    # throughput_verification()
    # throughput_estimation()
    # delete_old_plots()
    return



if __name__ == "__main__":
    main()