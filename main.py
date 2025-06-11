import pandas as pd
from matplotlib import pyplot as plt

df= pd.read_csv("beers.csv")
breweries = pd.read_csv("breweries.csv")
# Merge brewery name into beers DataFrame
# breweries.csv index is the brewery_id, so set index for merge
breweries = breweries.rename(columns={"name": "brewery_name"})
df = df.merge(breweries[["brewery_name"]], left_on="brewery_id", right_index=True, how="left")

print(df.head(3))
#print(df["abv"].describe())

def count_unique_ids_per_style(df):
    result = df.groupby('style')['id'].nunique().sort_values(ascending=False)
    print(result.describe())
    # Group styles with count <= 3 into 'Other'
    mask = result <= 15
    if mask.any():
        other_sum = result[mask].sum()
        result = result[~mask]
        result['Other'] = other_sum
    print(result)
    plt.figure(figsize=(12, 6))
    total = result.sum()
    labels = [f"{name} {count / total * 100:.1f}%" if count > 40 else '' for name, count in result.items()]
    result.plot(kind='pie', labels=labels)
    plt.title('Number of Unique Beer IDs per Style')
    plt.ylabel('')  # Hide y-label for pie chart
    plt.tight_layout()
    plt.show()



def count_varieties_per_brewery(df):
    result = df.groupby('brewery_name')['name'].nunique().sort_values(ascending=False)
    print(result[:10])
    plt.figure(figsize=(12, 6))
    result[:10].plot(kind='bar')
    plt.title('Number of Unique Beer IDs per Brewery')
    plt.xlabel('Brewery')
    plt.ylabel('Number of Unique Beer IDs')
    plt.xticks(rotation=60)
    plt.tight_layout()
    plt.show()
    
