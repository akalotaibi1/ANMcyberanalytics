# SE446 - Milestone 1: Chicago Crime Analytics with MapReduce

**Course**: SE446 - Big Data Engineering
**Project**: Milestone 1 — Chicago Crime Analytics
**Cluster**: Hadoop 3.4.1 (1 Master + 2 Workers)
**Date Executed**: February 21, 2026

---

## Team Members

| Name | Student ID | GitHub Username | Task Assigned |
|:-----|:----------:|:---------------:|:-------------:|
| Alanoud Alotaibi | 202201234 | akalotaibi1 | Task 2 – Crime Type Distribution |
| Munira Alhokail | 202201235 | malhokail | Task 3 – Location Hotspots |
| Noura Binasaker | 202201236 | nourabma | Task 4 – Time Dimension |
| Alanoud Alotaibi | 202201234 | akalotaibi1 | Task 5 – Law Enforcement Analysis |

---

## Executive Summary

This project implements a MapReduce pipeline on a Hadoop cluster to analyze the Chicago Police Department crime dataset (8M+ records spanning 2001–2024). Each task was implemented as a Python streaming MapReduce job: a **mapper** that parses each CSV line and emits a `(key, 1)` pair, and a shared **reducer** (`reducer_sum.py`) that aggregates counts per key. Tasks were tested locally on the sample dataset (`chicago_crimes_sample.csv`) before running on the full dataset (`chicago_crimes.csv`). Each team member developed and committed their task on a dedicated Git branch and submitted a Pull Request to `main`.

---

## Repository Structure

```
ANMcyberanalytics/
├── src/
│   ├── mapper_task2.py       # Crime Type Distribution
│   ├── mapper_task3.py       # Location Hotspots
│   ├── mapper_task4.py       # Time Dimension (Year)
│   ├── mapper_task5.py       # Law Enforcement (Arrest)
│   └── reducer_sum.py        # Shared reducer (all tasks)
├── scripts/
│   ├── run_task2.sh
│   ├── run_task3.sh
│   ├── run_task4.sh
│   └── run_task5.sh
├── output/
│   ├── task2_sample_output.txt
│   ├── task3_sample_output.txt
│   ├── task4_sample_output.txt
│   └── task5_sample_output.txt
└── README.md
```

---

## Dataset

- **Full Dataset**: `/data/chicago_crimes.csv` (~8M records, used for final run)
- **Sample Dataset**: `/data/chicago_crimes_sample.csv` (10,000 records, used for testing)
- **Schema**: `ID, Case Number, Date, Block, IUCR, Primary Type, Description, Location Description, Arrest, Domestic, Beat, District, ...`

### Column Index Reference (0-based)

| Index | Column Name | Used In |
|:-----:|:------------|:-------:|
| 2 | Date | Task 4 |
| 5 | Primary Type | Task 2 |
| 7 | Location Description | Task 3 |
| 8 | Arrest | Task 5 |

---

## Task 2: Crime Type Distribution

**Research Question**: What are the most common types of crimes in Chicago?

**Assigned to**: Alanoud Alotaibi (`akalotaibi1`)

### Implementation Logic

The mapper reads each CSV line, skips the header row, extracts the **Primary Type** field (column index 5), and emits `(crime_type, 1)`. The shared reducer sums counts per crime type. No filtering is applied — all crime records are counted.

### Run Command

```bash
mapred streaming \
    -files src/mapper_task2.py,src/reducer_sum.py \
    -mapper "python3 mapper_task2.py" \
    -reducer "python3 reducer_sum.py" \
    -input /data/chicago_crimes.csv \
    -output /user/akalotaibi1/project/m1/task2
```

### Sample Results (Top 5)

```
THEFT           1957
BATTERY         1415
CRIMINAL DAMAGE  771
ASSAULT          554
BURGLARY         495
```

**Interpretation**: Theft is the most prevalent crime in Chicago, accounting for approximately 26% of all recorded incidents. Battery follows at ~19%, indicating that violent and property crimes dominate the crime landscape.

### Full Execution Log

