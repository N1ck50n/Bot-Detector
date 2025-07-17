import re
from datetime import datetime, timedelta

logFile = "sample-log.log"

def readLog():
    IPLayout = re.compile(r"^(\d+\.\d+\.\d+\.\d+)") 
    timeLayout = re.compile(r"\[(.*?)\]")

    IPCounts = {}
    IPTimes = {}

    try:
        with open(logFile, "r") as file:
            for line in file:
                IPmatch = IPLayout.match(line)
                timeMatch = timeLayout.search(line)

                if IPmatch:
                    ip = IPmatch.group(1)
                    IPCounts[ip] = IPCounts.get(ip, 0) + 1

                if timeMatch and IPmatch:
                    fullTimeRequest = timeMatch.group(1)
                    try:
                        timeRequest = datetime.strptime(fullTimeRequest, "%d/%m/%Y:%H:%M:%S")
                        IPTimes.setdefault(ip, []).append(timeRequest)
                    except ValueError:
                        continue  # skip malformed timestamps

    except FileNotFoundError:
        print(f"Could not find '{logFile}'")

    return IPCounts, IPTimes

def analyzeLog(IPCounts, IPTimes):
    print("🔎 IP Addresses with unusually high request counts (>10):")
    for ip, count in IPCounts.items():
        if count > 10:
            print(f"  🚩 {ip} made {count} requests")

    print("\n📈 IP Addresses with bursts (>=10 requests within 5 seconds):")
    timeInterval = 5  # seconds
    threshold = 10

    for ip, times in IPTimes.items():
        times.sort()
        start = 0
        for end in range(len(times)):
            while times[end] - times[start] > timedelta(seconds=timeInterval):
                start += 1
            requestCount = end - start + 1
            if requestCount >= threshold:
                print(f"  🚨 {ip} made {requestCount} requests within {timeInterval} seconds")
                break  # only show each IP once

def main():
    IPCounts, IPTimes = readLog()
    analyzeLog(IPCounts, IPTimes)

if __name__ == "__main__":
    main()