def avg_abv_per_style_desc(df):
    result = df.groupby('style')['abv'].mean().sort_values(ascending=False) * 100
    print(result[:10])
    plt.figure(figsize=(12, 6))
    result[:10].plot(kind='bar')
    plt.title('Average ABV per Style')
    plt.xlabel('Style')
    plt.ylabel('Average ABV (%)')
    plt.xticks(rotation=45)
    # Add mean ABV values above each bar
    for i, v in enumerate(result[:10]):
        plt.text(i, v+0.01, f"{v:.1f}%", ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.show()


def avg_abv_per_style_asc(df):
    result = df.groupby('style')['abv'].mean().sort_values(ascending=True) * 100
    print(result[:10])
    plt.figure(figsize=(12, 6))
    result[:5].plot(kind='bar')
    plt.title('Average ABV per Style')
    plt.xlabel('Style')
    plt.ylabel('Average ABV (%)')
    plt.xticks(rotation=45)
    # Add mean ABV values above each bar
    for i, v in enumerate(result[:10]):
        plt.text(i, v+0.01, f"{v:.1f}%", ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.show()

def avg_ibu_per_style_asc(df):
    result = df.groupby('style')['ibu'].mean().sort_values(ascending=True)
    print(result[:10])
    plt.figure(figsize=(12, 6))
    result[:5].plot(kind='bar')
    plt.title('Average IBU per Style')
    plt.xlabel('Style')
    plt.ylabel('Average IBU')
    plt.xticks(rotation=45)
    # Add mean IBU values above each bar
    for i, v in enumerate(result[:5]):
        plt.text(i, v+0.01, f"{v:.1f}", ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.show()


def avg_ibu_per_style_desc(df):
    result = df.groupby('style')['ibu'].mean().sort_values(ascending=False)
    print(result[:10])
    plt.figure(figsize=(12, 6))
    result[:5].plot(kind='bar')
    plt.title('Average IBU per Style')
    plt.xlabel('Style')
    plt.ylabel('Average IBU')
    plt.xticks(rotation=45)
    # Add mean IBU values above each bar
    for i, v in enumerate(result[:5]):
        plt.text(i, v+0.01, f"{v:.1f}", ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.show()


def show_beers_info(df):
    print('beers.csv info:')
    print(f'Rows: {df.shape[0]}')
    print(f'Columns: {df.shape[1]}')
    print(f'Columns names: {list(df.columns)}')
    print()

def show_breweries_info(breweries):
    print('breweries.csv info:')
    print(f'Rows: {breweries.shape[0]}')
    print(f'Columns: {breweries.shape[1]}')
    print(f'Columns names: {list(breweries.columns)}')
    print()

def check_missing_data(df, name):
    print(f"Missing data in {name}:")
    missing = df.isnull().sum()
    print(missing[missing > 0] if missing.sum() > 0 else 'No missing data')
    print()

def abv_vs_popularity(df):
    # Calculate average ABV per style
    avg_abv = df.groupby('style')['abv'].mean()
    # Calculate number of unique beers per style
    popularity = df.groupby('style')['id'].nunique()
    # Merge into a single DataFrame
    summary = pd.DataFrame({'avg_abv': avg_abv * 100, 'num_beers': popularity})
    print(summary.sort_values('num_beers', ascending=False).head(10))
    plt.figure(figsize=(10, 6))
    # Scatter plot
    plt.scatter(summary['avg_abv'], summary['num_beers'], label='Styles')
    # Bin ABV values for standard deviation line
    bins = pd.cut(summary['avg_abv'], bins=10)
    std_popularity_per_bin = summary.groupby(bins)['num_beers'].std()
    bin_centers = [interval.mid for interval in std_popularity_per_bin.index]
    plt.plot(bin_centers, std_popularity_per_bin.values, color='red', marker='o', linestyle='-', label='Std Dev of Popularity')
    plt.xlabel('Average ABV (%)')
    plt.ylabel('Number of Unique Beers within the Style')
    plt.title('Std Dev of Popularity of Beer Style vs. Average ABV')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

def ibu_vs_popularity(df):
    # Remove rows with missing IBU values
    df_ibu = df.dropna(subset=['ibu'])
    # Calculate average IBU per style
    avg_ibu = df_ibu.groupby('style')['ibu'].mean()
    # Calculate number of unique beers per style
    popularity = df_ibu.groupby('style')['id'].nunique()
    # Merge into a single DataFrame
    summary = pd.DataFrame({'avg_ibu': avg_ibu, 'num_beers': popularity})
    print(summary.sort_values('num_beers', ascending=False).head(10))
    plt.figure(figsize=(10, 6))
    # Scatter plot
    plt.scatter(summary['avg_ibu'], summary['num_beers'], label='Styles')
    # Bin IBU values for standard deviation line
    bins = pd.cut(summary['avg_ibu'], bins=10)
    std_popularity_per_bin = summary.groupby(bins)['num_beers'].std()
    bin_centers = [interval.mid for interval in std_popularity_per_bin.index]
    plt.plot(bin_centers, std_popularity_per_bin.values, color='red', marker='o', linestyle='-', label='Std Dev of Popularity')
    plt.xlabel('Average IBU')
    plt.ylabel('Number of Unique Beers within the Style')
    plt.title('Std Dev of Popularity of Beer Style vs. Average IBU')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()

def show_brewery_info(brewery_name, breweries_df, beers_df):
    # Find the brewery row
    brewery_info = breweries_df[breweries_df['brewery_name'].str.lower() == brewery_name.lower()]
    if brewery_info.empty:
        print(f"No brewery found with name: {brewery_name}")
        return
    print("Brewery information:")
    print(brewery_info.T)
    print()
    # Find all beers for this brewery
    beers = beers_df[beers_df['brewery_name'].str.lower() == brewery_name.lower()]
    if beers.empty:
        print(f"No beers found for brewery: {brewery_name}")
    else:
        print(f"Beers from {brewery_name}:")
        print(beers.T)
    print()

def show_avg_abv_for_style(style_name, df):
    # Case-insensitive match for style
    mask = df['style'].str.lower() == style_name.lower()
    if not mask.any():
        print(f"No style found with name: {style_name}")
        return
    avg_abv = df.loc[mask, 'abv'].mean() * 100
    print(f"Average ABV for style '{style_name}': {avg_abv:.2f}%")

#show_beers_info(df)
#show_breweries_info(breweries)
#check_missing_data(df, 'beers.csv')
#check_missing_data(breweries, 'breweries.csv')
#count_unique_ids_per_style(df)
#count_varieties_per_brewery(df)
#show_brewery_info("Sun King Brewing Company", breweries, df)
#avg_abv_per_style_desc(df)
#avg_abv_per_style_asc(df)
#abv_vs_popularity(df)
#show_avg_abv_for_style("American Double / Imperial IPA", df)
#ibu_vs_popularity(df)
#avg_ibu_per_style_asc(df)
#avg_ibu_per_style_desc(df)
