# perform_account_mapping PRD

## Description
Maps extracted transaction data to the CoA system accounts by leveraging parsed product codes and a temporary lookup table, facilitating accurate financial accounting and analytics.


## Implementation Plan

### 1. Retrieve the extracted transaction data from the 'extract_transaction_data' node and the parsed product codes along with the temporary lookup table from the 'parse_product_codes' node.

| Category | Details |
| --- | --- |
| **Reason** | To perform the account mapping, we need the transaction data and the parsed product codes. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use the output of 'extract_transaction_data' and 'parse_product_codes' nodes as input. |

### 2. Iterate through each transaction in the extracted transaction data and use the product codes to find the corresponding CoA system account numbers from the temporary lookup table.

| Category | Details |
| --- | --- |
| **Reason** | To map transactions to CoA system accounts, we need to match product codes with account numbers. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Implement a loop that iterates through transactions and uses the lookup table for mapping. |

### 3. For each transaction, validate the mapping by checking if the product code exists in the lookup table and if the corresponding CoA account number is valid.

| Category | Details |
| --- | --- |
| **Reason** | To ensure accurate mapping, we need to validate the product codes and CoA account numbers. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Apply validation checks for product codes and CoA account numbers. |

### 4. Keep track of the number of successfully mapped transactions, discrepancies encountered, and errors found during the mapping process.

| Category | Details |
| --- | --- |
| **Reason** | To provide a detailed report, we need to track the mapping success rate and discrepancies. |
| **Impact** | HIGH |
| **Complexity** | LOW |
| **Method** | Use counters for mapped transactions, discrepancies, and errors. |

### 5. Calculate the mapping success rate by dividing the number of successfully mapped transactions by the total number of transactions.

| Category | Details |
| --- | --- |
| **Reason** | To provide a measure of mapping accuracy. |
| **Impact** | MEDIUM |
| **Complexity** | LOW |
| **Method** | Apply the formula for success rate. |

### 6. Compile the results into the required output structure, including lists of mapped transactions, discrepancies, CoA account numbers, mapping success rate, and error count.

| Category | Details |
| --- | --- |
| **Reason** | To meet the output requirements of the node. |
| **Impact** | HIGH |
| **Complexity** | MEDIUM |
| **Method** | Format the results according to the specified output structure. |
