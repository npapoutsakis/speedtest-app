import re
import pandas as pd

def parse_and_split_iperf_txt(txt_file, prefix):
    with open(txt_file, "r") as f:
        lines = f.readlines()

    interval_pattern = re.compile(
        r"\[\s*\d+\]\s+([\d\.]+)-([\d\.]+)\s+sec\s+[\d\.]+\s+MBytes\s+([\d\.]+)\s+Mbits/sec"
    )
    summary_pattern = re.compile(
        r"\[\s*\d+\]\s+0\.00-([\d\.]+)\s+sec\s+[\d\.]+\s+MBytes\s+([\d\.]+)\s+Mbits/sec"
    )
    test_start_pattern = re.compile(r"Server listening on 5201 \(test #(\d+)\)")
    test_map = {1: "1m", 2: "10m", 3: "moving"}
    current_test = 0
    intervals = []
    summary_row = None

    for line in lines:
        test_start = test_start_pattern.search(line)
        if test_start:
            # At new test, write previous test if any
            if current_test and intervals and summary_row:
                write_csv(prefix, test_map[current_test], intervals, summary_row)
                intervals = []
                summary_row = None
            current_test = int(test_start.group(1))
        match = interval_pattern.search(line)
        if match and current_test:
            start = float(match.group(1))
            end = float(match.group(2))
            # Only include strict 2s steps in [0,30]
            if start % 2 == 0 and end - start == 2.0 and end <= 30.0:
                intervals.append([
                    "INTERVAL",
                    start,
                    end,
                    float(match.group(3)),
                ])
        summary_match = summary_pattern.search(line)
        if summary_match and current_test:
            # Always take the last summary in each test
            summary_row = [
                "AGGREGATED",
                0.0,
                float(summary_match.group(1)),
                float(summary_match.group(2)),
            ]
    # Write last test
    if current_test and intervals and summary_row:
        write_csv(prefix, test_map[current_test], intervals, summary_row)

def write_csv(prefix, scenario, intervals, summary_row):
    df = pd.DataFrame(intervals + [summary_row], columns=[
        "Type", "IntervalStart_s", "IntervalEnd_s", "Throughput_Mbps"
    ])
    filename = f"./metrics/iperf/data/{prefix}_{scenario}.csv"
    df.to_csv(filename, index=False)
    print(f"Written: {filename}")


if __name__ == "__main__":
    parse_and_split_iperf_txt("./metrics/iperf/5ghz.txt", "5ghz")
    parse_and_split_iperf_txt("./metrics/iperf/2_4ghz.txt", "2_4ghz")
