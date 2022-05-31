import pandas as pd
import re

def extract_loss_cols(loss_log_df):
    loss_log_df['epoch'] = loss_log_df.raw.str.extract(r"((?<=epoch: )\d+)").astype(int)
    loss_log_df['loss'] = loss_log_df.raw.str.extract(r"((?<=loss: )[\d\.]+)").astype(float)
    loss_log_df['experiment_short_name'] = loss_log_df.raw.str.extract(r"((?<=experiments/).+(?=_2022))")
    loss_log_df = loss_log_df.set_index(['experiment_short_name', 'epoch']).sort_index()
    loss_log_df = loss_log_df[["loss", "raw"]]
    return loss_log_df


if __name__ == "__main__":
    train_loss_df = pd.read_csv('experiments/training_summaries.txt', names = ["raw"])
    val_loss_df = pd.read_csv('experiments/validation_summaries.txt', names = ["raw"])

    train_loss_df = extract_loss_cols(train_loss_df)
    val_loss_df = extract_loss_cols(val_loss_df)

    plot_df = pd.concat([train_loss_df, val_loss_df], axis = 0, keys=['train', 'val'])
    
    plot_df.to_csv('experiments/loss_trajectories.csv')