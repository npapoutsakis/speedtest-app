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

# 2 PLOTS TOTAL
def throughput_evaluation():
    
    for file, scenario in zip(SPEEDTEST_FILES, SCENARIOS):
        df = pd.read_csv(file)
        
        interval_data = df[df['Type'] == 'INTERVAL']
        aggregated_throughput = df[df['Type'] == 'AGGREGATED'].iloc[0]
        
        plt.figure(figsize=(10, 4))
        plt.plot(interval_data['IntervalStart_s'], interval_data['Throughput_Mbps'], marker='o', label='Throughput (Mbps)')
        plt.axhline(y=aggregated_throughput['Throughput_Mbps'], color='r', linestyle='--', label=f'Avg: {aggregated_throughput["Throughput_Mbps"]:.2f} Mbps', linewidth=0.8)

        plt.xticks(interval_data['IntervalStart_s'])
        plt.ylim(0, 175)
        plt.title(f'Throughput - {scenario}')
        plt.xlabel('Time (s)')
        plt.ylabel('Throughput (Mbps)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'./plots/throughput_evaluation/{scenario}.png', dpi=300)

        # save the statistics
        f = open(f'./statistics/throughput_evaluation/{scenario}.txt', 'w')
        f.write(f'=== Scenario: {scenario} ===\n')
        f.write(interval_data['Throughput_Mbps'].describe().to_string())
        f.close()

    return



"""
    This function will verify the throughput between SpeedTest & Iperf 
"""
# REMOVE MEAN LINE
# 6 PLOTS TOTAL
def throughput_verification():

    for iperf_file, speedtest, scenario in zip(IPERF_FILES, SPEEDTEST_FILES, SCENARIOS):
            
        df_speedtest = pd.read_csv(speedtest)
        speedtest_intervals = df_speedtest[df_speedtest['Type'] == 'INTERVAL']
        speedtest_agg = df_speedtest[df_speedtest['Type'] == 'AGGREGATED'].iloc[0]

        df_iperf = pd.read_csv(iperf_file)
        iperf_intervals = df_iperf[df_iperf['Type'] == 'INTERVAL']
        iperf_agg = df_iperf[df_iperf['Type'] == 'AGGREGATED'].iloc[0]

        plt.figure(figsize=(10, 4))
        plt.plot(speedtest_intervals['IntervalStart_s'], speedtest_intervals['Throughput_Mbps'], marker='o', label='SpeedTest (Mbps)')
        plt.plot(iperf_intervals['IntervalStart_s'], iperf_intervals['Throughput_Mbps'], marker='o', label='Iperf (Mbps)')
        plt.axhline(y=speedtest_agg['Throughput_Mbps'], color='r', linestyle='--', label=f'SpeedTest Avg: {speedtest_agg["Throughput_Mbps"]:.2f} Mbps', linewidth=0.8)
        plt.axhline(y=iperf_agg['Throughput_Mbps'], color='g', linestyle='--', label=f'Iperf Avg: {iperf_agg["Throughput_Mbps"]:.2f} Mbps', linewidth=0.8)
        plt.xticks(speedtest_intervals['IntervalStart_s'])
        plt.ylim(0, 175)
        plt.title(f'Throughput - {scenario}')
        plt.xlabel('Time (s)')
        plt.ylabel('Throughput (Mbps)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f'./plots/throughput_verification/{scenario}.png', dpi=300)
        plt
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
        plt.plot(time, df_sniff['mean_throughput'], marker='o', label='Wi-Fi Doctor (Mbps)')
        plt.plot(df_speedtest_intervals['IntervalStart_s'], df_speedtest_intervals['Throughput_Mbps'], marker='o', label='SpeedTest App')
        
        plt.title(f"Throughput Comparison - {scenario}")
        plt.xlabel("Time (s)")
        plt.ylabel("Throughput (Mbps)")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f'./plots/throughput_estimation/throughput_comparison_{scenario}.png', dpi=300)


        # Plot metrics
        fig, axs = plt.subplots(4, 1, figsize=(12, 12), sharex=True)
        axs[0].plot(time, df_sniff['mean_data_rate'], marker='o', color='b', label='Mean Data Rate (Mbps)')
        axs[0].set_ylabel('Data Rate (Mbps)')
        axs[0].set_xlable('Time (s)')
        axs[0].legend() 
        axs[0].grid(True)
        
        axs[1].plot(time, df_sniff['retry_percentage'], marker='o', color='r', label='Frame Loss Rate (%)')
        axs[1].set_ylabel('Frame Loss Rate (%)')
        axs[1].set_xlable('Time (s)')
        axs[1].legend()
        axs[1].grid(True)
        
        axs[2].plot(time, df_sniff['most_common_rssi'], marker='o', color='g', label='RSSI (dBm)')
        axs[2].set_ylabel('RSSI (dBm)')
        axs[2].set_xlable('Time (s)')
        axs[2].legend()
        axs[2].grid(True)
        
        axs[3].plot(time, df_sniff['mean_rate_gap'], marker='o', color='m', label='Rate Gap')
        axs[3].set_ylabel('Rate Gap')
        axs[3].set_xlabel('Time (s)')
        axs[3].legend()
        axs[3].grid(True)
        
        plt.suptitle(f"Wi-Fi Doctor Metrics - {scenario}")
        plt.tight_layout(rect=[0, 0, 1, 0.97])
        plt.savefig(f'./plots/throughput_estimation/metrics_{scenario}.png', dpi=300)


    return


def delete_old_plots():

    directories = [
        './plots/throughput_evaluation/',
        './plots/throughput_verification/',
        './plots/throughput_estimation/'
    ]

    for directory in directories:
        files = glob.glob(os.path.join(directory, '*'))
        for file in files:
            os.remove(file)



def main():
    # throughput_evaluation()
    # throughput_verification()
    # throughput_estimation()
    delete_old_plots()
    return




if __name__ == "__main__":
    main()