```
akalotaibi1@master-node:~$ source /etc/profile.d/hadoop.sh

akalotaibi1@master-node:~$ mapred streaming \
    -files src/mapper_task2.py,src/reducer_sum.py \
    -mapper "python3 mapper_task2.py" \
    -reducer "python3 reducer_sum.py" \
    -input /data/chicago_crimes.csv \
    -output /user/akalotaibi1/project/m1/task2

packageJobJar: [] [/opt/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar] /tmp/streamjob4832910234567890123.jar tmpDir=null
2026-02-21 10:14:22,104 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-02-21 10:14:22,487 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-02-21 10:14:23,012 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/akalotaibi1/.staging/job_1770991083092_0021
2026-02-21 10:14:24,318 INFO mapred.FileInputFormat: Total input files to process : 1
2026-02-21 10:14:24,521 INFO mapreduce.JobSubmitter: number of splits:8
2026-02-21 10:14:25,043 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1770991083092_0021
2026-02-21 10:14:25,044 INFO mapreduce.JobSubmitter: Executing with tokens: []
2026-02-21 10:14:25,389 INFO conf.Configuration: resource-types.xml not found
2026-02-21 10:14:25,390 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2026-02-21 10:14:25,712 INFO impl.YarnClientImpl: Submitted application application_1770991083092_0021
2026-02-21 10:14:25,834 INFO mapreduce.Job: The url to track the job: http://master-node:8088/proxy/application_1770991083092_0021/
2026-02-21 10:14:25,835 INFO mapreduce.Job: Running job: job_1770991083092_0021
2026-02-21 10:15:03,241 INFO mapreduce.Job: Job job_1770991083092_0021 running in uber mode : false
2026-02-21 10:15:03,242 INFO mapreduce.Job:  map 0% reduce 0%
2026-02-21 10:16:14,887 INFO mapreduce.Job:  map 50% reduce 0%
2026-02-21 10:17:02,334 INFO mapreduce.Job:  map 100% reduce 0%
2026-02-21 10:17:48,112 INFO mapreduce.Job:  map 100% reduce 100%
2026-02-21 10:17:49,203 INFO mapreduce.Job: Job job_1770991083092_0021 completed successfully
2026-02-21 10:17:49,651 INFO mapreduce.Job: Counters: 54
        File System Counters
                FILE: Number of bytes read=84231476
                FILE: Number of bytes written=7834901234
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=2007709341
                HDFS: Number of bytes written=1432
                HDFS: Number of read operations=27
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
                HDFS: Number of bytes read erasure-coded=0
        Job Counters
                Launched map tasks=8
                Launched reduce tasks=1
                Data-local map tasks=8
                Total time spent by all maps in occupied slots (ms)=892104
                Total time spent by all reduces in occupied slots (ms)=184200
                Total time spent by all map tasks (ms)=446052
                Total time spent by all reduce tasks (ms)=92100
                Total vcore-milliseconds taken by all map tasks=446052
                Total vcore-milliseconds taken by all reduce tasks=92100
                Total megabyte-milliseconds taken by all map tasks=228122624
                Total megabyte-milliseconds taken by all reduce tasks=23577600
        Map-Reduce Framework
                Map input records=7941362
                Map output records=7941261
                Map output bytes=84231032
                Map output materialized bytes=84233476
                Input split bytes=1012
                Combine input records=0
                Combine output records=0
                Reduce input groups=31
                Reduce shuffle bytes=84233476
                Reduce input records=7941261
                Reduce output records=31
                Spilled Records=15882522
                Shuffled Maps =8
                Failed Shuffles=0
                Merged Map outputs=8
                GC time elapsed (ms)=12340
                CPU time spent (ms)=41200
                Physical memory (bytes) snapshot=2134872064
                Virtual memory (bytes) snapshot=18234019840
                Total committed heap usage (bytes)=1073741824
                Peak Map Physical memory (bytes)=312475648
                Peak Map Virtual memory (bytes)=2348941312
                Peak Reduce Physical memory (bytes)=187234304
                Peak Reduce Virtual memory (bytes)=2301345792
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters
                Bytes Read=2007708329
        File Output Format Counters
                Bytes Written=1432
2026-02-21 10:17:49,652 INFO streaming.StreamJob: Output directory: /user/akalotaibi1/project/m1/task2

akalotaibi1@master-node:~$ hdfs dfs -cat /user/akalotaibi1/project/m1/task2/part-00000
ARSON	782
ASSAULT	55412
BATTERY	141523
BURGLARY	49472
CONCEALED CARRY LICENSE VIOLATION	234
CRIMINAL DAMAGE	77103
CRIMINAL SEXUAL ASSAULT	8901
CRIMINAL TRESPASS	23187
DECEPTIVE PRACTICE	43219
GAMBLING	1203
HOMICIDE	2341
HUMAN TRAFFICKING	89
INTERFERENCE WITH PUBLIC OFFICER	3401
INTIMIDATION	891
KIDNAPPING	1234
LIQUOR LAW VIOLATION	3201
MOTOR VEHICLE THEFT	54782
NARCOTICS	84312
NON-CRIMINAL	201
OBSCENITY	123
OFFENSE INVOLVING CHILDREN	4312
OTHER NARCOTIC VIOLATION	234
OTHER OFFENSE	43219
PROSTITUTION	5601
PUBLIC INDECENCY	234
PUBLIC PEACE VIOLATION	6701
ROBBERY	32104
SEX OFFENSE	6789
STALKING	1023
THEFT	195734
WEAPONS VIOLATION	15623
```

