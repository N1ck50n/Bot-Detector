import re
from datetime import datetime
from datetime import timedelta

logFile = "sample-log.log"

# Stores the IP Addresses in a dictionary with their respective counts.
IPCounts = {}

# Store the IP addresses with their respective times.
IPTimes = {}

def readLog():
    # Creates a layout of the IP addresses and the time for the request.
    IPLayout = re.compile(r"^(\d+\.\d+\.\d+\.\d+)") 
    timeLayout = re.compile(r"\[(.*?)\]")

    try:
        with open(logFile, "r") as file:
            for line in file:
                IPmatch = IPLayout.match(line)
                timeMatch = timeLayout.search(line)

                if IPmatch:
                    ip = IPmatch.group(1)
                    # Check if current IP is already stored in the IPCounts dictionary and update the frequency of it.
                    if ip in IPCounts:
                        IPCounts[ip] += 1
                    else:
                        IPCounts[ip] = 1

                if timeMatch:
                    fullTimeRequest = timeMatch.group(1)
                    timeRequest = datetime.strptime(fullTimeRequest, "%d/%m/%Y:%H:%M:%S")
                    
                    
                    if ip in IPTimes:
                        IPTimes[ip].append(timeRequest)
                    else:
                        IPTimes[ip] = [timeRequest]

                    
    except FileNotFoundError:
        print(f"Could not find '{logFile}'")

    return IPCounts, IPTimes

def analyzeLog(IPCounts, IPTimes):

    print("IP Adresses with unusual amount of requests: ")
    for ip, count in IPCounts.items():
        # Checks if an IP address appears more than 500 times, showing that it is probably not a user.
        if count > 500:
            print(f"{ip} : {count}")


    print("\nIP Addresses with suspicious quick repeated requests:")
    timeInterval = 5

    for ip, times in IPTimes.items():
        times.sort()
        start = 0
        
        for end in range(len(times)):
            # Move start pointer while time interval is more than 5 seconds.
            while times[end] - times[start] > timedelta(seconds=timeInterval):
                start += 1
           
            # Number of requests in the current window.
            requestCount = end - start + 1

            # Check if there are 10 or more requests in 5 seconds to detect burst repeated requests.
            if requestCount >= 10:
                print(f"{ip} made {requestCount} requests within 5 seconds")
                
                # Break to reduce excessive output.
                break  


def main():
    IPCounts, IPTimes = readLog()
    analyzeLog(IPCounts, IPTimes)

if __name__ == "__main__":
    main()
