import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('sysjitter_data.csv')

avg_cyc = df['Cycles'].mean()
p99_cyc = df['Cycles'].quantile(0.99)

print(f"Average: {avg_cyc:.2f}")
print(f"99th Percentile: {p99_cyc:.2f}")

df_clean = df[df['Cycles'] < df['Cycles'].quantile(0.999)]

plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")

sns.histplot(df_clean['Cycles'], bins=120, kde=True, color='#2c3e50', alpha=0.7)

plt.axvline(avg_cyc, color='green', linestyle='--', linewidth=2, label=f'Avg: {avg_cyc:.0f}')
plt.axvline(p99_cyc, color='red', linestyle='--', linewidth=2, label=f'99%: {p99_cyc:.0f}')

plt.title('System Call Latency Distribution')
plt.xlabel('CPU Cycles')
plt.ylabel('Frequency')
plt.yscale('log')
plt.legend()

plt.savefig('latency_distribution.png', dpi=300)
print("Graph saved.")