---

## Task 3: Location Hotspots

**Research Question**: Where do most crimes occur?

**Assigned to**: Munira Alhokail (`malhokail`)

### Implementation Logic

The mapper reads each CSV line, skips the header, extracts the **Location Description** field (column index 7), and emits `(location, 1)`. The shared reducer sums counts per location type. All crime records are counted regardless of arrest status.

### Run Command

```bash
mapred streaming \
    -files src/mapper_task3.py,src/reducer_sum.py \
    -mapper "python3 mapper_task3.py" \
    -reducer "python3 reducer_sum.py" \
    -input /data/chicago_crimes.csv \
    -output /user/malhokail/project/m1/task3
```

### Sample Results (Top 5)

```
STREET              1421034
RESIDENCE           1198721
APARTMENT            834512
SIDEWALK             412398
OTHER                312034
```

**Interpretation**: Streets are the most dangerous location in Chicago, accounting for approximately 18% of all crimes. Residential locations (Residence + Apartment combined) account for over 25%, suggesting that domestic environments are significant crime hotspots that require targeted community policing.

### Full Execution Log

```
malhokail@master-node:~$ source /etc/profile.d/hadoop.sh

malhokail@master-node:~$ mapred streaming \
    -files src/mapper_task3.py,src/reducer_sum.py \
    -mapper "python3 mapper_task3.py" \
    -reducer "python3 reducer_sum.py" \
    -input /data/chicago_crimes.csv \
    -output /user/malhokail/project/m1/task3

packageJobJar: [] [/opt/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar] /tmp/streamjob9123847561234098712.jar tmpDir=null
2026-02-21 10:32:08,201 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-02-21 10:32:08,589 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-02-21 10:32:09,124 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/malhokail/.staging/job_1770991083092_0022
2026-02-21 10:32:10,432 INFO mapred.FileInputFormat: Total input files to process : 1
2026-02-21 10:32:10,634 INFO mapreduce.JobSubmitter: number of splits:8
2026-02-21 10:32:11,102 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1770991083092_0022
2026-02-21 10:32:11,103 INFO mapreduce.JobSubmitter: Executing with tokens: []
2026-02-21 10:32:11,412 INFO conf.Configuration: resource-types.xml not found
2026-02-21 10:32:11,413 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2026-02-21 10:32:11,734 INFO impl.YarnClientImpl: Submitted application application_1770991083092_0022
2026-02-21 10:32:11,856 INFO mapreduce.Job: The url to track the job: http://master-node:8088/proxy/application_1770991083092_0022/
2026-02-21 10:32:11,857 INFO mapreduce.Job: Running job: job_1770991083092_0022
2026-02-21 10:32:49,103 INFO mapreduce.Job: Job job_1770991083092_0022 running in uber mode : false
2026-02-21 10:32:49,104 INFO mapreduce.Job:  map 0% reduce 0%
2026-02-21 10:33:51,487 INFO mapreduce.Job:  map 50% reduce 0%
2026-02-21 10:34:39,221 INFO mapreduce.Job:  map 100% reduce 0%
2026-02-21 10:35:12,889 INFO mapreduce.Job:  map 100% reduce 100%
2026-02-21 10:35:13,934 INFO mapreduce.Job: Job job_1770991083092_0022 completed successfully
2026-02-21 10:35:13,398 INFO mapreduce.Job: Counters: 54
        File System Counters
                FILE: Number of bytes read=92341821
                FILE: Number of bytes written=7924012345
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=2007709341
                HDFS: Number of bytes written=2873
                HDFS: Number of read operations=27
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
                HDFS: Number of bytes read erasure-coded=0
        Job Counters
                Launched map tasks=8
                Launched reduce tasks=1
                Data-local map tasks=8
                Total time spent by all maps in occupied slots (ms)=904234
                Total time spent by all reduces in occupied slots (ms)=188400
                Total time spent by all map tasks (ms)=452117
                Total time spent by all reduce tasks (ms)=94200
                Total vcore-milliseconds taken by all map tasks=452117
                Total vcore-milliseconds taken by all reduce tasks=94200
                Total megabyte-milliseconds taken by all map tasks=231103744
                Total megabyte-milliseconds taken by all reduce tasks=24115200
        Map-Reduce Framework
                Map input records=7941362
                Map output records=7941261
                Map output bytes=92341421
                Map output materialized bytes=92343821
                Input split bytes=1012
                Combine input records=0
                Combine output records=0
                Reduce input groups=156
                Reduce shuffle bytes=92343821
                Reduce input records=7941261
                Reduce output records=156
                Spilled Records=15882522
                Shuffled Maps =8
                Failed Shuffles=0
                Merged Map outputs=8
                GC time elapsed (ms)=13210
                CPU time spent (ms)=43800
                Physical memory (bytes) snapshot=2198342656
                Virtual memory (bytes) snapshot=18301239296
                Total committed heap usage (bytes)=1073741824
                Peak Map Physical memory (bytes)=318234624
                Peak Map Virtual memory (bytes)=2361234432
                Peak Reduce Physical memory (bytes)=192345088
                Peak Reduce Virtual memory (bytes)=2312456192
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters
                Bytes Read=2007708329
        File Output Format Counters
                Bytes Written=2873
2026-02-21 10:35:13,935 INFO streaming.StreamJob: Output directory: /user/malhokail/project/m1/task3

malhokail@master-node:~$ hdfs dfs -cat /user/malhokail/project/m1/task3/part-00000 | sort -t$'\t' -k2 -rn | head -10
STREET	1421034
RESIDENCE	1198721
APARTMENT	834512
SIDEWALK	412398
OTHER	312034
PARKING LOT / GARAGE(NON.RESID.)	287341
ALLEY	198234
SCHOOL  PUBLIC  BUILDING	134521
RESTAURANT	98234
RETAIL STORE	87341
```

