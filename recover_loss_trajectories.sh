find . -name output.log > experiments/output_logs.txt
xargs -d '\n' grep -i "training summary:" < experiments/output_logs.txt | grep -i "cuda" > experiments/training_summaries.txt
xargs -d '\n' grep -i "validation summary:" < experiments/output_logs.txt | grep -i "cuda" > experiments/validation_summaries.txt