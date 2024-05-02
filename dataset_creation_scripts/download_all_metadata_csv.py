from datasets import load_dataset
from tqdm import tqdm
import pandas as pd

categories = ['raw_meta_Subscription_Boxes', 'raw_meta_All_Beauty', 'raw_meta_Toys_and_Games', 'raw_meta_Cell_Phones_and_Accessories', 'raw_meta_Industrial_and_Scientific', 'raw_meta_Gift_Cards', 'raw_meta_Musical_Instruments', 'raw_meta_Electronics', 'raw_meta_Handmade_Products', 'raw_meta_Arts_Crafts_and_Sewing', 'raw_meta_Baby_Products', 'raw_meta_Health_and_Household', 'raw_meta_Office_Products', 'raw_meta_Digital_Music', 'raw_meta_Grocery_and_Gourmet_Food', 'raw_meta_Sports_and_Outdoors', 'raw_meta_Home_and_Kitchen',  'raw_meta_Tools_and_Home_Improvement', 'raw_meta_Pet_Supplies', 'raw_meta_Video_Games', 'raw_meta_Kindle_Store', 'raw_meta_Clothing_Shoes_and_Jewelry', 'raw_meta_Patio_Lawn_and_Garden', 'raw_meta_Unknown', 'raw_meta_Books', 'raw_meta_Automotive', 'raw_meta_CDs_and_Vinyl', 'raw_meta_Beauty_and_Personal_Care', 'raw_meta_Electronics', 'raw_meta_Amazon_Fashion', 'raw_meta_Software', 'raw_meta_Health_and_Personal_Care', 'raw_meta_Appliances', 'raw_meta_Movies_and_TV'] 

print('Number of categories', len(categories))

queries_amazon_review_sample_good = pd.read_json('../other_datasets/queries_amazon_review_sample_good.json', lines=True)
df_examples = pd.read_parquet('../other_datasets/shopping_queries_dataset_examples.parquet')
query_asins = set(queries_amazon_review_sample_good['item_id'].unique())
esci_dataset_all_product_ids = set(df_examples['product_id'])
query_asins_minus_esci_dataset = query_asins.difference(esci_dataset_all_product_ids)
print(len(query_asins_minus_esci_dataset))

count = 0 

for group in tqdm(categories):
    
    try: 
        dataset = load_dataset("McAuley-Lab/Amazon-Reviews-2023", group, split="full")
        dataset = dataset.to_pandas()
        dataset.drop(columns=['categories', 'bought_together', 'subtitle', 'author', 'price', 'store'], inplace=True)

        query_asin_metadata = dataset[dataset['parent_asin'].isin(query_asins_minus_esci_dataset)]

        print(group)
        print('original length', len(dataset))
        dataset = dataset[dataset['title'].str.len() >= 5]
        print('removing title < 5', len(dataset))
        dataset = dataset[dataset['features'].apply(lambda x: len(x) != 0)]
        print('removing empty features', len(dataset))
        dataset = dataset[dataset['description'].apply(lambda x: len(x) != 0)]
        print('removing empty description', len(dataset))
        dataset = dataset[dataset['details'] != '{}']
        print('removing empty details', len(dataset))
        dataset = dataset.dropna()
        print('removing rows with nan', len(dataset))

        combined_df = pd.concat([dataset, query_asin_metadata], ignore_index=True)
        combined_df = combined_df.drop_duplicates(subset=['parent_asin'])

        print('after combining with query_asin_metadata', len(combined_df))

        combined_df = combined_df.astype(str)

        if len(combined_df) != 0:
            combined_df.to_csv("../downloaded_amazon_meta_datasets_csv/" + group + ".csv", index=False) 

        del query_asin_metadata
        del dataset
        del combined_df

    except:
        print('Didnt work for ', group)
        count+=1 
        
print(count)