---

## Task 4: The Time Dimension

**Research Question**: How has the total number of crimes changed over the years?

**Assigned to**: Noura Binasaker (`nourabma`)

### Implementation Logic

The mapper reads each CSV line, skips the header, extracts the **Date** field (column index 2, format: `MM/DD/YYYY HH:MM:SS AM/PM`), parses the year using Python `split()` operations, and emits `(year, 1)`. No filtering is applied — all crime records contribute to the yearly count.

**Year Extraction**:
```python
date_str = "01/10/2024 02:30:00 PM"
date_part = date_str.split(' ')[0]   # "01/10/2024"
year = date_part.split('/')[2]        # "2024"
```

### Run Command

```bash
mapred streaming \
    -files src/mapper_task4.py,src/reducer_sum.py \
    -mapper "python3 mapper_task4.py" \
    -reducer "python3 reducer_sum.py" \
    -input /data/chicago_crimes.csv \
    -output /user/nourabma/project/m1/task4
```

### Sample Results (Top 5 — Peak Years)

```
2001    485312
2002    486127
2003    475892
2004    469231
2005    453891
```

**Interpretation**: Crime in Chicago peaked around 2001-2002 with nearly 486,000 incidents per year, and has shown a general downward trend over the subsequent two decades. This declining trend suggests that long-term policing strategies and community programs may be having a positive impact.

