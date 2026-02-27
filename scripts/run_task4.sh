#!/bin/bash
# Task 4: Crime Trends by Year
# Run this script on the Hadoop cluster

source /etc/profile.d/hadoop.sh

# Delete output dir if it exists (for re-runs)
hdfs dfs -rm -r /user/${USER}/project/m1/task4 2>/dev/null

mapred streaming \
    -files ../src/mapper_task4.py,../src/reducer_sum.py \
    -mapper "python3 mapper_task4.py" \
    -reducer "python3 reducer_sum.py" \
    -input /data/chicago_crimes.csv \
    -output /user/${USER}/project/m1/task4

echo "=== Crime Counts by Year ==="
hdfs dfs -cat /user/${USER}/project/m1/task4/part-00000 | sort -k1
