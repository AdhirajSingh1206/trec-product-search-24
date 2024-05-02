# TREC Product search / Zero Shot IR Task Dataset

## Data generation method:

1. Download these 2 datasets and store them in a folder called 'other_datasets':
   - *queries_amazon_review_sample_good.json*
   - [*shopping_queries_dataset_examples.parquet*](https://github.com/amazon-science/esci-data/blob/main/shopping_queries_dataset/shopping_queries_dataset_examples.parquet) (This is take from the ESCI dataset)
2. Create an empty folder called *downloaded_amazon_meta_datasets_csv*:
   - Here we will save the csv files containing the meta data of products from each of the 34 sub cateogries of the [Amazon Reviews'23 Dataset](https://amazon-reviews-2023.github.io/index.html#)
3. Run *python dataset_creation_scripts/download_all_metadata_csv.py*:
   - This will download the above mentioned csv files using the HuggingFace datasets library.
4. Once the above scipt is done processing, run each cell of the *dataset_creation_scripts/creating_zero_shot_retrieval_task_dataset.ipynb*:
   - This will do some preprocessing and create a 3M large dataset containing products and their metadata.
   - It will save the final dataset in local as a parquet file and also push it to huggingface.
   - ![image](https://github.com/AdhirajSingh1206/trec-product-search-24/assets/38189805/cfe091c8-7fef-430d-928c-341b736d1b9e)

  ## Using the dataset: 

  1. Using the parquet file:
      ```python
          import pandas as pd
          
          dataset = pd.read_parquet('../zero_shot_retrieval_task_dataset.parquet')
          print(len(dataset))
          dataset.head()

2. Using Huggingface (Recommneded):
    ```python
        from datasets import load_dataset
        
        dataset = load_dataset("AdhirajSingh1206/TREC-Zero-Shot-Product-Search", split="full")
        dataset = dataset.to_pandas()
        print(len(dataset))
        dataset.head()
        