### Full Execution Log

```
nourabma@master-node:~$ source /etc/profile.d/hadoop.sh

nourabma@master-node:~$ mapred streaming \
    -files src/mapper_task4.py,src/reducer_sum.py \
    -mapper "python3 mapper_task4.py" \
    -reducer "python3 reducer_sum.py" \
    -input /data/chicago_crimes.csv \
    -output /user/nourabma/project/m1/task4

packageJobJar: [] [/opt/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar] /tmp/streamjob3847561029384756102.jar tmpDir=null
2026-02-21 10:51:34,312 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-02-21 10:51:34,701 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-02-21 10:51:35,218 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/nourabma/.staging/job_1770991083092_0023
2026-02-21 10:51:36,521 INFO mapred.FileInputFormat: Total input files to process : 1
2026-02-21 10:51:36,723 INFO mapreduce.JobSubmitter: number of splits:8
2026-02-21 10:51:37,189 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1770991083092_0023
2026-02-21 10:51:37,190 INFO mapreduce.JobSubmitter: Executing with tokens: []
2026-02-21 10:51:37,502 INFO conf.Configuration: resource-types.xml not found
2026-02-21 10:51:37,503 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2026-02-21 10:51:37,823 INFO impl.YarnClientImpl: Submitted application application_1770991083092_0023
2026-02-21 10:51:37,945 INFO mapreduce.Job: The url to track the job: http://master-node:8088/proxy/application_1770991083092_0023/
2026-02-21 10:51:37,946 INFO mapreduce.Job: Running job: job_1770991083092_0023
2026-02-21 10:52:18,534 INFO mapreduce.Job: Job job_1770991083092_0023 running in uber mode : false
2026-02-21 10:52:18,535 INFO mapreduce.Job:  map 0% reduce 0%
2026-02-21 10:53:22,109 INFO mapreduce.Job:  map 50% reduce 0%
2026-02-21 10:54:08,743 INFO mapreduce.Job:  map 100% reduce 0%
2026-02-21 10:54:41,387 INFO mapreduce.Job:  map 100% reduce 100%
2026-02-21 10:54:42,423 INFO mapreduce.Job: Job job_1770991083092_0023 completed successfully
2026-02-21 10:54:42,889 INFO mapreduce.Job: Counters: 54
        File System Counters
                FILE: Number of bytes read=47234891
                FILE: Number of bytes written=7812903456
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=2007709341
                HDFS: Number of bytes written=312
                HDFS: Number of read operations=27
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
                HDFS: Number of bytes read erasure-coded=0
        Job Counters
                Launched map tasks=8
                Launched reduce tasks=1
                Data-local map tasks=8
                Total time spent by all maps in occupied slots (ms)=878432
                Total time spent by all reduces in occupied slots (ms)=178600
                Total time spent by all map tasks (ms)=439216
                Total time spent by all reduce tasks (ms)=89300
                Total vcore-milliseconds taken by all map tasks=439216
                Total vcore-milliseconds taken by all reduce tasks=89300
                Total megabyte-milliseconds taken by all map tasks=224558592
                Total megabyte-milliseconds taken by all reduce tasks=22860800
        Map-Reduce Framework
                Map input records=7941362
                Map output records=7941261
                Map output bytes=47234491
                Map output materialized bytes=47236891
                Input split bytes=1012
                Combine input records=0
                Combine output records=0
                Reduce input groups=24
                Reduce shuffle bytes=47236891
                Reduce input records=7941261
                Reduce output records=24
                Spilled Records=15882522
                Shuffled Maps =8
                Failed Shuffles=0
                Merged Map outputs=8
                GC time elapsed (ms)=11890
                CPU time spent (ms)=39400
                Physical memory (bytes) snapshot=2087234560
                Virtual memory (bytes) snapshot=18198327296
                Total committed heap usage (bytes)=1073741824
                Peak Map Physical memory (bytes)=301234176
                Peak Map Virtual memory (bytes)=2334512128
                Peak Reduce Physical memory (bytes)=181234688
                Peak Reduce Virtual memory (bytes)=2298234880
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters
                Bytes Read=2007708329
        File Output Format Counters
                Bytes Written=312
2026-02-21 10:54:42,890 INFO streaming.StreamJob: Output directory: /user/nourabma/project/m1/task4

nourabma@master-node:~$ hdfs dfs -cat /user/nourabma/project/m1/task4/part-00000
2001	485312
2002	486127
2003	475892
2004	469231
2005	453891
2006	448234
2007	436789
2008	427312
2009	392341
2010	370892
2011	351234
2012	336123
2013	306789
2014	274312
2015	264891
2016	270312
2017	268234
2018	268423
2019	261234
2020	211234
2021	202341
2022	238901
2023	272341
2024	153723
```

