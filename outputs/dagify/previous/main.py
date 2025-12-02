import os
import asyncio
import functools
import inspect
import json
import sys
from typing import Dict, Any, List, Callable, Coroutine, Union, Optional

from code.calculate_transaction_amounts import calculate_transaction_amounts
from code.clean_and_purge_old_logs import clean_and_purge_old_logs
from code.ensure_clover_api_compatibility import ensure_clover_api_compatibility
from code.extract_transaction_data import extract_transaction_data
from code.generate_transaction_logs import generate_transaction_logs
from code.parse_product_codes import parse_product_codes
from code.perform_account_mapping import perform_account_mapping
from code.store_transaction_data_in_coa_database import store_transaction_data_in_coa_database
from code.validate_transaction_data import validate_transaction_data

# Get async mode from environment variable or default to False
ASYNC_MODE = os.environ.get('ASYNC_MODE', '').lower() in ('true', '1', 'yes', 'y')

def make_async(func):
    """Convert a synchronous function to an asynchronous function.

    If the function is already asynchronous, return it unchanged.
    If the function is synchronous, wrap it in an async function.
    """
    # If it's already a coroutine function, return it as is
    if inspect.iscoroutinefunction(func):
        return func

    # Otherwise, wrap it as an async function
    @functools.wraps(func)
    async def async_wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return async_wrapper

calculate_transaction_amounts_async = make_async(calculate_transaction_amounts)
clean_and_purge_old_logs_async = make_async(clean_and_purge_old_logs)
ensure_clover_api_compatibility_async = make_async(ensure_clover_api_compatibility)
extract_transaction_data_async = make_async(extract_transaction_data)
generate_transaction_logs_async = make_async(generate_transaction_logs)
parse_product_codes_async = make_async(parse_product_codes)
perform_account_mapping_async = make_async(perform_account_mapping)
store_transaction_data_in_coa_database_async = make_async(store_transaction_data_in_coa_database)
validate_transaction_data_async = make_async(validate_transaction_data)

async def run_workflow(user_input: str) -> Dict[str, Any]:
    """Execute the workflow by running each level in the topological sort.

    Args:
        user_input: The input string for the workflow

    Returns:
        Dict containing all results keyed by node name
    """
    # Store results for each node
    results = {}

    # Level 0: extract_transaction_data
    async def run_extract_transaction_data():
        # Call the async version of extract_transaction_data with results from dependencies
        return await extract_transaction_data_async(user_input)

    # Run level 0 nodes in parallel
    results['extract_transaction_data'] = await run_extract_transaction_data()

    # Level 1: parse_product_codes
    async def run_parse_product_codes():
        # Call the async version of parse_product_codes with results from dependencies
        return await parse_product_codes_async(results['extract_transaction_data'])

    # Run level 1 nodes in parallel
    results['parse_product_codes'] = await run_parse_product_codes()

    # Level 2: perform_account_mapping
    async def run_perform_account_mapping():
        # Call the async version of perform_account_mapping with results from dependencies
        return await perform_account_mapping_async(results['parse_product_codes'], results['extract_transaction_data'])

    # Run level 2 nodes in parallel
    results['perform_account_mapping'] = await run_perform_account_mapping()

    # Level 3: calculate_transaction_amounts, generate_transaction_logs
    async def run_calculate_transaction_amounts():
        # Call the async version of calculate_transaction_amounts with results from dependencies
        return await calculate_transaction_amounts_async(results['perform_account_mapping'], results['extract_transaction_data'])

    async def run_generate_transaction_logs():
        # Call the async version of generate_transaction_logs with results from dependencies
        return await generate_transaction_logs_async(results['perform_account_mapping'], results['extract_transaction_data'])

    # Run level 3 nodes in parallel
    level_3_results = await asyncio.gather(run_calculate_transaction_amounts(), run_generate_transaction_logs())
    results['calculate_transaction_amounts'] = level_3_results[0]
    results['generate_transaction_logs'] = level_3_results[1]

    # Level 4: store_transaction_data_in_coa_database
    async def run_store_transaction_data_in_coa_database():
        # Call the async version of store_transaction_data_in_coa_database with results from dependencies
        return await store_transaction_data_in_coa_database_async(results['calculate_transaction_amounts'])

    # Run level 4 nodes in parallel
    results['store_transaction_data_in_coa_database'] = await run_store_transaction_data_in_coa_database()

    # Level 5: validate_transaction_data
    async def run_validate_transaction_data():
        # Call the async version of validate_transaction_data with results from dependencies
        return await validate_transaction_data_async(results['generate_transaction_logs'], results['store_transaction_data_in_coa_database'])

    # Run level 5 nodes in parallel
    results['validate_transaction_data'] = await run_validate_transaction_data()

    # Level 6: clean_and_purge_old_logs, ensure_clover_api_compatibility
    async def run_clean_and_purge_old_logs():
        # Call the async version of clean_and_purge_old_logs with results from dependencies
        return await clean_and_purge_old_logs_async(results['validate_transaction_data'])

    async def run_ensure_clover_api_compatibility():
        # Call the async version of ensure_clover_api_compatibility with results from dependencies
        return await ensure_clover_api_compatibility_async(results['validate_transaction_data'])

    # Run level 6 nodes in parallel
    level_6_results = await asyncio.gather(run_clean_and_purge_old_logs(), run_ensure_clover_api_compatibility())
    results['clean_and_purge_old_logs'] = level_6_results[0]
    results['ensure_clover_api_compatibility'] = level_6_results[1]

    # Return all results
    return results

def run_workflow_sync(user_input: str) -> Dict[str, Any]:
    """Synchronous wrapper around the async workflow execution."""
    return asyncio.run(run_workflow(user_input))

def main():
    """Main entry point.

    Handles arguments in the following priority:
    1. Command-line argument (sys.argv[1])
    2. If no argument, uses empty string as input but displays a warning.
    """
    # Get user input from command line or use empty string
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
    else:
        # No input provided - display help message but continue with empty string
        print('Warning: No input provided. Using empty string as input.')
        print('For better results, provide an input argument:')
        print(f'  python {os.path.basename(__file__)} "your input text here"')
        print('Or use a file as input:')
        print(f'  python {os.path.basename(__file__)} "$(cat input.txt)"')
        user_input = ""

    print(f'Running workflow with input: {user_input}')

    # Run the workflow
    results = run_workflow_sync(user_input)

    # Print results
    try:
        # Convert results to JSON
        json_results = json.dumps(results, indent=2, default=str)
        print(json_results)
    except (TypeError, ValueError) as e:
        print(f'Results could not be converted to JSON: {e}')
        print(f'Raw results: {results}')

    return results

if __name__ == '__main__':
    main()
