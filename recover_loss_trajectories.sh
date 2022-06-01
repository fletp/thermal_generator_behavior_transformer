find . -name output.log > experiments/output_logs.txt
xargs -d '\n' grep -i "training summary:" < experiments/output_logs.txt > experiments/training_summaries.txt
xargs -d '\n' grep -i "validation summary:" < experiments/output_logs.txt > experiments/validation_summaries.txt
xargs -d '\n' grep -i "total runtime:" < experiments/output_logs.txt > experiments/time_summaries.txt