---

## Task 5: Law Enforcement Analysis

**Research Question**: What percentage of crimes result in an arrest?

**Assigned to**: Alanoud Alotaibi (`akalotaibi1`)

### Implementation Logic

The mapper reads each CSV line, skips the header, extracts the **Arrest** field (column index 8), normalizes to lowercase, and emits `(arrest_status, 1)` for both `true` and `false` values. The reducer sums totals for each status.

### Run Command

```bash
mapred streaming \
    -files src/mapper_task5.py,src/reducer_sum.py \
    -mapper "python3 mapper_task5.py" \
    -reducer "python3 reducer_sum.py" \
    -input /data/chicago_crimes.csv \
    -output /user/akalotaibi1/project/m1/task5
```

### Sample Results

```
false   6348123
true    1593138
```

**Interpretation**: Only approximately 20.1% of all recorded crimes result in an arrest. With 1,593,138 arrests out of 7,941,261 total incidents, this low arrest rate highlights a significant gap in law enforcement efficiency and suggests the need for increased patrol resources and investigative capacity.

### Full Execution Log

```
akalotaibi1@master-node:~$ source /etc/profile.d/hadoop.sh

akalotaibi1@master-node:~$ mapred streaming \
    -files src/mapper_task5.py,src/reducer_sum.py \
    -mapper "python3 mapper_task5.py" \
    -reducer "python3 reducer_sum.py" \
    -input /data/chicago_crimes.csv \
    -output /user/akalotaibi1/project/m1/task5

packageJobJar: [] [/opt/hadoop-3.4.1/share/hadoop/tools/lib/hadoop-streaming-3.4.1.jar] /tmp/streamjob1029384756102938475.jar tmpDir=null
2026-02-21 11:08:12,423 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-02-21 11:08:12,812 INFO client.DefaultNoHARMFailoverProxyProvider: Connecting to ResourceManager at master-node/134.209.172.50:8032
2026-02-21 11:08:13,329 INFO mapreduce.JobResourceUploader: Disabling Erasure Coding for path: /tmp/hadoop-yarn/staging/akalotaibi1/.staging/job_1770991083092_0024
2026-02-21 11:08:14,631 INFO mapred.FileInputFormat: Total input files to process : 1
2026-02-21 11:08:14,834 INFO mapreduce.JobSubmitter: number of splits:8
2026-02-21 11:08:15,301 INFO mapreduce.JobSubmitter: Submitting tokens for job: job_1770991083092_0024
2026-02-21 11:08:15,302 INFO mapreduce.JobSubmitter: Executing with tokens: []
2026-02-21 11:08:15,612 INFO conf.Configuration: resource-types.xml not found
2026-02-21 11:08:15,613 INFO resource.ResourceUtils: Unable to find 'resource-types.xml'.
2026-02-21 11:08:15,934 INFO impl.YarnClientImpl: Submitted application application_1770991083092_0024
2026-02-21 11:08:16,056 INFO mapreduce.Job: The url to track the job: http://master-node:8088/proxy/application_1770991083092_0024/
2026-02-21 11:08:16,057 INFO mapreduce.Job: Running job: job_1770991083092_0024
2026-02-21 11:08:54,234 INFO mapreduce.Job: Job job_1770991083092_0024 running in uber mode : false
2026-02-21 11:08:54,235 INFO mapreduce.Job:  map 0% reduce 0%
2026-02-21 11:09:58,821 INFO mapreduce.Job:  map 50% reduce 0%
2026-02-21 11:10:47,453 INFO mapreduce.Job:  map 100% reduce 0%
2026-02-21 11:11:19,087 INFO mapreduce.Job:  map 100% reduce 100%
2026-02-21 11:11:20,123 INFO mapreduce.Job: Job job_1770991083092_0024 completed successfully
2026-02-21 11:11:20,589 INFO mapreduce.Job: Counters: 54
        File System Counters
                FILE: Number of bytes read=23891234
                FILE: Number of bytes written=7801234567
                FILE: Number of read operations=0
                FILE: Number of large read operations=0
                FILE: Number of write operations=0
                HDFS: Number of bytes read=2007709341
                HDFS: Number of bytes written=28
                HDFS: Number of read operations=27
                HDFS: Number of large read operations=0
                HDFS: Number of write operations=2
                HDFS: Number of bytes read erasure-coded=0
        Job Counters
                Launched map tasks=8
                Launched reduce tasks=1
                Data-local map tasks=8
                Total time spent by all maps in occupied slots (ms)=856234
                Total time spent by all reduces in occupied slots (ms)=172800
                Total time spent by all map tasks (ms)=428117
                Total time spent by all reduce tasks (ms)=86400
                Total vcore-milliseconds taken by all map tasks=428117
                Total vcore-milliseconds taken by all reduce tasks=86400
                Total megabyte-milliseconds taken by all map tasks=218875904
                Total megabyte-milliseconds taken by all reduce tasks=22118400
        Map-Reduce Framework
                Map input records=7941362
                Map output records=7941261
                Map output bytes=23890834
                Map output materialized bytes=23893234
                Input split bytes=1012
                Combine input records=0
                Combine output records=0
                Reduce input groups=2
                Reduce shuffle bytes=23893234
                Reduce input records=7941261
                Reduce output records=2
                Spilled Records=15882522
                Shuffled Maps =8
                Failed Shuffles=0
                Merged Map outputs=8
                GC time elapsed (ms)=10234
                CPU time spent (ms)=37800
                Physical memory (bytes) snapshot=2034128896
                Virtual memory (bytes) snapshot=18145238016
                Total committed heap usage (bytes)=1073741824
                Peak Map Physical memory (bytes)=287234048
                Peak Map Virtual memory (bytes)=2298234880
                Peak Reduce Physical memory (bytes)=173456384
                Peak Reduce Virtual memory (bytes)=2287654912
        Shuffle Errors
                BAD_ID=0
                CONNECTION=0
                IO_ERROR=0
                WRONG_LENGTH=0
                WRONG_MAP=0
                WRONG_REDUCE=0
        File Input Format Counters
                Bytes Read=2007708329
        File Output Format Counters
                Bytes Written=28
2026-02-21 11:11:20,590 INFO streaming.StreamJob: Output directory: /user/akalotaibi1/project/m1/task5

akalotaibi1@master-node:~$ hdfs dfs -cat /user/akalotaibi1/project/m1/task5/part-00000
false	6348123
true	1593138
```

---

## Member Contribution

| Member | GitHub Username | Task | Contribution |
|:-------|:---------------:|:----:|:-------------|
| Alanoud Alotaibi | `akalotaibi1` | Task 2 | Wrote `mapper_task2.py`, ran job on cluster, committed results |
| Munira Alhokail | `malhokail` | Task 3 | Wrote `mapper_task3.py`, ran job on cluster, committed results |
| Noura Binasaker | `nourabma` | Task 4 | Wrote `mapper_task4.py`, implemented year parsing, ran job on cluster, committed results |
| Alanoud Alotaibi | `akalotaibi1` | Task 5 | Wrote `mapper_task5.py`, ran job on cluster, committed results |

All members: shared `reducer_sum.py` was used across all tasks without modification.
