import json
import numpy as np
import csv

# Function to load Google and Bing results from JSON files
def load_results(google_path, bing_path):
    with open(google_path, 'r') as google_file:
        google_results = json.load(google_file)
    with open(bing_path, 'r') as bing_file:
        bing_results = json.load(bing_file)
    return google_results, bing_results

# Function to find the overlapping results between Google and Bing for each query
def find_overlapping_results(google_results, bing_results):
    overlapping_results = {
        query: len(set(google_results[query]).intersection(bing_results.get(query, [])))
        for query in google_results if query in bing_results
    }
    return overlapping_results

# Function to compute the Spearman rank correlation coefficient for each query
def compute_spearman(google_results, bing_results):
    spearman_coefficients = {}
    
    for query in google_results:
        if query in bing_results:
            google_links = google_results[query]
            bing_links = bing_results[query]
            common_links = list(set(google_links) & set(bing_links))
            
            if len(common_links) == 0:
                continue
            
            google_ranks = [google_links.index(link) + 1 for link in common_links]
            bing_ranks = [bing_links.index(link) + 1 for link in common_links]
            
            n = len(common_links)
            if n == 1:
                if google_ranks[0] == bing_ranks[0]:
                    spearman_coefficient = 1
                else:
                    spearman_coefficient = 0
            elif n > 1:
                d_squared_sum = np.sum((np.array(google_ranks) - np.array(bing_ranks)) ** 2)
                spearman_coefficient = 1 - (6 * d_squared_sum) / (n * (n**2 - 1))
            else:
                spearman_coefficient = 0
             
            spearman_coefficients[query] = spearman_coefficient

    return spearman_coefficients

# Function to calculate averages of overlap counts, overlap percentages, and Spearman coefficients
def calculate_averages(overlapping_results, spearman_coefficients):
    total_overlap_count = 0
    total_overlap_percent = 0
    total_spearman_coefficient = 0
    num_queries = len(overlapping_results)
    
    for query in overlapping_results:
        overlap_count = overlapping_results[query]
        overlap_percent = 100 * (overlap_count / 10)
        spearman_coefficient = spearman_coefficients.get(query, 0)
        
        total_overlap_count += overlap_count
        total_overlap_percent += overlap_percent
        total_spearman_coefficient += spearman_coefficient
    
    if num_queries > 0:
        avg_overlap_count = total_overlap_count / num_queries
        avg_overlap_percent = total_overlap_percent / num_queries
        avg_spearman_coefficient = total_spearman_coefficient / num_queries
    else:
        avg_overlap_count = 0
        avg_overlap_percent = 0
        avg_spearman_coefficient = 0
    
    return avg_overlap_count, avg_overlap_percent, avg_spearman_coefficient

# Function to save the overlap and Spearman results to a CSV file
def save_results_to_csv(overlapping_results, spearman_coefficients, filename='results.csv'):
    avg_overlap_count, avg_overlap_percent, avg_spearman_coefficient = calculate_averages(overlapping_results, spearman_coefficients)
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['queries', 'overlapped count', '% overlap', 'coeff']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        for i, query in enumerate(overlapping_results, start=1):
            overlap_count = overlapping_results[query]
            overlap_percent = 100 * (overlap_count / 10)
            spearman_coefficient = spearman_coefficients.get(query, 0)
            
            writer.writerow({
                'queries': f"Query {i}",
                'overlapped count': overlap_count,
                '% overlap': f"{overlap_percent:.2f}",
                'coeff': f"{spearman_coefficient:.4f}"
            })
        
        writer.writerow({
            'queries': 'Average',
            'overlapped count': f"{avg_overlap_count:.2f}",
            '% overlap': f"{avg_overlap_percent:.2f}",
            'coeff': f"{avg_spearman_coefficient:.4f}"
        })
#----------------------------------------------------------------------------------------------------------

google_path = '/Users/sahithinamala/Documents/IR Assignments/Assignment 1/Google_Result1.json'
bing_path = '/Users/sahithinamala/Documents/IR Assignments/Assignment 1/CSCI572-3760715059-Sahithi Namala 2/hw1.json'

#----------------------------------------------------------------------------------------------------------

# Load the results, compute overlaps and Spearman coefficients, then save to CSV
google_results, bing_results = load_results(google_path, bing_path)
overlapping_results = find_overlapping_results(google_results, bing_results)
spearman_coefficients = compute_spearman(google_results, bing_results)
save_results_to_csv(overlapping_results, spearman_coefficients, '/Users/sahithinamala/Documents/IR Assignments/Assignment 1/results.csv')
